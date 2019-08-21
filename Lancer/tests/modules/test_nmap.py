from modules import nmap

import os
import tempfile
import pytest
import io
import sys


def test_parse_down_nmap_scan():
    xml_output = '<hosts up="0" down="1" total="1"/>'
    file_descriptor, file_path = tempfile.mkstemp(suffix='.tmp')

    open_file = os.fdopen(file_descriptor, 'w')
    open_file.write(xml_output)
    open_file.close()

    captured_output = io.StringIO()
    sys.stdout = captured_output

    with pytest.raises(SystemExit):
        nmap.parse_nmap_scan(file_path)

    sys.stdout = sys.__stdout__
    os.unlink(file_path)
    assert "unreachable" in captured_output.getvalue()
