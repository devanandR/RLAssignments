import numpy as np
import csv
import math
import sys
import copy
import random
sys.setrecursionlimit(10000)
#########################################################
#Initalization
#Read MDP file for retrieving the information
f =open("InputTraject.txt","r") # open/create a file
#foutput =open("OutputValue.txt","w+") # no output required
StateNmbr =int(f.readline())
#print StateNmbr, "State" # number of states
ActionNmbr =int(f.readline()) # number of actions
#print ActionNmbr, "Actions"
DiscFact =float(f.readline()) # Discount Factor
#print DiscFact, "Discount Factor" 
lines = f.readlines()
f.close()
rmsecntr =0
#Experiment =1000
OptValue = np.zeros(StateNmbr)
'''f1 = open("v2.txt","r")
lines1=f1.readlines()
for i in xrange(len(lines1)):
    line1=lines1[i] # uncommend if want to use actual output.....
    parts1=line1.split()
    OptValue[i] =float(parts1[0])
print OptValue,"TempValue"
#exit(0)#'''
CheckErr =100
DoEstimate =1
#while(CheckErr>=0.69):# uncomment for the learnig of lambda
while(DoEstimate > 0):
    DoEstimate =0
    Value = np.zeros(StateNmbr)# initialize value vector
    TempValue = np.zeros(StateNmbr) 
    #s =0 # intialize state
    alpha = .00001
    Lambda = .789839386318
    #Lambda =1
    #for line in lines:
    Delta =2
    Delta1 =np.zeros(StateNmbr)
    #Theta =.004
#    Iteration =100
    count =0
    #rmsecntr =0
    #Experiment=10
#while(rmsecntr<=Experiment):
#    Lambda = random.random()
#    alpha =random.random()
    while (Delta>=.000002):
        TempValue = copy.deepcopy(Value)   
        #TempValue = Value[:]
        ElgblTrce =np.zeros(StateNmbr) # inittialize Eligibility Trace 
        f =open("InputTraject.txt","r")
        #f =open("d2.txt","r")
        f.readline()
        f.readline()
        line =f.readline()
        #print line,"reqd line..........................."
        lines = f.readlines()
        # print lines,"read line kam kar rha h ...........?" 
        for i in xrange(len(lines)):
            line=lines[i]
            parts = line.split() # split line into parts
            # parts= lines[i]
            # print lines[i+1]
            #print parts
            if len(parts) > 1:
                state =int(parts[0])# state s
                # print state
                action =int(parts[1])# action a given by unknown policy pi for state s
                reward =float(parts[2])# reward genewrated by taking action a on s  
            elif len(parts)==1:
                Laststate =int(parts[0])
                break
            nextline= lines[i+1]
            nextpart = nextline.split()
            nextstate =int(nextpart[0])# next state s' by taking action a on state s
            TdError = reward + DiscFact*Value[nextstate] -Value[state] # evaluate TD error 
            ElgblTrce[state] = ElgblTrce[state]+1 # increment Eligibility Trace
            for j in range(StateNmbr):
                #Value[j] =Value[j]+ (1.0/(i+1))*TdError*ElgblTrce[j]
                Value[j] =Value[j]+ alpha*TdError*ElgblTrce[j]

           #     print TempValue, "TempValue"
              #  print Value, "Value........................"
        #       break
                ElgblTrce[j] = (math.pow(DiscFact,Lambda))*ElgblTrce[j]
               # ElgblTrce[j] = 1*ElgblTrce[j] # no change in case of t-d zero case
    #           print Value,"**value"
       #    break

#        print Value,"Value"
        for j in range(StateNmbr):
            Delta1[j] = abs(Value[j] -TempValue[j])
        Delta =  max(Delta1)
  #      print Delta,"Delta Value"
        count =count +1
        f.close()
   #     print count, "Counter............................................................................................................"
    #    print Value, "Value................................................................................................................."
     #   print TempValue, "Tempvalue................................................................................................................"
    rmsecntr = rmsecntr +1
#    print rmse(Value, OptValue)
   # for i in range(StateNmbr):
   #     CheckErr =CheckErr + abs(Value[i]-OptValue[i])
    CheckErr =np.sqrt(np.mean((Value-OptValue)**2))
    #print Value, "Value"
   # print OptValue,"Opt Value"
   # print Value, "Value"
   # print alpha,"alpha value"
   # print Lambda,"Lambda value"
   # print CheckErr, "CheckError"
for i in range(StateNmbr):
    print Value[i]

