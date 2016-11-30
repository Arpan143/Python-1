#coding=utf-8
#�ýű�������ͬһ��������ͬ�������߳�����
import threading
from time import sleep,ctime

loops = [4,2,6] #����ִ�е�ʱ��

def loop(nloop, nsec): #�����̺߳�������Ҫ����������nloopΪ�߳��� nsecΪִ��ʱ��
	print 'start loop', nloop, 'at:', ctime()
	sleep(nsec)
	print 'loop', nloop, 'done at:', ctime()

def main():
	print 'starting at:', ctime()
	threads = [] #�����߳��б�
	nloops = range(len(loops)) #�����߳�����
	
	for i in nloops: #forѭ�������߳�
		t = threading.Thread(target=loop, args=(i, loops[i])) #ʹ��threading.Thread�����̺߳���Ϊloop ������Ĳ���Ϊ�߳�����ִ��ʱ��
		threads.append(t)
	
	for i in nloops: #��ÿ���߳̿�ʼ����
		threads[i].start()
		
	for i in nloops: #Ϊÿ���߳�������������̲߳�Ӱ�����������м��ɲ���
		threads[i].join()
	
	print 'all DONE at:', ctime()
	
if __name__ == '__main__':
	main()