import sys, os

sys.path.append(os.getenv('BC'))

from lib import generate_pig_data


def create_news_list(src_dir, dest):
	news_targets = set()
	for row in generate_pig_data(src_dir):
		target = row[4].lower().strip()
		refsite = row[5].strip()
		if refsite == 'googlenews' and target not in news_targets:
			news_targets.add(target)

	with open(dest, 'w') as f:
		for target in news_targets:
			f.write('%s\n' % target)

if __name__ == '__main__':
	create_news_list(
		os.path.join(os.getenv('BD'), 'benzene', 'clicks', 'fixed-period', 'oct2014'),
		os.path.join(os.getenv('BR'), 'news-list.txt')
	)
