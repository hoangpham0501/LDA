from csv_unicode import *
import os.path
from optparse import OptionParser
import pandas as pd 

def main():
	parser = OptionParser("usage: %prog [options] arg")
	parser.add_option("-f", "--file", dest="filename", help="read from")
	parser.add_option("-o", "--output", dest="output_filename", help ="write to")
	parser.add_option("-d", "--check-dup", action="store_true", dest="check_duplicate_abstracts")
	parser.add_option("-s", "--skip-dup", action="store_true", dest ="skip_duplicate_abstracts")
	parser.add_option("-m", "--missing-only", action ="store_true", dest="download_missing_only")
	parser.add_option("-t", "--clean-titles", action ="store_true", dest="clean_titles ")
	parser.add_option("-c", "--clean-categories", action ="store_true", dest ="clean_categories")
	parser.add_option("-r", "--reorder-columns", action ="store_true", dest ="reorder_columns")
	parser.set_defaults(filename ="scraped_2015.csv", output_filename ="selected_2015.csv", 
		check_duplicate_abstracts =False,
		skip_duplicate_abstracts =False,
		clean_titles =True,
		clean_categories =True,
		reorder_columns =True,
		download_missing_only = False)
	(options, args) = parser.parse_args()
	if len(args) != 0: 
		parser.error("incorrect number of arguments")
	url_base = "http://www.pnas.org"
	categories_major = [u"Biological Sciences", u"Physical Sciences", u"Social Sciences"]
	reader = pd.read_csv(options.filename)
	firstline = reader.columns
	# Create output file
	with open(options.output_filename, 'w', encoding='utf-8') as f:
		writer = csv.writer(f)

		# # Add header line to output , always the same extra columns ,regardless of options
		if options.reorder_columns == True :
			firstline =["category","category_minor","authors","title","year",
			"volume","issue","pages","url_abstract","url_extract", "url_fulltext","url_fullpdf"]
		writer.writerow(firstline + ["url_abstract_is_duplicate", "download_abstract", "download_fullpdf"])

		processed_abstract_fields = []
		url_abstract_duplicates = 0
		relevant_abstracts = 0
		relevant_fullpdfs = 0
		found_fullpdfs = 0
		found_abstracts = 0
		marked_abstracts = 0
		marked_fullpdfs = 0
		irrelevant_abstracts = 0
		irrelevant_fullpdfs = 0
		for row in reader.index:
			url_abstract = reader['url_abstract'][row]
			url_abstract_is_duplicate = ""
			download_abstract =""
			download_fullpdf =""
			# Clean manually some misformed major categories
			if options.clean_categories == True :
				if reader['category'][row]== u"Biological Sciences : Biochemistry":
					reader['category'][row]= u"Biological Sciences"
					reader['category_minor'][row]= u"Biochemistry"
				if reader['category'][row]== u"Biological Sciences :Biophysics":
					reader['category'][row]= u"Biological Sciences"
					reader['category_minor'][row]= u"Biophysics"
				if reader['category'][row]== u"Biological Sciences : Evolution":
					reader['category'][row]= u"Biological Sciences"
					reader['category_minor'][row]= u"Evolution"
				if reader['category'][row]== u"Evolution":
					reader['category'][row]= u"Biological Sciences"
					reader['category_minor'][row]= u"Evolution"
				if reader['category'][row]== u"Immunology":
					reader['category'][row]= u"Biological Sciences"
					reader['category_minor'][row]= u"Immunology"
				if reader['category'][row]== u"Physical Sciences : Chemistry":
					reader['category'][row]= u"Physical Sciences"
					reader['category_minor'][row]= u"Chemistry"
				if reader['category'][row]== u"Physical Sciences : Geophysics":
					reader['category'][row]= u"Physical Sciences"
					reader['category_minor'][row]= u"Geophysics"
				if reader['category'][row]== u"Profile":
					reader['category'][row]= u"Profiles"
				if reader['category'][row]== u"Perspective":
					reader['category'][row]= u"Perspectives"
				if reader['category'][row]== u"Letter (Online Only)":
					reader['category'][row]= u"Letters (Online Only)"
				if reader['category'][row]== u"Correction (Online Only)":
					reader['category'][row]= u"Corrections (Online Only)"

			# Check duplicate abstracts url
			if options.check_duplicate_abstracts == True and url_abstract in processed_abstract_fields :
				url_abstract_is_duplicate ="yes"
				url_abstract_duplicates += 1

			## if a line has no category_minor
			if reader['url_abstract'][row]!= u"" and reader['category_minor'][row]!= u"":
			## if no duplicate checking is active , this will always work
				if options.skip_duplicate_abstracts == True and url_abstract_is_duplicate =="yes":
					pass
				else :
					download_abstract ="yes"
					relevant_abstracts +=1

			### Full PDFs for abstracts that lack a category
			if reader['url_abstract'][row]!= u"" and reader['category'][row]==u"Research Article" and reader['url_fullpdf'][row]!= u"":
				if options.skip_duplicate_abstracts == True and url_abstract_is_duplicate ==" yes ":
					pass
				else :
					download_abstract ="yes"
					relevant_abstracts +=1
					download_fullpdf ="yes"
					relevant_fullpdfs +=1

			if options.download_missing_only == True :
				abstract_filename = url_abstract.split("/")[-1]
				base_filename = abstract_filename.split(".")[0]
				local_base_path = str(reader['year'][row])+ "/"+ base_filename
				local_path = str(reader['year'][row])+ "/"+ abstract_filename
				if os.path.isfile(local_path) and os.path.getsize (local_path) !=0:
					if download_abstract =="" and url_abstract_is_duplicate =="":
						irrelevant_abstracts +=1

					download_abstract =""
					found_abstracts +=1
				local_path = str(reader['year'][row])+ "/"+ base_filename +".full.pdf"
				if os.path.isfile(local_path) and os.path.getsize(local_path ) !=0:
					if download_fullpdf =="" and url_abstract_is_duplicate =="": 
						irrelevant_fullpdfs +=1
					download_fullpdf =""
					found_fullpdfs +=1

			if options.clean_titles == True:
				if download_abstract =="yes": 
					marked_abstracts +=1
				if download_fullpdf =="yes": 
					marked_fullpdfs +=1
				readers_additional =[url_abstract_is_duplicate , download_abstract , download_fullpdf]
				if options.reorder_columns == True :
					read = [reader[i][row] for i in firstline]
				writer.writerow(read + readers_additional)

			if options.check_duplicate_abstracts == True and url_abstract !=u"": 
				processed_abstract_fields.append(url_abstract)

		if options.check_duplicate_abstracts == True : 
			print("Duplicate url_abstract entries :", url_abstract_duplicates)
	print(".abstract : relevant : %5d, found : %5d, found but irrelevant :%5d, marked for download : %5d" % ( relevant_abstracts , found_abstracts , irrelevant_abstracts , marked_abstracts ))
	print(".fullpdf : relevant : %5d, found : %5d, found but irrelevant :%5d, marked for download : %5d" % ( relevant_fullpdfs , found_fullpdfs , irrelevant_fullpdfs , marked_fullpdfs ))
	print("Irrelevant files (non - duplicate ): leftovers from other scrapers or manual download selection ")
	print("Relevant files : these include Research articles with unknown category . Some files will later be recognized as irrelevant (5-zip .py).")

if __name__ == "__main__":
	main()