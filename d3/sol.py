import re

def read_in():
	instructions = ''
	with open('f.in') as f:
		for line in f:
			instructions += line
	return instructions


def compute_correct_muls():
	pattern = r"mul\((?P<num1>[0-9]{1,3}),(?P<num2>[0-9]{1,3})\)"
	instructions = read_in()

	matches = re.finditer(pattern, instructions)
	total = 0
	for m in matches:
		num1 = int(m.group("num1"))
		num2 = int(m.group("num2"))
		total += num1 * num2
	return total


def compute_enabled_muls():
	instructions = read_in()
	combined_pattern = r"mul\((?P<num1>[0-9]{1,3}),(?P<num2>[0-9]{1,3})\)|do\(\)|don\'t\(\)"

	enabled = True
	curr_idx = 0
	total = 0
	while curr_idx < len(instructions):
		match = re.search(combined_pattern, instructions[curr_idx:])
		if not match:
			break
		curr_idx += match.end()

		if match.group() == "do()":
			enabled = True
		elif match.group() == "don't()":
			enabled = False
		else:
			num1 = int(match.group("num1"))
			num2 = int(match.group("num2"))
			if enabled:
				total += num1 * num2
	return total

if __name__ == '__main__':
	# res = compute_correct_muls()
	res = compute_enabled_muls()
	print(f'Result: {res}')
