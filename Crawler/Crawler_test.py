import random,threading,time,re,repr,urllib,urllib2
import argparse
from Queue import Queue
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

num = 0
def filewrite(write_text):
	global num
	f = open('./html/' + str(num) + '.html', 'w')
	f.write(write_text)
	num += 1
	
class freebuf_test:
	def __init__(self,url,re):
		self.url = url
		self.re = re
		self.num = 0

	def url_num(self):
		html = urllib.urlopen(self.url).read()
		urls = re.findall(self.re,html) 
		self.urls = urls
		self.resultsread = []
		print 1
		
	def thread_map(self):
		pool = ThreadPool(4)
		results = pool.map(urllib2.urlopen,self.urls)
		print 2
		pool.close()
		pool.join()
		for i in results:
			self.resultsread.append(i.read())
		# print self.resultsread
		# time.sleep(10)
		print 3
		
	def filewrite_map(self):
		print len(self.resultsread)
		pool = Pool()
		pool.map(filewrite,self.resultsread)
		pool.close()
		pool.join()
	
def main():
	parser = argparse.ArgumentParser(description='Web Crawler')
	parser.add_argument('-u', dest='TARGET_url', required=True, help='Target url')#url = http://www.freebuf.com
	parser.add_argument('-re', dest='TARGET_re', required=True, help='Web host re')#re = r'''(?<=a href=").*.html'''
	args = parser.parse_args()
	success = freebuf_test(args.TARGET_url,args.TARGET_re)
	success.url_num()
	success.thread_map()
	success.filewrite_map()
	
if __name__ == '__main__':
	main()