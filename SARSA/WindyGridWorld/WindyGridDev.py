from Tkinter import *
import numpy as np
import random as rndm
import matplotlib.pyplot as plt
class MainWindow():

    def __init__(self, master):
        self.master = master
        self.master.title('WindyGrid')
        self.v = StringVar()
        self.w =StringVar()
        self.x =StringVar()
        self.t =StringVar()
        self.L1 = Label(self.master, text = 'Input Wind Intensity, plz give the space btw entries')
        self.L1.pack(side = TOP)
        self.E1 = Entry(self.master, textvariable = self.v, bd = 5)
        self.E1.pack(side = TOP)
        self.L2 = Label(self.master, text = 'Row and Column, Plz give the space  btw them')
        self.L2.pack(side = TOP)
        self.E2 = Entry(self.master, textvariable = self.w, bd = 5)
        self.E2.pack(side = TOP)
        self.L3 = Label(self.master, text = 'epsilon, gamma and alpha, plz give the space btwn them')
        self.L3.pack(side = TOP)
        self.E3 = Entry(self.master, textvariable = self.x, bd = 5)
        self.E3.pack(side = TOP)
        self.L4 = Label(self.master, text = 'Input 0 for Stndrd moves or 1 for King`s Move')
        self.L4.pack(side = TOP)       
        self.E4 = Entry(self.master, textvariable = self.t, bd = 5)
        self.E4.pack(side = TOP)
        self.z = StringVar()
        self.L6 =Label(self.master, text ='Input 1 if wind is stochastic, else 0')
        self.L6.pack(side=TOP)
        self.E6 = Entry(self.master, textvariable =self.z, bd=5)
        self.E6.pack(side =TOP)
        self.y = StringVar()
        self.L5 = Label(self.master, text = 'Input Start(s1,s2) & Goal(g1,g2). Format: s1 s2 g1 g2')
        self.L5.pack(side = TOP)
        self.E5 = Entry(self.master, textvariable = self.y, bd = 5)
        self.E5.pack(side = TOP)
        self.B1 = Button(self.master, text = 'Submit', command = self.userinput,bd =4, bg= 'blue')
        self.B1.pack(side = BOTTOM)
    #-----------------------------------

    def userinput(self):

        global external_variable1, external_variable2, external_variable3,external_variable4, external_variable5, external_variable6     
        external_variable1 = self.v.get()
        external_variable2 = self.w.get()
        external_variable3 = self.x.get()
        external_variable4 = self.t.get()
        external_variable5 = self.y.get()
        external_variable6 = self.z.get()
        MainWindow.WindyGrid(self) # Call WindyGrid function 

    def ActionStndrd(self,BstActn, Scurrent):

        if(BstActn==0):#.................................... Right
            Snew = min(Scurrent + 1, ((1+Scurrent/clmn)*clmn -1))
        if(BstActn==1):#.......................................Left 
            Snew = max(Scurrent - 1, (Scurrent/clmn)*clmn)
        if(BstActn==2):#.......................................Top
            if(Scurrent< clmn):
                Snew = Scurrent
            else:
                Snew= Scurrent - clmn
        if(BstActn==3):#.................................Bottom
            if(Scurrent >= clmn*(row-1)):
                Snew =Scurrent
            else:
                Snew= Scurrent +clmn
        return Snew


    def ActionKing(self,BstActn, Scurrent):

        if(BstActn==0):#.................................... Right
            Snew = min(Scurrent + 1, ((1+Scurrent/clmn)*clmn -1))
        if(BstActn==1):#.......................................Left 
            Snew = max(Scurrent - 1, (Scurrent/clmn)*clmn)
        if(BstActn==2):#.......................................Top
            if(Scurrent< clmn):
                Snew = Scurrent
            else:
                Snew= Scurrent - clmn
        if(BstActn==3):#.................................Bottom
            if(Scurrent >= clmn*(row-1)):
                Snew =Scurrent
            else:
                Snew= Scurrent +clmn
        if(BstActn==4):
            if(Scurrent<clmn or (Scurrent+1)%clmn ==0):
                Snew =Scurrent#----------- Do smthng Right-Top
            else:
                Snew =(Scurrent- clmn +1)

        if(BstActn==5):
            if(Scurrent>=clmn*(row-1) or (Scurrent+1)%clmn==0):
                Snew =Scurrent #---------------- Do smthng Right-Bottom
            else:
                Snew = Scurrent + clmn+1
        if(BstActn==6):
            if(Scurrent<clmn or Scurrent%clmn==0):
                Snew=Scurrent #......................... Do smthng Left-Top
            else:
                Snew =Scurrent -clmn-1

        if(BstActn==7):
            if(Scurrent>=clmn*(row-1) or Scurrent%clmn==0):
                Snew =Scurrent# Finally Left-Bottom
            else:
                Snew = Scurrent + clmn-1
        return Snew


    def PlotEpsds(self,CntngEpsds):

        plt.plot(CntngEpsds,'r')
        plt.xlabel('Time Steps')
        plt.ylabel('Episodes')
       # plt.show()
        plt.savefig("Episodes.png")
        plt.close()
        return
       
    def PlotRcrdEpsd(self,RcrdEpsds):
        
        PltRcrd =plt.plot(RcrdEpsds,'b')
        plt.xlabel('Episode number')
        plt.ylabel('length of the Episode')
        #plt.show()
        plt.savefig("Convergence.png")
        plt.close()
        return
