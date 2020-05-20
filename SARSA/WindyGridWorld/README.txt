The simulator is GUI based. It is very simple to input different data. 
Following are the steps to run the code and obtain the plots:

1) The folder DevWindyGrid should be the pwd

2) Hit the command on terminal ./windygrid.sh 

3) A window (WindyGrid) will get display with many input options. For example, to fill the input given in Example 6.5: Windy Gridworld, 
	* Input wind intensity, plz give a space btw them 
		 for example, 0 0 0 1 1 1 2 2 1 0
	* Row and Column, plz give the space btw them    	
 		 for example, 7 10
	* epsilon, gamma and alpha, plz give the space btw them 
		 for example, .1 1 .1
	* Input 0 for stndrd moves or 1 for king's moves
		 for example, 0
	* Input 1 if wind is stochastic, else 0 # Note that in this case we are considering king's move show above option should be 			enable
		for example, 0
	* Input Start(s1,s2) & Goal(g1,g2). Format : s1 s2 g1 g2
		 for example 3 0 3 7       # Note that coordinate system has (0,0) as origin. So (3 0) points to 4th row and 1 column    	
4) After input the oprtions (correctly. Otherwise, it will show an error). Press a blue button "Submit". 

5) After that a new window with the same name will appear. In this window, one can well analyze the best possible path (episode) that the running experiment could get after long run. 

6) Two plots, one shows the convergence of the episode length and other, number of episodes along the time axis, get saved (automatically) in the current running directory.      
