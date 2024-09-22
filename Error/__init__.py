def string_with_arrows(text, pos_start, pos_end):
    result = ''

    idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0: 
        idx_end = len(text)

    line_count = pos_end.ln - pos_start.ln + 1
    for i in range(line_count):
        line = text[idx_start:idx_end]
        col_start = pos_start.col if i == 0 else 0
        col_end = pos_end.col if i == line_count - 1 else len(line) - 1

        result += line + '\n\t\t'
        result += ' ' * col_start + '^' * (col_end - col_start)

        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0: 
            idx_end = len(text)

    return result


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = 'ErrorBack(Parsing an expression)\n'
        result += f"\tIn the line {self.pos_start.ln} of the file {self.pos_start.fn}\n"
        result += '\n\t\t' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end) + "\n"
        result += f'{self.error_name}: {self.details}'
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'IllegalCharacter', details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'InvalidSyntax', details)


class InvalidValueError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'InvalidValue', details)


class RunningTimeError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'RuntimeError', details)


class DefinedError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'DefinedError', details)


class InvalidTypeError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'TypeError', details)
