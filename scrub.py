from bs4 import BeautifulSoup
import codecs
import os
import glob
import sys
import subprocess
import re

def soup_flatten(soup):
	soupstring = ""
	try:
		soupstring = "".join(soup.findAll(text = True))
		soupstring = soupstring.replace (u"\n",u" ")
		soupstring = re.sub('[^A-Za-z0-9 ]+', '', soupstring)
		if soupstring == "Abstract":
			soupstring = ""
		# soupstring = "".join(soupstring.split())
	except:
		print("NavigableString")
	return soupstring

def abstract_scrub(filename):
	inputfile = codecs.open(filename , "r", encoding ='utf-8').read()
	soup = BeautifulSoup(inputfile)
	
	# abstract content
	div_class_list = ["section abstract", "article extract-view", "article fulltext-view"]
	for div_class in div_class_list:
		abstractdiv = soup.find("div", class_ = div_class)
		if abstractdiv != None:
			# if abstractdiv.p != None:
			with codecs.open(filename +".txt ","w", encoding ="utf-8") as outputabstract:
				for i in abstractdiv:
					outputabstract.write(soup_flatten(i)+"\n")
			# keywords , optional
			keywordsgroup = soup.find("ul", class_ = "kwd-group")
			if keywordsgroup != None :
				with codecs.open(filename +".keywords","w", encoding="utf-8") as outputkeywords:
					for i in keywordsgroup:
						outputkeywords.write(soup_flatten(i)+"\n")
			return 0
	return 1

def main():

	errorfile = open("errors-scrub-pdf.txt","w")
	for folder in ["2011","2012","2013"]:
		errors = 0
		successes = 0
		print("\n", "="*60)
		print(folder , "Converting .abstract to .abstract.txt ")
		print("-"*40)
		for filename in glob.glob (folder +"/"+"*.abstract"):
			if abstract_scrub(filename) !=0:
				print(filename ,": Could not be parsed . Empty or partial abstract ?")
				errorfile.write(filename + "\n")
				errors += 1
			else : 
				successes +=1
		print("="*60)
		print("Successes :", successes , " Errors :", errors)
	errorfile.close()

if __name__ == "__main__":
	main()