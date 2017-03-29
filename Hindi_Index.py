# import ElementTree to parse the hindi document and read according to tag
import xml.etree.ElementTree as ET
# import string to find the list of string punctuation 
import string 
# import glob to read all document of particuler folder
import glob
# import pickle to store dictionary in unreadable format of .p extension
import pickle
import collections
import math
import os

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Make a class of inverted index in which all the process is present to find inverted index
class invertedIndex():
	# This is an constructor which will start fetch the document word and finally will make an inverted index
	def __init__(self):
		self.exclude = list(string.punctuation)
		self.exclude.append('।') 
		if(os.path.isdir("hindi/*.txt") == True):
			self.fileName = glob.glob("hindi/*.txt")
			self.fileName.sort()
			print("hello")
		else:
			print("hindi corpus does not have file")

	def start(self):
		# self.exclude is an array which have punctuation of string
		self.exclude = list(string.punctuation)
		self.exclude.append('।') #append one hindi punctuation 
		#print(exclude)
		#open file to write
		self.f4 = open("wordIndex.txt", 'w')
		#read all file from the hindi folder and store in list(self.fileName)
		# sort the list to find sequence of file
		self.doc_id = 1 
		#self.doc_id (To store the document name with some id)
		#self.indexDict is an dictionary to store the posting list
		self.indexDict = {}
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

		#we apply all the operation in one-one file which comes sequentially using loop and store it as posting list.
		for i in range(0,len(self.fileName)):
			#Apply try catch because some document have invalid XML character(&""''<>) which can not parse
			try:
				print(self.fileName[i])
				#parse the document using ElementTree
				tree = ET.parse(self.fileName[i])
				root = tree.getroot()
				text = ''
				#read the content of title tag and store in self.text1 variable
				for i in root.findall('title'):
					self.text1 = i.text
				#read the content of content tag and store in self.text2 variable
				for i in root.findall('content'):
					self.text2 = i.text
				#now read content store in one variable
				text = self.text1 + self.text2
				#call the first operation(Remove punctuation from the document) and update the value of text variable
				text = self.remove_punctuation(text)
				#call the second operation(Remove stop word from the document) and store it in text variable in form of array
				text = self.remove_stop_word(text)
				#call the operation to apply stemming on word and store it with their document name in posting list
				self.make_PostingList(text)
				#self.doc_id = self.doc_id + 1
			except:
				#catch the error if document can not be parse
				print(self.fileName[i])
				f= open(self.fileName[i],'r').read()
				#read the content of file like substring between tag title
				start = f.find('<title>')+len('<title>')
				end = f.find('</title')
				self.text1 = f[start:end]
				#read the content of file like substring between tag content
				start = f.find('<content>')+len('<content>')
				end = f.find('</content')
				self.text2 = f[start:end]
				text = self.text1 + self.text2
				print(text)
				text = self.remove_punctuation(text)
				#call the second operation(Remove stop word from the document) and store it in text variable in form of array
				tex = self.remove_stop_word(text)
				#call the operation to apply stemming on word and store it with their document name in posting list
				self.make_PostingList(tex)
				#print(self.doc_id)
			finally:
				#increment the document id because for different document it will have different id
				self.doc_id = self.doc_id + 1
				#print(self.doc_id)
				#source.close()
		#After all this we the posting list in the file

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
		for i in self.indexDict.keys():
			self.f4.write(i + "\t\t\t")
			self.f4.write(str(self.indexDict.get(i)) + "\n")
		self.f4.close()

	# def write_in_one_file(self, text):
	# 	self.f = open("allInOne.txt", 'a+')
	# 	self.f.write(text)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#An operation to apply stemming and store word with their document id and frequency
	def make_PostingList(self, word):
		#appy stemming on each word and store in lsit(word)
		word = [self.stem_word(w) for w in word]
		#convert the list into set data type and again convert to into list to find the unique word of that file
		l = set(word)
		wordUnique = list(l)
		for i in range(len(wordUnique)):
			c=word.count(str(wordUnique[i]))
			#make condition that if word present in another document then append the current document at that place otherwise make another row and store it there
			if self.doc_id > 1:
				if str(wordUnique[i]) in self.indexDict.keys():
					self.indexDict[str(wordUnique[i])][self.doc_id] = c
					# self.f4.write(str(wordUnique[i]) + '\t\t\t')
					# self.f4.write(str(c) + '\t\t\t')
					# self.f4.write("doc" + str(self.doc_id) + '\n')
				else:
					self.indexDict[str(wordUnique[i])] = {}
					self.indexDict[str(wordUnique[i])][self.doc_id] = c
					#self.indexDict[str(wordUnique[i])] = [0]
					# self.f4.write(str(wordUnique[i]) + '\t\t\t')
					# self.f4.write(str(c) + '\t\t\t')
					# self.f4.write("doc" + str(self.doc_id) + '\n')

			else:
				#print(self.doc_id)
				self.indexDict[str(wordUnique[i])] = {}
				self.indexDict[str(wordUnique[i])][self.doc_id] = 1
				# self.f4.write(str(wordUnique[i]) + '\t\t\t')
				# self.f4.write(str(c) + '\t\t\t')
				# self.f4.write("doc" + str(self.doc_id) + '\n')
			#print(documentLocations)

		#print(self.indexDict)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#An operation to remove stop word
	def remove_stop_word(self, text):
		#print("removing stop word")
		#listOut all the stop word in stopWord list 
		stopWord=open("stopWord.txt", "r").read().split("\n")
		text3 = []
		#print(stopWord)
		text = text.split()
		#make condition if text are stop word then it will remove
		for c in text:
			if c not in stopWord:
				text3.append(c)
				#print(c)
		# tex = "".join(c for c in text if c not in stopWord)
		return text3
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#An operation to remove punctuation
	def remove_punctuation(self, text):
		text = "".join(c for c in text if c not in self.exclude)
		return text

	def dotproduct(self, Qvector, Dvector):
		return sum([x*y for x,y in zip(Qvector,Dvector)])

	def getLength(self, a):
		#print(a)
		f= open(a,'r').read()
		#read the content of file like substring between tag title
		start = f.find('<title>')+len('<title>')
		end = f.find('</title')
		self.text1 = f[start:end]
		#read the content of file like substring between tag content
		start = f.find('<content>')+len('<content>')
		end = f.find('</content')
		self.text2 = f[start:end]
		text = self.text1 + self.text2
		return len(text)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#An operation to find the root word by doing stemming