#......................................... Min Algo Sarsa(0)...
    def Sarsa(self):

        if(MoveFlag==0):
            ActnQ =4
        else:
            ActnQ =8
        Qvalue = np.zeros((row*clmn,ActnQ)) # note that at max we have 4 action, say 0 1 2 3
        # Action 0:RIGHT, 1:LEFT, 2: TOP, 3:BOTTOM
        Tmax =1200 # Tmax name misleading, actually it max number of episodes I have kept it 1200 ti see the convergence
        Action= np.arange(ActnQ)
        State= np.arange(row*clmn)
        StrtState =State[S0*clmn+S1]
        GoalState =State[G0*clmn+G1]
        global RcrdEpsds
        RcrdEpsds= np.zeros(Tmax)
        NumEpsds =0
        global CntngEpsds
        CntngEpsds = []
        Jvalue =0
        CnvrgAray =[[] for _ in range(Tmax)]
        #.......................................................................
        for i in range(Tmax):
            Scurrent = StrtState
            PthLnth =0
        #......... Epsilon greedy based action selection
            TmpRnd = rndm.random()
            if(TmpRnd>Epsln):
                qaray = Qvalue[Scurrent,:]
                bst =[k for k, l in enumerate(qaray) if l == max(qaray)]
                BstActn = rndm.choice(bst)
            else:
                BstActn =rndm.randint(0,ActnQ-1)
            
            while(Scurrent!= GoalState):
            
                CnvrgAray[i].append(Scurrent)
                Jvalue=Jvalue+1
                if(MoveFlag==0):
                    Snew =MainWindow.ActionStndrd(self,BstActn,Scurrent)
                else:
                    Snew =MainWindow.ActionKing(self,BstActn,Scurrent)
           #......... Add Wind Effect...............
                if(Snew>=clmn):
                    IndxWnd = Scurrent%clmn
                    Snew = max(Snew%clmn, (Snew - clmn*int(wind[IndxWnd])))
          #.......If Stochasticity is enable.....
                if(Stcstcty==1):
                    TmpRnd =rndm.random()
        
                    if(TmpRnd>=float(1/3) and TmpRnd<float(2/3)):
                        Snew= MainWindow.ActionKing(self,2,Snew) # Do smthng keep Snew one above
                    if(TmpRnd>float(2/3)):
                        Snew= MainWindow.ActionKing(self,3,Snew) # Do smthng keep Snew one below
           #............End Wind Effect--------------------------  
                if(Snew !=GoalState):
                    reward = -1 # Obtain a reward -1, 
                else:
                    NumEpsds =NumEpsds+1
                    reward = 0 

                TmpRnd = rndm.random()
                if(TmpRnd>Epsln):
                    qaray1 = Qvalue[Snew,:]
                    bst1 =[k for k, l in enumerate(qaray1) if l == max(qaray1)]
                    NewBstActn = rndm.choice(bst1)
                else:
                    NewBstActn =rndm.randint(0,ActnQ-1)
              # Update Q value using TD control 
                if(Snew==GoalState):
                    Qvalue[Scurrent,BstActn] =Qvalue[Scurrent,BstActn] + Alpha*(reward-Qvalue[Scurrent,BstActn])
                else:
                    Qvalue[Scurrent,BstActn] =Qvalue[Scurrent,BstActn] + Alpha*(reward+gamma*Qvalue[Snew,NewBstActn]-Qvalue[Scurrent,BstActn])

                Scurrent =Snew
                BstActn =NewBstActn
                PthLnth=PthLnth+1

                if(Jvalue<15000):
                    CntngEpsds.append(NumEpsds)
            RcrdEpsds[i]= PthLnth
