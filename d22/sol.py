# Template
import argparse
import math
from collections import defaultdict


def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	secrets = []
	with open(f_name) as f:
		for line in f:
			secrets.append(int(line.strip()))
	return secrets


def _compute_next_secret(secret):
	res = secret * 64
	secret = res ^ secret # mix
	secret = secret % 16777216 # prune

	res = math.floor(secret / 32)
	secret = res ^ secret # mix
	secret = secret % 16777216 # prune

	res = secret * 2048
	secret = res ^ secret # mix
	secret = secret % 16777216 # prune

	return secret



def solve(secrets):
	print(secrets)
	total = 0
	for s in secrets:
		next_ = s
		for _ in range(2000):
			next_ = _compute_next_secret(next_)
		print(s, ': ', next_)
		total += next_
	return total

def _compute_banana_seq(s):
	next_ = s
	ld = int(str(next_)[-1])

	diffs = []
	bananas = {}
	for i in range(2000):
		nv = _compute_next_secret(next_)
		nld = int(str(nv)[-1])

		diff = ld - nld
		diffs.append(str(diff))
		if i >= 3:
			if i >= 4:
				diffs.pop(0)
			key = ''.join(diffs)
			if key not in bananas:
				bananas[key] = nld
		next_ = nv
		ld = nld
	return bananas


def solve_2nd(secrets):
	all_seq = defaultdict(int)
	for s in secrets:
		bananas = _compute_banana_seq(s)
		for k, v in bananas.items():
			all_seq[k] += v
	print(len(all_seq))

	max_val = 0
	for k, v in all_seq.items():
		if v > max_val:
			print(f'Found greater value {v} for seq {k}')
			max_val = v
	print('Done!')
		




if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	in_values = read_in(args.test)
	res = solve_2nd(in_values)
	
	print(f'Result: {res}')