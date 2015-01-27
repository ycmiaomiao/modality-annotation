from __future__ import division
import pandas as pd
import numpy as np
import nltk
from nltk.metrics.agreement import AnnotationTask
from nltk.metrics import ConfusionMatrix
"""
Library of the functions used for exploring the annotation results
"""

#=======
# collapsing categories for experimental purposes
#=======
def dichotomy(df): #collapse categories into priority vs. non-priority
        cats=df.modality_type.tolist()
        coarse_cat=[]

        nonpri=['epistemic','ability_circumstantial','circumstantial','ability','epistemic_circumstantial']

        pri=['deontic','teleological','buletic','buletic_teleological','priority']
        for type in cats:
                if type in pri:
                        coarse_cat.append('Priority')
                elif type in nonpri:
                        coarse_cat.append('nonPriority')
                else:
                        coarse_cat.append('null')
        print len(cats),len(coarse_cat)
        df['coarse_type']=coarse_cat
        df=df[df.coarse_type!='null']
        print 'length of df without nulls',len(df)
        return df 


def two_dimensions(df): #convert original categories into types in the two-dimensional frame
          cats=df.modality_type.tolist()        
          coarse_cat=[]
          
          subjective=['epistemic']
          objective=['ability_circumstantial','circumstantial','ability']
          neutral=['epistemic_circumstantial']
          deontic=['deontic']
          goal=['teleological','buletic','buletic_teleological']
          vague=['priority']
          for type in cats:
                    if type in subjective:
                              coarse_cat.append('subjective')
                    elif type in objective:
                              coarse_cat.append('objective')
                    elif type in neutral:
                              coarse_cat.append('neutral')
                    elif type in deontic:
                              coarse_cat.append('deontic')
                    elif type in goal:
                              coarse_cat.append('goal')
                    elif type in vague:
                              coarse_cat.append('vague')
                    else:
                              coarse_cat.append('null')
                    
          print len(coarse_cat),len(cats)
          df['coarse_type']=coarse_cat
          return df



#========
# make annotation tasks that feed the agreement measurements provided by nltk.metrics.agreement
#========
def makeAT_all(df):

        panel=df[['author','primaryKey','modality_type']]
        panel_tuple = [tuple(x) for x in panel.values]	
	t_all=AnnotationTask(panel_tuple)
	return t_all

def makeAT_coarse(df):
        
        feature=options.get("features")
        panel=df[['author','primaryKey','modality_type']]
        panel_tuple = [tuple(x) for x in panel.values]	
	t_coarse=AnnotationTask(panel_tuple)
	return t_coarse



#==========
# make cofusion matrix for a subset of annotation results
#==========

def make_CM(df,item,**options):
        # argument df should contain double annotations for each item; item should be a list
        # creates a confusion matrix with nltk.metrics.ConfusionMatrix  


        item_slice=df[df.lemma.isin(item)]
                
        split_slice=split_by_author(item_slice)
        
        panel1=split_slice[0]
        panel2=split_slice[1]
        

        ref=[]
        test=[]
        if options.get("coarse")==0:
                ref=panel1.modality_type.tolist()
                test=panel2.modality_type.tolist()

        elif options.get("coarse")==1:

                ref=panel1.coarse_type.tolist()
                test=panel2.coarse_type.tolist()
                
        elif options.get("cat_type")=='non_priority':
                ref=panel1["non_priority_dimension"].tolist()
                test=panel2["non_priority_dimension"].tolist() 

        elif options.get("cat_type")=='priority':
                ref=panel1["priority_dimension"].tolist()
                test=panel2["priority_dimension"].tolist()
                
                
        cm=ConfusionMatrix(ref,test)
        
        return cm


#==========
# compare results before and after collapsing
#==========

def compare_FineCoarse(df,items):
        """
        make sure the first arguement contains both 'modaltiy_type' and 'coarse_type'; make sure the second argument 'items' is a list
        note that when items is a list of multiple items, what returned are aggregated results rather than itemwise results

        """
        item_slice=df[df.lemma.isin(items)]
        #  compare agreement measures
        at_all = makeAT_all(item_slice)
        at_coarse = makeAT_coarse(item_slice)
        
        #  compare confusion matrix
        cm_all = make_CM(item_slice,items,coarse = 0)
        cm_coarse = make_CM(item_slice,items,coarse = 1)

        return at_all, at_coarse, cm_all, cm_coarse


#=========
# distribution of categories by item
#=========

"""
creates item-by-category matrix like below:
          cat1        cat2        cat3
item1       1          2          5
item2       10         8          0  


"""


def itemByCat(df,lemmaSet,cats):

          table=pd.DataFrame()
          table['lemma']=lemmaSet
          i=0
          while i < len(cats):
                    name=cats[i]
                    cat = []
                    for l in lemmaSet:
                              l_s=df[df.lemma==l]
                              
                              l_cat=len(l_s[l_s.modality_type==name]) 
                              cat.append(l_cat)
                              
                    table[name]=cat 
                    i+=1
                    
          return table
                    

#===========
# get double annotated portion
#===========
def double_anno_only(df):
        gg=df.groupby('primaryKey').groups
        dai=[key for key in gg if len(gg[key])==2]
        double=df[df.primaryKey.isin(dai)]
        return double



#==========
# split the whole datat frame into two panels by different authros 
#==========
def split_by_author(df):
        df = df.sort(['primaryKey','author'])

        n=len(df)
        even=range(0,n,2)
        odd=range(1,n,2)

        panel1=df.iloc[even]
        panel2=df.iloc[odd]

        return panel1,panel2


#=======================
# utilities
#=======================

def slice_by_pos(df,pos):
        lemma_set = list(set(df.lemma.tolist()))
        lemma_tags = nltk.pos_tag(lemma_set)
        lemma_by_pos = [pair[0] for pair in lemma_tags if pair[1]==pos]
        slice_by_pos = df[df.lemma.isin(lemma_by_pos)]
        return slice_by_pos

def pos_prob(df,pos):
        """ Returns the frequency and probability of given pos in the whole data."""

        total = len(df)

        selected_df=slice_by_pos(df,pos)
        pos_count = len(selected_df)
        pos_prob = pos_count/total

        return pos_prob

def freq_dist(df,feature):
        import matplotlib.pyplot as plt
        df_grouped = df.groupby(feature).groups
        counts = [len(df_grouped[key]) for key in df_grouped].sort()
        plt.hist(counts,bins=15,histtype='step',color='black')
        plt.xlabel(feature+' frequency')
        plt.ylabel('number of '+feature+'s')
        plt.show()

        



















