# coding=utf-8
import re,time,argparse
import urllib,urllib2
from bs4 import BeautifulSoup
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

num = 0
def filewrite(data):
	global num
	f = open('./html/' + str(num) + '.html', 'w')
	f.write(data)
	num += 1
	
class Crawler:
	def __init__(self,url,tag):
		self.url= url
		self.tag= tag
		# self.re= re
		self.resultsread= []

	def url_num(self):
		try:
			html = urllib.urlopen(self.url).read()
			urls = re.findall(r'''(?<=a href=").*.html''',html) 
			self.urls = urls
		except:
			print self.url,' is error!'
		
	def thread_map(self):
		pool = ThreadPool(4)
		results = pool.map(urllib2.urlopen,self.urls)
		pool.close()
		pool.join()
		for i in results:
			self.resultsread.append(i.read())
		
	def filewrite_map(self):
		print len(self.resultsread)
		pool = Pool()
		pool.map(filewrite,self.resultsread)
		pool.close()
		pool.join()

	def get_tag(self):
		num= 0
		for i in self.resultsread:
			soup = BeautifulSoup(i,'lxml')
			for y in soup.find_all(self.tag):
				print y
				try:
					urllib.urlretrieve(y.get('src'),'./img/'+ str(num)+ '.png')
					num+= 1
				except:
					pass

def main():
	print '''
 _        _   _      _  _    __    _  __________  _           _
| |      | | \ \    / /| |  /  \  | ||  ________|| |         | |
| |______| |  \ \  / / | | / /\ \ | || |________ | |         | |
|  ______  |   \ \/ /  | | | || | | ||  ________|| |         | |
| |      | |    \  /   | |_| || |_| || |         | |         | |
| |      | |    |  |    \   /  \   / | |________ | |________ | |________
|_|      |_|    |__|     \_/    \_/  |__________||__________||__________|
'''
	parser = argparse.ArgumentParser(description= 'Web Crawler')
	parser.add_argument('-u', dest= 'TARGET_url', required= True, help= 'Target url')#url= http://www.freebuf.com
	parser.add_argument('-t', dest= 'TARGET_tag', required= True, help= 'Target tag')#tag= img
	# parser.add_argument('-re', dest='TARGET_re', required=True, help='Web host re')#re = r'''(?<=a href=").*.html'''
	args = parser.parse_args()
	success = Crawler(args.TARGET_url, args.TARGET_tag)
	success.url_num()
	success.thread_map()
	success.filewrite_map()
	success.get_tag()
	
if __name__ == '__main__':
	main()