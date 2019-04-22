import os

def read_list(filepath):
	items = []
	with open(filepath, 'r') as f:
		items = set([l.lower().strip() for l in f.readlines()])
	return items


def compare_items(items1, items2, dest_dir):
	common = set()
	only_in1 = set()
	only_in2 = set()
	
	for item in items1:
		if item in items2:
			common.add(item)
		else:
			only_in1.add(item)

	for item in items2:
		if item not in items1:
			only_in2.add(item)

	def write_to_file(filepath, items):
		with open(filepath, 'w') as f:
			for item in items:
				f.write('%s\n' % item)

	write_to_file(os.path.join(dest_dir, 'common.txt'), common)
	write_to_file(os.path.join(dest_dir, 'only_in1.txt'), only_in1)
	write_to_file(os.path.join(dest_dir, 'only_in2.txt'), only_in2)


if __name__ == '__main__':
	compare_items(
		read_list(os.path.join(os.getenv('TD'), 'news-urls-filtered-2016-12-09.txt')),
		read_list(os.path.join(os.getenv('TD'), 'news-urls-filtered.txt')),
		os.path.join(os.getenv('TD'))
	)
