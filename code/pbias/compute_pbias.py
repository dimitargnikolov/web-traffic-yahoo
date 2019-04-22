import sys, os, csv, argparse, logging

sys.path.append(os.getenv("BC"))
from lib import pbias, generate_pig_data
from constants import SITE_IDX, CAT_IDX, LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)


def index_data(datadir, category_index):
	index = {}
	for row in generate_pig_data(datadir):
		# (dt, sid, bcookie, referrer, target, refsite, refcat, targetsite, targetcat)
		# category_index will be either 5 or 6 for refsite or refcat
		category = row[category_index]
		user = row[1]
		pagerank = float(row[9])
		if category not in index:
			index[category] = {}
		if user not in index[category]:
			index[category][user] = {}
		if pagerank not in index[category][user]:
			index[category][user][pagerank] = 0
		index[category][user][pagerank] += 1
	return index


def read_pagerank_pctl_ranks(filepath):
	ranks = []
	with open(filepath, 'r') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			ranks.append((int(row[0]), float(row[1]), float(row[2]), int(row[3])))
	return ranks


def compute_pbias_for_dataset(data_dir, dest, category_index, pagerank_pctl_ranks):
	if not os.path.exists(os.path.dirname(dest)):
		os.makedirs(os.path.
dirname(dest))

	print "Creating index."
	index = index_data(data_dir, category_index)

	print "Computing pbias."
	with open(dest, 'w') as f:
		writer = csv.writer(f, delimiter="\t")
		for cat in index:
			for user in index[cat]:
				writer.writerow([cat, user, pbias(index[cat][user], pagerank_pctl_ranks)])


def compute_pbias_for_sample():
	pagerank_pctl_ranks = read_pagerank_pctl_ranks(os.path.join(os.getenv('BR'), 'pbias', 'pagerank-percentile-rank-ranges.tab'))

	basename = 'u1200-c100-cat'
	print 'Processing', basename
	src = os.path.join(os.getenv('BD'), 'benzene', 'clicks', 'sample', basename)
	dest = os.path.join(os.getenv('BR'), 'pbias', '%s-dl10.tab' % basename)
	compute_pbias_for_dataset(src, dest, CAT_IDX, pagerank_pctl_ranks)

	basename = 'u750-c1000-cat'
	print 'Processing', basename
	src = os.path.join(os.getenv('BD'), 'benzene', 'clicks', 'sample', basename)
	dest = os.path.join(os.getenv('BR'), 'pbias', '%s-dl10.tab' % basename)
	compute_pbias_for_dataset(src, dest, CAT_IDX, pagerank_pctl_ranks)

	basename = 'u150-c100-site'
	print 'Processing', basename
	src = os.path.join(os.getenv('BD'), 'benzene', 'clicks', 'sample', basename)
	dest = os.path.join(os.getenv('BR'), 'pbias', '%s-dl10.tab' % basename)
	compute_pbias_for_dataset(src, dest, SITE_IDX, pagerank_pctl_ranks)

	basename = 'u500-c100-site'
	print 'Processing', basename
	src = os.path.join(os.getenv('BD'), 'benzene', 'clicks', 'sample', basename)
	dest = os.path.join(os.getenv('BR'), 'pbias', '%s-dl10.tab' % basename)
	compute_pbias_for_dataset(src, dest, SITE_IDX, pagerank_pctl_ranks)

	basename = 'u500-c1000-site'
	print 'Processing', basename
	src = os.path.join(os.getenv('BD'), 'benzene', 'clicks', 'sample', basename)
	dest = os.path.join(os.getenv('BR'), 'pbias', '%s-dl10.tab' % basename)
	compute_pbias_for_dataset(src, dest, SITE_IDX, pagerank_pctl_ranks)


def compute_pbias_for_fixed_period_data():
	print 'Reading percentile ranks.'
	pagerank_pctl_ranks = read_pagerank_pctl_ranks(os.path.join(os.getenv('BR'), 'pbias', 'pagerank-percentile-rank-ranges.tab'))

	basename = 'oct2014-gte10'

	print 'Processing', basename
	src = os.path.join(os.getenv('BD'), 'benzene', 'clicks', 'fixed-period', basename)
	dest = os.path.join(os.getenv('BR'), 'pbias', '%s-site-dl10.tab' % basename)
	compute_pbias_for_dataset(src, dest, SITE_IDX, pagerank_pctl_ranks)

	print 'Processing', basename
	src = os.path.join(os.getenv('BD'), 'benzene', 'clicks', 'fixed-period', basename)
	dest = os.path.join(os.getenv('BR'), 'pbias', '%s-cat-dl10.tab' % basename)
	compute_pbias_for_dataset(src, dest, CAT_IDX, pagerank_pctl_ranks)


def compute_pbias_for_news_data():
	print 'Reading percentile ranks.'
	pagerank_pctl_ranks = read_pagerank_pctl_ranks(os.path.join(os.getenv('BR'), 'pbias', 'pagerank-percentile-rank-ranges-news.tab'))

	basename = 'oct2014-news-gte10'

	print 'Processing', basename
	src = os.path.join(os.getenv('BD'), 'benzene', 'clicks', 'news', basename)
	dest = os.path.join(os.getenv('BR'), 'pbias', '%s-site-dl10.tab' % basename)
	compute_pbias_for_dataset(src, dest, SITE_IDX, pagerank_pctl_ranks)


def test():
	print 'Reading percentile ranks.'
	pagerank_pctl_ranks = read_pagerank_pctl_ranks(os.path.join(os.getenv('BR'), 'pbias', 'pagerank-percentile-rank-ranges.tab'))

	print 'Computing bias.'
	src = os.path.join(os.getenv('BD'), 'test', 'oct2014-gte50')
	dest = os.path.join(os.getenv('BR'), 'pbias', 'test.tab')
	compute_pbias_for_dataset(src, dest, 5, pagerank_pctl_ranks)


def main():
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('cat_index', type=int, help='The index for the referrer category. 5 for site (facebook, google, etc.), 6 for category (social, search, etc.)')
	parser.add_argument('src_dataset', type=str, help='A directory with Pig generated data for the source dataset.')
	parser.add_argument('dest', type=str, help='A file where the results will be stored.')
	args = parser.parse_args()

	if not os.path.exists(os.path.dirname(args.dest)):
		os.makedirs(os.path.dirname(args.dest))

	print 'Reading percentile ranks.'
	pagerank_pctl_ranks = read_pagerank_pctl_ranks(os.path.join(os.getenv('BR'), 'pbias', 'pagerank-percentile-rank-ranges.tab'))

	print 'Computing pbias.'
	compute_pbias_for_dataset(args.src_dataset, args.dest, args.cat_index, pagerank_pctl_ranks)


if __name__ == "__main__":
	compute_pbias_for_news_data()