#(Taken from Github)
	def stem_word(self,word):
		#suffixes have all the suffixes of hindi word which mostly comes at the end of word
		suffixes = {
		    1: ["ो","े","ू","ु","ी","ि","ा"],
		    2: ["कर","ाओ","िए","ाई","ाए","ने","नी","ना","ते","ीं","ती","ता","ाँ","ां","ों","ें"],
		    3: ["ाकर","ाइए","ाईं","ाया","ेगी","ेगा","ोगी","ोगे","ाने","ाना","ाते","ाती","ाता","तीं","ाओं","ाएं","ुओं","ुएं","ुआं"],
		    4: ["ाएगी","ाएगा","ाओगी","ाओगे","एंगी","ेंगी","एंगे","ेंगे","ूंगी","ूंगा","ातीं","नाओं","नाएं","ताओं","ताएं","ियाँ","ियों","ियां"],
		    5: ["ाएंगी","ाएंगे","ाऊंगी","ाऊंगा","ाइयाँ","ाइयों","ाइयां"],
		}

		#make condition if word will end with these suffixes then that part will remove 
		for k in 5, 4, 3, 2, 1:
			if len(word) > k:
					#print('h')
				for s in suffixes[k]:
					if word.endswith(s):
						#print(sf)
						return (word[:-k])
			
		return word
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

if __name__ == "__main__":
	#finally call all the operation by making the object of the class
	import os
	if os.path.isfile("wordIndex.p") != True:
		obj = invertedIndex()
		if(os.path.isdir("hindi/*.txt") == True):
			obj.start()
		#finally dump the posting list in wordIndex.p in binary format
		pickle.dump(obj.indexDict,open( "wordIndex.p", "wb" ))
	indexDict = {}
	indexDict = pickle.load(open("wordIndex.p", "rb" ))
	print(len(indexDict))
	# while 1:
	# 	word = input("enter word u want posting list\n")
	# 	idf = len(indexDict[word])
	# 	print(idf)
	# 	for i in indexDict[word].keys():
	# 		print("term freq in " + i + "is" + indexDict[word][i])
	# 	#print(indexDict[word])
	# 	if 44 in indexDict[word].keys():
	# 		print('yes')
	# 	else:
	# 		print('no')
	obj = invertedIndex()
	# print(obj.fileName[1])
	# print(len(obj.fileName[1]))
	query = input("enter Your Query\n")
	query = obj.remove_punctuation(query)
	query = obj.remove_stop_word(query)
	query1 = set(query)
	query1 = list(query)
	length = len(query1)
	docVector = collections.defaultdict(lambda: [0] * length)
	queryVector = [0]*length
	#print(query1)
	N = 50691
	for q in range(0,len(query1)):
		Qtf = query.count(query1[q])
		idf = math.log(N/(len(query1)))
		queryVector[q] = Qtf * idf
		# queryVector.insert(q,Qtf)
	sumQvector = sum([x for x in queryVector])
	# print(queryVector)
	queryVector = [(x)/sumQvector for x in queryVector]
	# print(queryVector)
	j = 0
	for i in query:
		queryWord = obj.stem_word(i)
		OccuresDocument = indexDict[queryWord]
		df = len(OccuresDocument)
		idf = math.log(N/df)
		# flag =0
		for o in OccuresDocument.keys():
			tf = indexDict[queryWord][o]
			w = (tf)*(idf)
			# queryLenght.insert(i,w)
			docVector[o][j] = w
		j = j+1
	docVec = sorted(docVector.items())


	#print(docVec)
	for doc, weight in docVector.items():
		#print(obj.fileName[doc-1])
		docLength = obj.getLength(obj.fileName[doc-1])
		#print(docLength)
		for i in range(0,len(weight)):
			#print("hello")
			# print((docVector[doc][i]))
			docVector[doc][i] = (docVector[doc][i])/(docLength)
	#print(docVector)

	Scores=[ [obj.dotproduct(DocVec, queryVector), doc] for doc, DocVec in docVector.items() ]
	Scores.sort(reverse = True)
	print([x[1] for x in Scores[:20]])

	#print(query[0],query[1])उत्तम हिन्दी	