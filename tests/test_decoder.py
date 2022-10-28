"""
Unit tests for JSONDecoder
"""
import unittest
import json

from jsonjsc import JSONCommentDecoder

TEST_JSON_DECODER = r'''{
    /*
    This is a test of the JSON decoder in full
    */
    "test1": "message1", // this comment should parse out.
    // "junk1": "message",
    /*
    "junk2": "another message",
    */
    "test2": "message2"
}'''


class JSONCommentDecoderTests(unittest.TestCase):
    """
    Test case for JSONDecoder implementation.
    """
    def test_json_decoder(self):
        test = json.loads(TEST_JSON_DECODER, cls=JSONCommentDecoder)
        self.assertIn("test1", test)
        self.assertNotIn("junk1", test)
        self.assertNotIn("junk2", test)
        self.assertIn("test2", test)

        self.assertEqual(test["test1"], "message1")
        self.assertEqual(test["test2"], "message2")


if __name__ == "__main__":
    unittest.main()
