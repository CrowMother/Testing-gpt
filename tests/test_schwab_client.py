from pathlib import Path
import importlib.util
from unittest.mock import patch
import os

module_dir = Path(__file__).resolve().parents[1] / "src" / "clients"
module_path = module_dir / "schwab_api.py"
spec = importlib.util.spec_from_file_location("schwab_api", module_path)
schwab_api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schwab_api)
CharlesSchwabClient = schwab_api.CharlesSchwabClient


def test_get_authorization_url() -> None:
    os.environ["SCHWAB_CLIENT_ID"] = "client123"
    with patch("aiohttp.ClientSession"):
        client = CharlesSchwabClient()
        url = client.get_authorization_url(
            "https://example.com/callback",
            "state42",
        )
    expected = (
        "https://api.schwab.com/oauth2/authorize?"
        "response_type=code&client_id=client123&"
        "redirect_uri=https://example.com/callback&"
        "state=state42&scope=accounts trading"
    )
    assert url == expected
