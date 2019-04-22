import sys, os, csv, logging

sys.path.append(os.getenv("BC"))
from lib import generate_pig_data
from constants import LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)


def compute_user_click_counts(datadir):
	click_counts = {}

	all_clicks = 0
	clicks_without_user = 0
	for row in generate_pig_data(datadir):
		all_clicks += 1
		# (dt, sid, bcookie, referrer, target, refsite, refcat, targetsite, targetcat)
		# category_index will be either 5 or 6 for refsite or refcat
		user = row[1].strip()

		if user == '':
			clicks_without_user += 1
			continue
		else:
			if user not in click_counts:
				click_counts[user] = 0
			click_counts[user] += 1

	logging.debug('All clicks: %d' % all_clicks)
	logging.debug('Clicks without users: %d' % clicks_without_user)
	return click_counts


def reduce_news_dataset(datadir, dest, num_clicks):

	if not os.path.exists(os.path.dirname(dest)):
		os.makedirs(os.path.dirname(dest))

	logging.info('Computing click counts.')
	click_counts = compute_user_click_counts(datadir)
	logging.debug('Num users: %d' % len(click_counts))

	logging.info('Computing good users.')
	good_users = {user: click_count for user, click_count in click_counts.items() if click_count >= num_clicks}
	logging.debug('Num good users: %d' % len(good_users))

	logging.info('Writing results.')
	with open(dest, 'w') as f:
		writer = csv.writer(f, delimiter="\t")
		for row in generate_pig_data(datadir):
			user = row[1].strip()
			if user in good_users:
				writer.writerow(row)


if __name__ == "__main__":
	datadir = os.path.join(os.getenv('BD'), 'benzene', 'clicks', 'news', 'oct2014-news4')
	dest = os.path.join(os.getenv('BD'), 'benzene', 'clicks', 'news', 'oct2014-news4-gte10')
	reduce_news_dataset(datadir, dest, 10)
