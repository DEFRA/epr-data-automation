import jwt
import time
from typing import Dict, Optional
from playwright.async_api import async_playwright
    
def generate_jwt(
    issuer: str,
    secret: str,
    algorithm: str = "HS256",
    additional_payload: Optional[Dict] = None
) -> str:
    """
    Generates a signed JWT token.

    Args:
        issuer (str): The 'iss' claim for the JWT.
        secret (str): The secret key used to sign the JWT.
        algorithm (str): The signing algorithm. Defaults to "HS256".
        additional_payload (dict, optional): Extra claims to include in the payload.

    Returns:
        str: Signed JWT token.
    """
    # Base payload with issuer and issued-at timestamp
    payload = {
        "iss": issuer,
        "iat": int(time.time())
    }

    # Add additional claims if provided
    if additional_payload:
        payload.update(additional_payload)

    # JWT header
    headers = {
        "alg": algorithm,
        "typ": "JWT"
    }

    # Generate and return the signed token
    token = jwt.encode(payload, secret, algorithm=algorithm, headers=headers)
    return token

async def get_notification_response(
    target_email: str,
    issuer: str,
    secret: str,
    endpoint: str = "v2/notifications",
    api_base_url: str = "https://api.notifications.service.gov.uk"
) -> str:
    """
    Sends an async GET request to the specified endpoint, filters notifications
    by the target_email, and returns the 'body' of the matching notification.
    """

    # ✅ Generate JWT token
    jwt_token = generate_jwt(issuer, secret)

    # ✅ Set Authorization header
    headers = {"Authorization": f"Bearer {jwt_token}"}

    async with async_playwright() as pw:
        # ✅ Create a new API request context
        request_context = await pw.request.new_context(
            base_url=api_base_url,
            extra_http_headers=headers
        )

        # ✅ Send GET request (Playwright automatically joins base_url + endpoint)
        response = await request_context.get(endpoint)

        if not response.ok:
            print(f"❌ Failed GET {endpoint} — {response.status}")
            return ""

        data = await response.json()

        # ✅ Clean up
        await request_context.dispose()

        # ✅ Filter by email
        for n in data.get("notifications", []):
            if n.get("email_address") == target_email:
                return n.get("body", "")

        return ""

def get_verification_code(notificationRequestBody: str) -> str:
    """
    Extracts text between '6-digit verification code:' and 
    'This code will expire in 10 minutes' from the given message,
    removing any leading '#' symbol.
    """
    import re

    match = re.search(
        r"6-digit verification code:(.*?)This code will expire in 10 minutes",
        notificationRequestBody,
        re.DOTALL
    )

    if not match:
        return ""

    # Clean and strip whitespace
    code = match.group(1).strip()

    # ✅ Remove leading '#' if present
    if code.startswith("#"):
        code = code[1:].strip()

    return code

