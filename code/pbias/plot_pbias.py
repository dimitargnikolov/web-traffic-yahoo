import sys, os, csv, matplotlib, numpy
from operator import itemgetter

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages

sys.path.append(os.getenv("BC") + '-old')
from constants import CATEGORY_COLORS, ALL_COLORS, DISPLAY_LABELS
from plotting import set_common_rc_params

from matplotlib import rcParams
set_common_rc_params(rcParams)

TITLE_FONT_SIZE = 36
XAXIS_FONT_SIZE = 36
YAXIS_FONT_SIZE = 28


def read_data(filepath):
	hs = {}
	with open(filepath, 'r') as f:
		reader = csv.reader(f, delimiter="\t")
		for row in reader:
			try:
				cat = row[0]
				h = float(row[2])
				if cat not in hs:
					hs[cat] = []
				hs[cat].append(h)
			except:
				print 'Could not read:', row
				exit()
	return hs


def plot_pbias(dest, user_bias, cat_excludes=set(), xline=None,
			   title=None, xlabel=None, ylabel=None, show_legend=False, elinewidth=2,
			   xticksfont=XAXIS_FONT_SIZE, yticksfont=YAXIS_FONT_SIZE):

	if not os.path.exists(os.path.dirname(dest)):
		os.makedirs(os.path.dirname(dest))

	# plot using bars
	cats_means = {cat: numpy.mean(h) for cat, h in user_bias.items() if cat not in cat_excludes}
	ordered_cats_means = sorted(cats_means.items(), key=itemgetter(1))
	cats, means = zip(*ordered_cats_means)
	errs = [2 * numpy.std(user_bias[c]) / numpy.sqrt(len(user_bias[c])) for c in cats]

	error_config = {'linewidth': elinewidth, 'capsize': 0, 'ecolor': '#000000'}

	x = range(len(means))

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)

	ax.barh(x, means,
			alpha=1, align='center', linewidth=1,
			color=[ALL_COLORS[c] for c in cats],
			xerr=errs, error_kw=error_config)

	if show_legend:
		patches = []
		for cat in sorted(CATEGORY_COLORS):
			p = mpatches.Patch(
				edgecolor='#000000',
				linewidth=1,
				facecolor=CATEGORY_COLORS[cat],
				label=DISPLAY_LABELS[cat]
			)
			patches.append(p)
		plt.legend(handles=patches, loc='lower left')

	ax.set_ylim(bottom=x[0] - 1, top=x[-1] + 1)

	yvals = numpy.linspace(x[0] - 1, x[-1] + 1, 50)

	if xline is not None:
		yvals = numpy.linspace(x[0] - 1, x[-1] + 1, 50)
		ax.plot([xline for _ in range(len(yvals))], yvals, color='#000000')
		ax.annotate('random walker\nbaseline',
					xy=(xline - .005, x[0] - .7), xycoords='data',
					xytext=(50, 10), textcoords='offset points',
					arrowprops=dict(
						arrowstyle="->",
						connectionstyle="angle3,angleA=90,angleB=0"
					)
		)

	plt.yticks(x, [DISPLAY_LABELS[c] if c in DISPLAY_LABELS else c for c in cats])

	plt.legend()

	for tick in ax.yaxis.get_major_ticks():
		tick.label.set_fontsize(yticksfont)

	for tick in ax.xaxis.get_major_ticks():
		tick.label.set_fontsize(xticksfont)

	if title is not None:
		plt.title(title, fontsize=TITLE_FONT_SIZE, y=1.02)

	if xlabel is not None:
		ax.set_xlabel(xlabel, fontsize=TITLE_FONT_SIZE)

	if ylabel is not None:
		ax.set_ylabel(ylabel, fontsize=TITLE_FONT_SIZE)

	if not os.path.exists(os.path.dirname(dest)):
		os.makedirs(os.path.dirname(dest))

	plt.tight_layout()

	pp = PdfPages(dest)
	fig.savefig(pp, format='pdf')
	pp.close()
	plt.close()


