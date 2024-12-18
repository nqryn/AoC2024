# Template
import argparse
from types import SimpleNamespace
from common.shortest_path import bfs_sp


def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	
	falling_bytes = []
	with open(f_name) as f:
		for line in f:
			x, y = line.strip().split(',')
			falling_bytes.append(SimpleNamespace(x=int(x), y=int(y)))
	return falling_bytes


def solve(fb, size, bytes_cnt):
	corrupted = [(b.x, b.y) for b in fb[:bytes_cnt]]

	def _get_neighbours(tpl):
		(x, y) = tpl
		nb = []
		for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
			nx = x + i
			ny = y + j
			if 0 <= nx < size and 0 <= ny < size and (nx, ny) not in corrupted:
				nb.append((nx, ny))
		return nb

	sp = bfs_sp((0, 0), (size-1, size-1), _get_neighbours)
	print(sp)
	return len(sp) - 1

def solve2(fb, size, min_bytes_cnt):
	corrupted = [(b.x, b.y) for b in fb[:min_bytes_cnt]]
	def _get_neighbours(tpl):
		(x, y) = tpl
		nb = []
		for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
			nx = x + i
			ny = y + j
			if 0 <= nx < size and 0 <= ny < size and (nx, ny) not in corrupted:
				nb.append((nx, ny))
		return nb

	next_ = min_bytes_cnt
	sp = bfs_sp((0, 0), (size-1, size-1), _get_neighbours)

	while next_ < len(fb):
		next_byte = (fb[next_].x, fb[next_].y)
		corrupted.append(next_byte)

		if next_byte in sp:
			# If the falling byte is in path, we need to see if another path is valid
			sp = bfs_sp((0, 0), (size-1, size-1), _get_neighbours)	
			if not sp:
				return next_byte	
		
		next_ += 1


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	in_values = read_in(args.test)
	size = 7 if args.test else 71
	bytes_cnt = 12 if args.test else 1024
	res = solve2(in_values, size, bytes_cnt)
	
	print(f'Result: {res}')