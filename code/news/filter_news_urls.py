import sys, os, fnmatch

sys.path.append(os.getenv('BC'))
from lib import nth_level_domain, normalize_url

# not used but included in case we decide to analyze these sources again
WIKI_PLATFORMS = frozenset([
	'wikipedia.org',
	'wikimedia.org',
	'wictionary.org',
	'wikiquote.org',
	'wikibooks.org',
	'wikisource.org',
	'wikinews.org',
	'wikiversity.org',
	'wikidata.org',
	'wikivoyage.org',
	'wikimediafoundation.org'
])

# not used but included in case we decide to analyze these sources again
BLOGGING_PLATFORMS = frozenset([
	'xanga.com',
	'blogspot.com', 
	'blogger.com', 
	'wordpress.com',
	'wordpress.org',
	'tumblr.com',
	'typepad.com',
	'livejournal.com',
	'hubpages.com'
])

# not used but included in case we decide to analyze these sources again
NEWS_RECOMMENDERS = frozenset([
	'news.google.com',
	'news.yahoo.com',
	'news.aol.com'
])

EMAIL_PLATFORMS = frozenset([
	'umail.iu.edu',
	'imail.iu.edu',
	'webmail.iu.edu',
	'webmail.indiana.edu',
	'exchange.indiana.edu',
	'gmail.com',
	'mail.google.com',
	'ymail.com',
	'mail.yahoo.com',
	'hotmail.com',
	'mail.live.com',
	'webmail.aol.com',
	'hotmail.msn.com'
])

SOCIAL_MEDIA_PLATFORMS = frozenset([
	'facebook.com', 
	'myspace.com',
	'twitter.com', 
	'youtube.com',
	'plus.google.com',
	'linkedin.com',
	'pinterest.com',
	'reddit.com',
	'instagram.com',
	'vube.com'
])

SEARCH_ENGINES = frozenset([
	'search.aol.com',
	'google.com',
	'bing.com',
	'ask.com',
	'search.yahoo.com',
	'search.msn.com',
	'duckduckgo.com',
	'search.naver.com',
	'baidu.com'
])

EXCEPTIONS = frozenset([
	'desktopapps.bbc.co.uk',
	'newsrss.bbc.co.uk',
	'catalog.video.msn.com',
	'graphics8.nytimes.com',
	'public-xml.nytimes.com',
	'newsimg.bbc.co.uk',
	'media-ori.msnbc.msn.com',
	'webfarm.tpa.foxnews.com'
])
EXCEPTION_PATTERNS = [
	'img*.catalog.video.msn.com',
	'*.video.msn.com',
	'feeds.*',
	'ads.*',
	'rss.*',
	'rssfeeds.*',
	'pheedo*.msnbc.msn.com',
	'graphics*.nytimes.com',
	'*.edu',
	'*.edu.*'
]
UNWANTED_URLS = frozenset().union(EMAIL_PLATFORMS).union(SOCIAL_MEDIA_PLATFORMS).union(SEARCH_ENGINES).union(NEWS_RECOMMENDERS).union(BLOGGING_PLATFORMS).union(EXCEPTIONS)


def fnmatches_multiple(patterns, s):
	for p in patterns:
		if fnmatch.fnmatch(s, p):
			return True
	return False


def domain_level(host):
	"""
	>>> domain_level('')
	0
	>>> domain_level('    ')
	0
	>>> domain_level('com')
	1
	>>> domain_level('facebook.com')
	2
	>>> domain_level('indiana.facebook.com')
	3
	"""
	if host.strip() == '':
		return 0
	else:
		return len(host.strip().split('.'))


def parents(url):
	"""
	>>> parents('facebook.com')
	[]
	>>> parents('indiana.facebook.com')
	['facebook.com']
	>>> parents('1.2.3.news.bbc.co.uk')
	['2.3.news.bbc.co.uk', '3.news.bbc.co.uk', 'news.bbc.co.uk', 'bbc.co.uk']
	"""
	parent_urls = []
	dl = domain_level(url)
	if is_exception(url):
		end = 2
	else:
		end = 1
	for parent_dl in range(dl-1, end, -1):
		parent_urls.append(nth_level_domain(url, parent_dl))
	return parent_urls


def is_exception(host):
	"""
	Exceptions are domain names such as google.co.uk or hire.mil.gov, where the top level domain can be thought of co.uk or mil.gov rather than .uk or .gov. These domains need to be processed as a special case when converting the domain level from one level to another, since they are essentially of one level higher than they would ordinarily be thought of. That is, google.co.uk is a 3rd level domain, but for practicel purposes it should be considered a 2nd level domain.

	>>> is_exception('')
	False
	>>> is_exception('google.com')
	False
	>>> is_exception('google.co.uk')
	True
	>>> is_exception('hire.mil.gov')
	True
	>>> is_exception('indiana.edu')
	False
	>>> is_exception('indiana.edu.us')
	True
	>>> is_exception('whitehouse.gov')
	False
	"""
	exceptions = [".com.", ".net.", ".org.", ".edu.", ".mil.", ".gov.", ".co."]
	for e in exceptions:
		if e in host:
			return True
	return False


def prune_news_dataset(news_sources_file):
	f = open(news_sources_file, 'r')
	news_urls = set()
	for line in f:
		if '://' in line:
			host = line[line.index('://') + 3:]
		else: 
			host = line
		host = host.strip().split('/')[0]

		host = normalize_url(host)

		if host in news_urls or host in UNWANTED_URLS or fnmatches_multiple(EXCEPTION_PATTERNS, host):
			continue

		news_urls.add(host)
	
	for host in sorted(list(news_urls)):
		disregard = False
		for parent in parents(host):
			if parent in news_urls or parent in UNWANTED_URLS:
				disregard = True
				break
		if not disregard:
			print host

def main():
	prune_news_dataset(os.path.join(os.getenv("BR"), "news", "news-urls-googlenews.txt"))


def test():
	import doctest
	doctest.testmod()

if __name__ == "__main__":
	main()
