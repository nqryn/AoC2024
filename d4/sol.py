import re

def read_in():
	matrix = []
	with open('f_test.in') as f:
		for line in f:
			matrix.append(line.strip())
	return matrix


def _count_xmas_for_idx(i, j, w, h, mat):
	# Count all occurences of correct XMAS starting from point i, j in all directions in matrix
	directions = {
		'N': [-1, 0],
		'NE': [-1, 1],
		'E': [0, 1],
		'SE': [1, 1],
		'S': [1, 0],
		'SW': [1, -1],
		'W': [0, -1],
		'NW': [-1, -1]
	}
	next_letters = {
		'X': 'M',
		'M': 'A',
		'A': 'S',
		'S': None
	}
	count = 0
	for d, (inc_i, inc_j) in directions.items():
		# print(f'Direction: {d}')
		current_letter = 'X'
		next_i, next_j = i, j
		# print('\t', next_i, next_j)
		while True:
			# print('\t\t', current_letter)
			if not next_letters[current_letter]:
				# Found a correct match, count and continue
				# print('\t', d)
				count += 1
				break
			# check boundaries
			if not ((0 <= next_i + inc_i < h) and (0 <= next_j + inc_j < w)):
				break
			# compute next position, and check if it's the expected letter	
			next_i, next_j = next_i + inc_i, next_j + inc_j
			# print('\t', next_i, next_j)
			next_letter = mat[next_i][next_j]
			if next_letter != next_letters[current_letter]:
				# Not a good match, stop
				break
			current_letter = next_letter
	return count


def count_xmas():
	mat = read_in()
	h, w = len(mat), len(mat[0])
	total = 0
	print(f'Width: {w}, height: {h}')
	for i, line in enumerate(mat):
		for j, char in enumerate(line):
			# Only count when finding an X, in all possible directions
			if char == 'X':
				res = _count_xmas_for_idx(i, j, w, h, mat)
				total += res
				# print(res)
	return total


def is_x_mas_for_idx(i, j, mat):
	corner_directions = {
		'NE': [-1, 1],
		'SE': [1, 1],
		'SW': [1, -1],
		'NW': [-1, -1]
	}
	corner_letters = ''
	for d, (inc_i, inc_j) in corner_directions.items():
		letter = mat[i + inc_i][j + inc_j]
		if letter not in 'MS':
			return False
		corner_letters += letter

	acceptable_corners = ['SSMM', 'SMMS', 'MMSS', 'MSSM'] 
	return corner_letters in acceptable_corners
	



def count_x_mas():
	# Basically, find all A's that have 2 M's and 2 S's on non-opposite corners
	mat = read_in()
	h, w = len(mat), len(mat[0])
	total = 0
	for i, line in enumerate(mat[1:h-1]):
		for j, char in enumerate(line[1:w-1]):
			# Only count when finding an A
			if char == 'A':
				if is_x_mas_for_idx(i + 1, j + 1, mat):
					total += 1
	return total


if __name__ == '__main__':
	res = count_x_mas()
	print(f'Result: {res}')
