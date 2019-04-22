import sys, os, csv, matplotlib, numpy
from operator import itemgetter

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages

sys.path.append(os.getenv("BC"))
from constants import CATEGORY_COLORS, ALL_COLORS, DISPLAY_LABELS, CAT_IDX, SITE_IDX
from plotting import set_common_rc_params

from matplotlib import rcParams
set_common_rc_params(rcParams)

TITLE_FONT_SIZE = 36
XAXIS_FONT_SIZE = 36
YAXIS_FONT_SIZE = 28

DOMAIN_LEVEL = 10


def read_data(filepath):
	hs = {}
	with open(filepath, 'r') as f:
		reader = csv.reader(f, delimiter="\t")
		for row in reader:
			cat = row[0]
			h = float(row[2])
			if cat not in hs:
				hs[cat] = []
			hs[cat].append(h)
	return hs


def plot_hbias(dest, user_hs, cat_excludes=set(), xline=None,
			   title=None, xlabel=None, ylabel=None, show_legend=False, elinewidth=2,
			   xticksfont=XAXIS_FONT_SIZE, yticksfont=YAXIS_FONT_SIZE):
	if not os.path.exists(os.path.dirname(dest)):
		os.makedirs(os.path.dirname(dest))

	# plot using bars
	mean_hs = {cat: numpy.mean(h) for cat, h in user_hs.items() if cat not in cat_excludes}
	ordered_mean_hs = sorted(mean_hs.items(), key=itemgetter(1))
	cats, means = zip(*ordered_mean_hs)
	errs = [2 * numpy.std(user_hs[c]) / numpy.sqrt(len(user_hs[c])) for c in cats]

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
		plt.legend(handles=patches, loc='lower right', fontsize='xx-small')

	ax.set_ylim(bottom=x[0] - 1, top=x[-1] + 1)
	ax.set_xlim(left=0.0, right=1.0)

	if xline is not None:
		yvals = numpy.linspace(x[0] - 1, x[-1] + 1, 50)
		ax.plot([xline for _ in range(len(yvals))], yvals, color='#000000')
		ax.annotate('random walker\nbaseline',
					xy=(xline - .005, x[0] - .7), xycoords='data',
					xytext=(80, 10), textcoords='offset points',
					arrowprops=dict(
						arrowstyle="->",
						connectionstyle="angle3,angleA=90,angleB=0"
					)
		)

	plt.yticks(x, [DISPLAY_LABELS[c] if c in DISPLAY_LABELS else c for c in cats])

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


def run_plot(src_dir, basename, dest_dir, cat_idx, domain_level, norm_by_all_targets):
	filename = 'dl%d-normall%s-cat%d-%s' % (domain_level, norm_by_all_targets, cat_idx, basename)
	src = os.path.join(src_dir, filename + '.tab')
	dest = os.path.join(dest_dir, filename + '.pdf')

	plot_hbias(
		dest,
		read_data(src),
		cat_excludes=set(['hi5', 'timewarner', 'earthlink', 'comcast', 'gmail', 'linkedin', 'yelp', 'duckduckgo', 'aolmail', 'livemail', 'tumblr', 'yahoomail']),
		#cat_excludes=set(['hi5', 'timewarner', 'earthlink', 'comcast', 'gmail', 'linkedin', 'yelp', 'duckduckgo']),
		xline=None,
		elinewidth=2, xticksfont=22, yticksfont=14,
		xlabel='$B_h$',
		show_legend=True
	)


if __name__ == '__main__':
	src_dir = os.path.join(os.getenv('BR'), 'hbias')
	dest_dir = os.path.join(os.getenv('BP'), 'hbias')
	domain_level = 10
	norm_by_all_targets = True

	#run_plot(src_dir, 'u1200-c100-cat', dest_dir, CAT_IDX, domain_level, norm_by_all_targets)
	#run_plot(src_dir, 'u750-c1000-cat', dest_dir, CAT_IDX, domain_level, norm_by_all_targets)
	#run_plot(src_dir, 'u500-c100-site', dest_dir, SITE_IDX, domain_level, norm_by_all_targets)
	#run_plot(src_dir, 'u150-c100-site', dest_dir, SITE_IDX, domain_level, norm_by_all_targets)
	#run_plot(src_dir, 'u500-c1000-site', dest_dir, SITE_IDX, domain_level, norm_by_all_targets)
	#run_plot(src_dir, 'oct2014-news1-gte10', dest_dir, SITE_IDX, domain_level, norm_by_all_targets)
	#run_plot(src_dir, 'oct2014-news2-gte10', dest_dir, SITE_IDX, domain_level, norm_by_all_targets)
	run_plot(src_dir, 'oct2014-news4-gte10', dest_dir, SITE_IDX, domain_level, norm_by_all_targets)
