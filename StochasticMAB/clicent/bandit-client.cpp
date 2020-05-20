// thompson sampling for Multi armed bandit variance based
#include <iostream>
#include <algorithm>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#define MAXHOSTNAME 256
#include <vector>
#include <cmath>
#include <chrono>
#include <random>
using namespace std;

void options(){

  cout << "Usage:\n";
  cout << "bandit-agent\n"; 
  cout << "\t[--numArms numArms]\n";
  cout << "\t[--randomSeed randomSeed]\n";
  cout << "\t[--horizon horizon]\n";
  cout << "\t[--hostname hostname]\n";
  cout << "\t[--port port]\n";
}


/*
  Read command line arguments, and set the ones that are passed (the others remain default.)
*/
bool setRunParameters(int argc, char *argv[], int &numArms, int &randomSeed, unsigned long int &horizon, string &hostname, int &port){

  int ctr = 1;
  while(ctr < argc){

    //cout << string(argv[ctr]) << "\n";

    if(string(argv[ctr]) == "--help"){
      return false;//This should print options and exit.
    }
    else if(string(argv[ctr]) == "--numArms"){
      if(ctr == (argc - 1)){
	return false;
      }
      numArms = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--randomSeed"){
      if(ctr == (argc - 1)){
	return false;
      }
      randomSeed = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--horizon"){
      if(ctr == (argc - 1)){
	return false;
      }
      horizon = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--hostname"){
      if(ctr == (argc - 1)){
	return false;
      }
      hostname = string(argv[ctr + 1]);
      ctr++;
    }
    else if(string(argv[ctr]) == "--port"){
      if(ctr == (argc - 1)){
	return false;
      }
      port = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else{
      return false;
    }

    ctr++;
  }

  return true;
}



int main(int argc, char *argv[]){

  // Run Parameter defaults.
  int numArms = 5;
  int randomSeed = time(0);
  unsigned long int horizon = 1000;
  string hostname = "localhost";

  int port = 5000;

  //Set from command line, if any.
  if(!(setRunParameters(argc, argv, numArms, randomSeed, horizon, hostname, port))){
    //Error parsing command line.
    options();
    return 1;
  }

  struct sockaddr_in remoteSocketInfo;
  struct hostent *hPtr;
  int socketHandle;
  bzero(&remoteSocketInfo, sizeof(sockaddr_in));
  
  if((hPtr = gethostbyname((char*)(hostname.c_str()))) == NULL){
    cerr << "System DNS name resolution not configured properly." << "\n";
    cerr << "Error number: " << ECONNREFUSED << "\n";
    exit(EXIT_FAILURE);
  }

  if((socketHandle = socket(AF_INET, SOCK_STREAM, 0)) < 0){
    close(socketHandle);
    exit(EXIT_FAILURE);
  }

  memcpy((char *)&remoteSocketInfo.sin_addr, hPtr->h_addr, hPtr->h_length);
  remoteSocketInfo.sin_family = AF_INET;
  remoteSocketInfo.sin_port = htons((u_short)port);

  if(connect(socketHandle, (struct sockaddr *)&remoteSocketInfo, sizeof(sockaddr_in)) < 0){
    close(socketHandle);
    exit(EXIT_FAILURE);
  }

  char sendBuf[256];
  char recvBuf[256];

  
  std::vector<double> alpha(numArms);
  std::vector<double> beta(numArms); //define two arrays alpha and beta for every arm  
 // std::vector<double> prmtr(numArms); // a parameter propotioal to variance
// initialize for all the arms before pulling them
  for(int i=0;i<numArms;++i){
      alpha[i] =1.0;
      beta[i] =1.0;
	 // prmtr[i] =1.0;
  }
  int armToPull =rand()%(numArms + 1);
  std::cout<<"Initial Pull"<<armToPull<<"\n";
  sprintf(sendBuf, "%d", armToPull);
  std::cout << "Sending action" << armToPull << ".\n";
  double HrznCnt =1;
  double prmtr=5;// input value is critical, need to learn off line 
  double Epsilon =5; // input value is critical need to learn off line
  while(send(socketHandle, sendBuf, strlen(sendBuf)+1, MSG_NOSIGNAL) >= 0){
	float reward = 0;
	HrznCnt = HrznCnt+1;
    recv(socketHandle, recvBuf, 256, 0);
    sscanf(recvBuf, "%f", &reward);
    cout << "Received reward " << reward << ".\n";
   // select the next best possible arm using beta distribution 
    std::vector<double> theta(numArms,0.0);// define and initialize theta 
    if(reward==1){
      alpha[armToPull]+=1;
    }else{
      beta[armToPull] +=1;
    }

    double x1 =1;
    double y1 =1;
    for(int i=0;i<numArms;++i){
	 //  unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
	  // std::default_random_engine generator; 
	   unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
	   std::default_random_engine generator (seed);
       std::gamma_distribution<double> distribution (alpha[i]/prmtr, 1.0);
       x1 =distribution(generator);

       std::gamma_distribution<double> distributionb (beta[i]/prmtr, 1.0);
       y1 =distributionb(generator); 
	  
	   std::cout<<"values of x and y are "<<x1<<" and "<<y1<<std::endl;
       theta[i] = x1/(x1+y1);
    }
	for(int i=0;i<numArms;++i)
	{
		std::cout<<"theta["<<i<<"]="<<theta[i]<<"\n";
	}
    double max_value =0;
	int max_num =0;
	for(int i=0; i<numArms;++i){
		if(theta[i]>=max_value){
			max_num =i;
			max_value =theta[i];
		}
	}
	armToPull = max_num;
    // update parameter 
	prmtr = Epsilon*(log (HrznCnt)/HrznCnt);
	if(prmtr<=.1)
		prmtr =.1;
    std::cout<<"prmtr..................."<<prmtr<<"\n";
    sprintf(sendBuf, "%d", armToPull);
    cout << "Sending action " << armToPull << ".\n";    
  }
 
  close(socketHandle);
  cout << "Terminating.\n";
  }
