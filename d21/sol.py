# Template
import argparse
from collections import defaultdict
from itertools import product
from functools import lru_cache


# DOOR_KP = {
# 	'7': {'8': '>', '9': '>>', '4': 'v', '5': '>v', '6': '>>v', '1': 'vv', '2': '>vv', '3': '>>vv', '0': '>vvv', 'A': '>>vvv'},
# 	'8': {'7': '<', '9': '>', '4': '<v', '5': 'v', '6': '>v', '1': '<vv', '2': 'vv', '3': '>vv', '0': 'vvv', 'A': '>vvv'},
# 	'9': {'7': '<<', '8': '<', '4': '<<v', '5': '<v', '6': 'v', '1': '<<vv', '2': '<vv', '3': 'vv', '0': '<vvv', 'A': 'vvv'},
# 	'4': {'7': '^', '8': '>^', '9': '>>^', '5': '>', '6': '>>', '1': 'v', '2': '>v', '3': '>>v', '0': '>vv', 'A': '>>vv'},
# 	'5': {'7': '^<', '8': '^', '9': '>^', '4': '<', '6': '>', '1': '<v', '2': 'v', '3': '>v', '0': 'vv', 'A': '>vv'},
# 	'6': {'7': '^<<', '8': '^<', '9': '^', '4': '<<', '5': '<', '1': '<<v', '2': '<v', '3': 'v', '0': '<vv', 'A': 'vv'},
# 	'1': {'7': '^^', '8': '>^^', '9': '>>^^', '4': '^', '5': '>^', '6': '>>^', '2': '>', '3': '>>', '0': '>v', 'A': '>>v'},
# 	'2': {'7': '^^<', '8': '^^', '9': '>^^', '4': '^<', '5': '^', '6': '>^', '1': '<', '3': '>', '0': 'v', 'A': '>v'},
# 	'3': {'7': '^^<<', '8': '^^<', '9': '^^', '4': '^<<', '5': '^<', '6': '^', '1': '<<', '2': '<', '0': '<v', 'A': 'v'},
# 	'0': {'7': '^^^<', '8': '^^^', '9': '>^^^', '4': '^^<', '5': '^^', '6': '>^^', '1': '^<', '2': '^', '3': '>^', 'A': '>'},
# 	'A': {'7': '^^^<<', '8': '^^^<', '9': '^^^', '4': '^^<<', '5': '^^<', '6': '^^', '1': '^<<', '2': '^<', '3': '^', '0': '<'}
# }
# ROBOT_KP = {
# 	'^': {'A': '>', '<': 'v<', 'v': 'v', '>': '>v', '^': ''},
# 	'A': {'^': '<', '<': 'v<<', 'v': '<v', '>': 'v', 'A': ''},
# 	'<': {'^': '>^', 'A': '>>^', 'v': '>', '>': '>>', '<': ''},
# 	'v': {'^': '^', 'A': '>^', '<': '<', '>': '>', 'v': ''},
# 	'>': {'^': '<^', 'A': '^', '<': '<<', 'v': '<', '>': ''},
# }


DOOR_KP = { 
	"0": {"A": [">"], "8": ["^^^"]},
	"1": {"A": [">v>", ">>v"]},
	"2": {"6": [">^", "^>"], "8": ["^^"]},
	"3": {"A": ["v"]},
	"5": {"A": [">vv", "vv>"]},
	"6": {"7": ["<<^", "^<<"], "A": ["vv"]},
	"7": {"0": [">vvv"], "1": ["vv"]},
	"8": {"2": ["vv"], "3": ["vv>", ">vv"], "5": ["v"]},
	"A": {"0": ["<"], "2": ["<^", "^<"], "6": ["^^"], "8": ["^^^<", "<^^^"]}
}

ROBOT_KP = {
	"^": {"A": [">"],"<": ["v<"],"v": ["v"],">": ["v>", ">v"], "^": [""]},
	"A": {"^": ["<"],"<": ["v<<"],"v": ["<v","v<"],">": ["v"], "A": [""]},
	"<": {"^": [">^"],"A": [">>^"],"v": [">"],">": [">>"], "<": [""]},
	"v": {"^": ["^"],"A": ["^>", ">^"],"<": ["<"],">": [">"], "v": [""]},
	">": {"^": ["^<","<^"],"A": ["^"],"<": ["<<"],"v": ["<"], ">": [""]}
}


# DOOR_KP = [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], [-1, '0', 'A']]
# ROBOT_KP = [[-1, '^', 'A'], ['<', 'v', '>']]


