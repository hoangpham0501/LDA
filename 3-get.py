from time import sleep
from csv_unicode import *
import os
import sys
import pycurl
import codecs
import pandas as pd

def download_file_urllib(urlbase , urlpath , tofolder):
	from urllib2 import Request , urlopen
	filename = urlpath.split ("/")[ -1]
	if not os.path.exists(tofolder):
		os.makedirs(tofolder)
	req = Request(urlbase + urlpath)
	try:
		response = urlopen(req)
	except IOError as e:
		if hasattr(e, 'reason'):
			print(urlbase + urlpath + ': We failed to reach a server.')
			print('Reason : ', e.reason)
		elif hasattr(e, 'code'):
			print(urlbase + urlpath + ': The server couldn \'t fulfill the request.')
			print('Error code : ', e.code)
		return 1
	try :
		fileout = open(tofolder + "/" + filename , "wb")
		fileout.write(response.read())
		fileout.close
	except :
		print(tofolder + filename + ": Error saving ")
		return 1
	return 0

def download_file(url, tofolder, socks = False):
	filename = url.split("/")[ -1]
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

def main():
	url_base = "http://www.pnas.org"
	interval = 10
	filename = "selected.csv"
	reader = pd.read_csv(filename)
	sockssupport = False
	if "socks" in sys.argv :
		sockssupport = True

	downloaded = 0
	missinglist = []

	if "abstracts" in sys.argv :
		print("abstracts:")
		for row in reader.index:
			print(reader["url_abstract"][row])
			if reader['download_abstract'][row]== "yes":
				print("Downloading :", reader['url_abstract'][row], reader['year'][row])
				if download_file(reader['url_abstract'][row], str(reader['year'][row]), sockssupport)!= 0: 
					missinglist.append((reader['url_abstract'][row], reader['year'][row]))
				else :
					downloaded += 1
				sleep(interval)
		print("="*40)
		print("Successful downloads :", downloaded)
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