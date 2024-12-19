# Template
import argparse


def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	# Define vars here
	disk_map = []
	with open(f_name) as f:
		for line in f:
			# Remeber to line.strip() !!!!
			disk_map = [int(x) for x in line.strip()]
	return disk_map


def solve(disk_map):
	last_id = len(disk_map) // 2
	last_id_idx = -1
	first_id = 0

	curr_pos = 0
	total = 0
	curr_id = 0
	is_space = False

	ids_map = []

	while last_id >= first_id:
		if not is_space:
			ids_map.append((first_id, disk_map[curr_pos]))
			first_id += 1
			is_space = True
			curr_pos += 1
		else:
			slots = disk_map[curr_pos]
			need = disk_map[last_id_idx]

			if slots > need:
				ids_map.append((last_id, need))
				disk_map[last_id_idx] = 0
				disk_map[curr_pos] -= need
				last_id -= 1
				last_id_idx -= 2
			else:
				ids_map.append((last_id, slots))
				disk_map[last_id_idx] -= slots
				is_space = False
				curr_pos += 1

	# # WOOHOOOO
	# print(ids_map)
	# for t in ids_map:
	# 	print(str(t[0]) * t[1], end='')
	# print()

	total = 0
	curr_pos = 0
	for file_id, cnt in ids_map:
		for inc in range(cnt):
			# print(f'{file_id} * {curr_pos}')
			total += file_id * curr_pos
			curr_pos += 1
	return total


def solve_second(disk_map):
	SPACE = -1
	curr_id = 0
	is_space = False

	ids_map = []

	# Build ids map such that we keep spaces with -1 key
	for idx, block_size in enumerate(disk_map):
		if is_space:
			ids_map.append((SPACE, block_size))
			is_space = False
		else:
			ids_map.append((curr_id, block_size))
			curr_id += 1
			is_space = True

	# print(ids_map) # [(0, 1), (-1, 2), (1, 3), (-1, 4), (2, 5)]

	# start from the end and try to move files to the left where they fit
	end = -1
	while abs(end) < len(ids_map):
		file_id, file_size = ids_map[end]
		if file_id == SPACE:
			end -= 1
			continue
		for idx, (block_id, block_size) in enumerate(ids_map[:len(ids_map) + end]):
			if block_id == SPACE and block_size >= file_size:
				# Move, bitch
				ids_map[idx] = (file_id, file_size)
				if block_size > file_size:
					ids_map.insert(idx+1, (SPACE, block_size - file_size))
				ids_map[end] = (SPACE, file_size)
				break
		end -= 1

	# # LGTM <3
	# print(ids_map)
	# for t in ids_map:
	# 	if t[0] == SPACE:
	# 		print('.' * t[1], end='')
	# 	else:
	# 		print(str(t[0]) * t[1], end='')
	# print()

	total = 0
	curr_pos = 0
	for file_id, cnt in ids_map:
		if file_id == SPACE:
			file_id = 0
		for inc in range(cnt):
			# print(f'{file_id} * {curr_pos}')
			total += file_id * curr_pos
			curr_pos += 1
	return total	



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	disk_map = read_in(args.test)
	res = solve_second(disk_map)
	
	print(f'Result: {res}')