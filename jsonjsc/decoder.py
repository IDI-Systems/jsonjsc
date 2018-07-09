import json

from jsonjsc.parser import parse

class JSONCommentDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        s = parse(s)
        return super(JSONCommentDecoder, self).decode(s, **kwargs)