# def _compute_paths():
# 	door_combos = defaultdict(dict)
# 	directions = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
# 	for x, line in enumerate(DOOR_KP):
# 		for y, val in enumerate(line):


def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	# Define vars here
	codes = []
	with open(f_name) as f:
		for line in f:
			codes.append(line.strip())
	return codes


def _get_shortest_sequence(code):
	print('Code: ', code)
	
	next_ = 'A'
	seq = ''
	print('Door:')
	# Door keypad
	for c in code:
		print(DOOR_KP[next_][c] + 'A', end=' ')
		seq += DOOR_KP[next_][c] + 'A'
		next_ = c
	print()


	next_ = 'A'
	robot1_seq = ''
	print('Robot 1:'),
	for c in seq:
		print(ROBOT_KP[next_][c] + 'A', end=' ')
		robot1_seq += ROBOT_KP[next_][c] + 'A'
		next_ = c

	print('\n', len(robot1_seq), '\n')
	

	next_ = 'A'
	robot2_seq = ''
	print('Robot 2:'),
	for c in robot1_seq:
		print(ROBOT_KP[next_][c] + 'A', end=' ')
		robot2_seq += ROBOT_KP[next_][c] + 'A'
		next_ = c

	
	print('\nFinal: ', len(robot2_seq), '\n')
	print()

	return len(robot2_seq)


@lru_cache(10**15)
def _get_robot_seq(s):
	seq = ''
	key = 'A'

	for ch in s:
		seq += ROBOT_KP[key][ch][0] + 'A'
		key = ch
	return seq


def _get_shortest_sequence_v2(code, nr_robots):
	print('Code: ', code)
	print('*' * 80)
	# 671A
	dumb = {'6': 'A', '7': '6', '1': '7', 'A': '1'}
	start = dumb[code]

	curr = dumb[code] # A
	# print('Door:')
	options = []
	# Door keypad
	for c in code:
		options.append(DOOR_KP[curr][c])
		curr = c
	

	min_seq_len = 10**9
	for option in product(*options):
		seq = 'A'.join(option) + 'A'
		# seq = ''.join(option)
		print(seq, len(seq))
		cnt = nr_robots
		next_seq = seq
		while cnt:
			next_seq = _get_robot_seq(next_seq)	
			# print(nr_robots - cnt, ' : ', len(next_seq))
			print(next_seq, len(next_seq))
			cnt -= 1
		min_seq_len = min(min_seq_len, len(next_seq))
		print()
	return min_seq_len



def solve(codes):
	for bots in range(5, 6):
		complexities = 0
		bot_lens = []
		for c in codes:
			# ss_len = _get_shortest_sequence(c)
			ss_len = _get_shortest_sequence_v2(c, bots)
			bot_lens.append(ss_len)
			# num_code = int(c[:-1])
			num_code = 1
			complexities += ss_len * num_code

		print(bots, ' : ', bot_lens, complexities)

	return complexities


def _idk_what_im_doing():
	distances = defaultdict(str)
	for from_, values in ROBOT_KP.items():
		for to_ in values:
			print(f'{from_}{to_} => {len(values[to_][0])}')
			distances[f'{from_}{to_}'] = len(values[to_][0])
	print('DONE 1')
	
	new_distances = defaultdict(str)
	for dist, val in distances.items():
		path = dist[0] + 'A' + dist[1] + 'A'
		path_dist = distances[dist[0] + 'A'] + distances['A' + dist[1]] + distances[dist[1] + 'A']
		new_distances[path] = path_dist
		print(f'{path} => {path_dist}')
	print('DONE')

	seq = '^^A<<^AvvA>>vA'
	dist1, dist2 = 0, 0
	for c1, c2 in zip(seq[:-1], seq[1:]):
		dist1 += distances[c1+c2]
		dist2 += new_distances[c1+'A'+c2+'A']

	print('Results: ', dist1, ' AND ', dist2)


def _i_gotta_get_that_last_star():
	for s in '^<>vA':
		new_s = s + 'A'
		print('_' * 80)
		print(f'For initial {new_s}: ')
		for _ in range(7):
			new_s = _get_robot_seq(new_s)
			print(f'R{_} : {len(new_s)}\n {new_s}\n')
		print()



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	# in_values = read_in(args.test)
	# res = solve(in_values)
	# _idk_what_im_doing()
	_i_gotta_get_that_last_star()
	res = 0
	
	print(f'Result: {res}')