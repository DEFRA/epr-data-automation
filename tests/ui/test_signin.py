import pytest

@pytest.mark.smoke
def test_homepage_loads(settings, page):
    page.goto(settings.base_url)
    assert page.title() is not None
