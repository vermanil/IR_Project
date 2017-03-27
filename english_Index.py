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
from nltk import PorterStemmer
import string
import pickle

class english_Index():
	def __init__(self):
		f = open("path.txt","r").read()
		path = (f.split())
		self.flag = 0
		self.fileName = []
		for i in range(0,len(path)):
			p = path[i] + "/"
			for file in os.listdir(p):
				self.fileName.append(p + file)
		self.english_dict = {}

		print(len(self.fileName))


	def start(self):
		# print("start")
		N = len(self.fileName)
		for i in range(0,2):
			# print(self.fileName[i])
			f= open(self.fileName[i],'r').read()
			#read the content of file like substring between tag title
			self.text1 = ""
			self.text2 = ""
			if(f.find('<DOCNO>') != -1):
				start = f.find('<DOCNO>')+len('<DOCNO>')
				end = f.find('</DOCNO')
				self.doc_id = f[start:end]
			# print(self.doc_id)
			if(f.find('<TITLE>') != -1):
				start = f.find('<TITLE>')+len('<TITLE>')
				end = f.find('</TITLE')
				self.text1 = f[start:end]
			#read the content of file like substring between tag content
			if(f.find('<TEXT>') != -1):
				start = f.find('<TEXT>')+len('<TEXT>')
				end = f.find('</TEXT')
				self.text2 = f[start:end]
			text = self.text1 + self.text2
			text = self.remove_punctuation(text)
			text2 = self.remove_stopWord(text)
			text2 = self.stemming(text2)
			self.makePostingList(text2)	
		# print(self.english_dict)

	def remove_punctuation(self, text):
		# print("remove")
		self.exclude = list(string.punctuation)
		text = "".join(c for c in text if c not in self.exclude)
		return text

	def remove_stopWord(self,text):
		# print("stopWord")
		stopWord=open("stop_eng.txt", "r").read().split("\n")
		# print(stopWord)
		text1 = []
		text = text.split()
		for c in text:
			if c not in stopWord:
				text1.append(c)
		return text1

	def stemming(self,text):
		# print("stemming")
		s = PorterStemmer()
		root = [s.stem(w) for w in text]
		return root

	def makePostingList(self,text):
		# print("posting")
		l = set(text)
		wordUnique = list(l)
		for i in range(len(wordUnique)):
			c=text.count(str(wordUnique[i]))
			#make condition that if word present in another document then append the current document at that place otherwise make another row and store it there
			if self.flag != 0:
				if wordUnique[i] in self.english_dict.keys():
					self.english_dict[str(wordUnique[i])][self.doc_id] = c

				else:
					self.english_dict[str(wordUnique[i])] = {}
					self.english_dict[str(wordUnique[i])][self.doc_id] = c

			else:
				self.english_dict[str(wordUnique[i])] = {}
				self.english_dict[str(wordUnique[i])][self.doc_id] = 1
				self.flag = 1

if __name__ == "__main__":
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
		obj = english_Index()
		obj.start()
		pickle.dump(obj.english_dict,open( "englishWordIndex.p", "wb" ))