from csv_unicode import *
import os.path
import sys # for args
import pandas as pd

category_merged_dict = {u"Agricultural Sciences":"Agricultural Sciences", 
u"Anthropology":"Anthropology",
u"Applied Biological Sciences":"Applied Biological Sciences",
u"Applied Mathematics":"Applied Mathematics",
u"Applied Physical Sciences":"Applied Physical Sciences",
u"Astronomy":"Astronomy",
u"Biochemistry":"Biochemistry",
u"Biophysics":"Biophysics",
u"Botany":"Plant Biology",
u"Cell Biology":"Cell Biology",
u"Chemistry":"Chemistry",
u"Computer Sciences":"Computer Sciences",
u"Developmental Biology":"Developmental Biology",
u"Ecology":"Ecology",
u"Economic Sciences":"Economic Sciences",
u"Engineering":"Engineering",
u"Evolution":"Evolution",
u"Genetics":"Genetics",
u"Geology":"Geology",
u"Geophysics":"Geophysics",
u"Immunology":"Immunology",
u"Mathematics":"Mathematics",
u"Medical Sciences":"Medical Sciences",
u"Molecular Biology":"Biochemistry",
u"Microbiology":"Microbiology",
u"Neurobiology":"Neurobiology",
u"Neurosciences":"Neurobiology",
u"Pharmacology":"Physiology / Pharmacology",
u"Physics":"Physics",
u"Physiology":"Physiology / Pharmacology",
u"Plant Biology":"Plant Biology",
u"Plant Sciences":"Plant Biology",
u"Political Sciences":"Social Sciences",
u"Population Biology":"Population Biology",
u"Psychology":"Psychology",
u"Social Sciences":"Social Sciences",
u"Statistics":"Statistics",
u"Biophysics and Computational Biology":"Biophysics and Computational Biology",
u"Earth, Atmospheric, and Planetary Sciences":"Earth, Atmospheric, and Planetary Sciences",
u"Psychological and Cognitive Sciences":"Psychological and Cognitive Sciences",
u"Immunology and Inflammation":"Immunology and Inflammation",
u"Neuroscience":"Neuroscience",
u"Sustainability Science":"Sustainability Science",
u"Environmental Sciences":"Environmental Sciences",
u"Systems Biology":"Systems Biology",
u"Applied mathematics":"Applied Mathematics",
u"Medical sciences":"Medical Sciences",
u"Applied Biological sciences":"Applied Biological Sciences",
u"Earth, Atmospheric, and Planetary sciences":"Earth, Atmospheric, and Planetary Sciences"}

def main():
	url_base = "http://www.pnas.org "
	filename = "selected_2018.csv"
	reader = pd.read_csv(filename)
	firstline = reader.columns
	print(firstline.tolist())
	categories_major = [u"Biological Sciences", u"Physical Sciences", u"Social Sciences"]

	with open("meta_2018.csv", 'w', encoding='utf-8') as f:
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

		writer.writerow(firstline.tolist() + ["abstract_local_path", "local_fullpdf_path", "category_fullpdf", 
			"category_abstract_1_major", "category_abstract_1_minor", 
			"category_abstract_2_major", "category_abstract_2_minor",
			"category_merged", "keywords", "warning"])

		for row in reader.index :
			add_local_abstract_path = ""
			add_local_fullpdf_path = ""
			add_category_fullpdf = ""
			add_keywords = ""
			add_warning = ""
			add_category_abstract_1_major =""
			add_category_abstract_1_minor =""
			add_category_abstract_2_major =""
			add_category_abstract_2_minor =""
			add_category_merged =""
			url_abstract = reader['url_abstract'][row]

			if url_abstract !="" and url_abstract in processed_abstract_fields :
				add_warning += "CSV : duplicate abstract path , "
				print(url_abstract)
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

				## get pdf path
				local_meta_path = local_base_path + ".full.pdf "
				if os.path.isfile(local_meta_path):
					add_local_fullpdf_path = local_meta_path

				## get category
				local_meta_path = local_base_path + ".full.category "
				if os.path.isfile(local_meta_path):
					metafile = open(local_meta_path , "rb")
					add_category_fullpdf = unicode(metafile.readline().strip())
					metafile.close()

				## get keywords
				local_meta_path = local_base_path + ".abstract.keywords"
				if os.path.isfile(local_meta_path):
					with codecs.open(local_meta_path , "rb", encoding ='utf-8') as metafile:
						add_keywords = metafile.readline()


				## get categories from abstract
				local_meta_path = local_base_path + ".abstract.categories"
				if os.path.isfile(local_meta_path):
					cat_reader = UnicodeReader(open(local_meta_path , "rb"))
					linesread =0
					for line in cat_reader :
						if line[0] in categories_major :
							if linesread ==0:
								add_category_abstract_1_major = line[0]
								add_category_abstract_1_minor = line[1]
							if linesread ==1:
								add_category_abstract_2_major = line[0]
								add_category_abstract_2_minor = line[1]
						linesread +=1

			if reader['category'][row] in categories_major :
				## generate merged categories
				if reader['category_minor'][row]!= "":
					add_category_merged = category_merged_dict[reader['category_minor'][row]]
				else :
					add_warning += "META : no minor category , "
					if errorlineskip : continue
			elif reader["category"][row]== "Research Article":
				if add_category_fullpdf in [u"Colloquium Paper",u"Commentary",u"Review",u"Symposium Paper"]:
					add_warning += "META : 'Research article': irrelevant add_category_fullpdf,"
					if errorlineskip : continue
				else :
					if add_category_fullpdf !="": 
						add_category_merged = category_merged_dict[add_category_fullpdf]
					else :
						add_warning += "META : 'Research article': empty add_category_fullpdf ,"
						if errorlineskip : 
							continue
			elif reader["category"][row]!= "" and reader["category_minor"][row]!= "" and add_category_abstract_1_major == "" and add_category_abstract_1_minor == "" and add_category_abstract_2_major in categories_major :
				add_category_merged = category_merged_dict[add_category_abstract_2_minor ]
			
			else :
				add_warning += "META : no category details ,"
				if errorlineskip : 
					continue

			if reader["download_abstract"][row] == u"":
				add_warning += "CSV : not selected for download ,"
				notselected += 1
				if errorlineskip :
					continue

			read = [reader[i][row] for i in firstline]
			if add_local_abstract_path != "":
				writer.writerow( read + [add_local_abstract_path , add_local_fullpdf_path , add_category_fullpdf ,
					add_category_abstract_1_major , add_category_abstract_1_minor , add_category_abstract_2_major ,
					add_category_abstract_2_minor ,
					add_category_merged , add_keywords , add_warning ])
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