import sys, os, csv, logging

sys.path.append(os.getenv("BC"))
from lib import generate_pig_data
from constants import LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)


def collect_pr_vs_volume_data(clicks_dir, dest):
	prs = {}
	for row in generate_pig_data(clicks_dir):
		pr = row[-1]
		if pr not in prs:
			prs[pr] = 0
		prs[pr] += 1

	sorted_prs = sorted([(float(pr), pr) for pr in prs.keys()], reverse=True)
	with open(dest, 'w') as f:
		writer = csv.writer(f, delimiter='\t')
		for (pr_fl, pr_str) in sorted_prs:
			writer.writerow([pr_str, prs[pr_str]])


if __name__ == "__main__":
	clicks_dir = os.path.join(os.getenv('BD'), 'benzene', 'clicks', 'news', 'news-targets-with-pageranks-gte10')
	dest = os.path.join(os.getenv('BR'), 'pr-vs-volume.csv')

	if not os.path.exists(os.path.dirname(dest)):
		os.makedirs(os.path.dirname(dest))

	collect_pr_vs_volume_data(clicks_dir, dest)
