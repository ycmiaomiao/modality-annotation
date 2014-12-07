import pandas as pd
import numpy as np
import cPickle
from bs4 import BeautifulSoup as bs
import os
from os.path import join
import re
import nltk

"""
The goal is to create a dataframe that stores the following information:
for each annotated modal:
          its span and the id of the file that contains it, 
          the annotators who (is supposed to) annotated this item,
          modal type by each annotator,
          the context in which it appears (current sentence, previous sentence, and following sentence)
"""


if __name__=="__main__":
          
          author = [] # the annotator
          Prefix = [] # the unique prefix shared by the base data and annotated data of the same file
          m_id = [] # the id of markable in a file
          span = [] # span of the annotated modal
          primaryKey = [] # unique key for each markable; composed with Prefix and m_id
          modalType = [] # the value of modality type selected by the annotator
          lemma = [] # the lemma of the annotated markable

	  # ---- collecting information for each result file ---- 
          for root, dirs,files in os.walk(data):
                    for f in files:
                              fullname=join(root,f)
                              #--- check file name, only look at the files end with "_modal_level.xml"
                              suffix=r'(.*)_modal_level\.xml$'
                              checkSuffix = re.match(suffix,fullname)
                              if checkSuffix:
                                        
                                        #------Now call the BeautifulSoup to parse the xmls ------#
                                        Soup = bs(open(fullname),'xml')
                                        for markable in Soup.find_all('markable'):
                                                  Prefix.append(os.path.basename(checkSuffix.group(1)))
                                                  #group(0) returns the whole matched pattern; group(1) returns the pattern in the first ()
                                                  author.append(Soup.markables['Author'])
                                                  span.append(Soup.markable['span'])
                                                  lemma.append(Soup.markable['lemma'])
                                                  m_id.append(Soup.markable['id'])
                                                  modalType.append(Soup.markable['modality_type'])
                                                  primaryKey.append(os.path.basename(checkSuffix.group(1))+Soup.markable['id'])

          # -------Now that information is collected, put the arrays together into a dataframe------------
          dataFrame = pd.DataFrame({'author':author,
                                    'file':Prefix,
                                    'm_id':m_id,
                                    'primaryKey':primaryKey,
                                    'modal_span':span,
                                    'lemma':lemma,
                                    'modality_type':modalType
                                    }          

          print (dataFrame.head())
          #--------Pickle the dataframe ---------#
          saveDf = open('annoResult.dat','w')
          cPickle.dump(dataFrame,saveDf)
          saveDataframe.close()
