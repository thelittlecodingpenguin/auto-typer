import lexer

lang = lexer.Language()

keywords = ('False', 'None', 'True', 'and', 'as', 'assert', 'async','await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield')

builtins = ('abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip', 'self')

# parsed from top to bottom
lang.set_definitions(
	(r'[\)}\]]', lexer.tokens.closeBracket),
	(r'[\({\[]', lexer.tokens.openBracket),
	(r"'''(?s).*?'''", lexer.tokens.string),
	(r'"""(?s).*?"""', lexer.tokens.string),
	(r"'[^']*'", lexer.tokens.string),
	(r'"[^"]*"', lexer.tokens.string),
	(r'#(.*)', lexer.tokens.comment),
	(r'-?(.?[0-9])+', lexer.tokens.number),
	(r'\b(' + '|'.join(keywords) + r')\b', lexer.tokens.keyword),
	(r'\b(' + '|'.join(builtins) + r')\b', lexer.tokens.builtin),
	(r'\+|\-|=|\*|\/|==|>=|<=|!=', lexer.tokens.operator),
	(r"\w+", lexer.tokens.variable),
	(r"\s+", lexer.tokens.whitespace)
)

vs_dark = {
	lexer.tokens.string: (206, 145, 120),
	lexer.tokens.comment: (169, 169, 169),
	lexer.tokens.builtin: (255, 207, 158),
	lexer.tokens.keyword: (86, 156, 214),
	lexer.tokens.number: (181, 206, 168),
}

highlights = vs_dark

def parse(code):
	parsed = lang.parse(code)
	return parsed

def highlight(parsed):
	skip_positions = set()
	output = ''

	for token_data in parsed:
		token, text = token_data
		color = highlights.get(token, '97')

		if isinstance(color, tuple):
			color = '38;2;' + ';'.join(map(str, color))
    
		ansi_color = f'\033[{color}m'
		for i in range(len(ansi_color)):
			skip_positions.add(len(output) + i)
    
		output += ansi_color
		output += text
  
	return skip_positions, output
