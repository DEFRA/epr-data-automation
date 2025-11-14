from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import time
import jwt
from playwright.async_api import async_playwright


@dataclass(frozen=True)
class NotificationsConfig:
    """
    Configuration for the GOV.UK Notify (or equivalent) API.
    - issuer: JWT issuer / API key ID
    - secret: shared secret used to sign JWT
    """
    issuer: str
    secret: str
    api_base_url: str = "https://api.notifications.service.gov.uk"
    endpoint: str = "v2/notifications"
    algorithm: str = "HS256"
    timeout_s: int = 30

    def build_jwt(self) -> str:
        payload = {"iss": self.issuer, "iat": int(time.time())}
        headers = {"alg": self.algorithm, "typ": "JWT"}
        # returns a str (PyJWT v2+)
        return jwt.encode(payload, self.secret, algorithm=self.algorithm, headers=headers)


class NotificationsClient:
    """
    Minimal async client to fetch notifications and extract verification codes.
    """

    def __init__(self, cfg: NotificationsConfig):
        self._cfg = cfg

    async def fetch_notification_body(self, target_email: str) -> str:
        """
        Returns the 'body' of the first notification whose email_address == target_email.
        If none found or request fails, returns "".
        """
        token = self._cfg.build_jwt()
        headers = {"Authorization": f"Bearer {token}"}

        async with async_playwright() as pw:
            ctx = await pw.request.new_context(
                base_url=self._cfg.api_base_url,
                extra_http_headers=headers,
                timeout=self._cfg.timeout_s * 1000,
            )
            try:
                resp = await ctx.get(self._cfg.endpoint)
                if not resp.ok:
                    return ""
                data = await resp.json()
            finally:
                await ctx.dispose()

        for n in data.get("notifications", []):
            if n.get("email_address") == target_email:
                return n.get("body", "")
        return ""

    @staticmethod
    def extract_verification_code(notification_body: str) -> str:
        """
        Extracts the verification code from a notification body.

        Looks for the text between:
          '6-digit verification code:' and 'This code will expire in 10 minutes'
        Trims a leading '#' if present.
        """
        import re

        m = re.search(
            r"6-digit verification code:(.*?)This code will expire in 10 minutes",
            notification_body,
            re.DOTALL,
        )
        if not m:
            return ""
        code = m.group(1).strip()
        if code.startswith("#"):
            code = code[1:].strip()
        return code
