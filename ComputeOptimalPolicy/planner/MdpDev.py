import numpy as np
import csv
import sys
import os
sys.setrecursionlimit(10000)
#######################################################################################################
#Initalization
#Read MDP file for retrieving the information
f =open("InputMdp.txt","r") # open/create a file
finput =open("OutputPi.txt","w+")
StateNmbr =int(f.readline())
#print StateNmbr, "State" # number of states
ActionNmbr =int(f.readline())
#print ActionNmbr, "Action" # number of actions
lines = f.readlines()
f.close()
RewardDist = np.zeros((2*ActionNmbr*StateNmbr,StateNmbr),dtype ='float')
#ScalarInfo = np.zeros((1,3), dtype ='float')
i =0
for line in lines:
    parts = line.split() # split line into parts
    #print parts
    if len(parts) > 1:
        for j in range(len(parts)):
            RewardDist[i,j] = parts[j]
        i =i+1
    elif len(parts)==1:
        DiscFact =float(parts[0]) 
#print DiscFact, "Discount factor"   
Value = np.zeros(StateNmbr) # initiialize Value vector
Pi =np.zeros(StateNmbr) # initalize initial policy for all states ... action 0 is assign to everyone 
#Delta =4 # initalize delta, a stopping criteria
#Theta = .04 # small value to stop teh while loop
##########################################################################################################
# Policy Evaluation 
def PolicyEvaluation(Pi, Value):
	Delta =4 
	Theta =.0000000004
	while (Delta >=Theta):
		Delta =0
		for s in range(StateNmbr):
			TempValue = Value[s]
			CurrentR =0
			for s1 in range(StateNmbr):	
				TempReward= RewardDist[(s*ActionNmbr+ Pi[s]),s1]
			#	print TempReward, "TempReward"
				x = DiscFact*Value[s1]
			#	print x, "value of x"
				TempDist= RewardDist[(StateNmbr*ActionNmbr+s*ActionNmbr+Pi[s]),s1]
			#	print TempDist, "Distribution"
				CurrentR = CurrentR + (TempReward + DiscFact*Value[s1])*TempDist
			Value[s] =CurrentR
		#	print Value[s], "value of s"
			Delta = max(Delta, abs(TempValue - Value[s]))

##########################################################################################################
# Policy improvement
	PolicyStable =1
	PiCheck =np.zeros(StateNmbr)
	PiArg =np.zeros(ActionNmbr)
	for s in range(StateNmbr):
		TempAction =Pi[s]
		#Pi(s) =0
		for a1 in range(ActionNmbr):
			PiCheck[s] =0
			for s1 in range(StateNmbr):
				TempReward =RewardDist[(s*ActionNmbr + a1),s1]
				TempDist= RewardDist[(StateNmbr*ActionNmbr+s*ActionNmbr+a1),s1]
				PiCheck[s] = PiCheck[s] + (TempReward + DiscFact*Value[s1])*TempDist	
			PiArg[a1] =PiCheck[s]
	
#		print PiArg, "Array for ArgMax"
		Pi[s] =np.argmax(PiArg)
		if TempAction!=Pi[s]:
			PolicyStable = 0
	if PolicyStable ==1:
	#	print "U r lucky!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                for i in range(StateNmbr):

                    finput.write(str(Value[i])+'\t')
                    finput.write(str(int(Pi[i]))+'\n')
                
        else: 
		PolicyEvaluation(Pi, Value)	

############################################################################################################
# input the inital argument
PolicyEvaluation(Pi, Value)
