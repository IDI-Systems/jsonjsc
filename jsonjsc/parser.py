import json

class JSONCommentDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        s = self.parse(s)
        return super().decode(s, **kwargs)

    def parse(self, s):
        in_multi_line = False
        parsed_lines = []
        input_lines = s.split('\n')
        for line in input_lines:
            if not ("//" in line or "/*" in line or "*/" in line):
                if in_multi_line:
                    line = ""
                parsed_lines.append(line)
                continue
            
            in_string = False
            ci = -1
            line = list(line)
            for c in line:
                ci += 1
                
                if not in_multi_line:
                    if not in_string and c == '"':
                        in_string = True
                    elif in_string and c == '"' and line[ci-1] != '\\':
                        in_string = False
                    if not in_string and c == '/' and line[ci-1] == '/':
                        line = line[:ci-1]
                        break
                if not in_string and not in_multi_line and c == '*' and line[ci-1] == '/':
                    line[ci] = ' '
                    line[ci-1] = ' '
                    in_multi_line = True
                elif in_multi_line and c == '*' and line[ci+1] == '/':
                    line[ci] = ' '
                    line[ci + 1] = ' '
                    in_multi_line = False
                elif in_multi_line:
                    line[ci] = ' '

            parsed_lines.append("".join(line))

        return "\n".join(parsed_lines)
