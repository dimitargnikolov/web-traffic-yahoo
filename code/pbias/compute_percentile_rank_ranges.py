import sys, os, csv

sys.path.append(os.getenv('BC'))
from lib import generate_pig_data


def read_pagerank_counts(dirpath):
	pageranks = {}
	for row in generate_pig_data(dirpath):
		pr = float(row[1])
		if pr not in pageranks:
			pageranks[pr] = 0
		pageranks[pr] += 1
	return pageranks


def compute_percentile_ranks(pagerank_counts):
	ranks = {}
	pageranks = sorted(pagerank_counts.keys())
	total = float(sum(pagerank_counts.values()))
	count = 0
	for pr in pageranks:
		ranks[pr] = count / total
		count += pagerank_counts[pr]
	return ranks


def compute_percentile_rank_ranges(percentile_ranks, pagerank_counts):
	ranks = range(1, 101)
	mins = {p: 1 for p in ranks}
	maxes = {p: 0 for p in ranks}
	counts = {p: 0 for p in ranks}

	for pagerank in percentile_ranks:
		prank = int(round(percentile_ranks[pagerank] * 100))
		if prank == 0:
			prank = 1
		if pagerank < mins[prank]:
			mins[prank] = pagerank
		if pagerank > maxes[prank]:
			maxes[prank] = pagerank
		counts[prank] += pagerank_counts[pagerank]

	final_ranks = []
	for rank in ranks:
		final_ranks.append((rank, mins[rank], maxes[rank], counts[rank]))
	return final_ranks


def main():
	src = os.path.join(os.getenv('BD'), 'benzene', 'pageranks-news')
	dest1 = os.path.join(os.getenv('BR'), 'pbias', 'pagerank-percentile-ranks-news.tab')
	dest2 = os.path.join(os.getenv('BR'), 'pbias', 'pagerank-percentile-rank-ranges-news.tab')

	if not os.path.exists(os.path.dirname(dest1)):
		os.makedirs(os.path.dirname(dest1))

	print 'Reading pagerank counts.'
	pagerank_counts = read_pagerank_counts(src)

	print 'Sorting ranks.'
	percentile_ranks = compute_percentile_ranks(pagerank_counts)

	with open(dest1, 'w') as f:
		writer = csv.writer(f, delimiter='\t')
		for rank in sorted(percentile_ranks):
			writer.writerow([rank, percentile_ranks[rank]])

	print 'Computing percentile ranges.'
	percentile_ranges = compute_percentile_rank_ranges(percentile_ranks, pagerank_counts)

	print 'Writing results.'
	with open(dest2, 'w') as f:
		writer = csv.writer(f, delimiter='\t')
		for row in percentile_ranges:
			if row[3] == 0:
				continue
			writer.writerow(row)


if __name__ == '__main__':
	main()
