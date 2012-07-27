
/*
dyncore.cpp


Dynamic core.


Date of creation: 2007-04-19


Copyright  Robotics and Automation Group, Pontificia Universidad Javeriana - Cali.

	Freddy Naranjo Perez, fnaranjo@puj.edu.co
	Antonio Alejandro Matta Gomez amatta@puj.edu.co
	Julian David Colorado, jdcolorado@puj.edu.co
	Juan Camilo Acosta Mejia, jcacosta@puj.edu.co

See the file "license.terms" for information on usage and redistribution of this file, and for a
DISCLAIMER OF ALL WARRANTIES
*/

#include "dynlib.h"

//MAT *dyncorec(MAT *SimParam,MAT *X,MAT *u)
int main()
{
	/*
	Dynamic simulation core.
	SimOptions: 1x7 char matrix
	SimParam: 4x6 float matrix
	Dynsimdic: Dynamic simulation dictionary
	X: state variable matrix: 4Xpt,  [x,theta,dx,dtheta]
	time: time 1 x points matrix
	u: 1x points Dynamic model input matrix
	*/
	
	Matrix SimParam(4,6);
	
	int i,j,pt,k;
	char linea[13];
	FILE *fp,*f1;
	
	//SimParam input
	fp = fopen("simparam.txt","r+");
	
	fseek (fp,0,SEEK_SET );
	for(i=1;i<=4;i++)
	{
		for(j=1;j<=6;j++)
		{
			fscanf(fp,"%s",&linea);
			SimParam(i,j)=atof(linea);
		}
	}
	fclose(fp);
	
	pt=int(SimParam(3,2)/SimParam(3,3))+1;
	k=int(SimParam(4,4)+SimParam(4,3));
	
	Matrix X(k,pt), u(1,pt);
	
	//input matrix
	f1 = fopen("Xini.txt","r+");
	
	//fseek (fp,0,SEEK_SET );
	for(i=1;i<=(SimParam(4,4)+SimParam(4,3));i++)
	{
		fscanf(f1,"%s",&linea);
		X(i,1)=atof(linea);
		
	}
	fclose(f1);
	
	/*if ( (fp = fopen("u.txt","r+")) == NULL )
		error(E_EOF,"my_function");
	m_finput(fp,u);
	fclose(fp);*/
	
	//Dynamic loop
	for(i=1;i<=pt-1;i++)
	{
		odesolver(SimParam,X,i,u);
	}	
	ofstream f2;
	f2.open ("X.txt");
	f2 << X;
	f2.close();
	
	f2.open ("u.txt");
	f2 << u;
	f2.close();
	
	return 0;
}
