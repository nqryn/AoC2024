# Template
import argparse
from types import SimpleNamespace
from enum import Enum

class Dir(Enum):
	E = 0
	N = 1
	W = 2
	S = 3


def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	# Define vars here
	walls = []
	start, end = -1, -1
	with open(f_name) as f:
		for x, line in enumerate(f):
			line = line.strip()
			wl = []
			for y, ch in enumerate(line):
				if ch == '#':
					wl.append(True)
					continue
				if ch == 'S':
					start = SimpleNamespace(x=x, y=y, d=Dir.E)
				if ch == 'E':
					stop = SimpleNamespace(x=x, y=y)
				wl.append(False)
			walls.append(wl)


	return walls, start, stop


def next_p(p, w, h):
	go = {
		Dir.E: [0, -1],
		Dir.W: [0, 1],
		Dir.N: [-1, 0],
		Dir.S: [1, 0],
	}
	nx, ny = p.x + go[p.d][0], p.y + go[p.d][1]
	if 0 > nx or nx >= h or 0 > ny or ny >= w:
		return None
	return SimpleNamespace(x=nx, y=ny, d=p.d)



def solve(walls, start, stop):
	costs = {
		(start.x, start.y, start.d): 0 
	}

	queue = [start]
	w, h = len(walls[0]), len(walls)

	# Smol keeps the cost of the shortest path to END
	smol = 10000000000
	# Keep the previous best nodes for each node 
	best_prevs = {
		(start.x, start.y, start.d): []
	}

	while queue:
		p = queue.pop(0)
		# Key is always position + direction
		p_key = (p.x, p.y, p.d)
		
		if p.x == stop.x and p.y == stop.y:
			smol = min(smol, costs[p_key])

		# Move
		np = next_p(p, w, h)
		if np and not walls[np.x][np.y]:
			cost = costs[p_key] + 1

			key = (np.x, np.y, np.d)
			# Don't stop when first finding a solution, there might be better ones
			if np.x == stop.x and np.y == stop.y:
				print(np.d, ' ===> ', cost)

			if (key in costs and cost < costs[key]) or (key not in costs):
				best_prevs[key] = [p]
				costs[key] = cost
				queue.append(np)
			if (key in costs and cost == costs[key]) and p not in best_prevs[key]:
				best_prevs[key].append(p)

		# Rotate
		for rot in [1, -1, 2]:
			next_d = Dir((p.d.value + rot) % 4)

			np = SimpleNamespace(x=p.x, y=p.y, d=next_d)
			if (nps := next_p(np, w, h)) and not walls[nps.x][nps.y]:
				cost = costs[p_key] + abs(rot) * 1000

				key = (np.x, np.y, next_d)
				if (key in costs and cost < costs[key]) or (key not in costs):
					costs[key] = cost
					best_prevs[key] = [p]
					queue.append(np)
				
				if (key in costs and cost == costs[key]) and p not in best_prevs[key]:
					best_prevs[key].append(p)
	

	# Compute reverse paths from end node: go in all directions that have smol value
	paths = []
	for i in range(4):
		k = (stop.x, stop.y, Dir(i))
		if k in costs and costs[k] == smol:
			paths.append(k)
	
	# Use a set to count distinct tiles for best paths
	dist = set()
	while paths:
		n = paths.pop(0)
		# Here, we only care if a tile was visited, not the direction
		dist.add(n[:2])
		if best_prevs[n]:
			paths.extend([(n.x, n.y, n.d) for n in best_prevs[n]])

	# Result for second part
	return len(dist)

	# Pretty print all visited tiles that are part of best paths
	for x in range(h):
		for y in range(w):
			if walls[x][y]:
				print('#', end='')
				continue
			if (x, y) in dist:
				print('O', end='')
				continue
			print('.', end='')
		print()


	return smol




if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	in_values = read_in(args.test)
	res = solve(*in_values)
	
	print(f'Result: {res}')