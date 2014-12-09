#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import cPickle
from bs4 import BeautifulSoup as bs
import os
from os.path import join
import re
import nltk


          
author = [] # the annotator
Prefix = [] # the unique prefix shared by the base data and annotated data of the same file
span = [] # span of the annotated modal
primaryKey = [] # unique key for each markable; composed with Prefix and m_id
modalType = [] # the value of modality type selected by the annotator
lemma = [] # the lemma of the annotated markable
          # loop through the files to collect information as listed above


suffix=r'(.*)_modal_level\.xml$'

for root, dirs,files in os.walk('./postprocessed'):
          for f in files:
                    fullname = join(root,f)
          
          #--- check file name, only look at the files end with "_modal_level.xml"
                    checkSuffix = re.match(suffix,fullname)
                    if checkSuffix:
                                        
          #------Now call the BeautifulSoup to parse the xmls ------#
                              Soup = bs(open(fullname),'xml')
                              for markable in Soup.find_all('markable'):
                                        author.append(Soup.markables['Author'])
                                        Prefix.append(os.path.basename(checkSuffix.group(1)))
                                        #group(0) returns the whole matched pattern; group(1) returns the pattern in the first ()
                                        span.append(markable['span'])
                                        lemma.append(markable['lemma'])
                                        modalType.append(markable['modality_type'])
                                        primaryKey.append(os.path.basename(checkSuffix.group(1))+markable['span'])
                    else:
                              pass
		
dataFrame = pd.DataFrame({'author':author,
                                    'file':Prefix,
                                    'primaryKey':primaryKey,
                                    'modal_span':span,
                                    'lemma':lemma,
                                    'modality_type':modalType})
print len(dataFrame)
          
saveData = open('annoResult.dat','w')
cPickle.dump(dataFrame,saveData)
saveData.close()
