from pprint import pprint
import itertools

OPERATOR_FUNCTIONS = {
	'+': lambda x, y: x + y,
	'*': lambda x, y: x * y,
	'||': lambda x, y: int(str(x)+str(y))
}


def read_in():
	equations = {}
	with open('f.in') as f:
		for line in f:
			res, values = line.strip().split(':')
			res = int(res)
			values = [int(x) for x in values.strip().split(' ')]
			equations[res] = values
	return equations


def _eval(eq: list[int], ops: list[str]):
	result = eq[0]
	for next_val, op in zip(eq[1:], ops):
		result = OPERATOR_FUNCTIONS[op](result, next_val)
	return result


def _test_equation(eq: list[int], expected: int) -> bool:
	# Generate all perms with repetition of acceptable operators
	operators = OPERATOR_FUNCTIONS.keys()
	for ops in itertools.product(operators, repeat=len(eq)-1):
		result = _eval(eq, ops)
		if result == expected:
			return True
	return False


def get_calibration_result() -> int:
	equations = read_in()
	total = 0
	for expected, eq in equations.items():
		if _test_equation(eq, expected):
			total += expected
	return total



if __name__ == '__main__':
	res = get_calibration_result()
	
	print(f'Result: {res}')