#......................................................................................................
        global MinLnth
        MinLnth =100000
        for i in range(Tmax-1):
            if(MinLnth>len(CnvrgAray[i])):
                MinLnth =len(CnvrgAray[i])
                MinIndx =i
        for i in range(MinLnth):    
            if(i>0):
                cntr1 =Label(canvas, text ='*', anchor='center',bg='white')
                canvas.create_window(30*(CnvrgAray[MinIndx][i]%clmn),30*(CnvrgAray[MinIndx][i]/clmn),width=30,height=30,window=cntr1,anchor='nw')

#........................................... Windy GridWorld gets Impleted here
    def WindyGrid(self):

        global wind
        wind = external_variable1.split()
        rowclm=external_variable2.split()
        global row, clmn, Epsln, S0,S1,G0,G1,MoveFlag, Alpha,gamma,Stcstcty
        row =int(rowclm[0])
        clmn =int(rowclm[1])
        self.L1.pack_forget()
        self.E1.pack_forget()
        self.L2.pack_forget()
        self.E2.pack_forget()
        self.L3.pack_forget()
        self.E3.pack_forget()
        self.L4.pack_forget()
        self.E4.pack_forget()
        self.L5.pack_forget()
        self.E5.pack_forget()
        self.L6.pack_forget()
        self.E6.pack_forget()
        self.B1.pack_forget()
        EpsAlpha =external_variable3.split()
        Epsln = float(EpsAlpha[0])
        gamma =float(EpsAlpha[1])
        Alpha =float(EpsAlpha[2])

        MoveFlag =int(external_variable4)
        Stcstcty= int(external_variable6)
        StrtGl = external_variable5.split()
        S0 =int(StrtGl[0])
        S1 =int(StrtGl[1])
        G0 =int(StrtGl[2])
        G1 =int(StrtGl[3])
        global canvas
        canvas = Canvas(width=500, height=500, bg='gray')
        canvas.pack(expand=YES, fill=BOTH)
   
                
        for i in range(clmn):
            for j in range(row):
                canvas.create_rectangle(i*30, 30*j+30, 30*i+30, 30*j, width=3, fill ='red')
        #.................................................................................
        for j in range(row):
            for i in range(clmn):
               # varcord.set(j*row+i)
                cntr =Label(canvas, text =i+clmn*j, anchor='center')
                canvas.create_window(30*i,30*j,width=30,height=30,window=cntr,anchor='nw')
        # Add start and Goal state
        t = Label(canvas, text="S", anchor='center',bg ='blue')
        canvas.create_window(S1*30, S0*30, width=30, height=30, window=t, anchor='nw')
        t1 = Label(canvas, text="G", anchor='center',bg='blue')
        canvas.create_window(30*G1,30*G0, width=30, height=30, window=t1,anchor='nw')
        # add wind srength 
        for i in range(clmn):
            wind1 = Label(canvas, text =int(wind[i]), anchor='center',fg ='red')
            canvas.create_window(30*i, row*30, width=30, height=30, window= wind1, anchor='nw')
        # Episode Length and path 
        EpsdShw =Label(canvas,text = " White path with `*` in the grid widow \n is the episode with min length",  anchor='center',bg='pink',fg='green')
        canvas.create_window(0, row*30 +60,width=30*clmn,height= 60, window=EpsdShw,anchor='nw')
        
        EpsdShw1 =Label(canvas,text = " Plz see plots for more analysis, Convergence.png \n and Episodes.png, saved in pwd",  anchor='center',bg='pink',fg='green')
        canvas.create_window(0, row*30 +122,width=30*clmn,height= 60, window=EpsdShw1,anchor='nw')


###########################################----------------------------------------------
      #  mainwindow =MainWindow(master)
        MainWindow.Sarsa(self)
        mainloop()
        MainWindow.PlotEpsds(self,CntngEpsds) # plot the result
        MainWindow.PlotRcrdEpsd(self,RcrdEpsds) 
#----------------------------------------------------------------------
external_variable1 = 0
external_variable2 = 0
external_variable3 = 0
external_variable4 = 0
external_variable5 = 0

master = Tk()
MainWindow(master)
master.mainloop()

