import re

class ParseException(BaseException): pass

class tokens:
	class baseToken():
		pass
	class closeBracket(baseToken): pass
	class openBracket(baseToken): pass
	class string(baseToken): pass
	class variable(baseToken): pass
	class whitespace(baseToken): pass
	class comment(baseToken): pass
	class operator(baseToken): pass
	class keyword(baseToken): pass
	class builtin(baseToken): pass
	class number(baseToken): pass


class Language:
	definitions = []

	def add_definition(self, regex, token_name):
		self.definitions.append((token_name, re.compile('^' + regex)))

	def set_definitions(self, *definitions):
		for data in definitions:
			regex, token_name = data
			self.add_definition(regex, token_name)

	def parse(self, code, raise_exceptions=False):
		code_left = code
		tokens = []
		token_before = ''
		matched_tmp = ''
		while code_left:
			token = None
			for definition_data in self.definitions:
				token_name, regex = definition_data
				matched = regex.match(code_left)
				if matched is None:
					continue
				match_end = matched.span()[1]
				matched_text = code_left[:match_end]
				code_left = code_left[match_end:]
				token = token_name
				break
			if token is None:
				if raise_exceptions:
					if len(code_left) > 30:
						raise ParseException(f'Error parsing {code_left[:30]}...')
					else:
						raise ParseException(f'Error parsing {code_left}')
				else:
					matched_tmp += code_left[0]
					code_left = code_left[1:]
					token_before = None
					continue
			else:
				if token_before is None:
					tokens.append(('unknown', matched_tmp))
					matched_tmp = ''
				token_before = token
			tokens.append((token, matched_text))
		return tokens
