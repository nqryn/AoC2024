import re

def read_in():
	dep_graph = {}
	printing_orders = []
	with open('f.in') as f:
		# Read dependencies
		for line in f:
			if line == '\n':
				break
			before, after = (int(x) for x in line.strip().split('|'))
			if before not in dep_graph:
				dep_graph[before] = []
			# Keep each dependency only once
			if after not in dep_graph[before]:
				dep_graph[before].append(after)
		# Read printing orders
		for line in f:
			po = [int(x) for x in line.strip().split(',')]
			printing_orders.append(po)
	return dep_graph, printing_orders


def _compute_transitive_closure(graph):
    def dfs(node, visited):
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                dfs(neighbor, visited)

    transitive_closure = {}
    for node in graph:
        visited = set()
        dfs(node, visited)
        transitive_closure[node] = list(visited)

    return transitive_closure


def _is_correct_po(po, dep_graph):
	# Go through the printing order
	# For each element, check all previous items in its dep graph entry
	for idx, page in enumerate(po):
		if page not in dep_graph:
			continue
		prev_items = po[:idx]
		for dep in dep_graph[page]:
			if dep in prev_items:
				return False

	return True


def _reorder_po(po, dep_graph):
	# Reorder po to make it correct
	new_po = []
	for idx, page in enumerate(po):
		if page not in dep_graph:
			new_po.append(page)
			continue
		prev_items = po[:idx]
		for prev in prev_items:
			if prev in dep_graph[page]:
				# should insert current page before
				prev_idx = new_po.index(prev)
				new_po.insert(prev_idx, page)
				break
		else:
			new_po.append(page)
	return new_po



def compute_correct_orders_middle_page_sum():
	dep_graph, printing_orders = read_in()
	total = 0
	for po in printing_orders:
		if _is_correct_po(po, dep_graph):
			total += po[len(po)//2]

	return total


def compute_incorrect_orders_middle_page_sum():
	dep_graph, printing_orders = read_in()
	total = 0
	for po in printing_orders:
		correct = True
		while not _is_correct_po(po, dep_graph):
			correct = False
			po = _reorder_po(po, dep_graph)

		if not correct:
			total += po[len(po)//2]
	return total



if __name__ == '__main__':
	dep_graph, printing_orders = read_in()

	# res = compute_correct_orders_middle_page_sum()
	res = compute_incorrect_orders_middle_page_sum()
	
	print(f'Result: {res}')