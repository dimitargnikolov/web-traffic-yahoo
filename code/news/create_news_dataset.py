import sys, os, csv, logging

sys.path.append(os.getenv("BC"))
from lib import generate_pig_data
from constants import LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)


def create_news_dataset(datadir, dest, num_clicks):

	if not os.path.exists(os.path.dirname(dest)):
		os.makedirs(os.path.dirname(dest))

	with open(dest, 'w') as f:
		writer = csv.writer(f, delimiter='\t')

		for row in generate_pig_data(datadir):
			target = row[4].lower().strip()
			if target in news_urls:
				writer.writerow(row)


if __name__ == "__main__":
	datadir = os.path.join(os.getenv('BD'), 'benzene', 'clicks', 'fixed-period', 'oct2014')
	dest = os.path.join(os.getenv('BD'), 'benzene', 'clicks', 'fixed-period', 'oct2014-news4', 'part-00000')

	logging.info('Reading news urls.')
	with open(os.path.join(os.getenv('BR'), 'news', 'news-urls-filtered-2016-12-12.txt'), 'r') as f:
		news_urls = set([line.lower().strip() for line in f.readlines() if line.lower().strip() != ''])

	logging.info('Creating dataset.')
	create_news_dataset(datadir, dest, news_urls)
