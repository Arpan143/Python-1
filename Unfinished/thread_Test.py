#coding=utf-8
#该脚本作用是同一个函数不同参数多线程运行
import threading
from time import sleep,ctime

loops = [4,2,6] #定义执行的时间

def loop(nloop, nsec): #构建线程函数，需要两个参数，nloop为线程名 nsec为执行时间
	print 'start loop', nloop, 'at:', ctime()
	sleep(nsec)
	print 'loop', nloop, 'done at:', ctime()

def main():
	print 'starting at:', ctime()
	threads = [] #设置线程列表
	nloops = range(len(loops)) #设置线程数量
	
	for i in nloops: #for循环创建线程
		t = threading.Thread(target=loop, args=(i, loops[i])) #使用threading.Thread设置线程函数为loop 待传入的参数为线程名、执行时间
		threads.append(t)
	
	for i in nloops: #让每个线程开始运行
		threads[i].start()
		
	for i in nloops: #为每个线程设置锁，如果线程不影响主函数运行即可不用
		threads[i].join()
	
	print 'all DONE at:', ctime()
	
if __name__ == '__main__':
	main()