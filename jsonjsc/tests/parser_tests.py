"""
Unit tests for parser/JSONDecoder
"""
import unittest
import json

from jsonjsc.parser import parse
from jsonjsc import JSONCommentDecoder

TEST_COMMENT_ON_OWN_LINE = r'''{
    // This is a comment on it's own line
}'''

TEST_COMMENT_ON_OWN_LINE_NO_TAB = r'''{
// This is a comment on it's own line
}'''

TEST_SINGLE_COMMENT_ON_LINE_WITH_JSON = r'''{
    "test": 123 // this is a comment after some JSON
}'''

TEST_DOUBLE_FORWARD_SLASH_IN_STRING = r'''{
    "test": "ab//cd"
}'''

TEST_BLOCK_COMMENT_SINGLE_LINE_ALONE = r'''{
    /* This is a block comment */
}'''

TEST_BLOCK_COMMENT_SINGLE_LINE_ALONE_NO_TAB = r'''{
/* This is a block comment */
}'''

TEST_BLOCK_COMMENT_SINGLE_LINE_BEFORE = r'''{
    /* This is a block comment */"test": "message"
}'''

TEST_BLOCK_COMMENT_SINGLE_LINE_AFTER = r'''{
    "test": "message"/* This is a block comment */
}'''

TEST_BLOCK_COMMENT_SINGLE_LINE_MIDDLE = r'''{
    "test": /* This is a block comment */ "message"
}'''

TEST_BLOCK_COMMENT_MULTIPLE_LINES = r'''{
    /*
    This is a block comment
    */
    "test": "message"
}'''

TEST_BLOCK_COMMENT_MULTIPLE_LINES_NO_TAB = r'''{
/*
This is a block comment
*/
    "test": "message"
}'''

TEST_BLOCK_COMMENT_MULTIPLE_LINES_NO_TAB_FANCY = r'''{
/*
 * This is a block comment
 */
    "test": "message"
}'''

TEST_COMMENTED_OUT_BLOCK_COMMENT = r'''{
    ///*
    "test": "message"
    //*/
}'''

TEST_ESCAPED_STRING = r'''{
    "test": "mess\"age" // This comment should go away!
}'''

TEST_BLOCK_COMMENT_IN_STRING = r'''{
    "test": "mess/**/age"
}'''

TEST_FANCY_BLOCK_COMMENT = r'''{
/************************
This is a fancy comment!
************************/
    "test": "message"
}'''

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

"""
Test case for parser.
"""
class JSONCommentParserTests(unittest.TestCase):
    def test_comment_on_own_line(self):
        result = parse(TEST_COMMENT_ON_OWN_LINE)
        result = result.split('\n')
        self.assertEqual(result[1], r'    ')

    def test_comment_on_own_line_no_tab(self):
        result = parse(TEST_COMMENT_ON_OWN_LINE_NO_TAB)
        result = result.split('\n')
        self.assertEqual(result[1], r'')

    def test_single_comment_on_line_with_json(self):
        result = parse(TEST_SINGLE_COMMENT_ON_LINE_WITH_JSON)
        result = result.split('\n')
        self.assertEqual(result[1], r'    "test": 123 ')

    def test_double_forward_slash_in_string(self):
        result = parse(TEST_DOUBLE_FORWARD_SLASH_IN_STRING)
        result = result.split('\n')
        self.assertEqual(result[1], r'    "test": "ab//cd"')

    def test_block_comment_single_line_alone(self):
        result = parse(TEST_BLOCK_COMMENT_SINGLE_LINE_ALONE)
        result = result.split('\n')
        self.assertEqual(result[1], r'                                 ')

    def test_block_comment_single_line_alone_no_tab(self):
        result = parse(TEST_BLOCK_COMMENT_SINGLE_LINE_ALONE_NO_TAB)
        result = result.split('\n')
        self.assertEqual(result[1], r'                             ')

    def test_block_comment_single_line_before(self):
        result = parse(TEST_BLOCK_COMMENT_SINGLE_LINE_BEFORE)
        result = result.split('\n')
        self.assertEqual(result[1], r'                                 "test": "message"')

    def test_block_comment_single_line_after(self):
        result = parse(TEST_BLOCK_COMMENT_SINGLE_LINE_AFTER)
        result = result.split('\n')
        self.assertEqual(result[1], r'    "test": "message"                             ')

    def test_block_comment_single_line_middle(self):
        result = parse(TEST_BLOCK_COMMENT_SINGLE_LINE_MIDDLE)
        result = result.split('\n')
        self.assertEqual(result[1], r'    "test":                               "message"')

    def test_block_comment_multiple_lines(self):
        result = parse(TEST_BLOCK_COMMENT_MULTIPLE_LINES)
        result = result.split('\n')
        self.assertEqual(result[1], r'      ')
        self.assertEqual(result[2], r'')
        self.assertEqual(result[3], r'      ')
        self.assertEqual(result[4], r'    "test": "message"')

    def test_block_comment_multiple_lines_no_tab(self):
        result = parse(TEST_BLOCK_COMMENT_MULTIPLE_LINES_NO_TAB)
        result = result.split('\n')
        self.assertEqual(result[1], r'  ')
        self.assertEqual(result[2], r'')
        self.assertEqual(result[3], r'  ')
        self.assertEqual(result[4], r'    "test": "message"')

    def test_block_comment_multiple_lines_no_tab_fancy(self):
        result = parse(TEST_BLOCK_COMMENT_MULTIPLE_LINES_NO_TAB_FANCY)
        result = result.split('\n')
        self.assertEqual(result[1], r'  ')
        self.assertEqual(result[2], r'')
        self.assertEqual(result[3], r'   ')
        self.assertEqual(result[4], r'    "test": "message"')

    def test_commented_out_block_comment(self):
        result = parse(TEST_COMMENTED_OUT_BLOCK_COMMENT)
        result = result.split('\n')
        self.assertEqual(result[1], r'    ')
        self.assertEqual(result[2], r'    "test": "message"')
        self.assertEqual(result[3], r'    ')

    def test_escaped_string(self):
        result = parse(TEST_ESCAPED_STRING)
        result = result.split('\n')
        self.assertEqual(result[1], r'    "test": "mess\"age" ')

    def test_block_comment_in_string(self):
        result = parse(TEST_BLOCK_COMMENT_IN_STRING)
        result = result.split('\n')
        self.assertEqual(result[1], r'    "test": "mess/**/age"')

    def test_fancy_block_comment(self):
        result = parse(TEST_FANCY_BLOCK_COMMENT)
        result = result.split('\n')
        self.assertEqual(result[1], r'                         ')
        self.assertEqual(result[2], r'')
        self.assertEqual(result[3], r'                         ')
        self.assertEqual(result[4], r'    "test": "message"')

"""
Test case for JSONDecoder implementation.
"""
class JSONCommentDecoderTests(unittest.TestCase):
    def test_json_decoder(self):
        test = json.loads(TEST_JSON_DECODER, cls=JSONCommentDecoder)
        self.assertIn("test1", test)
        self.assertNotIn("junk1", test)
        self.assertNotIn("junk2", test)
        self.assertIn("test2", test)

        self.assertEqual(test["test1"], "message1")
        self.assertEqual(test["test2"], "message2")

if __name__ == '__main__':
    unittest.main()
