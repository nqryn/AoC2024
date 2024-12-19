# Template
import argparse
from types import SimpleNamespace
from math import trunc
from time import sleep


def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	
	registers = SimpleNamespace(a=0, b=0, c=0)
	instructions = []
	with open(f_name) as f:
		a = f.readline().strip().split(': ')[1]
		registers.a = int(a)
		b = f.readline().strip().split(': ')[1]
		registers.b = int(b)
		c = f.readline().strip().split(': ')[1]
		registers.c = int(c)
		f.readline()
		program = f.readline().strip().split(': ')[1]
		instructions = [int(x) for x in program.split(',')]
		
	return registers, instructions


def op(registers, opcode, operand, outputs):
	operators = {0:0, 1:1, 2:2, 3:3, 4:registers.a, 5:registers.b, 6:registers.c}
	if opcode == 0:
		# adv => a division (combo) => a
		registers.a = trunc(registers.a / (2 ** operators[operand]))
	elif opcode == 1:
		# bxl = b bitwise xor (literal) => b
		registers.b = registers.b ^ operand
	elif opcode == 2:
		# bst = (combo) modulo 8 => b
		registers.b = operators[operand] % 8
	elif opcode == 3:
		# jnz = jump not zero (a)
		if registers.a != 0:
			return operand
	elif opcode == 4:
		# bxc = b bitwise xor c (ignore operand) => b
		registers.b = registers.b ^ registers.c
	elif opcode == 5:
		# out = (combo) modulo 8 => outputs it
		outputs.append(operators[operand] % 8)
	elif opcode == 6:
		# bdv = a division (combo) => b
		registers.b = trunc(registers.a / (2 ** operators[operand]))
	elif opcode == 7:
		# cdv = a division (combo) => c
		registers.c = trunc(registers.a / (2 ** operators[operand]))


def solve(registers, instructions):
	outputs = []
	opcode_idx = 0
	while True:
		if opcode_idx >= len(instructions):
			# Halt
			return outputs
		opcode, operand = instructions[opcode_idx:opcode_idx+2]
		ret = op(registers, opcode, operand, outputs)

		if ret is not None:
			opcode_idx = ret
		else:
			opcode_idx += 2


# Will brute force work? 🤔
def solve2(registers, instructions):
	for a in range(10000000000000):
		if a % 1_000 == 0:
			print('>', end=' ')
		if a % 100_000 == 0:
			print(a)
		registers.a = a
		if solve(registers, instructions) == instructions:
			return a

def solve3(registers, instructions):
	# outputs_d = {}
	# for a in range(8**15, 8**16-1):
		
	# 	registers.a = a
	# 	res = solve(registers, instructions)
	# 	print(f'For value {a} we got result {res} and octal {oct(a)}')
	# 	if res == instructions:
	# 		return a

		# a_size = len(str(a))
		# out_size = len(res)
		# if a_size in outputs_d:
		# 	if out_size not in outputs_d[a_size]:
		# 		print(a, out_size)
		# 	outputs_d[a_size].add(out_size)
		# else:
		# 	print(a, out_size)
		# 	outputs_d[a_size] = set([out_size])
		# assert len(res) == len(instructions), f"Got {len(res)}"
		# key = tuple(res)
		# if key in outputs_d:
		# 	outputs_d[key].append(a)
		# else:
		# 	outputs_d[key] = [a]

		# if a == 8**15 + 5000:
		# 	break

	# print()
	# for key, value in outputs_d.items():
	# 	print(key, ' => ', value)
	# size = len(instructions)-1
	# start = 4*(8**size) + 3*(8**(size-1)) + 5*(8**(size-2)) + 4*(8**(size-3)) + 3*(8**(size-4)) + 3*(8**(size-5)) + 3*(8**(size-6))
	# stop = start + 8

	# def gbz(nr):
	# 	octal = oct(nr)
	# 	return list(map(int, octal[2:]))[::-1]

	# print(instructions)
	# for a in range(start, stop):
	# 	registers.a = a
	# 	res = solve(registers, instructions)
	# 	print(f'{res} => {gbz(a)}')
	# 	if res == instructions:
	# 		return a

	size = len(instructions)-1

	# curr_nr = 0
	# helpme = []
	# for i in range(size, -1, -1):
	# 	for step in range(8):
	# 		tmp = curr_nr + step * (8 ** i)
	# 		registers.a = tmp
	# 		res = solve(registers, instructions)
	# 		print(res)
	# 		if len(res) == size+1 and res[i] == instructions[i]:
	# 			print(f'For index {i} we found value {step}')
	# 			curr_nr = tmp
	# 			helpme.append(step)
	# 			break
	# 	else:
	# 		print('No solution for index ', i)
	
	# print(curr_nr, helpme)
	# registers.a = curr_nr
	# print(solve(registers, instructions), ' == ', instructions)

	start = oct(8**size)


	print(int(start, 8), start)

	registers.a = int(start, 8)
	print(instructions, ' => ', solve(registers, instructions))

	i = 0
	val = 1
	curr = start
	while i <= size:
		curr = curr[:i+2] + str(val) + curr[i+3:]
		registers.a = int(curr, 8)
		res = solve(registers, instructions)
		if len(res) == size+1 and res[size - i] == instructions[size - i]:
			# Good value, move on to the next number
			i += 1
			val = 0
		else:
			while val == 7:
				# Backtrack
				curr = curr[:i+2] + '0' + curr[i+3:]
				i -= 1
				val = int(curr[i+2])
			
			val += 1

	print(curr, int(curr, 8))
	registers.a = int(curr, 8)
	print(instructions, ' AAAHHHHH ', solve(registers, instructions) == instructions)

	# nr = int(curr, 8)
	# for a in range(nr, nr + 8):
	# 	registers.a = a
	# 	res = solve(registers, instructions)
	# 	# print(f'{res} => {gbz(a)}')
	# 	if res == instructions:
	# 		print('HERE IS JOHNYY')
	# 		return a




	# s = len(instructions)
	# for i in range(8):
	# 	st = str(i) * s
	# 	nr = int(st, 8)
	# 	print(st)
	# 	if not i:
	# 		nr = int('1' + str(i) * (s - 1), 8)
	# 	registers.a = nr
	# 	res = solve(registers, instructions)
	# 	print(res, ' => ', i)



def tc():
	def _go(instrs, a=0, b=0, c=0):
		registers = SimpleNamespace(a=a, b=b, c=c)
		return solve(registers, instrs), registers

	# If register C contains 9, the program 2,6 would set register B to 1.
	outs, regs = _go([2,6], c=9)
	assert outs == [], f"Got {outs} instead"
	assert regs.b == 1
	# If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
	outs, regs = _go([5,0,5,1,5,4], a=10)
	assert outs == [0,1,2], f"Got {outs} instead"
	# If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
	outs, regs = _go([0,1,5,4,3,0], a=2024)
	assert outs == [4,2,5,6,7,7,7,7,3,1,0], f"Got {outs} instead"
	assert regs.a == 0
	# If register B contains 29, the program 1,7 would set register B to 26.
	outs, regs = _go([1,7], b=29)
	assert outs == [], f"Got {outs} instead"
	assert regs.b == 26
	# If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
	outs, regs = _go([4,0], b=2024, c=43690)
	assert outs == [], f"Got {outs} instead"
	assert regs.b == 44354


if __name__ == '__main__':
	# tc()
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	in_values = read_in(args.test)
	res = solve3(*in_values)
	print('Results: ', res)
	
	# res = solve(*in_values)
	# print(f'Result: {','.join(map(str, res))}')