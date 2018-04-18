from bs4 import BeautifulSoup
import codecs
import os
import glob
import sys
import subprocess
import re
from multiprocessing import Pool

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
		pass
	return soupstring

def category_scrub(category):
	category = category.replace(u"(rheumatic disease / nuclear autoantigen / epitope)", u"Immunology")
	category = category.replace(u"This paper is based on a presentation given during the 130 th Annual Meeting of the National Academy ofSciences",u"Review")
	category = category.replace(u"Vol. 89, pp. 6639 -6643 , July 1992", u"Neurobiology")
	category = category.replace(u"bull . At 40 -48 hr postfertilization , embryos were manually",u"Developmental Biology")
	category = category.replace(u",",u"")
	category = category.replace(u"'",u"")
	category = category.replace(u".",u"")
	category = category.replace(u"Anthropo ogy",u" Anthropology")
	category = category.replace(u"Applied 1 iological Sciences",u"Applied Biological Sciences")
	category = category.replace(u"Applied 1 iological Sciences",u"Applied Biological Sciences")
	category = category.replace(u"Applied Biologcal Sciences",u"Applied Biological Sciences")
	category = category.replace(u"Biocem stry",u"Biochemistry")
	category = category.replace(u"Biochemlstry",u"Biochemistry")
	category = category.replace(u"Biochemisty",u"Biochemistry")
	category = category.replace(u"Biochemnistry",u"Biochemistry")
	category = category.replace(u"Biochemnstry",u"Biochemistry")
	category = category.replace(u"Biochemsstry",u"Biochemistry")
	category = category.replace(u"Biochemstr",u"Biochemistry")
	category = category.replace(u"Biochemustry",u"Biochemistry")
	category = category.replace(u"Biochenistry",u"Biochemistry")
	category = category.replace(u"Biochenmstry",u"Biochemistry")
	category = category.replace(u"Biochenustry",u"Biochemistry")
	category = category.replace(u"Ccll Biology",u"Cell Biology")
	category = category.replace(u"Ceil Biology",u"Cell Biology")
	category = category.replace(u"Celi Biology",u"Cell Biology")
	category = category.replace(u"Cell Biofogy",u"Cell Biology")
	category = category.replace(u"Cell BioIlogy",u"Cell Biology")
	category = category.replace(u"Cell Bioiogy",u"Cell Biology")
	category = category.replace(u"Cell Biol [ ogy",u"Cell Biology")
	category = category.replace(u"Cell BioLogy",u"Cell Biology")
	category = category.replace(u"CeLl Biology",u"Cell Biology")
	category = category.replace(u"Cell Bio ogy",u"Cell Biology")
	category = category.replace(u"Cell Bio[ ogy",u"Cell Biology")
	category = category.replace(u"Cell Biotogy",u"Cell Biology")
	category = category.replace(u"Colioquium Paper",u"Colloquium Paper")
	category = category.replace(u"Development Biology",u"Developmental Biology")
	category = category.replace(u"exonuclease BAL -31 to generate ordered sets ofdeletions in", u"Microbiology")
	category = category.replace(u"ficrobiology",u"Microbiology")
	category = category.replace(u"ficrobiology",u"Microbiology")
	category = category.replace(u"fMicrobiology",u"Microbiology")
	category = category.replace(u"Immunoiogy",u"Immunology")
	category = category.replace(u"Inmunology",u"Immunology")
	category = category.replace(u"Immuno ogy",u"Immunology")
	category = category.replace(u"JBiophysics",u"Biophysics")
	category = category.replace(u"Medical ciences",u"Medical Sciences")
	category = category.replace(u"Medical Science", "Medical Sciences")
	category = category.replace(u"Medical science",u"Medical Sciences")
	category = category.replace(u"Medical Sclences",u"Medical Sciences")
	category = category.replace(u"Medical Sciencess", u"Medical Sciences")
	category = category.replace(u"Microbiology 0",u"Microbiology")
	category = category.replace(u"Microbiology a",u"Microbiology")
	category = category.replace(u"Ncurobiology",u"Microbiology")
	category = category.replace(u"Neurobiofogy",u"Microbiology")
	category = category.replace(u"NeurobioLogy",u"Microbiology")
	category = category.replace(u"Neurobio ogy",u"Microbiology")
	category = category.replace(u"Pharmaology",u"Pharmacology")
	category = category.replace(u"Phraoogy",u"Pharmacology")
	category = category.replace(u"Perspectives",u"Perspective")
	category = category.replace(u"ProfileS",u"Profile")
	return category

def abstract_scrub(filename):
	inputfile = codecs.open(filename , "r", encoding ='utf-8').read()
	soup = BeautifulSoup(inputfile)
	
	# abstract content
	abstractdiv = soup.find("div", class_ ="section abstract")
	if abstractdiv == None :
		abstractdiv = soup.find("div", class_ = "article extract-view")
		if abstractdiv == None:
			return 1
	if abstractdiv.p != None :
		outputabstract = codecs.open(filename +".txt ","w", encoding ="utf-8")
		outputabstract.write(soup_flatten(abstractdiv.p)+"\n")
		outputabstract.close()

	# keywords , optional
	keywordsgroup = soup.find("ul", class_ = "kwd-group")
	if keywordsgroup != None :
		with codecs.open(filename +".keywords","w", encoding="utf-8") as outputkeywords:
			for i in keywordsgroup:
				outputkeywords.write(soup_flatten(i)+"\n")

	return 0

def main():

	if len(sys.argv) < 2:
		print("No argument supplied . Available are : 'abstracts ' and /or 'fullpdfs '.")
		return 1

	errorfile = open("errors-scrub-pdf.txt","w")
	for folder in ["2011"]:
		if "abstracts" in sys.argv :
			errors = 0
			successes = 0
			print("\n", "="*60)
			print(folder , "Converting .abstract to .abstract.txt ")
			print("-"*40)
			# for filename in glob.glob (folder +"/"+"*.abstract"):
			# 	if abstract_scrub(filename) !=0:
			# 		print(filename ,": Could not be parsed . Empty or partial abstract ?")
			# 		errors += 1
			# 	else : 
			# 		successes +=1
			filenames = glob.glob(folder + "/" +"*.abstract")
			with Pool(3) as p:
				p.map(abstract_scrub, filenames)
			print("="*60)
			print("Successes :", successes , " Errors :", errors)

		if "fullpdfs" in sys.argv :
			errors = 0
			successes = 0
			print("\n", "="*60)
			print(folder , " Extracting .full.category from .full.pdf")
			print("-"*40)
			for filename in glob.glob(folder +"/"+"*.pdf"):
				if subprocess.call(['pdftotext','-raw',filename]) !=0:
					print(filename ,": pdftotext error.")
					errorfile.write(filename )
					errors += 1
				else :
					filebase = filename.replace(".pdf","")
					try :
						fulltext = codecs.open(filebase +".txt ","r", encoding ="utf -8")
						#next(fulltext)
						#next(fulltex)
						category = fulltext.readline().strip()
						category = category_scrub(category)
						fulltext.close()
						os.remove(filebase +".txt")
					except :
						print(filename , ": Error reading .full.txt. Is the PDF empty or not OCRed?")
						errors += 1
						continue
					try :
						categoryfile = codecs.open(filebase +".category","w", encoding ="utf -8")
						categoryfile.write(category)
						categoryfile.close()
						successes +=1
					except :
						print(filename , ": Error writing .full.category.")
						errors += 1
						print("="*60)
						print("Successes :", successes , " Errors :", errors)
						errorfile.close()
if __name__ == "__main__":
	main()