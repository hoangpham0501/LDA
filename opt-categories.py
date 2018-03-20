#! / usr / bin / python
from csv_unicode import *
import pandas as pd
import numpy as np
"""
Create a separate categories .csv , for deciding which categories to
merge .
Not needed for a regular run of the scraper .
"""

def main():
	categories_major = [u"Biological Sciences", u"Physical Sciences", u"Social Sciences"]
	filename = "selected.csv"
	reader = pd.read_csv(filename)
	firstline = reader.columns
	print(reader)
	writer = UnicodeWriter(open("categorises.csv", "wb"))

	categories ={}
	for year in range (2014 ,2019):
		categories[str(year)]=[]
	print(categories[str(2018)])
	for row in reader.index :
		print(reader['category'][row])
		# if reader["category_fullpdf"][row]!= u"":
			# categories[reader['year'][row]].append(reader["category_fullpdf"][row])
		if reader['category_minor'][row]!= "":
			# print(reader["category_minor"][row])
			categories[str(reader['year'][row])].append(str(reader['category_minor'][row])+ "(" + str(reader['category'][row]) + ")")
	writer.writerow(["year", "category"])
	for year in categories:
		for cat in set(categories[year]):
			print(year , cat)
			writer.writerow([year , cat])

if __name__ == "__main__":
	main()