if __name__ == "__main__":

	print "Processing random walks"
	#random_walker_hs = read_data(os.path.join(os.getenv('BR'), 'random-walks', 'random-walks-c100.tab'))
	#assert len(random_walker_hs) == 1
	#rwh = numpy.mean(random_walker_hs['random'])

	basename = 'news-targets-with-pageranks-gte10-cat-dl10'
	print 'Processing', basename
	plot_pbias(
		os.path.join(os.getenv('BP'), 'pbias', 'pbias-%s.pdf' % basename),
		read_data(os.path.join(os.getenv('BR'), 'pbias', '%s.tab' % basename)),
		cat_excludes=set(['earthlink', 'comcast', 'gmail', 'yelp', 'linkedin', 'timewarner', 'googleplus', 'hi5']),
		#xline=rwh,
		elinewidth=2, xticksfont=22, yticksfont=14,
		xlabel='$B_p$',
		show_legend=True
	)

	basename = 'oct2014-news4-gte10-site-dl10'
	print 'Processing', basename
	plot_pbias(
		os.path.join(os.getenv('BP'), 'pbias', 'pbias-%s.pdf' % basename),
		read_data(os.path.join(os.getenv('BR'), 'pbias', '%s.tab' % basename)),
		cat_excludes=set(['hi5', 'timewarner', 'earthlink', 'comcast', 'gmail', 'linkedin', 'yelp', 'duckduckgo', 'aolmail', 'livemail', 'tumblr', 'yahoomail']),
		#cat_excludes=set(['earthlink', 'comcast', 'gmail', 'yelp', 'linkedin', 'timewarner', 'googleplus', 'hi5']),
		#xline=rwh,
		elinewidth=2, xticksfont=22, yticksfont=14,
		xlabel='$B_p$',
		show_legend=True
	)
	'''
	basename = 'u150-c100-site-dl10'
	print 'Processing', basename
	plot_pbias(
		os.path.join(os.getenv('BP'), 'pbias', 'pbias-%s.pdf' % basename),
		read_data(os.path.join(os.getenv('BR'), 'pbias', '%s.tab' % basename)),
		cat_excludes=set(['earthlink', 'comcast']),
		#xline=rwh,
		elinewidth=2, xticksfont=22, yticksfont=14,
		xlabel='$B_p$',
		show_legend=True
	)

	basename = 'u500-c100-site-dl10'
	print 'Processing', basename
	plot_pbias(
		os.path.join(os.getenv('BP'), 'pbias', 'pbias-%s.pdf' % basename),
		read_data(os.path.join(os.getenv('BR'), 'pbias', '%s.tab' % basename)),
		cat_excludes=set(['earthlink', 'comcast']),
		#xline=rwh,
		elinewidth=2, xticksfont=22, yticksfont=14,
		xlabel='$B_p$',
		show_legend=True
	)

	basename = 'u500-c1000-site-dl10'
	print 'Processing', basename
	plot_pbias(
		os.path.join(os.getenv('BP'), 'pbias', 'pbias-%s.pdf' % basename),
		read_data(os.path.join(os.getenv('BR'), 'pbias', '%s.tab' % basename)),
		cat_excludes=set(['earthlink', 'comcast']),
		#xline=rwh,
		elinewidth=2, xticksfont=22, yticksfont=14,
		xlabel='$B_p$',
		show_legend=True
	)

	basename = 'u1200-c100-cat-dl10'
	print 'Processing', basename
	plot_pbias(
		os.path.join(os.getenv('BP'), 'pbias', 'pbias-%s.pdf' % basename),
		read_data(os.path.join(os.getenv('BR'), 'pbias', '%s.tab' % basename)),
		#xline=rwh,
		elinewidth=7, xticksfont=22, yticksfont=22,
		xlabel='$B_p$'
	)

	basename = 'u750-c1000-cat-dl10'
	print 'Processing', basename
	plot_pbias(
		os.path.join(os.getenv('BP'), 'pbias', 'pbias-%s.pdf' % basename),
		read_data(os.path.join(os.getenv('BR'), 'pbias', '%s.tab' % basename)),
		#xline=rwh,
		elinewidth=7, xticksfont=22, yticksfont=22,
		xlabel='$B_p$'
	)

	basename = 'feb2015-01to05-gte10-cat-dl10'
	print 'Processing', basename
	plot_pbias(
		os.path.join(os.getenv('BP'), 'pbias', 'pbias-%s.pdf' % basename),
		read_data(os.path.join(os.getenv('BR'), 'pbias', '%s.tab' % basename)),
		#xline=rwh,
		elinewidth=7, xticksfont=22, yticksfont=22,
		xlabel='$B_p$'
	)

	basename = 'feb2015-01to05-gte10-site-dl10'
	print 'Processing', basename
	plot_pbias(
		os.path.join(os.getenv('BP'), 'pbias', 'pbias-%s.pdf' % basename),
		read_data(os.path.join(os.getenv('BR'), 'pbias', '%s.tab' % basename)),
		cat_excludes=set(['earthlink', 'comcast', 'duckduckgo', 'gmail', 'googleplus', 'hi5', 'linkedin', 'timewarner', 'yelp']),
		#xline=rwh,
		elinewidth=2, xticksfont=22, yticksfont=14,
		xlabel='$B_p$',
		show_legend=True
	)

	basename = 'oct2014-gte10-cat-dl10'
	print 'Processing', basename
	plot_pbias(
		os.path.join(os.getenv('BP'), 'pbias', 'pbias-%s.pdf' % basename),
		read_data(os.path.join(os.getenv('BR'), 'pbias', '%s.tab' % basename)),
		#xline=rwh,
		elinewidth=7, xticksfont=22, yticksfont=22,
		xlabel='$B_p$'
	)

	basename = 'oct2014-gte10-site-dl10'
	print 'Processing', basename
	plot_pbias(
		os.path.join(os.getenv('BP'), 'pbias', 'pbias-%s.pdf' % basename),
		read_data(os.path.join(os.getenv('BR'), 'pbias', '%s.tab' % basename)),
		cat_excludes=set(['earthlink', 'comcast', 'duckduckgo', 'gmail', 'googleplus', 'hi5', 'linkedin', 'timewarner', 'yelp']),
		#xline=rwh,
		elinewidth=2, xticksfont=22, yticksfont=14,
		xlabel='$B_p$',
		show_legend=True
	)'''
