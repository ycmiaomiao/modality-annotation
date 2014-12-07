#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
- This code adds POS as an attribute to word elements in basedata
- Basedata are those end with _words.xml. I used the files in folder postprocessed_data/words_en
- Chuncks	
    1. Converts xml files into plain texts
	[ElementTree module is used to parse the xmls]
    2. Add POS tag for each word
	a. tokenize the texts
	b. add POS tags to tokens
	[nltk.tag.api submodule is applied]
	c. modify the basedata: add POS as an attribute to <word> elements
	[using ElementTree again]

Notes:
    Some files contain non ascii characters. They are sorted out: bug_files.zip	
"""

import os
import re
import nltk
from xml.etree import ElementTree as ET

if not os.path.exists('./POSxml'):
    os.mkdir('./POSxml')

filetype=r'(.*)_words\.xml$'

for root,dirs,files in os.walk('./words_en/'):
    for file in files:
	match=re.search(filetype,file)
	if match: #filter out the .dtd  
#	    print file

            tokens=[]
            tree = ET.parse('./words_en/'+file)
            root = tree.getroot()
#	    print root[:10]	
            for i in range(0,len(root)):
		tokens.append(root[i].text)
            pos_set=nltk.pos_tag(tokens) 
#	    print pos_set[:10]


	    for i in range(0,len(root)):
	        word=root[i].text.encode('utf-8')
                token=pos_set[i][0].encode('utf-8')
                pos=pos_set[i][1]
                if word==token:
                    root[i].set('POS', pos)
		    print root[i].attrib
                else: # make sure that POS is added to the right word...
                    print file
            tree.write('./POSxml/'+'POS_'+file)
            print file,'done!'  

	else:
	    pass	 
