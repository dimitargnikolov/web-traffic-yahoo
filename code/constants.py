import logging

SITE_IDX = 5
CAT_IDX = 6

LOGGING_LEVEL = logging.DEBUG


GOOGLE_SEARCH_URLS = ['google.com', 'google.de', 'google.ro', 'google.co.uk', 'google.fr', 'google.co.in', 'google.com.vn', 'google.co.id', 'google.ca', 'google.it', 'google.es', 'google.com.ph', 'google.com.my', 'google.com.eg', 'google.com.tw', 'google.com.br', 'google.com.au', 'google.com.hk', 'google.com.mx', 'google.com.sa', 'google.ae', 'google.gr', 'google.co.th', 'google.com.ar', 'google.at']

CATEGORY_MEMBERS = {
	'social': {
		'facebook': ['facebook.com'],
		'youtube': ['youtube.com'],
		'linkedin': ['linkedin.com'],
		'reddit': ['reddit.com'],
		'hi5': ['hi5.com'],
		'flickr': ['flickr.com'],
		'twitter': ['twitter.com'],
		'tumblr': ['tumblr.com'],
		'yelp': ['yelp.com'],
		'googleplus': ['plus.google.com'],
		'pinterest': ['pinterest.com']
	},
	'search': {
		'yahoosearch': ['search.yahoo.com'],
		'google': GOOGLE_SEARCH_URLS,
		'bing': ['bing.com'],
		'ask': ['ask.com'],
		'aolsearch': ['search.aol.com'],
		'duckduckgo': ['duckduckgo.com']
	},
	'email': {
		'yahoomail': ['mail.yahoo.com'],
		'gmail': ['mail.google.com', 'gmail.com'],
		'livemail': ['mail.live.com'],
		'aolmail': ['mail.aol.com'],
		'timewarner': ['mail.twc.com'],
		'earthlink': ['webmail.earthlink.net'],
		'comcast': ['mail.comcast.net']
	},
	'wiki': {
		'wikipedia': ['wikipedia.org']
	},
	'newsaggregator': {
		'googlenews': ['news.google.com']
	},
	'random': {
		'random': ['random']
	}
}

CATEGORY_COLORS = {
	'email': '#d7191c',
	'social': '#fdae61',
	'search': '#2c7bb6',
	'newsaggregator': '#abd9e9',
	'wiki': '#ffffff'
}

ALL_COLORS = {}
for cat in CATEGORY_COLORS:
	ALL_COLORS[cat] = CATEGORY_COLORS[cat]
	for site in CATEGORY_MEMBERS[cat]:
		ALL_COLORS[site] = CATEGORY_COLORS[cat]

DISPLAY_LABELS = {
	'newsaggregator': 'news aggregator',
	'yahoomail': 'yahoo mail',
	'yahoosearch': 'yahoo search',
	'livemail': 'live mail',
	'aolmail': 'aol mail',
	'aolsearch': 'aol search',
	'googlenews': 'google news',
	'duckduckgo': 'duck duck go',
	'all': 'all targets',
	'search': 'search',
	'social': 'social media',
	'email': 'email',
	'wiki': 'wiki',
	'wikipedia': 'wikipedia'
}
