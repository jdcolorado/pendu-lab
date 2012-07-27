"""
putmatrix.py --


Dynamic core.

Date of creation: 2007-03-14


Copyright  Robotics and Automation Group, Pontificia Universidad Javeriana - Cali.

	Freddy Naranjo Perez, fnaranjo@puj.edu.co
	Antonio Alejandro Matta Gomez amatta@puj.edu.co
	Julian David Colorado, jdcolorado@puj.edu.co
	Juan Camilo Acosta Mejia, jcacosta@puj.edu.co

See the file "license.terms" for information on usage and redistribution of this file, and for a
DISCLAIMER OF ALL WARRANTIES

"""

from numpy import *

def putmatrix(A,file):
	"""
	Saves numpy A matrix in file with meschach style
	"""
	n=len(A)
	m=size(A)/n
	f=open(file,'wb+')
	
	lines=[]
	#lines[0]="Matrix: %d by %d\n" %(n,m)
	for i in range(n):
		for j in range(m):
			lines.append(str(A[i,j])+'\n')
			
	f.writelines(lines)
	f.close()
	