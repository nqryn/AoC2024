
def read_in():
	left_list, right_list = [], []
	with open('1.in') as f:
		for line in f:
			l, r = line.split('   ')
			left_list.append(int(l))
			right_list.append(int(r))

	return left_list, right_list


def compute_total_distance():
	ll, rl = read_in()
	sll, srl = sorted(ll), sorted(rl)
	result = 0
	for x, y in zip(sll, srl):
		result += abs(x-y)
	return result



def compute_similarity_score():
	ll, rl = read_in()
	sim_score = 0
	for elem in ll:
		cnt = sum([int(elem == x) for x in rl])
		sim_score += cnt * elem
	return sim_score

if __name__ == '__main__':
	res = compute_total_distance()
	# res = compute_similarity_score()
	print(f'Result: {res}')