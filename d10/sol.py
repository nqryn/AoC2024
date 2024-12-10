# Template
import argparse


def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	# Define vars here
	trail_map = []
	with open(f_name) as f:
		for line in f:
			trail_map.append(line.strip())
	return trail_map


def _compute_trailhead_score(i: int, j: int, trail_map: list[str]) -> (int, int):
	w, h = len(trail_map[0]), len(trail_map)
	trails = []
	curr_val = '0'
	curr_i, curr_j = i, j
	def _is_in_bounds(i, j):
		return 0 <= i < h and 0 <= j < w

	def _get_next_val(curr_val: str):
		return chr(ord(curr_val) + 1)

	trailtails = set()
	ratings = 0

	while True:
		# For each direction (up, down, left, right) check if we can have a correct trail for the current position
		next_val = _get_next_val(curr_val)
		for inc_i, inc_j in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
			new_i, new_j = curr_i + inc_i, curr_j + inc_j
			if not _is_in_bounds(new_i, new_j):
				continue
			value = trail_map[new_i][new_j]
			if value != next_val:
				continue
			if value == '9':
				trailtails.add((new_i, new_j))
				ratings += 1
				continue
			trails.append((value, new_i, new_j))
		# Finish when all trails have finished
		if not trails:
			break
		curr_val, curr_i, curr_j = trails.pop(0)
	return len(trailtails), ratings




def compute_trailhead_scores_sum(trail_map: list[str]) -> (int, int):
	total1, total2 = 0, 0
	for i, line in enumerate(trail_map):
		for j, char in enumerate(line):
			if char == '0':
				score, rating = _compute_trailhead_score(i, j, trail_map)
				total1 += score
				total2 += rating
	return total1, total2
	


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	trail_map = read_in(args.test)
	res1, res2 = compute_trailhead_scores_sum(trail_map)
	
	print(f'Results: {res1} {res2}')