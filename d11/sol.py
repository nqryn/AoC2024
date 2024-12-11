# Template
import argparse
from pprint import pprint
from collections import Counter


def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	with open(f_name) as f:
		for line in f:
			return [int(x) for x in line.strip().split()]



class FSM:

	def __init__(self, stones: list[int]):
		self.stones = Counter(stones)

	def transform(self, stone: int) -> (int, int | None):
		if stone == 0:
			return (1,)
		digits = str(stone)
		digits_len = len(digits)
		if digits_len % 2 == 0:
			left, right = int(digits[:digits_len // 2]), int(digits[digits_len//2:])
			return (left, right)
		return (stone * 2024, )


	def step(self) -> None:
		stones_copy = {}
		for stone, occurences in self.stones.items():
			values = self.transform(stone)
			for v in values:
				if not v in stones_copy: 
					stones_copy[v] = 0
				stones_copy[v] += occurences
		self.stones = stones_copy


	def run(self) -> int:
		for _ in range(75):
			self.step()

		return sum(self.stones.values())



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	fsm = FSM(read_in(args.test))
	res = fsm.run()
	
	print(f'Result: {res}')