#!/usr/bin/python

"""
Main.py --                                                                                            
																																																		
This file implements the main controlab widget.                                              
																																																			
Date of creation: 2006-11-01                                                                        
																																																
Copyright  Robotics and Automation Group, Pontificia Universidad Javeriana - Cali.                  
	Freddy Naranjo Perez, fnaranjo@puj.edu.co                                                                   
	Antonio Alejandro Matta Gomez amatta@puj.edu.co                                      
	Julian David Colorado, jdcolorado@puj.edu.co                           
	Juan Camilo Acosta Mejia, jcacosta@puj.edu.co                                    
																																																		
See the file "license.terms" for information on usage and redistribution of this file, and for a    
DISCLAIMER OF ALL WARRANTIES.                                                                       
																																																			
"""
import wx
import vtk
import os
from numpy import *
import thread
from vtk.wx.wxVTKRenderWindow import wxVTKRenderWindow
from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor
from graphengine import camera
from graphengine import world
from interface import interpreter
from interface import dynmode
from interface import plotwindow
from interface import symvalues

#dynmode window
from interface import sysparams
from interface import paramvaluestree
from interface import dynparamscroll

from systems import basesystem
from systems import cartpole
from systems import furuta
from systems import pendubot
from systems import acrobot
from systems import inertiawheel
from wx.py import shell, editor

#global variables
background_color = (0.8, 0.8, 0.8 )
radstodeg = (180/pi)
resx=1024
resy=768
vertical_dash_pos = resx-335
horizontal_dash_pos=resy-230
FALSE = 0
TRUE = 1

