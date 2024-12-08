# Template
import argparse
import string
from pprint import pprint




def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	# Antennas will contain antenna identifier as key, and a list of all positions where that antenna is found
	char_list = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
	antennas = {
		c: [] for c in char_list
	}
	w, h = 0, 0
	with open(f_name) as f:
		for line in f:
			line = line.strip()
			w = len(line)			

			for idx, c in enumerate(line):
				if c != '.':
					antennas[c].append((h, idx))
			h += 1
			
	return antennas, w, h


def _place_antinodes(positions: list[tuple], w: int, h: int, antinodes: list[str]) -> None:
	if len(positions) < 2:
		return

	def _is_in_bounds(x, y):
		return 0 <= x < h and 0 <= y < w

	# Place all antinodes for a certain antenna type positions
	for i, ant1 in enumerate(positions):
		for ant2 in positions[i+1:]:
			x1, y1 = ant1
			x2, y2 = ant2

			dx, dy = x2 - x1, y2 - y1
			if _is_in_bounds(x3 := x1 - dx, y3 := y1 - dy):
				antinodes[x3][y3] = '#'
			if _is_in_bounds(x4 := x2 + dx, y4 := y2 + dy):
				antinodes[x4][y4] = '#'


def _place_antinodes_with_resonant_harmonics(positions: list[tuple], w: int, h: int, antinodes: list[str]) -> None:
	if len(positions) < 2:
		return

	def _is_in_bounds(x, y):
		return 0 <= x < h and 0 <= y < w

	# Place all antinodes for a certain antenna type positions
	for i, ant1 in enumerate(positions):
		for ant2 in positions[i+1:]:
			x1, y1 = ant1
			x2, y2 = ant2
			antinodes[x1][y1] = '#'
			antinodes[x2][y2] = '#'

			dx, dy = x2 - x1, y2 - y1
			
			x, y = x1, y1
			while _is_in_bounds(x := x - dx, y := y - dy):
				antinodes[x][y] = '#'

			x, y = x2, y2
			while _is_in_bounds(x := x + dx, y := y + dy):	
				antinodes[x][y] = '#'


def solve(antennas, w, h):
	antinodes = []
	for _ in range(h):
		antinodes.append(['.'] * w)
	for antenna_id in antennas:
		# _place_antinodes(antennas[antenna_id], w, h, antinodes)
		_place_antinodes_with_resonant_harmonics(antennas[antenna_id], w, h, antinodes)

	return sum([_.count('#') for _ in antinodes])



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	in_values = read_in(args.test)
	res = solve(*in_values)
	
	print(f'Result: {res}')