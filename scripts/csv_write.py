# Util for writing data to csv formats
# This slightly extends csv module to fit current needs

import csv

class CSVWriter(object):
	def __init__(self, headers, name):
		self.name = name
		self.headers = headers

	def __write(self):
		path = "data/%s.csv" %(self.name)
		self.__f = open(path, "wt")
		self.__writer = csv.writer(self.__f)
		self.__writer.writerow(self.headers)
	
	def writer(self):
		self.__write()
		return self.__writer

	def close(self):
		self.__f.close()
