from mockextras import patch
import os
from mock import sentinel


@patch("os.getcwd", return_value=sentinel.patched)
def test_patch_works(mock_getcwd):
    assert sentinel.patched == os.getcwd()
    mock_getcwd.assert_called_once_with()
