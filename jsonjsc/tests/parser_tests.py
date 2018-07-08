import unittest
import json

from jsonjsc.parser import JSONCommentDecoder

test_comment_on_own_line = r'''{
    // This is a comment on it's own line
}'''

test_single_comment_on_line_with_json = r'''{
    "test": 123 // this is a comment after some JSON
}'''

test_double_forward_slash_in_string = r'''{
    "test": "ab//cd"
}'''

test_block_comment_single_line_alone = r'''{
    /* This is a block comment */
}'''

test_block_comment_single_line_before = r'''{
    /* This is a block comment */"test": "message"
}'''

test_block_comment_single_line_after = r'''{
    "test": "message"/* This is a block comment */
}'''

test_block_comment_single_line_middle = r'''{
    "test": /* This is a block comment */ "message"
}'''

test_block_comment_multiple_lines = r'''{
    /*
    This is a block comment
    */
    "test": "message"
}'''

test_commented_out_block_comment = r'''{
    ///*
    "test": "message"
    //*/
}'''

test_escaped_string = r'''{
    "test": "mess\"age" // This comment should go away!
}'''

test_block_comment_in_string = r'''{
    "test": "mess/**/age"
}'''

test_json_decoder = r'''{
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
    def setUp(self):
        self.decoder = JSONCommentDecoder()

    def test_comment_on_own_line(self):
        result = self.decoder.parse(test_comment_on_own_line)
        result = result.split('\n')
        self.assertEqual(result[1], r'    ')

    def test_single_comment_on_line_with_json(self):
        result = self.decoder.parse(test_single_comment_on_line_with_json)
        result = result.split('\n')
        self.assertEqual(result[1], r'    "test": 123 ')

    def test_double_forward_slash_in_string(self):
        result = self.decoder.parse(test_double_forward_slash_in_string)
        result = result.split('\n')
        self.assertEqual(result[1], r'    "test": "ab//cd"')

    def test_block_comment_single_line_alone(self):
        result = self.decoder.parse(test_block_comment_single_line_alone)
        result = result.split('\n')
        self.assertEqual(result[1], r'                                 ')

    def test_block_comment_single_line_before(self):
        result = self.decoder.parse(test_block_comment_single_line_before)
        result = result.split('\n')
        self.assertEqual(result[1], r'                                 "test": "message"')

    def test_block_comment_single_line_after(self):
        result = self.decoder.parse(test_block_comment_single_line_after)
        result = result.split('\n')
        self.assertEqual(result[1], r'    "test": "message"                             ')

    def test_block_comment_single_line_middle(self):
        result = self.decoder.parse(test_block_comment_single_line_middle)
        result = result.split('\n')
        self.assertEqual(result[1], r'    "test":                               "message"')

    def test_block_comment_multiple_lines(self):
        result = self.decoder.parse(test_block_comment_multiple_lines)
        result = result.split('\n')
        self.assertEqual(result[1], r'      ')
        self.assertEqual(result[2], r'')
        self.assertEqual(result[3], r'      ')
        self.assertEqual(result[4], r'    "test": "message"')

    def test_commented_out_block_comment(self):
        result = self.decoder.parse(test_commented_out_block_comment)
        result = result.split('\n')
        self.assertEqual(result[1], r'    ')
        self.assertEqual(result[2], r'    "test": "message"')
        self.assertEqual(result[3], r'    ')

    def test_escaped_string(self):
        result = self.decoder.parse(test_escaped_string)
        result = result.split('\n')
        self.assertEqual(result[1], r'    "test": "mess\"age" ')

    def test_block_comment_in_string(self):
        result = self.decoder.parse(test_block_comment_in_string)
        result = result.split('\n')
        self.assertEqual(result[1], r'    "test": "mess/**/age"')

    def test_json_decoder(self):
        test = json.loads(test_json_decoder, cls=JSONCommentDecoder)
        self.assertIn("test1", test)
        self.assertNotIn("junk1", test)
        self.assertNotIn("junk2", test)
        self.assertIn("test2", test)

        self.assertEqual(test["test1"], "message1")
        self.assertEqual(test["test2"], "message2")

if __name__ == '__main__':
    unittest.main()