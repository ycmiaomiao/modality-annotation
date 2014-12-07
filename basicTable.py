import pandas as pd
import numpy as np
import cPickle
from bs4 import BeautifulSoup as bs
import os
from os.path import join
import re
import nltk

"""
1. The goal is to create a table that stores the following information:
for each annotated modal:
          its span and the id of the file that contains it, 
          the annotators who (is supposed to) annotated this item,
          modal type by each annotator,
          the context in which it appears (current sentence, previous sentence, and following sentence)
The span, annotator and modal type can be directly read from the post-processed xml files;
What is tricky is that some modals are not double annotated, and there will be a missing entry in the xmls
[we need to collect the basic information, and do some "normalizations" afterwards]

For the contexts,we need to locate the corresponding basedata file,
and use the span of the modal as an anchor to find the preceeding and following sentence boundaries
[This can be done simultaneously with the basic task]

------
Problems:
1. It seems like there are redundant data in the basic table. Some 
How to solve? Use pandas.DataFrame.drop_duplicates() #only unique rows are dropped in a new data frame. Pickle that out

2. Some modals are only single annotated. We need to give them a second value: NONE
How to do that?
a. for primaryKey, if there is only one entry, duplicate it.
          How to? for key in df['primaryKey']:key
b. then subsitute the modal type as NONE,
and the Author as AUTO

OK, does it matter? why do we need to normalize the data?
------
go ahead and get the next step done!
------
Next step is to extract the contexts in which the markable is used. current, previous and following sentence 
we will need a column called currentSentence, leftSentence, and rightSentence. the last two could be empty


"""


if __name__=="__main__":
          
          author = [] # the annotator
          Prefix = [] # the unique prefix shared by the base data and annotated data of the same file
          m_id = [] # the id of markable in a file
          span = [] # span of the annotated modal
          primaryKey = [] # unique key for each markable; composed with Prefix and m_id
          modalType = [] # the value of modality type selected by the annotator
          lemma = [] # the lemma of the annotated markable

          # loop through the files to collect information as listed above
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
#          saveDf = open('annoResult.dat','w')
#          cPickle.dump(dataFrame,saveDf)
#          saveDataframe.close()
