import sys, os, csv, logging

sys.path.append(os.getenv("BC"))
from lib import generate_pig_data
from constants import LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)


def create_pageranks_dataset(pageranks_dir, dest, news_urls):

	if not os.path.exists(os.path.dirname(dest)):
		os.makedirs(os.path.dirname(dest))

	with open(dest, 'w') as f:
		writer = csv.writer(f, delimiter='\t')

		for row in generate_pig_data(pageranks_dir):
			domain = row[0].strip().lower()
			pr = float(row[1])
			if domain in news_urls:
				writer.writerow(row)


if __name__ == "__main__":
	pageranks_dir = os.path.join(os.getenv('BD'), 'benzene', 'pageranks')
	dest = os.path.join(os.getenv('BD'), 'benzene', 'pageranks-news', 'part-00000')

	if not os.path.exists(os.path.dirname(dest)):
		os.makedirs(os.path.dirname(dest))

	logging.info('Reading news urls.')
	with open(os.path.join(os.getenv('BR'), 'news', 'news-urls-filtered-2016-12-12.txt'), 'r') as f:
		news_urls = set([line.lower().strip() for line in f.readlines() if line.lower().strip() != ''])

	logging.info('Creating pagerank dataset.')
	create_pageranks_dataset(pageranks_dir, dest, news_urls)
