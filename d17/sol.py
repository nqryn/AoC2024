# Template
import argparse


def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	# Define vars here
	x = 1
	with open(f_name) as f:
		for line in f:
			# Remeber to line.strip() !!!!
			x += int(line.strip())
	return x


def solve(data):
	return data + 1


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	in_values = read_in(args.test)
	res = solve(in_values)
	
	print(f'Result: {res}')