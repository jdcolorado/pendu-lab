#include <iostream>
#include <fstream>
#include <string>
#include <math.h>


#include "newmat/newmatap.h"
#include "newmat/newmatio.h"




/*
dynlib.h
Controlab.
Copyright  Robotics and Automation Group, Pontificia Universidad Javeriana - Cali.

	Freddy Naranjo Perez, fnaranjo@puj.edu.co
	Antonio Alejandro Matta Gomez amatta@puj.edu.co
	Julian David Colorado, jdcolorado@puj.edu.co
	Juan Camilo Acosta Mejia, jcacosta@puj.edu.co


See the file "license.terms" for information on usage and redistribution of this file, and for a
DISCLAIMER OF ALL WARRANTIES.
*/


/*
odesolver

Ordinary differential equations solver with 4 order runge kutta or euler, or eulerimproved

Date of creation: 2007-02-03


INPUT
MAT SimParam: Simulation Parameters 4 x 6
MAT X: State matrix 4 x pt
int i: Actual point
double u: Control action

OUTPUT

MAT X: i+1 position modified.
*/
void odesolver(Matrix &SimParam,Matrix &X,int i,Matrix &u);
/*
DYNMODEL

Cart pole system Model

Date of creation: 2007-02-03

INPUT
MAT SimParam: Simulation Parameters 4 x 6
VEC X: State vector 4
double TAU: Torque input

OUTPUT

VEC out: State modified.

*/

void dynmodel(Matrix &SimParam,Matrix &X,int i,double Tau,ColumnVector &out);

/*

linear quadratic regulator

Date of creation: 2007-02-05

*/

void controller(Matrix &SimParam,Matrix &Xm,int i,int ui,double *Tau,ColumnVector &dX);
/*

Swing up controller

Date of creation: 2007-02-05

*/
void swing_up(Matrix &SimParam,Matrix &Xm,int i,int ui,double *Tau,ColumnVector &dX);

/*
dcmotors.c

DC motors library

Date of creation: 2007-02-14

*/
double dcmotors(Matrix &SimParam,double u,Matrix &X,int i);


/*
odefunc.c --

Ordinary Differential equation function, complete state variables constructor


Date of creation: 2007-02-22
*/

void odefunc(Matrix &SimParam,Matrix &X,int i,Matrix &u,int ui,ColumnVector &out);
