"""
Traductor lib

Date of creation: 2007-04-12


Copyright  Robotics and Automation Group, Pontificia Universidad Javeriana - Cali.

	Freddy Naranjo Perez, fnaranjo@puj.edu.co
	Antonio Alejandro Matta Gomez amatta@puj.edu.co
	Julian David Colorado, jdcolorado@puj.edu.co
	Juan Camilo Acosta Mejia, jcacosta@puj.edu.co

See the file "license.terms" for information on usage and redistribution of this file, and for a
DISCLAIMER OF ALL WARRANTIES

"""


from numpy import *

def chain_arrange(temp):
	temp=temp[0].split('\n')
	temp=''.join(temp)
	temp=temp.split(" ")
	return temp

def eq_trad(lines,system,motor):
	"""
	Funcion para cambiar solo las ecuaciones.
	"""
	new=[]
	
	for i in range(size(lines)):
		line=lines[i]
		
		temp=line.split('dot')
		if(line!=temp[0]):
			line='dotproduct'.join(temp)
		
	
		line=U_Equivalence(line,'U')
		if (system=='cartpole'):
			line=Simparam_Equivalence(line,1,1,'M1')
			line=Simparam_Equivalence(line,1,2,'M2')
			line=Simparam_Equivalence(line,1,3,'L')
			line=Simparam_Equivalence(line,1,4,'g')
			line=Simparam_Equivalence(line,1,5,'VF')
			line=Simparam_Equivalence(line,1,6,'PF')
			
			line=Simparam_Equivalence(line,3,1,'TI')
			line=Simparam_Equivalence(line,3,2,'TF')
			line=Simparam_Equivalence(line,3,3,'CSTEP')
			line=Simparam_Equivalence(line,3,4,'STEP')
			
			line=Simparam_Equivalence(line,4,1,'RG')
			line=Simparam_Equivalence(line,4,2,'SO')
			line=Simparam_Equivalence(line,4,3,'CO')
			line=Simparam_Equivalence(line,4,4,'DO')
		
		if (system=='furuta'):
			line=Simparam_Equivalence(line,1,1,'m')
			line=Simparam_Equivalence(line,1,2,'r')
			line=Simparam_Equivalence(line,1,3,'L')
			line=Simparam_Equivalence(line,1,4,'I')
			line=Simparam_Equivalence(line,3,5,'g')
			line=Simparam_Equivalence(line,1,5,'bs')
			
			line=Simparam_Equivalence(line,3,1,'TI')
			line=Simparam_Equivalence(line,3,2,'TF')
			line=Simparam_Equivalence(line,3,3,'CSTEP')
			line=Simparam_Equivalence(line,3,4,'STEP')
			
			line=Simparam_Equivalence(line,4,1,'RG')
			line=Simparam_Equivalence(line,4,2,'SO')
			line=Simparam_Equivalence(line,4,3,'CO')
			line=Simparam_Equivalence(line,4,4,'DO')
			
		if (system=='pendubot' or system=='acrobot'):
			line=Simparam_Equivalence(line,1,1,'M1')
			line=Simparam_Equivalence(line,1,2,'M2')
			line=Simparam_Equivalence(line,1,3,'L1')
			line=Simparam_Equivalence(line,1,4,'L2')
			line=Simparam_Equivalence(line,3,5,'g')
			line=Simparam_Equivalence(line,1,5,'I1')
			line=Simparam_Equivalence(line,1,6,'I2')
			
			line=Simparam_Equivalence(line,3,1,'TI')
			line=Simparam_Equivalence(line,3,2,'TF')
			line=Simparam_Equivalence(line,3,3,'CSTEP')
			line=Simparam_Equivalence(line,3,4,'STEP')
			
			line=Simparam_Equivalence(line,4,1,'RG')
			line=Simparam_Equivalence(line,4,2,'SO')
			line=Simparam_Equivalence(line,4,3,'CO')
			line=Simparam_Equivalence(line,4,4,'DO')
		
		if (system=='inertiawheel'):
			line=Simparam_Equivalence(line,1,1,'M1')
			line=Simparam_Equivalence(line,1,2,'M2')
			line=Simparam_Equivalence(line,1,3,'L1')
			line=Simparam_Equivalence(line,3,5,'g')
			line=Simparam_Equivalence(line,1,5,'I1')
			line=Simparam_Equivalence(line,1,6,'I2')
			
			line=Simparam_Equivalence(line,3,1,'TI')
			line=Simparam_Equivalence(line,3,2,'TF')
			line=Simparam_Equivalence(line,3,3,'CSTEP')
			line=Simparam_Equivalence(line,3,4,'STEP')
			
			line=Simparam_Equivalence(line,4,1,'RG')
			line=Simparam_Equivalence(line,4,2,'SO')
			line=Simparam_Equivalence(line,4,3,'CO')
			line=Simparam_Equivalence(line,4,4,'DO')
				

		if(len(line.split('\n')[0])!=0):
			new.append('	')
			new.append(line.split('\n')[0])
			temp=line.split('=')
			if(len(temp)==2):
				a=temp[0][len(temp[0])-1]
				b=temp[1][0]
				if(a!='=' and a!='<' and a!='>' and a!='!'):
					if(b!='='):
						new.append(';\n')
					else:
						new.append('\n')
				else:
					new.append('\n')
			else:
				new.append('\n')
					
	new=''.join(new)
	return new

