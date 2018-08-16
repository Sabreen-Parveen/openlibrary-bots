#!/usr/bin/python
import json
from olclient.openlibrary import OpenLibrary
ol = OpenLibrary()

infile = "olids-to-update.txt"

# infile is the json output of an archive.org search query
# containing an 'openlibrary' (edition olid) and 'identifier' (ocaid) fields


def sync_ol_to_ia(olid):
    r = ol.session.get(ol.base_url + "/admin/sync?edition_id=" + olid)
    if 'error' in r.json() and r.json()['error'] == 'No qualifying edition':
        print("%s, %s: %s" % (olid, ocaid, r.json()))

start = 187
start = 7649
end = False
with open(infile) as f:
   for count, line in enumerate(f):
       # OLD TSV FORMAT: ocaid, olid = line.split()
       data = json.loads(line)
       ocaid = data.get('identifier')
       olid  = data.get('openlibrary')
       if start and count < start:
           continue
       if end and count > end:
           break
       # check and add ocaid to OL edition
       print "Adding %s to %s" % (ocaid, olid)
       edition = ol.get(olid)
       #while not hasattr(edition, 'title')
       try:
           assert edition.title
       except:
           print "]%s[" % olid
           break

       if hasattr(edition, 'ocaid'):
           print("  OCAID already found: %s" % edition.ocaid)
       else:
           edition.ocaid = ocaid
           edition.save('add ocaid') 
       # sync the edition
       sync_ol_to_ia(olid)
