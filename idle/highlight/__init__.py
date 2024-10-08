import re


def _search(text_widget, text, tag):
    start_index = '1.0'
    while True:
        start_index = text_widget.search(text, start_index, 'end')
        if not start_index:
            break
        end_index = f"{start_index}+{len(text)}c"
        text_widget.tag_add(tag, start_index, end_index)
        start_index = end_index


def _pattern_search(text_widget, pattern, text, tag):
    start_index = '1.0'
    while True:
        start_index = text_widget.search(pattern, start_index, 'end', regexp=True)
        if not start_index:
            break
        end_index = f"{start_index}+{len(text)}c"
        text_widget.tag_add(tag, start_index, end_index)
        start_index = end_index


def _regex_search(text_widget, regex, text, tag):
    result = re.findall(regex, text)
    for r in result:
        start_index = '1.0'
        while True:
            start_index = text_widget.search(r, start_index, 'end')
            if not start_index:
                break
            end_index = f"{start_index}+{len(r)}c"
            text_widget.tag_add(tag, start_index, end_index)
            start_index = end_index


def _match_parentheses(text_widget, text, colors):
    color_index = {
        '(': 0,
        ')': "(",
        '[': 0,
        ']': "[",
        '{': 0,
        '}': "{"
    }
    tag_index = {
        '(': 0,
        ')': "(",
        '[': 0,
        ']': "[",
        '{': 0,
        '}': "{"
    }

    start_index = "1.0"
    for i, char in enumerate(text):
        start_index = text_widget.search(char, start_index, 'end')
        if char in ('(', '[', '{'):
            tag_name = f"{tag_index[char]}_{tag_index[char]}"
            text_widget.tag_configure(tag_name, foreground=colors[color_index[char] % len(colors)])
            text_widget.tag_add(tag_name, start_index, f"{start_index}+1c")
            tag_index[char] += 1
            color_index[char] += 1
        elif char in (')', ']', '}'):
            tag_name = f"{tag_index[tag_index[char]]}_{tag_index[tag_index[char]] - 1}"
            text_widget.tag_configure(tag_name, foreground=colors[(color_index[color_index[char]] - 1) % len(colors)])
            text_widget.tag_add(tag_name, start_index, f"{start_index}+1c")
            tag_index[tag_index[char]] -= 1
            color_index[color_index[char]] -= 1
        else:
            continue
        start_index = f"{start_index}+1c"


def highlight(text_widget, syntaxes: list, function, settings: dict):
    syntaxes.extend(['true', 'false', 'null'])
    text_widget.tag_remove("keyword", "1.0", "end")
    text_widget.tag_remove("builtin", "1.0", "end")
    text_widget.tag_remove("number", "1.0", "end")
    text_widget.tag_remove("string", "1.0", "end")
    text_widget.tag_remove("comment", "1.0", "end")

    _match_parentheses(text_widget, text_widget.get(0.0, 'end'), settings['highlight']['including'])
    for syntax in syntaxes:
        _pattern_search(text_widget, rf"\y{re.escape(syntax)}\y", syntax, "keyword")

    for f in function:
        _pattern_search(text_widget, rf"\y{re.escape(f)}\y", f, "builtin")

    _regex_search(text_widget, r'-?\d+', text_widget.get("1.0", "end"), "number")
    _regex_search(text_widget, r'-?\d+\.\d+', text_widget.get("1.0", "end"), "number")
    _regex_search(text_widget, r"'[^']*'" + r"|\"[^\"]*\"", text_widget.get("1.0", "end"), "string")
    _regex_search(text_widget, r'/\*.*?\*/', text_widget.get("1.0", "end"), "comment")