def Simparam_Equivalence(line,i,j,char):
	""" This function search line for a variable name and replaces it with Simparam position.."""
	
	temp=line.split(char)
	if(line!=temp[0]):
		for k in range(len(temp)-1):
			if(len(temp[0+k])!=0):
				a=temp[0+k][len(temp[0+k])-1]
			else:
				a='+'
			b=temp[1+k][0]
			
			if(a=='+' or a=='(' or a==')' or a=='[' or a==']' or a=='-' or a=='=' or a=='' or a==' ' or a=='*' or a=='/' or a==','):
				if(b=='+' or b=='(' or b==')' or b=='[' or b==']' or b=='-' or b=='=' or b=='' or b=='*' or b=='/' or b==',' or b=='\n'):
					temp[0+k]=temp[0+k]+('SimParam('+str(i)+','+str(j)+')')
				else:
					temp[0+k]=temp[0+k]+char
			else:
				temp[0+k]=temp[0+k]+char
			
	return ''.join(temp)

def U_Equivalence(line,char):
	"""This function searches for U and changes for *U"""
	
	temp=line.split(char)
	if(line!=temp[0]):
		for k in range(len(temp)-1):
			if(len(temp[0+k])!=0):
				a=temp[0+k][len(temp[0+k])-1]
			else:
				a='+'
			b=temp[1+k][0]
			
			if(a=='+' or a=='(' or a==')' or a=='[' or a==']' or a=='-' or a=='=' or a=='' or a==' ' or a=='*' or a=='/' or a==','):
				if(b=='+' or b=='(' or b==')' or b=='[' or b==']' or b=='-' or b=='=' or b=='' or b=='*' or b=='/' or b==',' or b=='\n'):
					temp[0+k]='*'+char+temp[0+k]
				else:
					temp[0+k]=temp[0+k]+char
			else:
				temp[0+k]=temp[0+k]+char
			
	return ''.join(temp)

