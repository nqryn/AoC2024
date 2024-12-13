# Template
import argparse
import re
from types import SimpleNamespace
from time import sleep
import math



def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'

	# Define vars here
	button_pattern = r"X\+(\d{2}), Y\+(\d{2})"
	prize_pattern = r"X=(\d+), Y=(\d+)"

	test_cases = []
	
	with open(f_name) as f:
		tc = {}
		for line in f:
			line = line.strip()
			if line == "":
				test_cases.append(tc)
				tc = {}
			match = re.search(button_pattern, line)
			if match:
				x_value, y_value = map(int, match.groups())
				if line.startswith("Button A:"):
					tc["A"] = {"x": x_value, "y": y_value, "cost": 3}
				elif line.startswith("Button B:"):
					tc["B"] = {"x": x_value, "y": y_value, "cost": 1}
			match = re.search(prize_pattern, line)
			if match:
				x_value, y_value = map(int, match.groups())
				# Part 2
				x_value += 10000000000000
				y_value += 10000000000000
				tc["prize"] = {"x": x_value, "y": y_value}

	test_cases.append(tc)
	return test_cases


def solve_tc(tc):
	prize = SimpleNamespace(**tc["prize"])
	buttons = []
	buttons.append(SimpleNamespace(**tc["A"]))
	buttons.append(SimpleNamespace(**tc["B"]))
	
	max_x = (buttons[0].x + buttons[1].x) * 100
	max_y = (buttons[0].y + buttons[1].y) * 100  

	if prize.x > max_x or prize.y > max_y:
		return -1

	dp = []
	w, h = prize.x + 1, prize.y + 1
	for _ in range(w):
		dp.append([-1] * (h))

	dp[0][0] = 0


	for x in range(w):
		for y in range(h):
			if dp[x][y] != -1:
				for b in buttons:
					if x+b.x >= w or y+b.y >= h:
						continue
					if dp[x+b.x][y+b.y] == -1:
						dp[x+b.x][y+b.y] = dp[x][y] + b.cost
					else:
						dp[x+b.x][y+b.y] = min(dp[x][y] + b.cost, dp[x+b.x][y+b.y])

	return dp[prize.x][prize.y]


# This doesn't work :(
def solve_tc_optimal(tc):
	prize = SimpleNamespace(**tc["prize"])
	buttons = []
	buttons.append(SimpleNamespace(**tc["A"]))
	buttons.append(SimpleNamespace(**tc["B"]))

	w, h = prize.x + 1, prize.y + 1
	# (x, y, cost)
	queue = [(0, 0)]
	costs = {
		(0, 0): 0,
	}
	# import pdb
	print(f'Target: {prize}')
	while queue:
		# pdb.set_trace()
		x, y = queue.pop(0)
		cost = costs[(x, y)]
		print(f'\t({x}, {y}) => {cost}')

		if x == prize.x and y == prize.y:
			return cost

		for b in buttons:
			next_x, next_y = x + b.x, y + b.y
			if next_x > prize.x or next_y > prize.y:
				continue
			queue.append((next_x, next_y))
			if (next_x, next_y) in costs:
				costs[(next_x, next_y)] = min(costs[(next_x, next_y)], cost + b.cost)
			else:
				costs[(next_x, next_y)] = cost + b.cost
	return -1
			

def solve_integer_2x2(a1, b1, c1, a2, b2, c2):
    """
    Solve a system of two linear equations for integer solutions:
    a1 * x + b1 * y = c1
    a2 * x + b2 * y = c2
    Returns (x, y) if integer solutions exist; otherwise, None.
    """
    from math import gcd

    # Step 1: Eliminate one variable (use b1 and b2 to eliminate y)
    lcm = abs(b1 * b2) // gcd(b1, b2)  # Least common multiple of b1 and b2

    # Scale equations to eliminate y
    scale1 = lcm // b1
    scale2 = lcm // b2

    a1, b1, c1 = a1 * scale1, b1 * scale1, c1 * scale1
    a2, b2, c2 = a2 * scale2, b2 * scale2, c2 * scale2

    # Eliminate y
    a_new = a1 - a2
    c_new = c1 - c2

    # Step 2: Solve for x
    if a_new == 0 or c_new % a_new != 0:
        return None  # No integer solution for x
    x = c_new // a_new

    # Step 3: Solve for y using one of the original equations
    if b1 != 0:
        y = (c1 - a1 * x) // b1
    elif b2 != 0:
        y = (c2 - a2 * x) // b2
    else:
        return None

    # Check the solution satisfies both equations
    if a1 * x + b1 * y == c1 and a2 * x + b2 * y == c2:
        return x, y
    return None



def solve_dumb(tc):
	prize = SimpleNamespace(**tc["prize"])
	buttons = []
	buttonA = SimpleNamespace(**tc["A"])
	buttonB = SimpleNamespace(**tc["B"])

	
	sol = solve_integer_2x2(buttonA.x, buttonB.x, prize.x, buttonA.y, buttonB.y, prize.y)
	if sol:
		return sol[0]*buttonA.cost + sol[1]*buttonB.cost
	return -1

	w, h = prize.x + 1, prize.y + 1
	def _test(b1, b2, mul):
		x = b1.x * mul
		y = b1.y * mul
		if (rem_x := (prize.x - x)) % b2.x == 0 and (rem_y := (prize.y - y)) % b2.y == 0:
			if rem_x / b2.x == rem_y / b2.y:
				return rem_x / b2.x
		return -1


	solutions = []
	for i in range(max_steps):
		j = _test(buttonA, buttonB, i)
		if j != -1:
			solutions.append(int(i * buttonA.cost + j * buttonB.cost))
		j = _test(buttonB, buttonA, i)
		if j != -1:
			solutions.append(int(j * buttonA.cost + i * buttonB.cost))




	return solutions


def solve(test_cases):
	total = 0
	print(f'There are {len(test_cases)} TCs')
	for i, tc in enumerate(test_cases):
		# costs = solve_dumb(tc)
		# if costs:
		# 	total += min(costs)
		# print(f'{i} => {costs}')
		c = solve_dumb(tc)
		if c!= -1:
			total += c
		print(f'{i} => {c}')
	return total
		


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	test_cases = read_in(args.test)
	res = solve(test_cases)
	
	print(f'Result: {res}')