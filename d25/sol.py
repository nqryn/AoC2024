# Template
import argparse
from itertools import product



def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	locks = []
	keys = []
	with open(f_name) as f:
		data = f.readlines()
		for i in range(0, len(data), 8):
			matrix = data[i:i+7]
			if matrix[0].strip() == '#####':
				# Lock
				# print('...is lock')
				lock = [0, 0, 0, 0, 0]
				for line in matrix[1:6]:
					for j, val in enumerate(line.strip()):
						lock[j] += 1 if val == '#' else 0
				locks.append(lock)

			if matrix[6].strip() == '#####':
				# Key
				# print('...is lkey')
				key = [0, 0, 0, 0, 0]
				for line in matrix[1:6]:
					for j, val in enumerate(line.strip()):
						key[j] += 1 if val == '#' else 0
				keys.append(key)
	return locks, keys


def solve(locks, keys):
	# print(locks)
	# print(keys)

	def _fits(lock, key):
		# print(f'Try {lock} and {key}')
		for lh, kh in zip(lock, key):
			if lh + kh > 5:
				# print(f'Does not fit for {lh} and {kh}')
				return False
		return True

	matches = 0
	for lock, key in product(locks, keys):
		# print()
		if _fits(lock, key):
			matches += 1
	return matches



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	in_values = read_in(args.test)
	res = solve(*in_values)
	
	print(f'Result: {res}')