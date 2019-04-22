import sys, os, numpy as np, math
from scipy.optimize import curve_fit

sys.path.append(os.getenv('BC'))
from lib import equal


def polynomial3_fit(x, y, p0=None):
	fitf = lambda xi, a, b, c, d: a * xi ** 3 + b * xi ** 2 + c * xi + d
	params, covar = curve_fit(fitf, x, y, p0=p0)
	errors = np.sqrt(np.diag(covar))
	return params, errors


def sigmoid_fit(x, y, p0):
	fitf = lambda xi, L, k, x0: L / (1 + math.e ** (-k * (xi - x0)))
	params, covar = curve_fit(fitf, x, y, p0=p0)
	errors = np.sqrt(np.diag(covar))
	return params[0], params[1], params[2], errors


def linear_fit(x, y, p0=[1.0, 1.0]):
	fitf = lambda xi, a, b: a * xi + b
	params, covar = curve_fit(fitf, x, y, p0=p0)
	errors = np.sqrt(np.diag(covar))
	return params[0], params[1], errors[0], errors[1]  # a, b, aerror, berror


def fit_power_law1(x, y, p0=[2.0, 1.0]):
	logx = np.array(np.log10(x))
	logy = np.array(np.log10(y))
	fitf = lambda xi, alpha, c: -alpha * xi + c
	params, covar = curve_fit(fitf, logx, logy, p0=p0)
	return params[0], 10 ** params[1]  # alpha, c


def fit_power_law2(x, y, p0=[2.0, 1.0]):
	fitf = lambda x, alpha, c: c * (x ** -alpha)
	params, covar = curve_fit(fitf, x, y, p0=p0)
	return params[0], params[1]  # alpha, c


def set_common_rc_params(rcParams):
	rcParams['figure.autolayout'] = True
	rcParams['font.family'] = 'serif'
	rcParams['text.usetex'] = True
	rcParams['text.latex.unicode'] = True
	#rcParams['text.latex.preamble'] = '\\usepackage{amsmath},\\usepackage{amssymb}'
	rcParams['xtick.major.pad'] = '8'
	rcParams['ytick.major.pad'] = '8'


def set_axes_params(ax,
					xscale='linear', xbase=None, yscale='linear', ybase=None,
					xticks=None, yticks=None, axis_font_size=12,
					xmin=None, xmax=None, ymin=None, ymax=None):
	# set the scales, such as for linear or log plots
	if xscale is not None and xbase is not None:
		ax.set_xscale(xscale, basex=xbase)
	elif xscale is not None:
		ax.set_xscale(xscale)

	if yscale is not None and ybase is not None:
		ax.set_yscale(yscale, basey=ybase)
	elif yscale is not None:
		ax.set_yscale(yscale)

	# set the ticks font on both axes
	for tick in ax.xaxis.get_major_ticks():
		tick.label.set_fontsize(axis_font_size)

	for tick in ax.yaxis.get_major_ticks():
		tick.label.set_fontsize(axis_font_size)

	# set min/max values for the axes
	if xmin is not None:
		ax.set_xlim(left=xmin)

	if xmax is not None:
		ax.set_xlim(right=xmax)

	if ymin is not None:
		ax.set_ylim(bottom=ymin)

	if ymax is not None:
		ax.set_ylim(top=ymax)

	# set the axes ticks
	if xticks is not None:
		ax.set_xticks(xticks)

	if yticks is not None:
		ax.set_yticks(yticks)


def cum_distro_from_dict(counts):
	cum_counts = {}
	total = np.sum(counts.values())
	curr_sum = total
	for key in sorted(counts.keys()):
		cum_counts[key] = curr_sum
		curr_sum -= counts[key]
	return cum_counts


def cum_distro(seq):
	new_seq = []
	total = np.sum(seq)
	curr_sum = total
	for i in range(len(seq)):
		new_seq.append(curr_sum)
		curr_sum -= seq[i]
	return new_seq


def probs(seq):
	total = float(np.sum(seq))
	return [n / total for n in seq]


def logbin(x, y, num_bins, x_sorted=False):
	# sort x and y if necessary
	if not x_sorted:
		tuples = zip(x, y)
		sorted_tuples = sorted(tuples)
		x, y = zip(*sorted_tuples)

	# compute the bin boundaries
	min_x = np.min(x)
	max_x = np.max(x)

	lower_bound = np.log10(min_x)
	upper_bound = np.log10(max_x)
	bins = np.logspace(lower_bound, upper_bound, num_bins)

	# assign each value in x to a bin and accumulate the y values for that bin
	bin_vals = [0]
	bin_idx = 1
	for i in range(len(x)):
		while not equal(x[i], bins[bin_idx]) and x[i] > bins[bin_idx]:
			bin_idx += 1
			bin_vals.append(0)
			if bin_idx >= len(bins):
				raise ValueError('Bin boundaries are incorrect.')
		bin_vals[bin_idx-1] += y[i]

	return bins, bin_vals


def logbin2(x, y, num_bins, x_sorted=False, agg_fn=None):			
	# sort x and y if necessary
	if not x_sorted:
		tuples = zip(x, y)
		sorted_tuples = sorted(tuples)
		x, y = zip(*sorted_tuples)

	# compute the bin boundaries
	min_x = np.min(x)
	max_x = np.max(x)

	lower_bound = np.log10(min_x)
	upper_bound = np.log10(max_x)
	bins = np.logspace(lower_bound, upper_bound, num_bins)

	# assign each value in x to a bin and accumulate the y values for that bin
	bin_vals = [[]]
	bin_idx = 1
	for i in range(len(x)):
		while not equal(x[i], bins[bin_idx]) and x[i] > bins[bin_idx]:
			bin_idx += 1
			bin_vals.append([])
			if bin_idx >= len(bins):
				raise ValueError('Bin boundaries are incorrect.')
		bin_vals[bin_idx-1].append(y[i])

	if agg_fn is not None:
		new_bin_vals = []
		for i in range(len(bin_vals)):
			new_bin_vals.append(agg_fn(bin_vals[i]))
		bin_vals = new_bin_vals
	return bins, bin_vals


def plot_distro(ax, counts, bin_fn=None, use_cum_distro=False,
				marker='o', marker_edge_color='#000000', marker_face_color='none', marker_width=2):

	values = sorted(counts.keys())
	value_counts = [counts[val] for val in values]
	yprobs = probs(value_counts)

	if use_cum_distro:
		y = cum_distro(yprobs)
	else:
		y = yprobs

	if bin_fn is not None:
		x, y = bin_fn(values, y)

		# divide each probability by bin width
		y = [y[i] / float(x[i + 1] - x[i]) for i in range(len(y))]

		# for x values, take the midpoint of a bin
		x = [(x[i] + x[i + 1]) / 2.0 for i in range(len(x) - 1)]
	else:
		x = values

	ax.plot(x, y, marker,
			markeredgewidth=marker_width,
			markerfacecolor=marker_face_color,
			markeredgecolor=marker_edge_color)

	return x, y

if __name__ == "__main__":
	print("You are not supposed to run this from the command line.")
