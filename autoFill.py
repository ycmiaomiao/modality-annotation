#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
some items have single annotation. this program fillup the missing annotation to make sure every item is "double" annotated.
          
"""
import os.path
from os.path import join
import pandas as pd
import numpy as np
import cPickle
import nltk
from nltk.metrics.agreement import AnnotationTask as AT
import re


def addAnno(df,SingleAnnoItems):
        
	priKeys={'primaryKey':SingleAnnoItems}	        
   	row_mask=df.isin(priKeys).any(1)
	df_filtered=df[row_mask] # slice out the items with single annotation; 
#        print len(df_filtered)

	appended=pd.DataFrame() #create an empty dataframe to hold the auto filled rows

	for row in df_filtered.iterrows(): # iterate the single annotated rows, copy the row, only change the 'author' and 'modality_type'
                
        	newRow=row[1].copy()
                Item=row[1]['primaryKey']
                Coder=row[1]['author']
                prefix=row[1]['file']
                filename=prefix+'_modal_level.xml'
                
                for root,dirs,files in os.walk('./postprocessed'):
                        for file in files:
                                if file==filename:
                                        fullname=join(root,file)
                coderPair=r'_(\w)*-(\w)*_'
                matchCoders=re.search(coderPair,fullname).group(0).split('-')
                Coder1=re.sub('_','',matchCoders[0])
                Coder2=re.sub('_','',matchCoders[1])

                # ----- give the auto generated row a coder name and a default modality type
                if Coder==Coder1:
                        newRow['author']=Coder2
                                        
                elif Coder==Coder2:
                        newRow['author']=Coder1                            

                newRow['modality_type']='DEFAULT'

                appended=appended.append(newRow)

	return appended


if __name__ == "__main__":
          print ('beginning of new program')

          # --- read in the dataframe ---
          df = pd.read_pickle('annoResult_contexts.dat')
          print df.head(),len(df)
                    

          # Step1: group dataframe according to primaryKey (annotated items)
          groupedDf=df.groupby('primaryKey').groups
          SingleAnnoItems=[key for key in groupedDf if len(groupedDf[key])==1]

          # Step2: auto fill the missiing annotations
          appended=addAnno(df,SingleAnnoItems)       

          df=df.append(appended)

          # Save data
          saveDf=open('annoResult_normalized.dat','w')
          cPickle.dump(df,saveDf)
          saveDf.close()

          # testing the results 
          gg=df.groupby('primaryKey').groups
          sai=[key for key in gg if len(gg[key])==1]
          print sai

          print 'done!'
