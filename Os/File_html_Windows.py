# coding=utf-8
import time,os,regex,re,sys

# reload(sys)
# sys.setdefaultencoding('gb2312')

class File_html_Windows():
    def __init__(self):
        self.html = u"""
<self.html>
<head>
<title>Directories</title>
<meta http-equiv="Content-Type" content="text/self.html;charset=utf-8" />
</head>
<body>
<h1>Directories</h1>
<ul>
"""
    def Windows_all(self):
        path = os.getcwd()
        path = raw_input('请输入目录(C:\Test\Taeget_folder):')
        path = unicode(path,sys.stdin.encoding)
        a = 1
        for root, dirs, files in os.walk(path):
            if root[len(path):] == '':
                self.html = self.html + '<details>\n<summary>根目录</summary>'.decode(sys.stdin.encoding)
                for y in files:
                    self.html = self.html + '\n<li><a href = >' + y + '</a></li>'
                self.html = self.html +'\n</details>'
            else:
                self.html = self.html + '<details>\n<summary>' + root[len(path)+1:] +'</summary>'
                for y in files:
                    self.html = self.html + '\n<li><a href = >' + y + '</a></li>'
                self.html = self.html +'\n</details>'
            a =a +1
            print a
        self.html = self.html + '</ul>\n</body>\n</self.html>'
        self.html =self.html.encode('utf-8')
        # self.html = self.html.decode(sys.stdin.encoding).encode('utf-8')
        f = open('test.html','w+')
        f.write(self.html)
        f.close()

def main():
    print """
 _        _   _      _  _    __    _  __________  _           _
| |      | | \ \    / /| |  /  \  | ||  ________|| |         | |
| |______| |  \ \  / / | | / /\ \ | || |________ | |         | |
|  ______  |   \ \/ /  | | | || | | ||  ________|| |         | |
| |      | |    \  /   | |_| || |_| || |         | |         | |
| |      | |    |  |    \   /  \   / | |________ | |________ | |________
|_|      |_|    |__|     \_/    \_/  |__________||__________||__________|

    """
    success = File_html_Windows()
    success.Windows_all()

if __name__ == '__main__':
    main()