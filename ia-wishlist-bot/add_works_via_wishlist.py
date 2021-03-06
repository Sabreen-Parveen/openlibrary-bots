"""
Python Script to add books to Open Library using the Open Library Client

Input: 'wish_list_march_2018.ndjson'
* Parameters for the wishlist include "isbn10", "language", "author", "isbn13", "title" , "oclc", "date"

Output: Adding new works to Open Library 
"""

# Using the Open Library Client
from olclient.openlibrary import OpenLibrary
import olclient.common as common
import ndjson

# Import os to check for file exist and 
# urllib to download the file
import os
import urllib.request

# File used in the whole script
FILE = 'data/wish_list_march_2018.ndjson'

# Creating an object of the Open Library Client
ol = OpenLibrary()

# Check if a directory called data exists
if not os.path.isdir("data"):
	os.mkdir('data')

# If the required file is not available download the file
if not os.path.exists(FILE):
	file_name = FILE
	urllib.request.urlretrieve(
		'https://archive.org/download/openlibrary-bots/wish_list_march_2018.ndjson', file_name)
def row2book(new_book):
	# Data of the book
	title = new_book.get('title', u'')
	author = new_book.get('author', u'')
	date = new_book.get('date', u'')

	# Define a Book Object
	added_book = common.Book(title=title, authors=[common.Author(
		name=author)], publisher=u"", publish_date=date)

	return added_book

# Use the Wishlist ndjson file
with open(FILE) as f:
	data = ndjson.load(f)

# Iterates over the size of the data
for new_book in data:

	isbn10 = new_book.get('isbn10', u'')
	isbn13 = new_book.get('isbn13', u'')
	oclc = new_book.get('oclc', u'')

	added_book = row2book(new_book)

	# Add metadata like ISBN 10 and ISBN 13
	added_book.add_id(u'isbn_10', isbn10)
	added_book.add_id(u'isbn_13', isbn13)
	added_book.add_id(u'oclc', oclc)

	# Call create book to create the book
	newly_added_book = ol.create_book(added_book)

	# Add Bookcover if it is present
	bookcover_added = True
	if new_book['bookcover']:
		newly_added_book.add_bookcover(new_book['bookcover'])  
	else: 
		bookcover_added = False

	if not bookcover_added:
		print("Bookcover has not been found for the given book")