def eqtrad_main(file, controller,system,motor):
	"""
	Funcion principal del traductor de ecuaciones de lenguaje usuario -> cpp (Newmath)
	"""
	f=open(file,'r+')
	lines=f.readlines()
	f.close()
	for i in range(size(lines)):
		if lines[i]=='#MATRIX DECLARATION\n':
			m=i
		if lines[i]=='#COLUMN VECTOR DECLARATION\n':
			cv=i
		if lines[i]=='#ROW VECTOR DECLARATION\n':
			rv=i
		if lines[i]=='#DOUBLE VARIABLE DECLARATION\n':
			dv=i
		if lines[i]=='#INT VARIABLE DECLARATION\n':
			di=i
		if lines[i]=='#PROGRAM\n':
			pgr=i

			

	new=[]
	#Prototipo:
	new.append('/*\nGenerated c++ prg')
	new.append('\n\nCopyright  Robotics and Automation Group, Pontificia Universidad Javeriana - Cali.')
	new.append('\n\n     Freddy Naranjo Perez, fnaranjo@puj.edu.co')                                                           
	new.append('\n     Antonio Alejandro Matta Gomez amatta@puj.edu.co')
	new.append('\n     Julian David Colorado, jdcolorado@puj.edu.co')                        
	new.append('\n     Juan Camilo Acosta Mejia, jcacosta@puj.edu.co')
	new.append('\n\n     See the file "license.terms" for information on usage and redistribution of this file, and for a    ')
	new.append('\n     DISCLAIMER OF ALL WARRANTIES\n*/\n\n')
	new.append('#include "../../dynlib.h"\n\n')
	if(controller==1):
		new.append('void controller(Matrix &SimParam,Matrix &Xm,int i,int ui,double *U,ColumnVector &dX)\n{\n')
	else:
		new.append('void swing_up(Matrix &SimParam,Matrix &Xm,int i,int ui,double *U,ColumnVector &dX)\n{\n')
	
	
	
	#Solucion de declaracion de variables
	
	#matrices
	
	temp=chain_arrange(lines[m+1:cv])
	m_declar=['	'+'//Declaracion de matrices\n']
	if (temp!=['']):
		m_declar.append('	'+'Matrix ')
			
		for i in range(size(temp)):
			m_declar.append(temp[i])
			if(i!=size(temp)-1):
				m_declar.append(', ')
		m_declar.append(';\n\n')
	m_declar=''.join(m_declar)
	

	#vectores fila
	temp=chain_arrange(lines[cv+1:rv])	
	rv_declar=['	'+'//Declaracion de vectores Columna\n']
	rv_declar.append('	'+'ColumnVector ')
	rv_declar.append('X(fin)')
	if (temp!=['']):
		rv_declar.append(', ')
		for i in range(size(temp)):
			rv_declar.append(temp[i])
			if(i!=size(temp)-1):
				rv_declar.append(', ')
	rv_declar.append(';\n\n')
	rv_declar=''.join(rv_declar)
	#vectores columna
	temp=chain_arrange(lines[rv+1:dv])
	cv_declar=['	'+'//Declaracion de vectores Fila\n']
	if (temp!=['']):
		cv_declar.append('	'+'RowVector ')
		for i in range(size(temp)):
			cv_declar.append(temp[i])
			if(i!=size(temp)-1):
				cv_declar.append(', ')
		cv_declar.append(';\n\n')
	cv_declar=''.join(cv_declar)

	
	#Double variables
	temp=lines[dv+1:di]
	temp=''.join(temp)
	temp=temp.split('\n')
	temp=''.join(temp)
	temp=temp.split(' ')
	dv_declar=['	'+'//Declaracion de variables de tipo DOUBLE\n']
	if (temp!=['']):
		temp=filter(None,temp)
		dv_declar.append('	'+'double ')
		for i in range(size(temp)):
			dv_declar.append(temp[i])
			if(i!=(size(temp)-1)):
				dv_declar.append(', ')
		dv_declar.append(';\n\n')
	dv_declar=''.join(dv_declar)

	#Int variables
	temp=lines[di+1:pgr]
	temp=''.join(temp)
	temp=temp.split('\n')
	temp=''.join(temp)
	temp=temp.split(' ')

	iv_declar=['	'+'//Declaracion de variables de tipo INT\n']
	iv_declar.append('	'+'int ')
	iv_declar.append('fin')
	iv_declar.append(', j')
	if (temp!=['']):
		iv_declar.append(', ')
		temp=filter(None,temp)
		for i in range(size(temp)):
			iv_declar.append(temp[i])
			if(i!=(size(temp)-1)):
				iv_declar.append(', ')
	
	iv_declar.append(';\n\n')
	iv_declar=''.join(iv_declar)
	
	new.append(dv_declar)
	new.append(iv_declar)
	new.append('	fin=(int)(SimParam(4,4)+SimParam(4,3));\n')
	new.append(m_declar)
	new.append(rv_declar)
	new.append(cv_declar)
	new.append('\n	for (j=1;j++;j<=fin){\n	X(j)=Xm(j,i);}\n\n')
	
	#llamado a funciona principal, para convertir las ecuaciones
	
	temp=eq_trad(lines[pgr+1:],system,motor)
	new.append(temp)
	new.append('\n}\n')
	
	file2=file.split('.')[0]+'.cpp'
	f2=open(file2,'w+')
	f2.writelines(new)
	f2.close()
