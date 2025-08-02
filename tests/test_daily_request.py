"""Tests for the daily request script."""

import pytest
from unittest.mock import patch, MagicMock
import os
import sys
from pathlib import Path

# Add the scripts directory to the path so we can import the module
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# Import the script module
import daily_request


def test_mikey_secret_required():
    """Test that the script exits when MIKEY_SECRET is not set."""
    with patch.dict(os.environ, {}, clear=True):
        with patch('sys.exit') as mock_exit:
            with patch('builtins.print') as mock_print:
                daily_request.main()
                mock_exit.assert_called_with(1)
                mock_print.assert_called_with("Error: MIKEY_SECRET environment variable not set")


def test_successful_request():
    """Test successful request with mock response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<html><body>Test response</body></html>"
    mock_response.headers = {"content-type": "text/html"}
    mock_response.raise_for_status.return_value = None
    
    with patch.dict(os.environ, {"MIKEY_SECRET": "test_secret"}):
        with patch('requests.get', return_value=mock_response) as mock_get:
            with patch('builtins.open', create=True) as mock_open:
                with patch('builtins.print') as mock_print:
                    daily_request.main()
                    
                    # Verify the request was made with correct parameters
                    mock_get.assert_called_once()
                    call_args = mock_get.call_args
                    assert call_args[0][0] == "https://meltingscales.github.io"
                    assert call_args[1]["headers"]["Authorization"] == "Bearer test_secret"
                    
                    # Verify file was written
                    mock_open.assert_called_once_with("response.txt", "w", encoding="utf-8")


def test_request_failure():
    """Test handling of request failure."""
    with patch.dict(os.environ, {"MIKEY_SECRET": "test_secret"}):
        with patch('requests.get', side_effect=Exception("Network error")) as mock_get:
            with patch('sys.exit') as mock_exit:
                with patch('builtins.print') as mock_print:
                    daily_request.main()
                    mock_exit.assert_called_with(1)


if __name__ == "__main__":
    pytest.main([__file__]) 