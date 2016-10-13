# coding=utf-8
import time,os,argparse

class del_file:
	def __init__(self,path):
		self.path = path
		self.old_filename = []
		self.now_filename = []
	
	def Get_filename(self):
		for root, dirs, files in os.walk(self.path):
			for i in range(len(files)):
				filename = str(root) + '/' + files[i]
				filename = filename.replace('\\','/')
				self.old_filename.append(filename)
		print self.old_filename
		
	def keep_del(self):
		while True:
			for root, dirs, files in os.walk(self.path):
				for i in range(len(files)):
					now_filename = str(root) + '/' + files[i]
					now_filename = now_filename.replace('\\','/')
					self.now_filename.append(now_filename)
			del_filename_list = list(set(self.now_filename) - set(self.old_filename))
			if del_filename_list != []:
				for i in range(len(del_filename_list)):
					del_filename = del_filename_list[i]
					del_filename = del_filename.replace('/','\\')
				try:
					os.remove(del_filename)
				except:
					if os.path.exists(del_filename) != True:
						print del_filename + "is alread del or no exist!"
					else:
						print "please del " + del_filename
			print "\n>>Working---"
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
	parser = argparse.ArgumentParser(description='Os path')
	parser.add_argument('-p', dest='TARGET_path', required=True, help='Target path')
	args = parser.parse_args()
	success = del_file(args.TARGET_path)
	success.Get_filename()
	success.keep_del()
	time.sleep(1)

if __name__ == '__main__':
	main()