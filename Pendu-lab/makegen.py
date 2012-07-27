"""
makegen.py --


makefile generator


Date of creation: 2007-27-02


Copyright  Robotics and Automation Group, Pontificia Universidad Javeriana - Cali.

	Freddy Naranjo Perez, fnaranjo@puj.edu.co
	Antonio Alejandro Matta Gomez amatta@puj.edu.co
	Julian David Colorado, jdcolorado@puj.edu.co
	Juan Camilo Acosta Mejia, jcacosta@puj.edu.co

See the file "license.terms" for information on usage and redistribution of this file, and for a
DISCLAIMER OF ALL WARRANTIES

"""
def makegen(system,odesolver,dynmodel,motor,controller,swingup,ctrlnum):
	"""
	exemple
	makegen('cartpole','improvedeuler','cartpole','motor2','lqr_inte_motor2','swing_up_motor2',2)
	"""
	os='lin'
	f=open('makefile','w+t')
	lines=['']
	
	lines.append('OBJS= ')
	lines.append(odesolver)
	lines.append('.o ')
	lines.append(dynmodel)
	lines.append('.o ')

	if(ctrlnum==1 or ctrlnum==2):
		lines.append(controller)
		lines.append('.o ')
	if(ctrlnum==2):
		lines.append(swingup)
		lines.append('.o ')
	if(motor!=''):
		lines.append(motor)
		lines.append('.o ')
	lines.append('odefunc.o\n')
	
	#precompilation routines
	lines.append('\nmotor=-Ddcmotor\nnomotor=-Dnodcmotor')
	if(ctrlnum==0):
		lines.append('\nzero_controllers=-Dzero_controllers\n')
	if(ctrlnum==1):
		lines.append('\none_controllers=-Done_controllers\n')
	if(ctrlnum==2):
		lines.append('\ntwo_controllers=-Dtwo_controllers\n')
	
	if(os=='win'):
		lines.append('\nclwin: dyncorec.o $(OBJS)\n')
		lines.append('	g++ -c  dynlib_wrap.cpp -IE:/Python24/include -IMeschach/\n')
		lines.append('	g++ -shared dyncorec.o $(OBJS) dynlib_wrap.o  Meschach/meschach.a -lm -Le:/python24/libs/ -lpython24 -o _dynlib.dll\n')
	else:
		lines.append('\ncllnx: dyncorec.o $(OBJS)\n')
		lines.append('	g++ -o dyncorec dyncorec.o $(OBJS) newmat/libnewmat.a -lm\n')

	lines.append('clean:\n')
	lines.append('	rm $(OBJS)\n\n')
	
	#Ode function
	lines.append('#Ode function\n')
	lines.append('odefunc.o: dynlib.h ./odefunc.cpp\n')
	
	if(ctrlnum==0):
		if(motor==''):
			lines.append('	g++ -c ./odefunc.cpp $(zero_controllers) $(nomotor)\n')
		else:
			lines.append('	g++ -c ./odefunc.cpp $(zero_controllers) $(motor)\n')
	elif(ctrlnum==1):
		if(motor==''):
			lines.append('	g++ -c ./odefunc.cpp  $(one_controllers) $(nomotor)\n')
		else:
			lines.append('	g++ -c ./odefunc.cpp  $(one_controllers) $(motor)\n')
	else:
		if(motor==''):
			lines.append('	g++ -c ./odefunc.cpp  $(two_controllers) $(nomotor)\n')
		else:
			lines.append('	g++ -c ./odefunc.cpp  $(two_controllers) $(motor)\n')
		
	#Dyncore
	lines.append('#Dyncore\n')
	lines.append('dyncorec.o: dynlib.h dyncorec.cpp\n')
	lines.append('	g++ -c dyncorec.cpp \n')
	
	#Dc motors lib.
	if(motor!=''):
		lines.append('#Dc motors lib.\n')
		lines.append(motor)
		lines.append('.o: dynlib.h ./dynmodels/dcmotors/')
		lines.append(motor)
		lines.append('.cpp\n')
		lines.append('	g++ -c ./dynmodels/dcmotors/')
		lines.append(motor)
		lines.append('.cpp \n')

	#Ode solvers
	lines.append('#Ode solvers.\n')
	lines.append(odesolver)
	lines.append('.o: dynlib.h ./odesolvers/')
	lines.append(odesolver)
	lines.append('.cpp\n')
	lines.append('	g++ -c ./odesolvers/')
	lines.append(odesolver)
	lines.append('.cpp \n')
	
	#Dynmodels
	lines.append('#Dynmodels.\n')
	lines.append(dynmodel)
	lines.append('.o: dynlib.h ./dynmodels/')
	lines.append(system)
	lines.append('/')
	lines.append(dynmodel)
	lines.append('.cpp\n')
	lines.append('	g++ -c ./dynmodels/')
	lines.append(system)
	lines.append('/')
	lines.append(dynmodel)
	lines.append('.cpp \n')

	if(ctrlnum==2):
		#swing up
		lines.append('#swingup.\n')
		lines.append(swingup)
		lines.append('.o: dynlib.h ./controlaws/')
		lines.append(system)
		lines.append('/')
		lines.append(swingup)
		lines.append('.cpp\n')
		lines.append('	g++ -c ./controlaws/')
		lines.append(system)
		lines.append('/')
		lines.append(swingup)
		lines.append('.cpp \n')
	if(ctrlnum>0):
		#controller
		lines.append('#controller.\n')
		lines.append(controller)
		lines.append('.o: dynlib.h ./controlaws/')
		lines.append(system)
		lines.append('/')
		lines.append(controller)
		lines.append('.cpp\n')
		lines.append('	g++ -c ./controlaws/')
		lines.append(system)
		lines.append('/')
		lines.append(controller)
		lines.append('.cpp \n')

	f.writelines(lines)
	f.close()
