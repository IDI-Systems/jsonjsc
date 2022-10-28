# jsonjsc

[![CI - Test](https://github.com/IDI-Systems/jsonjsc/actions/workflows/test.yml/badge.svg)](https://github.com/IDI-Systems/jsonjsc/actions/workflows/test.yml)
[![CI - Build](https://github.com/IDI-Systems/jsonjsc/actions/workflows/build.yml/badge.svg)](https://github.com/IDI-Systems/jsonjsc/actions/workflows/build.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/jsonjsc.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/jsonjsc)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jsonjsc.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/jsonjsc)

A Python library for parsing out C/Javascript style comments in JSON files.


## Install

`pip install jsonjsc`


## Features

-  Simple and easy to use library with no other dependencies.
-  Supports C/JS block (`/* */`) and single line (`//`) comments.
-  Retains the line number and character column of JSON content after parsing, letting syntax error positions get properly reported by the normal Python JSON decoder.
-  Is easily dropped into existing JSON library usage as a decoder class.
-  Test backed via `unittest`.


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


## Development

jsonjsc uses [Hatchling](https://hatch.pypa.io/latest/) as a build backend and [flake8](https://flake8.pycqa.org/en/latest/) as a style guide.

```
$ pip install -e .
```

[Hatch](https://hatch.pypa.io/latest/) is the primary project manager of choice, but any project adhering to PEP 621 (`pyproject.toml` specification) can be used.

```
$ hatch shell
```

### Tests

Tests can be ran with [pytest](https://docs.pytest.org/). Hatch scripts are included for linting and testing.

```
# Lint
$ hatch run lint:all

# Test with current Python version
$ hatch run full
# Test with all Python versions
$ hatch run test:full
```

### TODOs

Implementation could probably be sped up significantly as it uses character by character searches to test if comments are in string values or not. No performance metrics have been taken.


## License

Licensed under the MIT License. See LICENSE for more information.
