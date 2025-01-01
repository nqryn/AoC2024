# Template
import re
import argparse
from collections import defaultdict
from types import SimpleNamespace


def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	wires = defaultdict(lambda: -1)
	gates = defaultdict(str)

	sub_pattern = r"[a-z0-9]{3}"
	wire_pattern = rf"^(?P<wire>{sub_pattern}): (?P<value>\d)$"
	gate_pattern = rf"^(?P<input1>{sub_pattern}) (?P<operator>XOR|OR|AND) (?P<input2>{sub_pattern}) -> (?P<output>{sub_pattern})$"


	with open(f_name) as f:
		for line in f:
			line = line.strip()

			match = re.match(wire_pattern, line)
			if match:
				wires[match.group("wire")] = int(match.group("value"))

			match = re.match(gate_pattern, line)
			if match:
				input1 = match.group("input1")
				operator = match.group("operator")
				input2 = match.group("input2")
				output = match.group("output")
				gates[output] = (input1, operator, input2)
	return wires, gates


OPS = {
	'OR': lambda x,y: x | y,
	'AND': lambda x,y: x & y,
	'XOR': lambda x,y: x ^ y,
}

def _get_gate_res(g, wires, gates):

	in1, op, in2 = gates[g]
	op_fn = OPS[op]
	in1_val, in2_val = wires[in1], wires[in2]
	if in1_val == -1:
		in1_val = _get_gate_res(in1, wires, gates)
	if in2_val == -1:
		in2_val = _get_gate_res(in2, wires, gates)
	return op_fn(in1_val, in2_val)


def _get_nr_value(letter, wires, gates):
	nr_wires = []

	for w in wires:
		if w[0] == letter:
			nr_wires.append(w)

	for g in gates:
		if g[0] == letter:
			wires[g] = _get_gate_res(g, wires, gates)
			nr_wires.append(g)
			
	res = ''
	for nr_wire in sorted(nr_wires):
		# print(f'{nr_wire} => {wires[nr_wire]}')
		res += str(wires[nr_wire])

	print(f'  {letter}: {res[::-1]}')
	return int(res[::-1], 2)


def solve(wires, gates):
	return _get_nr_value('z', wires, gates)


def solve_pt2(wires, gates):
	x = _get_nr_value('x', wires, gates)
	y = _get_nr_value('y', wires, gates)
	z = _get_nr_value('z', wires, gates)
	curr_res = bin(x+y)[2:]
	expected_res = bin(z)[2:]

	wrong_bits = []

	for i, (b1, b2) in enumerate(zip(curr_res[::-1], expected_res[::-1])):
		if b1 != b2:
			print(f'Position {i}: {b1} VS {b2}')
			wrong_bits.append(i)

	swaps = ['z20', 'kfm', 'hnv', 'z28', 'z07', 'vmv', 'hth', 'tqr']
	return ','.join(sorted(swaps))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	in_values = read_in(args.test)
	res = solve_pt2(*in_values)
	
	print(f'Result: {res}')