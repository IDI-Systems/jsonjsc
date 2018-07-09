# jsonjsc
A Python library for parsing out C/Javascript style comments in JSON files.

## Features
1. Simple and easy to use library with no other dependencies.
1. Supports C/JS block (`/* */`) and single line (`//`) comments.
1. Retains the line number and character column of JSON content after parsing, letting syntax error positions get properly reported by the normal Python JSON decoder.
1. Is easily dropped into existing JSON library usage as a decoder class.
1. Test backed via `unittest`.

## Example
```python
import json
import jsonjsc

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

test = json.loads(TEST_JSON_DECODER, cls=jsonjsc.JSONCommentDecoder)

print(test["test1"])

if "junk1" not in test:
    print("I guess junk1 was commented out?")

if "junk2" not in test:
    print("I guess junk2 was commented out too!")

print(test["test2"])
```

## TODOs

Implementation could probably be sped up significantly as it uses character by character searches to test if comments are in string values or not. No performance metrics have been taken.

## License

Licensed under the MIT License. See LICENSE for more information.
