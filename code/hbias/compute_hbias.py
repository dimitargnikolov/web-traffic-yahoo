import sys, os, csv, argparse, logging

sys.path.append(os.getenv("BC"))
from lib import nth_level_domain, hbias, generate_pig_data
from constants import SITE_IDX, CAT_IDX, LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)


def read_data(datadir, category_index, domain_level=None):
	index = {}

	all_clicks = 0
	clicks_without_user = 0
	for row in generate_pig_data(datadir):
		all_clicks += 1
		# (dt, sid, bcookie, referrer, target, refsite, refcat, targetsite, targetcat)
		# category_index will be either 5 or 6 for refsite or refcat
		category = row[category_index]
		user = row[1].strip()

		if user == '':
			clicks_without_user += 1
			continue

		if domain_level is not None:
			target = nth_level_domain(row[4], domain_level)
		else:
			target = row[4]

		if category not in index:
			index[category] = {}

		if user not in index[category]:
			index[category][user] = {}

		if target not in index[category][user]:
			index[category][user][target] = 0

		index[category][user][target] += 1

	logging.debug('All clicks: %d' % all_clicks)
	logging.debug('Clicks without users: %d' % clicks_without_user)
	return index


def compute_hbias(data_dir, dest, category_index, domain_level, norm_by_all_targets):

	logging.info('Reading data for %s.' % dest)
	data = read_data(data_dir, category_index, domain_level)

	# if we want to normalize by the number of all targets in the dataset,
	# we need to recover a list of unique targets
	if norm_by_all_targets:
		logging.info('Extracting unique targets.')
		unique_targets = set()
		for cat in data:
			for user in data[cat]:
				for target in data[cat][user]:
					if target not in unique_targets:
						unique_targets.add(target)
		N = len(unique_targets)

	logging.info('Computing hbias.')
	all_users = 0
	junk_users = 0
	with open(dest, 'w') as f:
		writer = csv.writer(f, delimiter="\t")
		for cat in data:
			for user in data[cat]:
				all_users += 1
				if sum(data[cat][user].values()) < 10:
					junk_users += 1
					continue

				# if we are not normalizing by the number of all targets,
				# we need to normalize by the number of targets in the current
				# user's list of targets
				if not norm_by_all_targets:
					N = len(data[cat][user].values())

				writer.writerow([cat, user, hbias(data[cat][user].values(), N)])
	logging.debug('All users: %d' % all_users)
	logging.debug('Junk users: %d' % junk_users)


def cmdline():
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('basename', type=str, help='')
	parser.add_argument('domain_level', type=int, help='')
	parser.add_argument('norm_by_all_targets', type=bool, help='')
	args = parser.parse_args()
	return args


def run_analysis(src_dir, basename, cat_idx, domain_level, norm_by_all_targets):
	src = os.path.join(src_dir, basename)
	dest = os.path.join(os.getenv('BR'), 'hbias', 'dl%d-normall%s-cat%d-%s.tab' % (domain_level, norm_by_all_targets, cat_idx, basename))
	if not os.path.exists(os.path.dirname(dest)):
		os.makedirs(os.path.dirname(dest))
	compute_hbias(src, dest, cat_idx, domain_level, norm_by_all_targets)


if __name__ == "__main__":
	domain_level = 10
	norm_by_all_targets = True

	clicks_dir = os.path.join(os.getenv('BD'), 'benzene', 'clicks')
	samples_dir = os.path.join(clicks_dir, 'sample')
	fixed_period_dir = os.path.join(clicks_dir, 'fixed-period')
	news_dir = os.path.join(clicks_dir, 'news')

	run_analysis(samples_dir, 'u1200-c100-cat', CAT_IDX, domain_level, norm_by_all_targets)
	run_analysis(samples_dir, 'u750-c1000-cat', CAT_IDX, domain_level, norm_by_all_targets)
	run_analysis(samples_dir, 'u500-c100-site', SITE_IDX, domain_level, norm_by_all_targets)
	run_analysis(samples_dir, 'u150-c100-site', SITE_IDX, domain_level, norm_by_all_targets)
	run_analysis(samples_dir, 'u500-c1000-site', SITE_IDX, domain_level, norm_by_all_targets)
	'''
	run_analysis(news_dir, 'oct2014-news1-gte10', SITE_IDX, domain_level, norm_by_all_targets)
	run_analysis(news_dir, 'oct2014-news2-gte10', SITE_IDX, domain_level, norm_by_all_targets)
	run_analysis(news_dir, 'oct2014-news3-gte10', SITE_IDX, domain_level, norm_by_all_targets)
	run_analysis(news_dir, 'oct2014-news4-gte10', SITE_IDX, domain_level, norm_by_all_targets)

	run_analysis(fixed_period_dir, 'feb2015-01to05', SITE_IDX, domain_level, norm_by_all_targets)
	run_analysis(fixed_period_dir, 'feb2015-01to05', CAT_IDX, domain_level, norm_by_all_targets)
	'''
