#!/usr/bin/python

import sys

def getMax(data):
	Max=0
	for c in data.split():
		if(c!=' '):
			Max=max(Max, abs(int(c)))
	return Max

def strip(data):
	data=data.replace('\n', '')
	data=data.replace('(', '')
	data=data.replace(')', '')
	data=data.replace(',', ' ')
	return data

def getClause(data):
	count=0
	for c in data:
		if(c==')'):
			count=count+1
	
	return count

def writeFile(file, data2):
	data2=data2.replace('\n', '')
	data2=data2.replace('(', '')
	data2=data2.replace(',', ' ')
	data2=data2.replace(')', ' #')
	for c in data2.split():
		if(c=='#'):
			file.write("0\n")
		else:
			file.write(c+" ")
	
def convert(filename):
	with open(filename, 'r') as myfile:
		data=myfile.read()
	
	data2=data
	numOfClause=getClause(data)
	data=strip(data)
	numOfVar=getMax(data)
	
	file=open("test1.convert", "w")
	file.write("c CNF formula\n")
	file.write("p cnf "+str(numOfVar)+" "+str(numOfClause)+"\n")
	writeFile(file, data2)

def main():
	convert(sys.argv[1])

if __name__ == '__main__':
	main()