class MainWindow(wx.Frame):
	"""This is the main window application."""
	def __init__(self, parent, id, title):
		"""It creates the application main frame."""
		wx.Frame.__init__(self, parent, id, title, wx.Point(0,0), wx.Size(resx, resy))
		vbox = wx.BoxSizer(wx.VERTICAL)
		
		
		# interface variables
		self.modify = True
		self.plotdestroy = True
		self.DHmat = matrix( [ [0.0]*4, [0.0]*4 ] )
		self.Makegen = [ ]
		self.flag = FALSE
		self.stereofl = FALSE
		self.dyncore=0
		self.plotsoptions=[0,0,0]
								
		#MenuBar
		menubar = wx.MenuBar()
		systems = wx.Menu()
		options = wx.Menu()
		simulation = wx.Menu()
		help = wx.Menu()
		
		#Help menu
		userg= wx.MenuItem( help, wx.NewId(), "&User's Guide\tF1", "A brief user's manual")
		userg.SetBitmap(wx.Image('interface/images/help.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		about = wx.MenuItem(help,wx.NewId(), '&About..', 'About the authors')
	
		exit = wx.MenuItem( help, wx.NewId(), '&Quit\tCtrl+Q', 'Quit the Application')
		exit.SetBitmap(wx.Image('interface/images/exit.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())

		help.AppendItem(userg)
		help.AppendItem( about)
		help.AppendSeparator()
		help.AppendItem(exit)
		
		#Options menu
		submenu = wx.Menu()
		plotsop = wx.Menu()
		submenu.Append(101, 'Visuns Dynamic Core', kind=wx.ITEM_RADIO)
		submenu.Append(102, 'Matlab files', kind=wx.ITEM_RADIO)
		plotsop.Append(103, 'Positions (X)', '',kind=wx.ITEM_CHECK)
		plotsop.Append(104, 'Velocities (dX)', kind=wx.ITEM_CHECK)
		plotsop.Append(105, 'Control (U)', kind=wx.ITEM_CHECK)
		plots = wx.MenuItem( options, wx.NewId(), 'Plot', 'Plot selected')
		plots.SetBitmap(wx.Image('interface/images/plot.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		
		dplots = wx.MenuItem( options, wx.NewId(), 'Delete Plots', 'Delete Selected Plots')
		dplots.SetBitmap(wx.Image('interface/images/delete2.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		
		options.AppendMenu(203, 'Results', submenu)
		options.AppendMenu(204, 'Plots Options', plotsop)
		options.AppendItem(plots)
		options.AppendItem(dplots)
				
		#Systems Menu
		m_furuta=wx.MenuItem( systems, wx.NewId(), "Furuta", "Furuta's Pendulum")
		m_furuta.SetBitmap(wx.Image('interface/images/furuta.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		m_cartpole=wx.MenuItem( systems, wx.NewId(), "Cartpole", "Inverted translational Pendulum")
		m_cartpole.SetBitmap(wx.Image('interface/images/cartpole.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		m_acrobot=wx.MenuItem( systems, wx.NewId(), "Acrobot", "Acrobot")
		m_acrobot.SetBitmap(wx.Image('interface/images/acrobot.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		m_pendubot=wx.MenuItem( systems, wx.NewId(), "Pendubot", "Pendubot")
		m_pendubot.SetBitmap(wx.Image('interface/images/pendubot.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		m_inertiawheel=wx.MenuItem( systems, wx.NewId(), "Inertia Wheel", "Inertia Wheel")
		m_inertiawheel.SetBitmap(wx.Image('interface/images/inertiawheel.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		
		systems.AppendItem(m_furuta)
		systems.AppendItem(m_cartpole)
		systems.AppendItem(m_acrobot)
		systems.AppendItem(m_pendubot)
		systems.AppendItem(m_inertiawheel)

		menubar.Append(systems, '&Systems')
		menubar.Append(options, '&Options')
		menubar.Append(help, '&Help')
		
		self.SetMenuBar(menubar)
		
		# ToolBar1: Simulation functions toolbar ( Interpreter, Play Simulation, Stop Simulation Buttons ) and virtual Mechanical systems (Acrobot...etc)
		toolbar1 = wx.ToolBar(self, -1,size=(24,32), style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT )
		toolbar1.SetToolBitmapSize((24,24))
		stop=toolbar1.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/stop.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Stop Simulation', '')
		pause=toolbar1.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/pause.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Pause simulation', '')
		playbegin=toolbar1.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/playBEGIN.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Go to the start of simulation', '')
		play=toolbar1.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/play.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Play simulation', '')
		playend=toolbar1.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/playEND.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Go to the end of simulation', '')
		playbackward=toolbar1.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/playBackward.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Play backwards', '')
		playforward=toolbar1.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/playForward.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Play forward', '')
		toolbar1.AddSeparator()
	
		plot=toolbar1.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/plot.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Plot results', '')
		dplot=toolbar1.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/delete2.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Destroy plot windows', '')
		int=toolbar1.AddSimpleTool(wx.NewId(), wx.Image('interface/images/interpreter.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Open Interpreter', '')
		Fext=toolbar1.AddSimpleTool(wx.NewId(), wx.Image('interface/images/perturbation.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Add Perturbation', '')
		toolbar1.AddSeparator()
	
		acrobot=toolbar1.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/acrobot.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Load acrobot', '')
		pendubot=toolbar1.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/pendubot.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Load pendubot', '')
		inertiawheel=toolbar1.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/inertiawheel.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Load Inertia Wheel', '')
		cartpole=toolbar1.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/cartpole.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Load cartpole', '')
		furuta=toolbar1.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/furuta.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Load furuta pendulum', '')
	
		toolbar1.Realize()
		vbox.Add(toolbar1, 0, wx.EXPAND)
						
		# ToolBar2: 3D display camera effects
		toolbar2 = wx.ToolBar(self, -1,size=(24,36), style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
		toolbar2.SetToolBitmapSize((24,24))
		GrPanel=toolbar2.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/3dpanel.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), '3D Panel Open', '')
		stereo=toolbar2.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/stereo3d.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), '3D stereo On / Off', '')
		persp=toolbar2.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/ortographic.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Perspective On / Off', '')
		top=toolbar2.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/top.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Top View', '')
		left=toolbar2.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/left.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Left View', '')
		right=toolbar2.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/right.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Right View', '')
		user=toolbar2.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/user.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'User View', '')
		all=toolbar2.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/all_views.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'All View', '')
		solid=toolbar2.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/solids.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Solid On/Off', '')
		grid=toolbar2.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/grid.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Grid On/Off', '')
		axes=toolbar2.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/axes.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Axes On/Off', '')
		wire=toolbar2.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/wireframe.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Wireframe On/Off', '')
		refresh=toolbar2.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/refresh.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Refresh', '')
		toolbar2.AddSeparator()
	
		move=toolbar2.AddSimpleTool(wx.ID_ANY, wx.Image('interface/images/move.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Move', '')
		toolbar2.Realize()
		vbox.Add( toolbar2, 0, wx.EXPAND )
		
		#Main window splitter windows.
		self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_3D | wx.SP_3DSASH )
		self.splitter.SetSashGravity(1.0)

		self.splitterLP = wx.SplitterWindow(self.splitter, -1, style=wx.SP_3D | wx.SP_3DSASH )
		self.splitterLP.SetSashGravity(0.8)
		
		self.splitterRP = wx.SplitterWindow(self.splitter, -1, style=wx.SP_3D | wx.SP_3DSASH )
		#self.splitterRP.SetSashGravity(1.0)
		
		self.splitterSS = wx.SplitterWindow(self.splitterLP,-1, style=wx.SP_3D | wx.SP_3DSASH )
		self.splitterSS.SetSashGravity(0.5)
					
		#VTK Rendering window
		
		self.ren = vtk.vtkRenderer()
		self.VTKwindow = wxVTKRenderWindow( self.splitterLP, -1)
		self.VTKwindow.GetRenderWindow().AddRenderer(self.ren)
		self.ren.SetBackground(background_color)
		camera.CameraSettings( self.ren, self.VTKwindow )
		self.systemworld = world.World( self.ren )
		self.systemworld.InitWorldGrid( self.ren  )
		
		#self.iren = wxVTKRenderWindowInteractor(self.splitterLP, -1)
		#self.interactor = vtk.vtkInteractorStyleFlight()
		#self.iren.SetInteractorStyle(self.interactor)
		#self.iren.SetRenderWindow(self.VTKwindow)
		
		# Python shell
		font = wx.Font(10, wx.ROMAN, wx.NORMAL, wx.BOLD)
		self.pyshell=shell.Shell( self.splitterSS,-1)
		
		#Control windows
		self.SymValuesFrame=symvalues.SymValuesWindow(self.splitterSS, -1)
		self.DynModeFrame=dynmode.DynModeWindow( self.splitterRP, -1 )
		self.SysParamsFrame=sysparams.SysParamsWindow(self.splitterRP, -1 ,self.pyshell)
				
		#Control windows splitter	
		self.splitterSS.SplitVertically(self.SymValuesFrame, self.pyshell,300)
		self.splitterRP.SplitHorizontally(self.DynModeFrame, self.SysParamsFrame)
		self.splitterLP.SplitHorizontally( self.VTKwindow, self.splitterSS,horizontal_dash_pos)
		self.splitter.SplitVertically( self.splitterLP, self.splitterRP, vertical_dash_pos )
		
		vbox.Add( self.splitter, 1, wx.EXPAND )
			
		self.SetSizer(vbox)
		self.statusbar = self.CreateStatusBar()
		
		#Bind menus buttons
		self.Bind(wx.EVT_MENU, self.VisunsDC ,id=101)
		self.Bind(wx.EVT_MENU, self.MatlabDC ,id=102)
		self.Bind(wx.EVT_MENU, self.PositionPlot ,id=103)
		self.Bind(wx.EVT_MENU, self.VelocitiePlot ,id=104)
		self.Bind(wx.EVT_MENU, self.ControlPlot ,id=105)
		
		self.Bind(wx.EVT_TOOL, self.OnPlot, plots)
		self.Bind(wx.EVT_TOOL, self.OnDPlot, dplots)
			
		self.Bind(wx.EVT_TOOL, self.OnAcrobot, m_acrobot)
		self.Bind(wx.EVT_TOOL, self.OnInertiaWheel, m_inertiawheel)
		self.Bind(wx.EVT_TOOL, self.OnCartpole, m_cartpole)
		self.Bind(wx.EVT_TOOL, self.OnFuruta, m_furuta)
		self.Bind(wx.EVT_TOOL, self.OnPendubot, m_pendubot)
		
		# Tie button clicks of toolbar1 to event handlers
		self.Bind(wx.EVT_TOOL, self.OnPause, pause )
		self.Bind(wx.EVT_TOOL, self.OnStop, stop )
		self.Bind(wx.EVT_TOOL, self.OnPlayBegin, playbegin )
		self.Bind(wx.EVT_TOOL, self.OnPlay, play )
		self.Bind(wx.EVT_TOOL, self.OnPlayEnd, playend )
		self.Bind(wx.EVT_TOOL, self.OnPlayBackward, playbackward )
		self.Bind(wx.EVT_TOOL, self.OnPlayForward, playforward )
		self.Bind(wx.EVT_TOOL, self.OnPlot, plot)
		self.Bind(wx.EVT_TOOL, self.OnDPlot, dplot)
		self.Bind(wx.EVT_TOOL, self.OnInt, int)
		self.Bind(wx.EVT_TOOL, self.OnExit, exit)
		self.Bind(wx.EVT_TOOL, self.OnUserg, userg)
		self.Bind(wx.EVT_TOOL, self.OnAbout, about)
		self.Bind(wx.EVT_TOOL, self.OnAcrobot, acrobot)
		self.Bind(wx.EVT_TOOL, self.OnInertiaWheel, inertiawheel)
		self.Bind(wx.EVT_TOOL, self.OnCartpole, cartpole)
		self.Bind(wx.EVT_TOOL, self.OnFuruta, furuta)
		self.Bind(wx.EVT_TOOL, self.OnPendubot, pendubot)
		
		
		# Tie button clicks of toolbar2 to event handlers
		self.Bind(wx.EVT_TOOL, self.OnGrPanel, GrPanel)
		self.Bind(wx.EVT_TOOL, self.OnStereo, stereo)
		self.Bind(wx.EVT_TOOL, self.OnPerspective, persp)
		self.pyshell.clear()
		
		#windows
		if (os.name=="nt"):
			os.popen('del *.o')
			os.popen('del dyncorec.exe')
		#others
		else:
			os.popen('rm *.o')
			os.popen('rm dyncorec.exe')
					
	def VisunsDC(self,event):
		"""Loads Simparam for using visuns Dynamic core"""
		self.dyncore=0
	def MatlabDC(self,event):
		"""Loads Simparam for using .mat files"""
		self.dyncore=1

	def PositionPlot(self,event):
		"""Load position plot option into plotoptions vector"""
		if (self.plotsoptions[0]==1):
			self.plotsoptions[0]=0
		else:
			self.plotsoptions[0]=1
		print self.plotsoptions
	def VelocitiePlot(self,event):
		"""Load position plot option into plotoptions vector"""
		if (self.plotsoptions[1]==1):
			self.plotsoptions[1]=0
		else:
			self.plotsoptions[1]=1
		print self.plotsoptions			
	def ControlPlot(self,event):
		"""Load position plot option into plotoptions vector"""
		if (self.plotsoptions[2]==1):
			self.plotsoptions[2]=0
		else:
			self.plotsoptions[2]=1
		print self.plotsoptions				
		
	#Binding functions of ToolBar 1
	def OnPause(self, event):
		"""Pauses dynamic simulation"""
		self.statusbar.SetStatusText('Pause simulation')
		
	def OnStop(self, event):
		"""Stops dynamic simulation"""
		self.statusbar.SetStatusText('Stop Simulation.')
		
	def OnPlayBegin(self, event):
		"""Goes to the start of simulation"""
		self.statusbar.SetStatusText('Start simulation')
		
	def OnPlay(self, event):
		"""Plays dynamic simulation"""
		#Fills dynamic simulation params.
		self.system.filldynsimulate( )
		self.system.simulate( self.ren, self.VTKwindow, self.pyshell)
		#It updates the sliders values from the SymValuesWindow after simualtion.
		self.SymValuesFrame.UpdateSliderswValues( self.system.X[0, (self.system.pt-2)], self.system.X[1, (self.system.pt-2)] )		
		self.statusbar.SetStatusText('Play Simulation.')
		
	def OnPlayEnd(self, event):
		"""Goes to end of simulation"""
		self.statusbar.SetStatusText('Goes to end of simulation')
		
	def OnPlayBackward(self, event):
		"""Play backwards"""
		self.statusbar.SetStatusText('Play backwards')
		
	def OnPlayForward(self, event):
		"""Play forward"""
		self.statusbar.SetStatusText('Play forward')
			
	def OnPlot(self, event):
		"""Plots state variables"""
		self.plotdestroy = True
		#Lists of plot data tuples.
		pos1plotdata = [ ]
		pos2plotdata = [ ]
		vel1plotdata = [ ]
		vel2plotdata = [ ]
		uplotdata=[ ]
		#Lists of y-axis limits
		poslimits = []
		vellimits = []
		ulimits=[ ]
		
		#Create data in wx GNUPlot format.
		plotwindow.CreatePlotData( self, pos1plotdata, pos2plotdata, vel1plotdata, vel2plotdata,uplotdata, poslimits, vellimits, ulimits)
		
		if (self.system.type =="cartpole"):
			xlimit = self.system.timevec[0, ( size ( self.system.timevec) -1) ]		
			self.plot1=plotwindow.PlotWindow( None, -1, 'Plot window', 'Cart Position', pos1plotdata, 'Time(segs)', 'Pos ( mts )', xlimit, poslimits[0], poslimits[1], 5, 410)
			self.plot2=plotwindow.PlotWindow( None, -1, 'Plot window', 'Pole Position', pos2plotdata, 'Time(segs)', 'Pos( grads )', xlimit, poslimits[2]*radstodeg, poslimits[3]*radstodeg, 510, 410 )	
			
		else:
			xlimit = self.system.timevec[0, ( size ( self.system.timevec) -1) ]
			self.plot1 = plotwindow.PlotWindow( None, -1, 'Plot window', 'Pole #1 Position', pos1plotdata, 'Time(segs)', 'Pos ( grads )', xlimit, poslimits[0]*radstodeg, poslimits[1]*radstodeg, 5, 410)
			if (self.system.type =="inertiawheel"):
				self.plot2 = plotwindow.PlotWindow( None, -1, 'Plot window', 'Wheel Position', pos2plotdata, 'Time(segs)', 'Pos( grads )', xlimit, poslimits[2]*radstodeg, poslimits[3]*radstodeg, 510, 410 )
			else:
				self.plot2 = plotwindow.PlotWindow( None, -1, 'Plot window', 'Pole #2 Position', pos2plotdata, 'Time(segs)', 'Pos( grads )', xlimit, poslimits[2]*radstodeg, poslimits[3]*radstodeg, 510, 410 )
		self.plot3=plotwindow.PlotWindow( None, -1, 'Plot window', 'Control', uplotdata, 'Time(segs)', 'U(volts)', xlimit, ulimits[0], ulimits[1], 5, 100 )	
		self.statusbar.SetStatusText('Plots state variables')
		
	def OnDPlot(self, event):
		"""Destroy Plot windows"""
		if self.plotdestroy:
			self.plot1.Destroy()
			self.plot2.Destroy()
			self.plot3.Destroy()
			self.plotdestroy = False
			
	def OnInt(self, event):
		"""Opens Interpreter of equations function"""
		self.statusbar.SetStatusText('Open Ecuation Editor')
		frame = interpreter.InterpreterWindow(None, -1, 'Ecuation Editor',self.system.type)
		frame.SetIcon(wx.Icon('interface/images/visuns2.ico', wx.BITMAP_TYPE_ICO))
		frame.Show(True)
		frame.SetFocus()
		
	def OnExit(self, event):
		"""Quits the Controlab application"""
		if self.modify:
			dlg = wx.MessageDialog(self, 'Do you really want to Exit?', '', wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)
			val = dlg.ShowModal()
			if val == wx.ID_YES:
				wx.Exit()
			elif val == wx.ID_NO:
				dlg.Destroy()
			elif val == wx.ID_CANCEL:
				dlg.Destroy()
			else:
				self.Destroy()
		else:
			self.Destroy()
	
	def OnAbout(self, event):		
		#not working yet
		dlg = wx.MessageDialog(self, 'VISUNS: Visual Simulation of Underactuated Systems\n\nRobotics and Automation Group\nPontificia Universidad Javeriana - Cali,Colombia\n\nDeveloped by:\nJuan Camilo Acosta M.\nJulian David Colorado M.\nAntonio Matta G.\n\nAdviced by:\nFreddy Naranjo P.','About VISUNS', wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
			
	def OnUserg(self, event):
		thread.start_new_thread(self.help,(event,))
		
		#frame.SetFocus()
	#Binding functions of ToolBar 2
	def OnGrPanel(self, event):		
		"""Opens 3d Panel"""
	def OnStereo(self, event):
		"""Enables/Disables stereoscopic vision"""
		if ( self.stereofl == TRUE):
			self.stereofl = FALSE
			self.statusbar.SetStatusText('3D Stereo Off.')
		else:
			self.stereofl = TRUE
			self.statusbar.SetStatusText('3D Stereo On.')
		camera.StereoOn( self.ren, self.VTKwindow, self.stereofl )
		self.VTKwindow.Render()
		
	def OnPerspective(self, event):
		"""Enables/Disables perspective projection"""
		if ( self.flag == TRUE):
			self.flag = FALSE
			self.statusbar.SetStatusText('Perspective On.')
		else:
			self.flag = TRUE
			self.statusbar.SetStatusText('Perspective Off.')
		camera.Perspective( self.ren, self.flag )
		self.VTKwindow.Render()
		
	def deleteActiveSystem(self ):
		"""Deletes an active system in order to render a new one"""
		self.systemworld.fadeout( self.ren, self.VTKwindow, self.system )
		
		
	def updateActiveSystem(self ):
		"""Updates active system's neccesary values to be drawn"""
		
		if (self.system.type =="cartpole"):
			#Rotate and translate cartpole's base transformation matrix.
			self.system.BaseTrans.Translate ( 0.0, self.system.BaseHeight, 0.0)
			self.system.BaseTrans.RotateWXYZ ( 90, 0, 1, 0)		
			self.system.RotCamHMTcompute(  self.RotCamMat )
			self.system.genericHMTcompute( self.DHmat[0,3], self.DHmat[1,2] )
		elif (self.system.type=="furuta"):
			self.system.RotCamHMTcompute(  self.RotCamMat )
			NewMatrix = vtk.vtkMatrix4x4()
			BaseMatrix = self.system.BaseTrans.GetMatrix( )
			BaseMatrix.Multiply4x4( self.system.RotCamHMT, BaseMatrix, NewMatrix )
			self.system.BaseTrans.SetMatrix( NewMatrix )
			self.system.BaseTrans.RotateWXYZ ( 90, 0, 0, 1)	
			self.system.genericHMTcompute( self.DHmat[0,2], self.DHmat[1,2] )
		elif (self.system.type =="pendubot" or self.system.type =="acrobot"):
			#Rotate and translate pendubot's base transformation matrix.
			self.system.BaseTrans.Translate ( 0.0, 0.65, 0.0)
			self.system.BaseTrans.RotateWXYZ ( 90, 0, 0, 1)
			self.system.RotCamHMTcompute(  self.RotCamMat )
			self.system.genericHMTcompute( self.DHmat[0,2], self.DHmat[1,2] )
		elif (self.system.type=="inertiawheel"):
			self.system.BaseTrans.Translate ( 0.0, 0.221, 0.0)
			self.system.BaseTrans.RotateWXYZ ( 270, 0, 0, 1)
			self.system.RotCamHMTcompute(  self.RotCamMat )
			self.system.genericHMTcompute( self.DHmat[0,2], self.DHmat[1,2] )

		self.system.dyncore=self.dyncore
		
		#3D renderize system.		
		#self.system.draw( self.ren, self.VTKwindow)
		self.systemworld.draw( self.ren, self.system)
		self.systemworld.fadein(self.ren, self.VTKwindow, self.system)
		
		#update System values window items
		self.SymValuesFrame.GetSystemValues( self.system, self.ren, self.VTKwindow )
		self.SymValuesFrame.UpdateSlidersValues()
		#update Dynamic model window values
		self.DynModeFrame.Scroll.SetImgDesc( self.system.type )
		#update Parameters window values
		self.SysParamsFrame.Scroll.GetSystemValues( self.system )
		#
		self.SysParamsFrame.ToolBar.GetSystemValues( self.system )
			
	def UpdateWindowsInfo( self ):
		"""Updates neccesary values to GUI widgets"""
		#System values window
		self.SymValuesFrame.SymValuesTree.Unselect( )
		self.SymValuesFrame.HideSlides( )
			
	def OnCartpole(self, event):
		"""Loads the cartpole underactuaded system"""
		#Fills Cartpole's DH matrix.	
		self.DHmat[0,:] = [ pi/2, 0.0425, pi/2, 0.0]
		self.DHmat[1,:] = [ 0.0, 0.3, pi, -0.0225 ]
		self.RotCamMat = [ 0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.35,-1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0 ]
		#Fills Cartpole's Makegen default values.
		self.Makegen = [ 'cartpole', 'improvedeuler', 'cartpole', 'motor2', 'lqregulator_motor2', 'swing_up_motor2' , 2]
		if (self.systemworld.type =="none"):			
			#create cartpole object.
			self.system=cartpole.Cartpole( self.DHmat, "translational", "revolute", self.Makegen )
			self.system.type = 'cartpole'
			self.systemworld.type = self.system.type
			self.updateActiveSystem()
		else:
			self.deleteActiveSystem( )
			#create cartpole object.
			self.system=cartpole.Cartpole( self.DHmat, "translational", "revolute", self.Makegen )
			self.system.type = 'cartpole'
			self.systemworld.type = self.system.type
			self.updateActiveSystem()
			self.UpdateWindowsInfo()		
		self.statusbar.SetStatusText('Cartpole loaded.')
		
	def OnFuruta(self, event):
		"""Loads the furuta underactuaded system"""
		#Fills Furuta's DH matrix.	
		self.DHmat[0,:] = [ pi/2, 0.0, 0.0, -0.4 ]
		self.DHmat[1,:] = [ pi, 0.0, pi, 0.2 ]
		self.RotCamMat = [  0.0,-1.0,0.0,0.0, 0.0,0.0,-1.0,0.06, 1.0,0.0,0.0,0.0, 0.0,0.0,0.0,1.0 ]
		#Fills Furuta's Makegen default values.
		self.Makegen = [ 'furuta', 'rungekutta', 'completefuruta', 'motor1', 'lqregulator_motor1', 'swing_up_motor1' , 2]	
		if (self.systemworld.type =="none"):
			#create furuta object
			self.system=furuta.Furuta( self.DHmat, "revolute", "revolute", self.Makegen )
			self.system.type ="furuta"
			self.systemworld.type = self.system.type
			self.updateActiveSystem()
		else:
			self.deleteActiveSystem( )
			#create furuta object
			self.system=furuta.Furuta( self.DHmat, "revolute", "revolute", self.Makegen )
			self.system.type ="furuta"
			self.systemworld.type = self.system.type
			self.updateActiveSystem()
			self.UpdateWindowsInfo()
		self.statusbar.SetStatusText('Furuta pendulum loaded.')
		
	def OnPendubot(self, event):
		"""Loads the pendubot underactuaded system"""
		#Fills pendubot's DH matrix.	
		self.DHmat[0,:] = [ 0.0, 0.3, pi, 0.025]
		self.DHmat[1,:] = [ 0.0, 0.25, 0, 0.005 ]
		self.RotCamMat = [ 0,-1,0,0.0,1,0,0,0.65,0,0,1,0,0,0,0,1 ]
		#Fills Pendubot's Makegen default values.
		self.Makegen = [ 'pendubot', 'rungekutta', 'pendubot', 'motor2', 'lqregulator_motor2', '' , 1]	
		if (self.systemworld.type=="none"):
			#create pendubot object.
			self.system=pendubot.Pendubot( self.DHmat, "revolute", "revolute", self.Makegen )
			self.system.type ="pendubot"
			self.systemworld.type = self.system.type
			self.updateActiveSystem()
		else:
			self.deleteActiveSystem( )
			#create pendubot object.
			self.system=pendubot.Pendubot( self.DHmat, "revolute", "revolute", self.Makegen )
			self.system.type ="pendubot"
			self.systemworld.type = self.system.type
			self.updateActiveSystem()
			self.UpdateWindowsInfo()		
		self.statusbar.SetStatusText('Pendubot loaded.')
	
	def OnAcrobot(self, event):
		"""Loads the acrobot underactuaded system"""
		#Fills acrobot's DH matrix.	
		self.DHmat[0,:] = [ 0.0, 0.3, pi, 0.025]
		self.DHmat[1,:] = [ 0.0, 0.25, 0, 0.005 ]
		self.RotCamMat = [ 0,-1,0,0.0,1,0,0,0.65,0,0,1,0,0,0,0,1 ]
		#Fills acrobot's Makegen default values.
		self.Makegen = [ 'acrobot', 'rungekutta', 'acrobot', 'motor3', 'lqregulator_motor3', '', 1]	
		if (self.systemworld.type=="none"):
			#create acrobot object.
			self.system=acrobot.Acrobot( self.DHmat, "revolute", "revolute", self.Makegen )
			self.system.type ="acrobot"
			self.systemworld.type = self.system.type
			self.updateActiveSystem()
		else:
			self.deleteActiveSystem( )
			#create acrobot object.
			self.system=acrobot.Acrobot( self.DHmat, "revolute", "revolute", self.Makegen )
			self.system.type ="acrobot"
			self.systemworld.type = self.system.type
			self.updateActiveSystem()
			self.UpdateWindowsInfo()		
		self.statusbar.SetStatusText('Acrobot loaded.')
		
	def OnInertiaWheel(self, event):
		"""Loads the Inertia Wheel underactuaded system"""
		#Fills InertiaWheel's DH matrix.	
		self.DHmat[0,:] = [ 0.0, -0.15, pi, 0.025]
		self.DHmat[1,:] = [ 0.0, 0.0, 0.0, 0.005 ]
		self.RotCamMat = [ 0.0,1.0,0.0,0.0,-1.0,0.0,0.0,0.221,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0 ]
		
		#Fills InertiaWheel's Makegen default values.

		self.Makegen = [ 'inertiawheel', 'rungekutta', 'inertiawheel', 'motor3', 'IWcontrol_motor3', ' ',1 ]	

		if (self.systemworld.type=="none"):
			#create InertiaWheel object.
			self.system=inertiawheel.InertiaWheel( self.DHmat, "revolute", "revolute", self.Makegen )
			self.system.type ="inertiawheel"
			self.systemworld.type = self.system.type
			self.updateActiveSystem()
		else:
			self.deleteActiveSystem( )
			#create InertiaWheel object.
			self.system=inertiawheel.InertiaWheel( self.DHmat, "revolute", "revolute", self.Makegen )
			self.system.type ="inertiawheel"
			self.systemworld.type = self.system.type
			self.updateActiveSystem()
			self.UpdateWindowsInfo()		
		self.statusbar.SetStatusText('Inertia Wheel loaded.')
		
#wxApp subclass that overloads the OnInit method
class MyApp(wx.App):
	"""Creates the main window and insert the custom frame"""
	def OnInit(self):
		"""Creates the main application frame"""
		frame = MainWindow(None, -1, 'VISUNS: Visual Simulation Of Underactuated Nonlinear Systems')
		frame.SetIcon(wx.Icon('interface/images/visuns.ico', wx.BITMAP_TYPE_ICO))
		frame.Show(True)
		return True

# Create the app and start processing messages
app = MyApp(0)
app.MainLoop()