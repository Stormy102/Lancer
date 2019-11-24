from modules.legacy.web import https

import sys
import io


def test_get_https_cert_values():
    captured_output = io.StringIO()
    sys.stdout = captured_output
    https.get_https_cert_values('www.google.com', 443)
    sys.stdout = sys.__stdout__
    assert "Common name is" in captured_output.getvalue()
