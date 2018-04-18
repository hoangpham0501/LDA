from csv_unicode import *
import os.path
import sys # for args
import pandas as pd

def main():
	filename = "selected_2011.csv"
	reader = pd.read_csv(filename)
	firstline = reader.columns

	with open("meta_2011.csv", 'w', encoding='utf-8') as f:
		writer = csv.writer(f)

		### All relevant abstracts
		notselected = 0
		processed_abstract_fields = []
		output_list = []
		duplicate_abstracts = 0
		downloads_selected =0
		lines_written =0
		count =0

		if len(sys.argv) == 1:
			print("Available arguments :")
			print("'all' ......... process all input lines.")
			print("'skiperrors'... only return complete metadata."); exit (1)
			print("Warnings are also stored in the resulting file.")
		elif len (sys.argv) == 2 and "all" in sys.argv : 
			errorlineskip = 0
		elif len (sys.argv ) == 2 and "skiperrors" in sys.argv : 
			errorlineskip = 1
		else : 
			print("Wrong argument")
			exit(1)
		print("Remember to previously run ./2-select.py without -m flag to ensure that all relevant abstracts are tagged for download !")

		writer.writerow(firstline.tolist() + ["abstract_local_path", "keywords", "warning"])

		for row in reader.index :
			add_local_abstract_path = ""
			add_keywords = ""
			add_warning = ""
			url_abstract = reader['url_abstract'][row]

			if url_abstract !="" and url_abstract in processed_abstract_fields :
				add_warning += "CSV : duplicate abstract path , "
				# print(url_abstract)
				duplicate_abstracts += 1
				if errorlineskip : continue
			processed_abstract_fields.append(url_abstract)
			if url_abstract =="": 
				add_warning += "CSV: Empty url_abstract , "

			## Only lines that were previously selected
			if reader["download_abstract"][row] == "yes":
				downloads_selected +=1
				abstract_filename = url_abstract.split("/")[-1]
				base_filename = abstract_filename.split(".")[0]
				local_base_path = str(reader['year'][row])+ "/"+ base_filename
				local_abstracttxt_path = str(reader['year'][row])+ "/"+ abstract_filename +".txt"

				if os.path.isfile(local_abstracttxt_path):
					if local_abstracttxt_path != "":
						add_local_abstract_path = local_abstracttxt_path
						add_warning += "FILE : OK: .abstract.txt ,"
					else :
						add_warning += "FILE : .abstract.txt is empty , "
						if errorlineskip : continue
				else :
					count += 1

				## get keywords
				local_meta_path = local_base_path + ".abstract.keywords"
				if os.path.isfile(local_meta_path):
					with codecs.open(local_meta_path , "rb", encoding ='utf-8') as metafile:
						add_keywords = metafile.readline()


			if reader["download_abstract"][row] == u"":
				add_warning += "CSV : not selected for download ,"
				notselected += 1
				if errorlineskip :
					continue

			read = [reader[i][row] for i in firstline]
			if add_local_abstract_path != "":
				writer.writerow( read + [add_local_abstract_path, add_keywords , add_warning ])
				lines_written +=1

	print("-"*80)
	print("Errors resulted in skipping a line :", errorlineskip and "yes, only good data is saved to .csv" or "no , all warnings can be read in .csv output ")
	print("Duplicate url_abstract :", duplicate_abstracts , errorlineskip and "( skipped )" or "( not skipped )")
	print("Lines with unique url_abstract :", len (processed_abstract_fields ), errorlineskip and "." or "( including empty )")
	print(" Abstracts originally selected for download :", downloads_selected , "( including 'Research Articles ')")
	print(" Output : lines written :", lines_written)
	print(count)
	print("-"*80)

if __name__ == "__main__":
	main()