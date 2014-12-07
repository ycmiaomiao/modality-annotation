#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
By Yanyan; last modified 12/03/2014

This program provides context information for the basic information extracted from the annotation results
It adds three columns to the dataframe containing basic annotation information
The three context columns are: previous_sentence, current_sentence (the sentence in which the modal is used), and the next_sentence

The main algorithm is as follows:
iterrate over all rows in the dateframe,for each row
	use the prefix to locate the corresponding basedata file;
	use the markable_span information to locate the position of the markable in the basedata [the index of the markable in basedata= beginning of the span-1]
	
	use ElementTree to parse the basedata files and convert them into lists
	in the basedata list, find the indices of sentence ending characters
	use the beginning of the markable span as an anchor to find two sentence boundaries preceding and following the anchor point
	[the lists of indices are transformed into trigram lists for this task]
	[previous sentence span=(p, p, A),current sentence span=(p A p), the next sentence span = (A, p, p), A is the anchor point, p's are the indices of sentence ending punctuations] 
	lastly, use the spans to select tokens from the basedata list, and join them into strings 	  

special packages and method used: 
- ElementTree (parse xmls, get tokens)
- ngrams [from nltk.util; turn a list into list of triples]
- enumerate (enumerate the index-token pairs in a list)

"""

import pandas as pd
import numpy as np
import cPickle
from bs4 import BeautifulSoup as bs
import os
from os.path import join
import re
from xml.etree import ElementTree as ET
import nltk
from nltk.util import ngrams

if __name__=="__main__":
        
        dfraw = pd.read_pickle('annoResult.dat')

        # ----- drop duplicated rows ------
        df=dfraw.drop_duplicates()
        print len(df)

        path=('./postprocessed/words_en/')
        basefile=path+df['file']+'_words.xml'
	df['basefile']=basefile
	spanStart=[]
	for span in df['modal_span']:
		spanStart.append(span.split('..')[0]) 
	df['spanStart']=spanStart
#        print df.head()


	preSen=[]
	curSen=[]
	nextSen=[]

        for row in df.iterrows():
                baseData=row[1]['basefile']

                # --- get all tokens in the basefile ---
                tokenList=[]
                tree = ET.parse(baseData)
                treeRoot = tree.getroot()
                tokenList=[treeRoot[i].text for i in range(0,len(treeRoot))]

                # --- locate the markable ---
                stripSpan=re.search(r'word_(\d*$)',row[1]['spanStart']).group(1)
                modal_index=int(stripSpan)-1
#                print (modal_index,tokenList[modal_index])

                # --- locate the sentence boundaries
                senBounds=['\n','.','?','!','...']
                boundPoints=[i for i, token in enumerate(tokenList) if token in senBounds or i==modal_index]
                
                
                # --- pick out the sentence spans
                boundTri=ngrams(boundPoints,3)
                contexts=[trigram for trigram in boundTri if modal_index in trigram]

                preSenSpan=()
                currentSenSpan=()
                postSenSpan=()

                if len(contexts)==3:
                        preSenSpan=(contexts[0][0],contexts[0][1])
                        currenSenSpan=(contexts[1][0],contexts[1][2])
                        postSenSpan=(contexts[2][1],contexts[2][2])

                if len(contexts)==1:
                        currentSenSpan=(contexts[0][0],contexts[0][2])

                else:
                        if contexts[0][1]==modal_index:
                                        currentSenSpan=(contexts[0][0],contexts[0][2])
                                        postSenSpan=(contexts[1][1],contexts[1][2])

                        else:
                                preSenSpan=(contexts[0][0],contexts[0][1])
                                currentSenSpan=(contexts[1][0],contexts[1][2])

#		print (contexts, preSenSpan, currentSenSpan, postSenSpan)
   
		# --- convert span to sentence
		pre_sen_list=[]
		pre_sen_str=""
		if len(preSenSpan)==2:
			pre_sen_list = [token for i, token in enumerate(tokenList) if i in range(preSenSpan[0]+1,preSenSpan[1])] 
		else: 
			pass
		pre_sen_str = ' '.join(pre_sen_list)
		preSen.append(pre_sen_str)

		cur_sen_list=[]
		cur_sen_str=""
		cur_sen_list = [token for i, token in enumerate(tokenList) if i in range(currentSenSpan[0]+1, currentSenSpan[1])]
		cur_sen_str=' '.join(cur_sen_list)	
		curSen.append(cur_sen_str)

		next_sen_list=[]
		next_sen_str=""
		if len(postSenSpan)==2:
			next_sen_list = [token for i, token in enumerate(tokenList) if i in range(postSenSpan[0]+1,postSenSpan[1])] 
		else:
			pass
		next_sen_str = ' '.join(next_sen_list)
		nextSen.append(next_sen_str)

	# --- add the new arrays in the dataframe

	df['previous_sentence']=preSen
	df['curren_sentence']=curSen
	df['next_sentence']=nextSen

	print df.head()


#----- pickle the updated dataframe
saveDf=open('annoResult_contexts.dat','w')
cPickle.dump(df,saveDf)
saveDf.close()
