# Template
import argparse
from collections import defaultdict
from pprint import pprint


def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	connections = []
	with open(f_name) as f:
		for line in f:
			connections.append(line.strip().split('-'))
	return connections


def solve(connections):
	links = defaultdict(list)
	for c1, c2 in connections:
		links[c1].append(c2)
		links[c2].append(c1)


	print(len(links), len(links['xt']))
	# pprint(links)


	lans = set()

	# Part 1
	# for c1, c1_neighbours in links.items():
	# 	if c1[0] == 't':
	# 		for c2 in c1_neighbours:
	# 			c2_neighbours = links[c2]
	# 			common = set(c1_neighbours) & set(c2_neighbours)
	# 			print(c1, c2, common)
	# 			if len(common) >= 1:
	# 				for c3 in common:
	# 					lan_key = sorted([c1, c2, c3])
	# 					lans.add(''.join(lan_key))


	def _is_clique(computers):
		for i, c1 in enumerate(computers):
			for c2 in computers[i+1:]:
				if c1 not in links[c2]:
					return False
		return True


	max_clique = []
	for c1, c1_neighbours in links.items():
		clique = c1_neighbours[:1]
		for c2 in c1_neighbours[1:]:
			clique.append(c2)
			if not _is_clique(clique):
				# print(len(clique), c1, ' MAX ', clique[:-1], len(clique))
				if len(clique) > len(max_clique):
					max_clique = clique[:-1]
					max_clique.append(c1)
				break

	print(','.join(sorted(max_clique)))



	def _find_recursive_common_neighbours(c1, c1_neighbours, visited):
		if not c1_neighbours:
			return set()

		for c2 in c1_neighbours:
			if c2 not in visited:
				visited.append(c2)
				c2_neighbours = links[c2]
				common_neighbours = set(c1_neighbours) & set(c2_neighbours)
				return _find_recursive_common_neighbours(c2, common_neighbours, visited)
			


					
	return len(lans)


	pprint(lans)
	# for k, v in lans.items():
	# 	if k[0] == 't':
	# 		print(k, ' => ', v)

	# sets = set()
	# for k, v in lans.items():
	# 	if k[0] == 't':
	# 		for i, c1 in enumerate(v):
	# 			for c2 in v[i+1:]:
	# 				set_k = sorted([k, c1, c2])
	# 				sets.add('-'.join(set_k))
	# print(sets)



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	in_values = read_in(args.test)
	res = solve(in_values)
	
	print(f'Result: {res}')