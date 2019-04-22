import sys, os, logging, csv
from operator import itemgetter

sys.path.append(os.getenv("BC"))
from lib import generate_pig_data
from constants import LOGGING_LEVEL, SITE_IDX, CAT_IDX

logging.basicConfig(level=LOGGING_LEVEL)


def count_users_per_cat(datadir, least_num_clicks):
	counts = {}

	logging.debug('Counting click counts per user per cat.')
	for row in generate_pig_data(datadir):
		# (dt, sid, bcookie, referrer, target, refsite, refcat, targetsite, targetcat)
		# category_index will be either 5 or 6 for refsite or refcat
		user = row[1].strip()
		site = row[SITE_IDX]
		cat = row[CAT_IDX]

		assert user != ''

		if site not in counts:
			counts[site] = {}
		if cat not in counts:
			counts[cat] = {}

		if user not in counts[site]:
			counts[site][user] = 0
		if user not in counts[cat]:
			counts[cat][user] = 0

		counts[site][user] += 1
		counts[cat][user] += 1

	logging.debug('Counts computed. Processing results.')
	cat_counts = {}
	for cat in counts:
		if cat not in cat_counts:
			cat_counts[cat] = 0
			if least_num_clicks is not None:
				for user in counts[cat]:
					if counts[cat][user] >= least_num_clicks:
						cat_counts[cat] += 1
			else:
				cat_counts[cat] = len(counts[cat])

	for cat in sorted(cat_counts.keys()):
		logging.info('%s\t%d' % (cat, cat_counts[cat]))


def find_popular_targets(datadir, site, dest):
	targets = {}

	logging.debug('Reading data.')
	for row in generate_pig_data(datadir):
		# (dt, sid, bcookie, referrer, target, refsite, refcat, targetsite, targetcat)
		# category_index will be either 5 or 6 for refsite or refcat
		user = row[1].strip()
		curr_site = row[SITE_IDX]
		target = row[4].strip()

		assert user != ''

		if curr_site == site:
			if user not in targets:
				targets[user] = {}

			if target not in targets[user]:
				targets[user][target] = 0
			targets[user][target] += 1

	logging.debug('Writing.')
	with open(dest, 'w') as f:
		writer = csv.writer(f, delimiter='\t')
		for user in targets:
			sorted_targets = sorted(targets[user].items(), reverse=True, key=itemgetter(1))
			for target, count in sorted_targets:
				writer.writerow([user, target, count])


if __name__ == "__main__":
	datadir = os.path.join(os.getenv('BD'), 'benzene', 'clicks', 'news', 'oct2014-news3-gte10')
	destdir = os.path.join(os.getenv('BR'), 'news')
	if not os.path.exists(destdir):
		os.makedirs(destdir)

	#count_users_per_cat(datadir, 10)
	cat = 'pinterest'
	find_popular_targets(datadir, cat, os.path.join(destdir, 'news3-%s.tab' % cat))
