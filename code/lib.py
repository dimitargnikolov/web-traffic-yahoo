import os, csv, numpy as np


def generate_pig_data(dirpath):
	for d, _, files in os.walk(dirpath):
		for filename in files:
			with open(os.path.join(d, filename), 'r') as f:
				reader = csv.reader(f, delimiter="\t")
				for row in reader:
					yield row


def hbias(numbers, N):
	if len(numbers) == 1:
		return 1.0
	else:
		return 1. - entropy(numbers) / max_entropy(N)


def entropy(nums):
	total = float(sum(nums))
	if total != 1.:
		probs = [n / total for n in nums]
	else:
		probs = nums
	return -sum([p * np.log2(p) for p in probs if p != 0])


def max_entropy(N):
	return np.log2(N)


def pbias(pagerank_counts, pagerank_pctl_ranks):

	def gini_old(sorted_list):
		height, area = 0., 0.
		for value in sorted_list:
			height += value
			area += height - value / 2.
		fair_area = height * len(sorted_list) / 2.
		return (fair_area - area) / fair_area

	def gini(x):
		# (Warning: This is a concise implementation, but it is O(n**2)
		# in time and memory, where n = len(x).  *Don't* pass in huge
		# samples!)

		# Mean absolute difference
		mad = np.abs(np.subtract.outer(x, x)).mean()
		# Relative mean absolute difference
		rmad = mad/np.mean(x)
		# Gini coefficient
		g = 0.5 * rmad
		return g


	def find_pctl_rank(pagerank):
		for rank, min_pr, max_pr, count in pagerank_pctl_ranks:
			if pagerank >= min_pr and pagerank <= max_pr:
				return rank

	pctl_rank_traffic = {}
	for pagerank, traffic in pagerank_counts.items():
		rank = find_pctl_rank(pagerank)
		if rank not in pctl_rank_traffic:
			pctl_rank_traffic[rank] = 0
		pctl_rank_traffic[rank] += traffic

	total_traffic = float(sum(pctl_rank_traffic.values()))

	ranks = [r for r, min_pr, max_pr, count in pagerank_pctl_ranks]
	all_ranks = range(np.min(ranks), np.max(ranks) + 1)

	y = []
	curr_total = 0
	for r in all_ranks:
		if r in pctl_rank_traffic:
			curr_total += pctl_rank_traffic[r]
		y.append(curr_total)

	y = [yi / total_traffic for yi in y]
	giniy = gini(y)

	return giniy


def equal(a, b, rel_tol=1e-10, abs_tol=0.0):
	return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def nth_level_domain(host, n):
	"""
	>>> nth_level_domain('facebook.com', 1)
	'com'
	>>> nth_level_domain('', 2)
	''
	>>> nth_level_domain('facebook.com', 2)
	'facebook.com'
	>>> nth_level_domain('facebook.com', 3)
	'facebook.com'
	>>> nth_level_domain('indiana.facebook.com', 2)
	'facebook.com'
	"""
	raw_parts = host.strip().split('.')
	parts = [p for p in raw_parts if p != '']
	if len(parts) <= n:
		return ".".join(parts)
	else:
		s = ".".join(n * ["%s"])
		new_parts = tuple(parts[-n:])
		return s % new_parts


if __name__ == "__main__":
	print('Testing...')
	import doctest
	doctest.testmod()
