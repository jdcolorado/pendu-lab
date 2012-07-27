/*
odefunc.c --

Ordinary Differential equation function, complete state variables constructor


Date of creation: 2007-02-22


Copyright  Robotics and Automation Group, Pontificia Universidad Javeriana - Cali.

	Freddy Naranjo Perez, fnaranjo@puj.edu.co
	Antonio Alejandro Matta Gomez amatta@puj.edu.co
	Julian David Colorado, jdcolorado@puj.edu.co
	Juan Camilo Acosta Mejia, jcacosta@puj.edu.co

See the file "license.terms" for information on usage and redistribution of this file, and for a
DISCLAIMER OF ALL WARRANTIES
*/
#include "./dynlib.h"
void odefunc(Matrix &SimParam,Matrix &X,int i,Matrix &u,int ui,ColumnVector &out)
{
	/*
	SimOptions: 1x7 char matrix
	SimParam: 4x6 float matrix
	Dynsimdic: Dynamic simulation dictionary
	X: state variable matrix: 4Xpt,  [x,theta,dx,dtheta]
	time: time 1 x points matrix
	u: 1x points Dynamic model input matrix
	*/

	//system=SimOptions->me[1][1];
	//tini=SimParam->me[3][1];				//tini
	//tfinal=SimParam->me[3][1];  			//tfinal
	//step=SimParam->me[3][3]; 				//model step time
	//controlstep=SimParam->me[3][4]; 		//control step time
	//controllerrange=SimParam->me[4][1];	//range
	//suOrder=SimParam->me[4][2];			//swing up order
	//coOrder=SimParam->me[4][3];			//controler order
	//pt=(int)(tfinal/step);
	//rel=controlstep/step;
	double Tau;
	int j;
	
	//Dyn model with motor precompilation routines
#ifdef dcmotor
	dynmodel(SimParam,X,i,dcmotors(SimParam,u(1,ui),X,i),out);
#endif

	
	//Dyn model with no motor precompilation routines
#ifdef nodcmotor
	dynmodel(SimParam,X,i,u(1,ui),out);
#endif
	
	//fixed numeric resolution
	if(out(3)<0.00001 && out(3)>-0.00001)
		out(3)=0.0;
	if(out(4)<0.00001 && out(4)>-0.00001)
		out(4)=0.0;
	

#ifdef zero_controllers
	u(1,ui+1)=0;
#endif

#ifdef one_controllers
	if((ui%(int)(SimParam(3,4)/SimParam(3,3)))==0)
	{
		controller(SimParam,X,i,ui,&Tau,out);
		for(j=int(SimParam(4,4)+1);j<=int(SimParam(4,2)+SimParam(4,4));j++)
			out(j)=0;
		if(sizeof(X)>(SimParam(4,2)+SimParam(4,3)+SimParam(4,4)))
		{
			u(1,ui+1)=Tau;
		}
	}
	else
	{
		u(1,ui+1)=0;
	}
#endif

#ifdef two_controllers
	if((ui%(int)(SimParam(3,4)/SimParam(3,3)))==0)
	{
		//Swing up control
		if(cos(X(2,i))<cos(SimParam(4,1)))
		{
			swing_up(SimParam,X,i,ui,&Tau,out);
			for(j=int(SimParam(4,4)+1);j<=int(SimParam(4,3)+SimParam(4,4));j++)
				out(j)=0;		
		}
		//lqr control
			else
		{
				controller(SimParam,X,i,ui,&Tau,out);
			for(j=int(SimParam(4,4)+1);j<=int(SimParam(4,2)+SimParam(4,4));j++)
				out(j)=0;
				
		}
		if(sizeof(X)>(SimParam(4,2)+SimParam(4,3)+SimParam(4,4)))
		{
			u(1,ui+1)=Tau;
		}
	}
	else
	{
		u(1,ui+1)=0;
	}
#endif




}
