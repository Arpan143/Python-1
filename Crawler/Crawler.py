# coding=utf-8
import time,re,urllib,urllib2
import argparse
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

num = 0
def filewrite(write_html):
	global num
	f = open('./html/' + str(num) + '.html', 'w')
	f.write(write_html)
	num += 1
	
class Crawler:
	def __init__(self,url):
		self.url = url
		# self.re = re
		self.resultsread = []
		self.num = 0

	def url_num(self):
		html = urllib.urlopen(self.url).read()
		urls = re.findall(r'''(?<=a href=").*.html''',html) 
		self.urls = urls
		
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
	
def main():
	print """
..'@b.........C@............`'@#................................!1......'!{.`...
.`'$b.........w@..............$@................................\B......`t@.'...
.`'$d.........k@'............`$$'..............|................/@......'f$.'...
.''$q.........W@`...........'^$$'..............8Q...............t$......'j$.'...
.'.$Z.........@$`...........'`$$...............$&...............j$.......r$.'...
...$Q.........$$'...........''$$...............$h...............x$.......n$.'...
...$J.........$$............'.*$...............%b..............'n$'......u$.'...
...$Y.........$@..............C$...............$C..............'v@`'.....c$.....
...$Y.........$@..............j$'..............$Y..............'v@^`.....c$.....
.'.$v'.'......$$..............>$]'`...........'$(........'......Y$......`Y$.'...
.'.$u.'..'`...$$............'."$u.'............$?......'.'......U$......'Y$.'...
.'.$x'......''$$............`'.$h...........'..@!.......'.......U$......'U$.'...
.'.$t'.'...'.,$$............''.$@'..........'':$`.....'.'.......J$......'J$''...
.'.$|.`......'$$.............''$$'..........`'}$................J$'.....'J$'....
...$1.`..'.'..$$..............'$$...........''z$......''.'......C$''.....C$'....
...$}^......''$$...............$$.'..........'k$........''......L$`'.....C$'....
..'$].u8W*kZCt$$.............'.%$.'..........'B$......}{^'......L$`'.....L@'....
..`$+`w@$$$$@$$$.'.........~-.`$@'......'...``B$....^a$$&'^^....O$.'.....O@.....
..`$>.m$$$$$$@$$..(j'....."88..$B.'......'....$$.^'`w$$$$C..'...O$.'.....O$.....
.'`$;'m@$$$B$$$$..$%`.....'$$`'$B.`......'....$$'`..$$$$$$,`....Z$.'.....O$.....
''`$^.J$$@$$$@$$..%@`......$8^`$$''..........`$$...\$$B$$%o.`...Z$.'.....O$.....
.'"$'._O*$$$$$$$..$$.......$$'.%$.......'...'^$$.`,B$%$$$$$.....Z$''.....Z$.....
.',$.`.'`!)Jp$$$..@%^.....\8b..m$"..........'.$$.`.$$${ip%8^....m$''.....Z$.....
..;$.....`.'''$$.'J$~.....@$_''|$|......<'..'.@@..+$@i.'.$$.`...m$''.....Z$.....
..!$....''...`$$'.`$a.....@$.'';Bm^.....a`..``@@''M@*...^o$z....m$''.....Z$.'...
.'-$........'.$$..,$$'''.`$$...,$$'..`'m$.'.`'$0'.@$i'.'.!$$....m$.......Z$.'...
..}$........'.$$...&$}....@#....$$`....$$+...}$'.'$%'.'..'$$....m$.......Z$.'...
..)$'.......'.$$..`)8h.``)${...'$@`...^$$w'..L@.'^@$.''...W$....m$.......Z$.'...
..\$'.........$$'..^$$.''*$.....$$...`q$$$.'`8$`.'%$.^....b$'...m$.......O$.'...
..f$`.........$$''..$@`'.$%`....M$,...$$$$..`$$`..B$..`.'>k$'...m$.......O$.'...
..x$^.........$$`.'^@@!'.%$.....c$j..^$$@$''.$@'..$&.`-Uh$8$....m$.......O$.'...
..n$^.........$$`..'$$i.^@*....`<$o..Z$$$B"'.$@.`^$*b%$$$$$$....m$.......O$.'...
.'z$........'.B$....dB*'Y$_....'`$$..@8$$$'..$k..`@$B$$$@$$$^...Z$''....'Z$''...
.'Y$........'.@$....:$$.%%"....'.@B!.$$?h$u^`$1...$$$$$@$$$M....O$''....'O$''...
.'J$........''@$'..`.$$.$$.......$$^'$$.|$$.f$'...$$$@@$@$d`^...0$''....'0$''...
..Q$.........'$$...^:$8j$$'.....'$$.O@@`.@8.#@'...@$$$$oQ+..'...C$''....'C$.....
..Z$'........'$$.....m$%$$'....'"@@.B$$..$$^$$`...B$f};'.``'....U$''....'U$.....
..q$`........'$$...'.;$$88......`$$'8$\.'$${$@...`@B"`'.....'...X$.'....'X$.....
'.d$`.......''$$...^`.B$$x.`.....%$W$B''.0$M$$...`$$'`...'.`....c$.'....'c$.....
'.k$`.......''$$....'`B$@.^^.....OB%B$''';$$%$...'$@.`.'..'`'...v$.'....'v$.....
.'h$'........^$$.....'B$@........>%$$}.`'.B@@%^..`B$J'''.^.....`v$'.....`n$`....
`.a$'.......`^$M......w$$:........$@@,..`.$$$U'...Y%@^..`.......t$......`t$.'...
''M$'.......`'Bq......!$*'........%$B...^.$$@~...:'$$@\1z.......)$.......|$.'...
.`&@........`^$U'....'X$-.........$BB...`^$$$....`.$@%@$$.......}B`......{@.....
.'*$.........._'......$$.'.......^b@>'.'.`]$$....`'x$$$$@......._%`'....._B.....
'.a$..........^......'%$,........`-$.'.....$8.....".&B$$$'......>$.'....'i$`....
'.m%...........'.....^$B...........n.''.'.'Bx....^..O$$$B`......"$......'"$`....
	"""
	t = time.time()
	parser = argparse.ArgumentParser(description='Web Crawler')
	parser.add_argument('-u', dest='TARGET_url', required=True, help='Target url')#url = http://www.freebuf.com
	# parser.add_argument('-re', dest='TARGET_re', required=True, help='Web host re')#re = r'''(?<=a href=").*.html'''
	args = parser.parse_args()
	success = Crawler(args.TARGET_url)
	success.url_num()
	success.thread_map()
	success.filewrite_map()
	print time.time()-t
	
if __name__ == '__main__':
	main()