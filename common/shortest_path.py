# Function to find the shortest path between two nodes of a graph
def bfs_sp(start, goal, get_neighbours):
	visited = []
	queue = [[start]]
	
	if start == goal:
		return []

	while queue:
		path = queue.pop(0)
		node = path[-1]
		
		if node not in visited:
			neighbours = get_neighbours(node)
			
			for neighbour in neighbours:
				new_path = list(path)
				new_path.append(neighbour)
				queue.append(new_path)
				
				if neighbour == goal:
					return new_path
			visited.append(node)

	return []

