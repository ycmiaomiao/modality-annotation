#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
This program reads in the annotation results in .html format, and stores the data in a Pandas dataframe 

"""


import pandas as pd
import numpy as np
import cPickle
from bs4 import BeautifulSoup as bs
import os
from os.path import join
import re
import nltk
import codecs
          
author = [] # the annotator
Prefix = [] # the unique prefix shared by the base data and annotated data of the same file
span = [] # span of the annotated modal
primaryKey = [] # unique key for each markable; composed with Prefix and m_id

#-------nonPri & Pri are the two modal values under two-dimensional model---------#

nonPri = [] # the value of non-priority dimension selected by the annotator
Pri=[] # the value of priority dimension selected by the annotator

#-------modality_type is the modal value under single dimensional model---------#

#modality_type=[] # the value of modality type selected by the annotator



lemma = [] # the lemma of the annotated markable
          # loop through the files to collect information as listed above
pos = []


suffix=r'(.*)_modal_level\.xml$'

for root, dirs,files in os.walk('./postprocessed/sample'):
          for f in files:
                    fullname = join(root,f)
          
          #--- check file name, only look at the files end with "_modal_level.xml"
                    checkSuffix = re.match(suffix,fullname)
                    if checkSuffix:
                                        
          #------Now call the BeautifulSoup to parse the xmls ------#
                              Soup = bs(codecs.open(fullname),'xml')
                              for markable in Soup.find_all('markable'):
                                        author.append(Soup.markables['Author'])
                                        Prefix.append(os.path.basename(checkSuffix.group(1)))
                                        #group(0) returns the whole matched pattern; group(1) returns the pattern in the first ()
                                        span.append(markable['span'])
                                        lemma.append(markable['lemma'])

#                                        modality_type.append(markable['modality_type'])

                                        Pri.append(markable['priority_dimension'])
                                        nonPri.append(markable['non_priority_dimension'])

                                        
                                        primaryKey.append(os.path.basename(checkSuffix.group(1))+markable['span'])
                                        
                                        
                    else:
                              pass

dataFrame = pd.DataFrame({'author':author,
                                    'file':Prefix,
                                    'primaryKey':primaryKey,
                                    'modal_span':span,
                                    'lemma':lemma,
                                    'priority_dimension':Pri,
                                    'non_priority_dimension':nonPri
                              })
print len(dataFrame)

saveData = codecs.open('basicData.dat','w','utf8')
cPickle.dump(dataFrame,saveData)
saveData.close()
