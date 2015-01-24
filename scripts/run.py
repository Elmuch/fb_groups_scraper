#!/usr/bin/python

from urlparse import urlparse
from urlparse import parse_qs
import time
import xlsxwriter
import feeds
import members
import subprocess

groups  = ['324309874271040','206494919465453','255488514638473','334271300068285']
#groups  = ['324309874271040'] # Use this for testing
pages = ['202027666597795']

workbook = xlsxwriter.Workbook('data/data.xlsx')
feeds = feeds.extract(workbook, groups, pages)
members = members.extract(workbook, groups, pages)

workbook.close()

try:
  subprocess.Popen("libreoffice --calc data/data.xlsx")
except Exception, e:
  print "Problem opening data.xlsx"