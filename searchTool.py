import sys
import pandas as pd
import numpy as np


#---- Input control: make sure the modal typed in is in the data ----#
def check_key(InPut):
        while True:
                
                if InPut in keys:
                        print InPut,' is a valid key'
                        return InPut
                        break
                
                else:
                        print keys,'\n'
                        sys.stdout.flush
                        print "Choose from the list above:\n"
                        sys.stdout.flush
                        InPut=raw_input().lower()               

#---- Input control: make sure the modality type entered are in the data ----#
def check_value(InPut):
        while True:
                
                if InPut in values:
                        print InPut,' is a valid type'
                        return InPut
                        break
                else:
                        print values,'\n'
                        sys.stdout.flush
                        print "Choose from the list above:\n"
                        sys.stdout.flush
                        InPut=raw_input().lower()

#=============================

#	Major Tasks

#=============================

#---- Given two assigned categories, return the modals that are assigned the two values ----#
def search_pair(type1,type2):
        print 'we are testing search pair'
        #### function under construction ####
	pan1=df[df.category1.isin([type1]) & df.category2.isin([type2])]
	pan2=df[df.category2.isin([type1]) & df.category1.isin([type2])]	
	Slice=pan1.append(pan2)
        lemmas=Slice.lemma.tolist()
        sentences=Slice.sentence.tolist()
        results=zip(lemmas,sentences)
	return results

#---- Given a modal and two types, return the instances where the modal are assigned the two values ----#
def search_triple(modal,type1,type2):
        
        item_slice=df[df.lemma==modal]

        pan1=item_slice[df.category1.isin([type1]) & df.category2.isin([type2])]
        pan2=item_slice[df.category2.isin([type1]) & df.category1.isin([type2])]
        results=pan1.append(pan2).sentence.tolist()

        return results

#---- Given a modal, return all annotation instances of that modal----# 
def search_modal(modal):
        
	item_slice=df[df.lemma==modal]
	examples=item_slice.sentence.tolist()
	anno1=item_slice.category1.tolist()
	anno2=item_slice.category2.tolist()
	results=zip(examples,anno1,anno2)

	return results


#============================================#

#     	 The Search Engine

#============================================#
def SEARCH():
        while True:
		#---- Select A Task Type ----#
                SearchType=raw_input('A: Search instances of a given modal.\nB: Search modals of certain type.\nC: Search instances of a modal with certain modality type.\n')

	
		#---- Search Annotation Instances of the Input Modal ----#
                if SearchType=='A' or SearchType=='a':
                
			#---- taking input ----#
		        print 'Choose a modal:'
                        sys.stdout.flush
                        InPut_modal=raw_input().lower()
                        check_key(InPut_modal)

               		#---- search ----#        
                        result=search_modal(InPut_modal)
			print len(result), ' instances in total.'
				
			N = len(result)
			onset=0
			offset=10
			#---- Output control: print results 10 lines at a time ----#  	
			while offset < N:
				for triple in result[onset:offset]:
					print triple[1],triple[2],triple[0],'\n'
					sys.stdout.flush
	
				r=raw_input('See more? Press Enter. Done? Enter Q')
				if r == 'q' or r=='Q':
					break
				else:
					pass
				onset = offset
				offset= offset+10
			for triple in result[onset:]:
				print triple[1],triple[2],triple[0],'\n'
	 
			break  #use "break" to jump out of the while loop                                


		#---- Search Modals That Are Assigned Given Types ----#
                elif SearchType=='B' or SearchType=='b':

                	#---- taking input ----#
                        print 'Choose a modality type:'
                        sys.stdout.flush        
                        InPut_type1=raw_input().lower()
                        check_value(InPut_type1)
        
                        print 'Choose the second modality type:'
                        sys.stdout.flush        
                        InPut_type2=raw_input().lower()
                        check_value(InPut_type2)


			#---- search ----#                       
                        result = search_pair(InPut_type1,InPut_type2)
                        print len(result), ' instances in total.' 
			lemmas_only=[pair[0] for pair in result]

                        N = len(result)
                        onset=0
                        offset=10

                        #---- Output control: print results 10 lines at a time ----#
                        while offset < N:
                        	for pair in result[onset:offset]:
                                        print pair[0],pair[1],'\n'
                                        sys.stdout.flush
                                        
				r=raw_input('See more? Press enter.\n\nDone? Enter Q.')
                                sys.stdout.flush
                                        
                              	if r == 'q' or r=='Q':
                               		break
				else:
					pass

                                onset=offset
                                offset= offset+10

			# there are 10 or less instances, the while loop will be skipped; 
			# also the results are not covered by the loop will be printed here 
#                        for pair in result[onset:]:
#                                print pair[0],pair[1],'\n'
#			r2=raw_input('See the list of modals only? Enter L')
#			if r2=='l' or r2=='L':
#				print lemmas_only
#			else:
#				pass
                        break


		#---- For Given Modal, Search for Instances Where It Is Assigned the Specified Two Types ----#
                elif SearchType=='C' or SearchType=='c':

                	#---- takeing input ----#
                        print 'Choose a modal:'
                        sys.stdout.flush
                        InPut_modal=raw_input().lower()
                        check_key(InPut_modal)

                        print 'Choose a modality type:'
                        sys.stdout.flush        
                        InPut_type1=raw_input().lower()
                        type1=check_value(InPut_type1)
                        if type1=='':
                                print 'WARNING: first type is not specified'
			else:
				pass
        
                        print 'Choose the second modality type:'
                        sys.stdout.flush        
                        InPut_type2=raw_input().lower()
                        check_value(InPut_type2)

                	#---- search ----#
                        result=search_triple(InPut_modal,InPut_type1,InPut_type2)
                        print len(result)
                        
			#---- output control ----#
                        for i, s in enumerate(result):
                                print i,s,'\n'
                        break

		
		#---- Error  ----#
                else:
                        print 'ERROR: invalid task'
                        sys.stdout.flush
                        SearchType==raw_input('Select A, B or C')
       
        
        
#===========================================================
#	Main			
#===========================================================
        
if __name__=='__main__':

        #----Initialize data------
        df=pd.read_pickle('forSearch.dat')
        keys=df.lemma.tolist()
        cats=list(set(df.category1.tolist()+df.category2.tolist()))
        values=[value.lower() for value in cats]

        #----First round------
        print 'What do you want to do?'
        SEARCH()

        #----Go again-----
        while True:
       		goagain = raw_input("Search again? (enter \"Y\" or \"y\" to continue and \"q\" or \"Q\" to quit)")
                if goagain == "Y" or goagain=="y":
                        # ---- Get values again
                        SEARCH() 
                elif goagain == "Q" or goagain=="q":
                        print "Bye!"
                        #---- End program
                        break
                else:
                        print"ERROR: invalid input. "
                        sys.stdout.flush
                        goagain==raw_input('Enter Y to continue or Q to quit')
        
