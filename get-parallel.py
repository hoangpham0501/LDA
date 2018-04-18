from time import sleep
from csv_unicode import *
import os
import sys
import pycurl
import codecs
import pandas as pd
from multiprocessing import Pool

missinglist = []

def download_file(url, tofolder, socks = False):
	filename = url.split("/")[-1]
	if not os.path.exists(tofolder):
		os.makedirs(tofolder)
	try :
		fileout = open(tofolder + "/" + filename , "wb")
	except :
		print(tofolder +"/"+ filename + ": Error opening file for saving ")
		return 1
	curl = pycurl.Curl()
	curl.setopt(pycurl.FOLLOWLOCATION, 1)
	curl.setopt(pycurl.MAXREDIRS, 5)
	curl.setopt(pycurl.CONNECTTIMEOUT, 30)
	curl.setopt(pycurl.TIMEOUT, 300)
	curl.setopt(pycurl.NOSIGNAL, 1)
	curl.setopt(pycurl.URL, url)
	curl.setopt(pycurl.WRITEDATA, fileout)
	if socks == True :
		curl.setopt(pycurl.PROXY, 'localhost')
		curl.setopt(pycurl.PROXYPORT, 8080)
		curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
	try :
		curl.perform()
	except :
		print(url+': Error downloading.')
		import traceback
		traceback.print_exc(file =sys.stderr)
		sys.stderr.flush()
		return(1)
	curl.close()
	fileout.close()
	return 0

def missing_loop(missinglist , filename , sockssupport):
	#the following is a loop that runs only if there were downloading errors.
	downloaded = 0
	missingloops = 1
	try :
		while missinglist != []:
			print("-"*40)
			print(" Retry loop ", str(missingloops), " -", "Items missing :", len(missinglist))
			print("-"*40)
			missinglist2 = []
			for missing in missinglist :
				sleep(1)
				if download_file(missing , sockssupport)!= 0:
					missinglist2.append(missing)
				else :
					downloaded += 1
			# overwrite old list
			missinglist = missinglist2
			missingloops += 1
	except KeyboardInterrupt :
		for missing in missinglist :
			filemissing = open(filename ,"wb")
			filemissing.write(missing[0]+ "\n")
			filemissing.close()
			print("Successfully downloaded :", downloaded)
			print("Sill missing :", len( missinglist ))
			print (filename , " written !")
	return downloaded

def parse(list_merge):
	print("Downloading :", list_merge[0], list_merge[1])
	if download_file(list_merge[0], str(list_merge[1])) != 0:
		missinglist.append(list_merge[0], str(list_merge[1]))
	sleep(10)

def main():
	url_base = "http://www.pnas.org"
	interval = 10
	filename = "selected.csv"
	reader = pd.read_csv(filename)
	sockssupport = False
	# if "socks" in sys.argv :
	# 	sockssupport = True

	if "abstracts" in sys.argv :
		print("abstracts:")
		list_merge = [list(a) for a in zip(reader['url_abstract'], reader['year'])]
		with Pool(3) as p:
			p.map(parse, list_merge)

		print("="*40)
		# print("Successful downloads :", downloaded)
		if missinglist != []:
			missingdownloaded = missing_loop(missinglist , "missing-abstracts.txt", sockssupport)
			print("Successful downloads in missing loop :", missingdownloaded)

	elif "fullpdfs" in sys.argv :
		print("fullpdfs :")
		for row in reader.index :
			if reader['download_fullpdf'][row]== "yes":
				url = reader['url_fullpdf'][row]
				print("Downloading :", url , reader['year'][row])
				if download_file (url, reader['year'][row], sockssupport)!= 0:
					missinglist.append((url , reader['year'][row]))
				else :
					downloaded += 1
				sleep(interval)
		print("="*40)
		print("Successful downloads :", downloaded)
		if missinglist != []:
			missingdownloaded = missing_loop(missinglist , "missing-fullpdf-res.txt ", sockssupport)
			print("Successful downloads in missing loop :", missingdownloaded)

	else :
		print("Fields in", filename , ":")
		print()
		print("Available arguments : 'fullpdfs ' and /or 'abstracts ' and /or 'socks '")
		print("Socks support : ssh -D 8080 -v -N h0053049@login .wu.ac.at")

if __name__ == "__main__":
	main()