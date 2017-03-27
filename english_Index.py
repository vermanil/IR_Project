#!/usr/bin/python
# import os
# import subprocess
# print("start")
# subprocess.call("./readAllFile.sh", shell=True)
# # print(rc.path)
# print(os.getenv('foo'))
# print("end")
import sys
import os
import glob
if os.path.isfile("path.txt") != True:
	path = []
	f = open("path.txt","w")
	t = 0
	for i in sys.argv:
		if(t!=0):
			f.write(i + "\n")
		t=1
	f.close()
else:
	# path = []
	f = open("path.txt","r").read()
	path = (f.split())
	print(path)
	# print("hello")