import sys
import os
import zlib

DIR_PATH = ""
CHK_SUM_PATH = ""
LIST_FILES = None

def main(argv):
	global DIR_PATH, CHK_SUM_PATH, LIST_FILES

	count_param = len(argv)

	DIR_PATH = argv[0]
	is_exist_path(DIR_PATH)

	LIST_FILES = os.listdir(DIR_PATH)

	if count_param == 2:
		CHK_SUM_PATH = argv[1]
		is_exist_path(CHK_SUM_PATH)
		compare_crc32_with_file()
	else:
		check_crc32()

def is_exist_path(path):
	if not os.path.exists(path):
		print '"' + path + '"' + " does not exist."
		sys.exit(1)

def rename(filename, ext, new_ext):
	new_filename = filename
	if not new_ext in filename:
		new_filename = filename.replace(ext, new_ext)
		# os.rename(DIR_PATH + filename, DIR_PATH + new_filename)
	return new_filename

def check_crc32_1_file(filename, ext):
	global DIR_PATH

	if ext == '.sfv' or ext == '.SFV' or ext == '.DS_Store':
		return None

	buf = open(DIR_PATH + filename, 'rb').read()
	crc = zlib.crc32(buf) & 0xffffffff
	return ('%08X' % crc)

def check_crc32():
	print 'calculating...'

	global DIR_PATH

	out_file = open(DIR_PATH + 'checksum.sfv', 'w')

	for filename in LIST_FILES:
		ext = "." + filename.split(".")[-1]
		crc = check_crc32_1_file(filename, ext)
		if crc == None:
			continue

		new_ext = ' [%s]%s' % (crc, ext)
		new_filename = rename(filename, ext, new_ext)
		line = '%s %s' % (new_filename, crc)
		out_file.write(line + '\n') 
	out_file.close()

def compare_crc32_with_file():
	print 'calculating...'

	global CHK_SUM_PATH

	chk_sum_file = open(CHK_SUM_PATH, "r").readlines()

	test_count = 0
	pass_count = 0
	fail_count = 0
	for filename in LIST_FILES:
		if filename.startswith('._'):
			continue

		ext = "." + filename.split(".")[-1]
		crc = check_crc32_1_file(filename, ext)
		if crc == None:
			continue

		test_count += 1
		new_ext = ' [%s]%s' % (crc, ext)
		new_filename = rename(filename, ext, new_ext)

		crc_from_file = get_crc_from_file(filename)
		if crc == crc_from_file:
			pass_count += 1
		else:
			fail_count += 1
			print 'FAIL', '--', filename, crc, crc_from_file
	
	print '\n'
	print 'TEST: ' + str(test_count)
	print 'PASS: ' + str(pass_count)
	print 'FAIL: ' + str(fail_count)

def get_crc_from_file(filename):
	global CHK_SUM_PATH
	chk_sum_file = open(CHK_SUM_PATH, "r").readlines()

	for line in chk_sum_file:
		if line.find(filename) != -1:
			return line.replace('\n', '').split(' ')[-1]

	return None

if __name__ == "__main__":
	count_param = len(sys.argv)
	if count_param <= 1:
		print "Plese enter path to your file."
	else:
		main(sys.argv[1:])
