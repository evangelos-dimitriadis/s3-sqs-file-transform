import unittest
import json
import logging
from xml_json import xml_json
from pathlib import Path


class TestXmlToJson(unittest.TestCase):

    # Disable logging
    logging.disable()

    def test_nofile_xml_json(self):
        self.assertRaises(FileNotFoundError, xml_json, 'nofile.xml')

    def test_file_xml_json(self):
        file = Path(__file__).parent.parent.joinpath('examples/example.xml')
        myjson = xml_json(file)
        with open(myjson, "r") as fd:
            try:
                json.load(fd)
            except ValueError:
                assert False
            assert True
