"""
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
This example data contains six reports each containing five levels.

The engineers are trying to figure out which reports are safe. The Red-Nosed reactor safety systems can only tolerate levels that are either gradually increasing or gradually decreasing. So, a report only counts as safe if both of the following are true:

The levels are either all increasing or all decreasing.
Any two adjacent levels differ by at least one and at most three.
In the example above, the reports can be found safe or unsafe by checking those rules:

7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.
"""


def read_in():
	reports = []
	with open('f.in') as f:
		for line in f:
			levels = [int(x) for x in line.split()]
			reports.append(levels)

	return reports


def _is_safe(report):
	inc = (report[1] - report[0]) > 0
	for lvl_inf, lvl_sup in zip(report[:-1], report[1:]):
		diff = lvl_sup - lvl_inf
		if (inc and diff < 0) or (not inc and diff > 0):
			return False 
		if not(1 <= abs(diff) <= 3):
			return False
	return True

def _is_safe_tolerate(report):
	if _is_safe(report):
		return True
	for i in range(len(report)):
		new_report = report[:i] + report[i+1:]
		if _is_safe(new_report):
			return True
	return False


def count_safe_reports():
	reports = read_in()
	cnt = sum([int(_is_safe_tolerate(report)) for report in reports])
	return cnt


if __name__ == '__main__':
	res = count_safe_reports()
	print(f'Result: {res}')






