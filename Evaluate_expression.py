import re

def is_valid_input(expression, minV, maxV):
	"""
	validates the input of the user.

	Parameters
	----------
	expression: string
		function to be plotted
	minV: int
		minimum number of x
	maxV: int
		maximum number of x

	Returns
	-------
	True: if the input is valid
	or
	False: if the input isn't valid
	"""
	pattern = re.compile("([0-9]+|[xX])([\+\-\*\/\^]([0-9]+|[xX]))*")
	if pattern.fullmatch(expression) is not None:
		return True
	"""
	if (pattern.fullmatch(expression) is not None and
			number.fullmatch(minV) is not None and
			number.fullmatch(maxV) is not None):
		return True
	"""
	return False

def exponentiate_parts(multiplicative_part):
	"""
	Split a multiply_part into exponents and raise to their power.

	Parameters
	----------
	multiplicative_part: string
		part to be split.

	Returns
	-------
	res: int
		result of exponentiating parts.
	"""
	exponents = re.split("[\^]", multiplicative_part)
	res = int(exponents[-1])
	for exponent in reversed(exponents[:-1]):
		exponent = int(exponent)
		res = exponent**res
	return res

def multiply_parts(additive_part):
	"""
	Split an additive_part into multiplicative_parts and multiplys them.

	Parameters
	----------
	additive_part: string
		part to be split.

	Returns
	-------
	res: int
		result of multiplying parts.
	"""
	multiplicative_parts = re.split("[*|/]", additive_part)
	signs = re.finditer("[*|/]", additive_part)	# distinguish between * and /
	i = 0
	res = exponentiate_parts(multiplicative_parts[i])
	for sign in signs:
		i += 1
		multiplicative_part = exponentiate_parts(multiplicative_parts[i])
		if sign[0] == '*':
			res *= multiplicative_part
		else:
			res /= multiplicative_part
	return res

def add_parts(expression):
	"""
	Split the expression to additive_parts and adds them together.

	Parameters
	----------
	expression: string
		function to be split

	Returns
	-------
	res: int
		result of adding parts
	"""
	expression = re.sub("\-\-", "+", expression)
	additive_parts = re.split('\+|(\d+)\-(\d+)', expression)
	# z holds the ready addidive parts after removing Nones and ''
	z = []
	for i, p in enumerate(additive_parts):
		# skip None or empty strings
		if p is None or p == '':
			continue
		else:
			x = p
			# combine strings '6*-' with '7'
			if p[-1]=='-' or p[-1]=='*' or p[-1]=='/' or p[-1]=='+' or p[-1]=='^':
				# concatenate this string with the following string
				x += additive_parts[i+1]
				# empty the following string
				additive_parts[i+1] = ''
			# append additive parts
			z.append(x)
	additive_parts = z
	# idx holds the index of a plus or minus sign in the expression
	idx = len(additive_parts[0])
	res = multiply_parts(additive_parts[0])
	for additive_part in additive_parts[1:]:
		l = len(additive_part)+1
		additive_part = multiply_parts(additive_part)
		if(expression[idx] == '+'):
			res += additive_part
		else:
			res -= additive_part
		idx += l
	return res
