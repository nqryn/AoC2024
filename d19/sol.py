# Template
import argparse
from collections import defaultdict
from pprint import pprint



def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	# Define vars here
	towels, tcs = [], []
	with open(f_name) as f:
		for i, line in enumerate(f):
			if i == 0:
				towels = line.strip().split(', ')
			elif i > 1:
				tcs.append(line.strip())
	return towels, tcs


# def solve(towels: list[str], tcs: list[str]):
# 	d_matches = defaultdict(list)

# 	for t in towels:
# 		d_matches[t[0]].append(t)

# 	for k, v in d_matches.items():
# 		d_matches[k] = sorted(d_matches[k], key=len)


# 	def _is_possible(substr: str) -> bool:
# 		if len(substr) == 0:
# 			return True

# 		first = substr[0]
# 		for match in d_matches[first]:
# 			match_len = len(match)
# 			if substr[:match_len] == match:
# 				if _is_possible(substr[match_len:]):
# 					return True

# 		return False


# 	possible_tcs_cnt = 0
# 	for tc in tcs:
# 		print(f'{tc} => {_is_possible(tc)}')
# 		if _is_possible(tc):
# 			possible_tcs_cnt += 1
# 	return possible_tcs_cnt


def solve_dp(towels: list[str], tcs: list[str]):

	def _is_possible_dp(tc: str) -> bool:
		n = len(tc)
		dp = [False] * (n + 1)
		# dp[i] = substring tc[:i] is possible
		dp[0] = True # empty string is possible

		for i in range(1, n+1):
			for towel in towels:
				towel_len = len(towel)
				if i >= towel_len and dp[i - towel_len] and tc[i - towel_len:i] == towel:
					# Match
					dp[i] = True
					break # We don't care how many other options there are (for the first part at least)
		return dp[n]

	possible_tcs_cnt = 0
	for tc in tcs:
		print(f'{tc} => {_is_possible_dp(tc)}')
		if _is_possible_dp(tc):
			possible_tcs_cnt += 1
	return possible_tcs_cnt


def solve2_dp(towels: list[str], tcs: list[str]):

	def _cnt_possible_dp(tc: str) -> int:
		n = len(tc)
		dp = [0] * (n + 1)
		# dp[i] = substring tc[:i] is possible
		dp[0] = 1 # empty string is possible

		for i in range(1, n+1):
			for towel in towels:
				towel_len = len(towel)
				if i >= towel_len and dp[i - towel_len] and tc[i - towel_len:i] == towel:
					# Match
					dp[i] += dp[i - towel_len]
		return dp[n]

	possible_tcs_cnt = 0
	for tc in tcs:
		print(f'{tc} => {_cnt_possible_dp(tc)}')
		possible_tcs_cnt += _cnt_possible_dp(tc)
	return possible_tcs_cnt



def here_we_go_again(towels, tcs):
	letters = set()
	lens = set()
	d_matches = defaultdict(list)
	for t in towels:
		letters.update([l for l in t])
		lens.add(len(t))
		d_matches[t[0]].append(t)
		# if 'w' in t:
		# 	print(t)
		

	print(letters)
	print(lens)
	for k, v in d_matches.items():
		d_matches[k] = sorted(d_matches[k], key=len)
	pprint(d_matches)






if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	in_values = read_in(args.test)
	# here_we_go_again(*in_values)
	res = solve2_dp(*in_values)

	
	print(f'Result: {res}')