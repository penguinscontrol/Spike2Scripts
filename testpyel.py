'''
 *  NOTICE:  This code was developed by the Laboratory of
 *  Sensorimotor Research in the National Eye Institute,
 *  a branch of the U.S. Government.  This code is
 *  distributed without copyright restrictions.  No
 *  individual, company, organization, etc., may copyright
 *  this code.  If it is passed on to others, this notice
 *  must be included.
 *
 *  No warranty is implied or offered for the usage of the software.
 *  
 *  Any Modifications to this code, especially bug fixes,
 *  should be reported to pierre.daye@gmail.com.
 * 
 *  Pierre M. Daye, Ph.D.
 *  Laboratory of Sensorimotor Research
 *  Bldg 49 Rm 2A50
 *  National Eye Institute, NIH
 *  9000 Rockville Pike, Bethesda, MD, 20892-4435
 *  (301) 496-9375.
 * 
 *  August 17, 2012
'''
import pdb
import dicom as dcm
from numpy import ones,tile,array, sum, dot, transpose, dstack, abs, squeeze, uint8, shape, pi, cos, sin, floor, ceil, integer, mgrid, where, intersect1d, nonzero, zeros, NAN, eye, union1d, arange, isreal, float64, rint, unique, sort, loadtxt, argsort, concatenate, savetxt,vstack

from pylab import Rectangle
from matplotlib import cm as cmm
from matplotlib import colors as cl

from numpy.linalg import inv
from string import find, replace

from pickle import dump, load, HIGHEST_PROTOCOL
from sys import argv, platform
from os import sep, listdir, path

from PyQt4.QtCore import SIGNAL, QRect, Qt, QMetaObject, QObject, QFileSystemWatcher, QFile, QIODevice
from PyQt4.QtGui import QMainWindow, QApplication, QWidget, QGroupBox, QLabel, QSpinBox, QVBoxLayout, QDoubleSpinBox, QHBoxLayout, QCheckBox, QPushButton, QAction, QFileDialog, QInputDialog, QIcon, QMessageBox, QProgressBar, QStatusBar, QDialog, QDialogButtonBox, QFont, QTabWidget, QTextEdit,QComboBox

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

from matplotlib.figure import Figure
from matplotlib.pyplot import get_cmap
from matplotlib.lines import Line2D
from itertools import product, combinations

class Form(QMainWindow):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle('pyElectrode: Place electrode position in MRI')
        self.resize(1200, 800)
        
        self.data = MRIData()
        
        self.MatRot = self.computeRotCam()
        self.EyePos = array([[300.0], [300.0], [300.0]])
        self.CamPos = array([[10000.0], [12000.0], [10000.0]])
        self.rotView = array([0.0, 0.0, 0.0], dtype=float)
        self.CoordView = array([0.0, 0.0, 0.0], dtype=float)
        self.MeanAddView = 0.0
        self.MinMaxMRI = 0.0
        self.memPos = array([0, 0, 0])
        self.memRot = array([0, 0, 0])
        
        self.LogFile = ''
        self.SaveElectFile = ''
        self.MonkeyNumExt=1
        self.TypeNeuronExt=1
        self.LogSTR=''
        
        r = [-127, 127]
        self.Cube = []
        
        self.NumImages = 255
        
        self.grid = False
        self.showNeuronsFlag = False
        
        for s, e in combinations(array(list(product(r, r, r))), 2):
            if sum(abs(s - e)) == r[1] - r[0]:
                tmps = dot(self.MatRot, transpose(array([s])) - self.CamPos)
                tmpe = dot(self.MatRot, transpose(array([e])) - self.CamPos)
                bs = squeeze(array([(tmps[0] - self.EyePos[0]) * (self.EyePos[2] / tmps[2]), (tmps[1] - self.EyePos[1]) * (self.EyePos[2] / tmps[2])]))
                be = squeeze(array([(tmpe[0] - self.EyePos[0]) * (self.EyePos[2] / tmpe[2]), (tmpe[1] - self.EyePos[1]) * (self.EyePos[2] / tmpe[2])]))
                self.Cube.append(zip(be, bs))
        
        self.create_main_frame()
        self.create_menu()
        
    def computeRotCam(self, alpha=0.0, beta= -pi / 16, gamma=0.0):
        RX = array([[1, 0, 0], [0, cos(alpha), -sin(alpha)], [0, sin(alpha), cos(alpha)]])
        RY = array([[cos(beta), 0, sin(beta)], [0, 1, 0], [-sin(beta), 0, cos(beta)]])
        RZ = array([[cos(gamma), -sin(gamma), 0], [sin(gamma), cos(gamma), 0], [0, 0, 1]])
        
        return dot(RX, dot(RY, RZ))
       
    def create_main_frame(self):
        self.main_frame = QWidget()
         
        self.main_frame.setFont(QFont("Times", 10))
        self.main_frame.setGeometry(0, 0, 1024, 1024/219*169.0)
        
        self.dpi = 100
        self.fig = Figure((4.0, 4.0), dpi=self.dpi)
        self.fig.subplots_adjust(wspace=0.05, hspace=0.05, left=0.01, right=0.99, bottom=0.01, top=0.99)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        
        self.axesA = self.fig.add_axes([0.01, 0.51, 0.48, 0.48], aspect='equal')#self.fig.add_subplot(221, aspect='equal')#
        self.axesB = self.fig.add_axes([0.51, 0.51, 0.48, 0.48], aspect='equal')#self.fig.add_subplot(222, aspect='equal')#
        self.axesC = self.fig.add_axes([0.01, 0.01, 0.48, 0.48], aspect='equal')#self.fig.add_subplot(223, aspect='equal')#
        self.axesD = self.fig.add_axes([0.51, 0.01, 0.48, 0.48], aspect='equal')#self.fig.add_subplot(224, aspect='equal')#
        
        # Remove ticks and labels
        self.axesA.get_xaxis().set_visible(False)
        self.axesA.get_yaxis().set_visible(False)
        self.axesB.get_xaxis().set_visible(False)
        self.axesB.get_yaxis().set_visible(False)
        self.axesC.get_xaxis().set_visible(False)
        self.axesC.get_yaxis().set_visible(False)
        self.axesD.get_xaxis().set_visible(False)
        self.axesD.get_yaxis().set_visible(False)
        
        self.Tab = QTabWidget()
        
        self.createStatusBar()
        # create progress bar
        self.pb = QProgressBar(self.statusBar())
        self.statusBar().addPermanentWidget(self.pb)
        self.pb.hide()
        
        # GUI controls
        # MRI CLIPPING
        self.ClipMRI = QGroupBox('MRI Clipping')
        
        self.CuttingPlane = QGroupBox('Cutting planes')
        ApCutLbl = QLabel('PL A +')
        self.ApCut = QSpinBox()
        self.ApCut.setRange(0, 127)
        self.ApCut.setValue(0)
        self.connect(self.ApCut, SIGNAL('valueChanged(int)'), self.ClipRange)
        ApCut = QVBoxLayout()
        ApCut.addWidget(ApCutLbl)
        ApCut.addWidget(self.ApCut)
        ApCut.addStretch()
        
        AmCutLbl = QLabel('PL A -')
        self.AmCut = QSpinBox()
        self.AmCut.setRange(0, 127)
        self.AmCut.setValue(0)
        self.connect(self.AmCut, SIGNAL('valueChanged(int)'), self.ClipRange)
        AmCut = QVBoxLayout()
        AmCut.addWidget(AmCutLbl)
        AmCut.addWidget(self.AmCut)
        AmCut.addStretch()
        
        BCutLbl = QLabel('Delta B')
        self.BCut = QSpinBox()
        self.BCut.setRange(0, 0)
        self.BCut.setValue(0)
        self.connect(self.BCut, SIGNAL('valueChanged(int)'), self.ClipRange)
        BCut = QVBoxLayout()
        BCut.addWidget(BCutLbl)
        BCut.addWidget(self.BCut)
        BCut.addStretch()
        
        CCutLbl = QLabel('Delta C')
        self.CCut = QSpinBox()
        self.CCut.setRange(0, 0)
        self.CCut.setValue(0)
        self.connect(self.CCut, SIGNAL('valueChanged(int)'), self.ClipRange)
        CCut = QVBoxLayout()
        CCut.addWidget(CCutLbl)
        CCut.addWidget(self.CCut)
        CCut.addStretch()
        
        CuttingPlane = QHBoxLayout()
        CuttingPlane.addLayout(AmCut)
        CuttingPlane.addLayout(ApCut)
        CuttingPlane.addLayout(BCut)
        CuttingPlane.addLayout(CCut)
        self.CuttingPlane.setLayout(CuttingPlane)
        
        self.ClipMRIBT = QPushButton("CLIP MRI")
        self.connect(self.ClipMRIBT, SIGNAL('clicked()'), self.PressClip)
        
        self.ClipFlag = QCheckBox("Allow Clipping")
        self.connect(self.ClipFlag, SIGNAL('stateChanged(int)'), self.setClipFlag)
        
        CLIP = QVBoxLayout()
        CLIP.addWidget(self.CuttingPlane)
        CLIP.addWidget(self.ClipMRIBT)
        CLIP.addWidget(self.ClipFlag)
        CLIP.addStretch(1)
        
        self.ClipMRI.setLayout(CLIP)
        
        self.Tab.addTab(self.ClipMRI, 'Clip MRI')
        
        # Original planes position
        self.ChamberCoordinate = QGroupBox('Chamber alignment')
        
        self.OriginalPlane = QGroupBox('Chamber planes')
        APosLbl = QLabel('PL A')
        self.APos = QSpinBox()
        self.APos.setRange(-127, 127)
        self.APos.setValue(0)
        self.connect(self.APos, SIGNAL('valueChanged(int)'), self.plotData)
        APlane = QVBoxLayout()
        APlane.addWidget(APosLbl)
        APlane.addWidget(self.APos)
        APlane.addStretch()
        
        BPosLbl = QLabel('PL B')
        self.BPos = QSpinBox()
        self.BPos.setRange(-127, 127)
        self.BPos.setValue(0)
        self.connect(self.BPos, SIGNAL('valueChanged(int)'), self.plotData)
        BPlane = QVBoxLayout()
        BPlane.addWidget(BPosLbl)
        BPlane.addWidget(self.BPos)
        BPlane.addStretch()
        
        CPosLbl = QLabel('PL C')
        self.CPos = QSpinBox()
        self.CPos.setRange(-127, 127)
        self.CPos.setValue(0)
        self.connect(self.CPos, SIGNAL('valueChanged(int)'), self.plotData)
        CPlane = QVBoxLayout()
        CPlane.addWidget(CPosLbl)
        CPlane.addWidget(self.CPos)
        CPlane.addStretch()
        
        self.CDepth = QDoubleSpinBox()
        self.CDepth.setRange(-100.0, 100.0)
        self.CDepth.setValue(0.0)
        self.CDepth.setDecimals(3)
        self.connect(self.CDepth, SIGNAL('valueChanged(double)'), self.plotData)
        CDepth = QVBoxLayout()
        CDepth.addWidget(self.CDepth)
        CDepth.addStretch()
        
        self.DepthCorr = QGroupBox('Depth correction')
        self.DepthCorr.setLayout(CDepth)        
                
        SelectPlanes = QHBoxLayout()
        SelectPlanes.addLayout(APlane)
        SelectPlanes.addLayout(BPlane)
        SelectPlanes.addLayout(CPlane)
        self.OriginalPlane.setLayout(SelectPlanes)
        
        self.OriginalRotation = QGroupBox('Chamber rotations')
        ARotOLbl = QLabel('Rot N A')
        self.ARotO = QDoubleSpinBox()
        self.ARotO.setRange(-180, 180)
        self.ARotO.setValue(0)
        self.ARotO.setDecimals(2)
        self.connect(self.ARotO, SIGNAL('valueChanged(double)'), self.plotData)
        APlane = QVBoxLayout()
        APlane.addWidget(ARotOLbl)
        APlane.addWidget(self.ARotO)
        APlane.addStretch()
        
        BRotOLbl = QLabel('Rot N B')
        self.BRotO = QDoubleSpinBox()
        self.BRotO.setRange(-180, 180)
        self.BRotO.setValue(0)
        self.BRotO.setDecimals(2)
        self.connect(self.BRotO, SIGNAL('valueChanged(double)'), self.plotData)
        BPlane = QVBoxLayout()
        BPlane.addWidget(BRotOLbl)
        BPlane.addWidget(self.BRotO)
        BPlane.addStretch()
        
        CRotOLbl = QLabel('Rot N C')
        self.CRotO = QDoubleSpinBox()
        self.CRotO.setRange(-180, 180)
        self.CRotO.setValue(0)
        self.CRotO.setDecimals(2)
        self.connect(self.CRotO, SIGNAL('valueChanged(double)'), self.plotData)
        CPlane = QVBoxLayout()
        CPlane.addWidget(CRotOLbl)
        CPlane.addWidget(self.CRotO)
        CPlane.addStretch()
                
        self.AlignChamber = QCheckBox("set chamber orientation/position")
        self.connect(self.AlignChamber, SIGNAL('stateChanged(int)'), self.setChamberFlags)
        
        self.LoadElecPosB = QPushButton("Select electrode file")
        self.connect(self.LoadElecPosB, SIGNAL('clicked()'), self.LoadElecPos)
        
        SelectRotation = QHBoxLayout()
        SelectRotation.addLayout(APlane)
        SelectRotation.addLayout(BPlane)
        SelectRotation.addLayout(CPlane)
        self.OriginalRotation.setLayout(SelectRotation)
        
        ChamberCalib = QVBoxLayout()
        ChamberCalib.addWidget(self.OriginalPlane)
        ChamberCalib.addWidget(self.DepthCorr)
        ChamberCalib.addWidget(self.OriginalRotation)
        ChamberCalib.addWidget(self.LoadElecPosB)
        ChamberCalib.addWidget(self.AlignChamber)
        ChamberCalib.addStretch(1)
        self.ChamberCoordinate.setLayout(ChamberCalib)
        
        self.Tab.addTab(self.ChamberCoordinate, 'Chamber')
        
        self.ViewCoordinate = QGroupBox('View alignment')
                
        self.ViewPlane = QGroupBox('View planes')
        AVPosLbl = QLabel('PL A')
        self.AVPos = QSpinBox()
        self.AVPos.setRange(-127, 127)
        self.AVPos.setValue(0)
        self.connect(self.AVPos, SIGNAL('valueChanged(int)'), self.plotData)
        AVPlane = QVBoxLayout()
        AVPlane.addWidget(AVPosLbl)
        AVPlane.addWidget(self.AVPos)
        AVPlane.addStretch()
        
        BVPosLbl = QLabel('PL B')
        self.BVPos = QSpinBox()
        self.BVPos.setRange(-127, 127)
        self.BVPos.setValue(0)
        self.connect(self.BVPos, SIGNAL('valueChanged(int)'), self.plotData)
        BVPlane = QVBoxLayout()
        BVPlane.addWidget(BVPosLbl)
        BVPlane.addWidget(self.BVPos)
        BVPlane.addStretch()
        
        CVPosLbl = QLabel('PL C')
        self.CVPos = QSpinBox()
        self.CVPos.setRange(-127, 127)
        self.CVPos.setValue(0)
        self.connect(self.CVPos, SIGNAL('valueChanged(int)'), self.plotData)
        CVPlane = QVBoxLayout()
        CVPlane.addWidget(CVPosLbl)
        CVPlane.addWidget(self.CVPos)
        CVPlane.addStretch()
                
        SelectViewPlanes = QHBoxLayout()
        SelectViewPlanes.addLayout(AVPlane)
        SelectViewPlanes.addLayout(BVPlane)
        SelectViewPlanes.addLayout(CVPlane)
        self.ViewPlane.setLayout(SelectViewPlanes)
        
        self.ViewRotation = QGroupBox('View rotations')
        AVRotOLbl = QLabel('Rot N A')
        self.AVRotO = QDoubleSpinBox()
        self.AVRotO.setRange(-180, 180)
        self.AVRotO.setValue(0)
        self.AVRotO.setDecimals(2)
        self.connect(self.AVRotO, SIGNAL('valueChanged(double)'), self.plotData)
        AVPlane = QVBoxLayout()
        AVPlane.addWidget(AVRotOLbl)
        AVPlane.addWidget(self.AVRotO)
        AVPlane.addStretch()
        
        BVRotOLbl = QLabel('Rot N B')
        self.BVRotO = QDoubleSpinBox()
        self.BVRotO.setRange(-180, 180)
        self.BVRotO.setValue(0)
        self.BVRotO.setDecimals(2)
        self.connect(self.BVRotO, SIGNAL('valueChanged(double)'), self.plotData)
        BVPlane = QVBoxLayout()
        BVPlane.addWidget(BVRotOLbl)
        BVPlane.addWidget(self.BVRotO)
        BVPlane.addStretch()
        
        CVRotOLbl = QLabel('Rot N C')
        self.CVRotO = QDoubleSpinBox()
        self.CVRotO.setRange(-180, 180)
        self.CVRotO.setValue(0)
        self.CVRotO.setDecimals(2)
        self.connect(self.CVRotO, SIGNAL('valueChanged(double)'), self.plotData)
        CVPlane = QVBoxLayout()
        CVPlane.addWidget(CVRotOLbl)
        CVPlane.addWidget(self.CVRotO)
        CVPlane.addStretch()
                
        SelectViewPlanes = QHBoxLayout()
        SelectViewPlanes.addLayout(AVPlane)
        SelectViewPlanes.addLayout(BVPlane)
        SelectViewPlanes.addLayout(CVPlane)
        self.ViewRotation.setLayout(SelectViewPlanes)
        
        self.NeuronView= QGroupBox('Electrode view')
                        
        self.ShowNeurons = QCheckBox("Show neurons")
        self.connect(self.ShowNeurons, SIGNAL('stateChanged(int)'), self.setShowNeuronsFlags)
        
        CloseN = QLabel('Closest #')
        self.CloseNeuron = QSpinBox()
        self.CloseNeuron.setRange(0, 1000)
        self.CloseNeuron.setValue(0)
        self.connect(self.CloseNeuron, SIGNAL('valueChanged(int)'), self.plotData)     
        CNum = QVBoxLayout()
        CNum.addWidget(CloseN)
        CNum.addWidget(self.CloseNeuron)
        CNum.addStretch()
        
        self.DistALbl= QLabel('Mx A: NaN')
        self.DistBLbl= QLabel('Mx B: NaN')
        self.DistCLbl= QLabel('Mx C: NaN')
        
        DistComp = QHBoxLayout()
        DistComp.addWidget(self.DistALbl)
        DistComp.addWidget(self.DistBLbl)
        DistComp.addWidget(self.DistCLbl)
        
        self.ElectTools = QHBoxLayout()
        MonkeyN = QLabel('Classification 1')
        self.MonkeyNum = QComboBox()
        self.MonkeyNum.addItem('All')
        self.connect(self.MonkeyNum, SIGNAL('activated(QString)'), self.plotData)
        '''self.MonkeyNum = QSpinBox()
        self.MonkeyNum.setRange(0, 0)
        self.MonkeyNum.setValue(0)
        self.connect(self.MonkeyNum, SIGNAL('valueChanged(int)'), self.plotData)'''
        
        TypeN = QLabel('Classification 2')
        self.TypeNeuron = QComboBox()
        self.TypeNeuron.addItem('All')
        self.connect(self.TypeNeuron, SIGNAL('activated(QString)'), self.plotData)
        
        MNum = QVBoxLayout()
        MNum.addWidget(MonkeyN)
        MNum.addWidget(self.MonkeyNum)
        MNum.addStretch()
        TNum = QVBoxLayout()
        TNum.addWidget(TypeN)
        TNum.addWidget(self.TypeNeuron)
        TNum.addStretch()
        self.ElectTools.addLayout(MNum)
        self.ElectTools.addLayout(TNum)
        
        Neuron= QVBoxLayout()
        Neuron.addWidget(self.ShowNeurons)
        Neuron.addLayout(CNum)
        Neuron.addLayout(DistComp)
        Neuron.addLayout(self.ElectTools)
        
        self.NeuronView.setLayout(Neuron)
        
        View = QVBoxLayout()
        View.addWidget(self.ViewPlane)
        View.addWidget(self.ViewRotation)
        View.addWidget(self.NeuronView)
        View.addStretch(1)
        self.ViewCoordinate.setLayout(View)        
        
        self.Tab.addTab(self.ViewCoordinate, 'View')
        
        self.ExtCoordinate = QGroupBox('External input point')
        EXAPPosLbl = QLabel('AP')
        self.EXAPPos = QDoubleSpinBox()
        self.EXAPPos.setRange(-800.0, 800.0)
        self.EXAPPos.setValue(0)
        self.connect(self.EXAPPos, SIGNAL('valueChanged(double)'), self.plotData)
        EXMLPos = QVBoxLayout()
        EXMLPos.addWidget(EXAPPosLbl)
        EXMLPos.addWidget(self.EXAPPos)
        EXMLPos.addStretch()
        
        EXMLPosLbl = QLabel('ML')
        self.EXMLPos = QDoubleSpinBox()
        self.EXMLPos.setRange(-800.0, 800.0)
        self.EXMLPos.setValue(0)
        self.connect(self.EXMLPos, SIGNAL('valueChanged(double)'), self.plotData)
        EXAPPos = QVBoxLayout()
        EXAPPos.addWidget(EXMLPosLbl)
        EXAPPos.addWidget(self.EXMLPos)
        EXAPPos.addStretch()
        
        EXDPPosLbl = QLabel('Depth')
        self.EXDPPos = QDoubleSpinBox()
        self.EXDPPos.setRange(0, 800.0)
        self.EXDPPos.setDecimals(3)
        self.EXDPPos.setValue(0)
        self.connect(self.EXDPPos, SIGNAL('valueChanged(double)'), self.plotData)
        EXDPPos = QVBoxLayout()
        EXDPPos.addWidget(EXDPPosLbl)
        EXDPPos.addWidget(self.EXDPPos)
        EXDPPos.addStretch()
                
        EXPT = QHBoxLayout()
        EXPT.addLayout(EXAPPos)
        EXPT.addLayout(EXMLPos)
        EXPT.addLayout(EXDPPos)
        
        self.BackTrackElect = QPushButton("Backtrack electrode")
        self.connect(self.BackTrackElect, SIGNAL('clicked()'), self.BackTrackElectFind)
        
        self.SavePoint = QPushButton("Save coordinates")
        self.connect(self.SavePoint, SIGNAL('clicked()'), self.SaveCoordinates)
        
        self.PlaneExternal = QCheckBox("Show linked planes")
        self.connect(self.PlaneExternal, SIGNAL('stateChanged(int)'), self.setLinkedFlag)
        
        self.PlaneCExternal = QCheckBox("Keep C Fixed")
        self.connect(self.PlaneCExternal, SIGNAL('stateChanged(int)'), self.setLinkedCFlag)
        
        self.AddExternal = QCheckBox("add external point")
        self.connect(self.AddExternal, SIGNAL('stateChanged(int)'), self.setExtFlag)
        
        PT = QVBoxLayout()
        PT.addLayout(EXPT)
        PT.addWidget(self.PlaneExternal)
        PT.addWidget(self.PlaneCExternal)
        PT.addWidget(self.BackTrackElect)
        PT.addWidget(self.SavePoint)
        PT.addWidget(self.AddExternal)
        PT.addStretch(1)
        
        self.ExtCoordinate.setLayout(PT)
        
        self.Tab.addTab(self.ViewCoordinate, 'View')
        self.Tab.addTab(self.ExtCoordinate, 'External point')
    
# RADU: Add Interface Elements
        self.canvas.mpl_connect('pick_event', self.on_pick) # binding for click on axes
		
        self.Sp2Coordinate = QGroupBox('External input point')
        Sp2APPosLbl = QLabel('AP')
        self.Sp2APPos = QDoubleSpinBox()
        self.Sp2APPos.setRange(-800.0, 800.0)
        self.Sp2APPos.setValue(0)
        self.connect(self.Sp2APPos, SIGNAL('valueChanged(double)'), self.plotData)
        Sp2MLPos = QVBoxLayout()
        Sp2MLPos.addWidget(Sp2APPosLbl)
        Sp2MLPos.addWidget(self.Sp2APPos)
        Sp2MLPos.addStretch()
        
        Sp2MLPosLbl = QLabel('ML')
        self.Sp2MLPos = QDoubleSpinBox()
        self.Sp2MLPos.setRange(-800.0, 800.0)
        self.Sp2MLPos.setValue(0)
        self.connect(self.Sp2MLPos, SIGNAL('valueChanged(double)'), self.plotData)
        Sp2APPos = QVBoxLayout()
        Sp2APPos.addWidget(Sp2MLPosLbl)
        Sp2APPos.addWidget(self.Sp2MLPos)
        Sp2APPos.addStretch()
        
        Sp2DPPosLbl = QLabel('Depth')
        self.Sp2DPPos = QDoubleSpinBox()
        self.Sp2DPPos.setRange(0, 800.0)
        self.Sp2DPPos.setDecimals(3)
        self.Sp2DPPos.setValue(0)
        self.connect(self.Sp2DPPos, SIGNAL('valueChanged(double)'), self.plotData)
        Sp2DPPos = QVBoxLayout()
        Sp2DPPos.addWidget(Sp2DPPosLbl)
        Sp2DPPos.addWidget(self.Sp2DPPos)
        Sp2DPPos.addStretch()
                
        EXSp2PT = QHBoxLayout()
        EXSp2PT.addLayout(Sp2APPos)
        EXSp2PT.addLayout(Sp2MLPos)
        EXSp2PT.addLayout(Sp2DPPos)
                
        self.Sp2SavePoint = QPushButton("Save coordinates")
        self.connect(self.Sp2SavePoint, SIGNAL('clicked()'), self.SaveSp2Coordinates)
        
        self.Sp2PlaneExternal = QCheckBox("Show linked planes")
        self.connect(self.Sp2PlaneExternal, SIGNAL('stateChanged(int)'), self.setLinkedFlag)
        
        self.Sp2PlaneCExternal = QCheckBox("Keep C Fixed")
        self.connect(self.Sp2PlaneCExternal, SIGNAL('stateChanged(int)'), self.setLinkedCFlag)
        
        self.AddSp2External = QCheckBox("add Sp2 point")
        self.connect(self.AddSp2External, SIGNAL('stateChanged(int)'), self.setSp2Flag)
        
        Sp2PT = QVBoxLayout()
        Sp2PT.addLayout(EXSp2PT)
        Sp2PT.addWidget(self.Sp2PlaneExternal)
        Sp2PT.addWidget(self.Sp2PlaneCExternal)
        Sp2PT.addWidget(self.Sp2SavePoint)
        Sp2PT.addWidget(self.AddSp2External)
        Sp2PT.addStretch(1)
        
        self.Sp2Coordinate.setLayout(Sp2PT)
        
        self.Tab.addTab(self.Sp2Coordinate, 'Sp2 point')
# end RADU        
        self.setExtFlag()
        self.setSp2Flag()
        self.setChamberFlags()
        self.setClipFlag()
	
        self.fs_mon_path = 'C:\Users\The Doctor\Documents\GitHub\Spike2Scripts\sp2pyelcoords.txt'
        self.fs_watcher = QFileSystemWatcher([self.fs_mon_path])
        self.connect(self.fs_watcher, SIGNAL('fileChanged(QString)'), self.getSp2Coords)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.mpl_toolbar)
        
        hbox = QHBoxLayout()
        hbox.addLayout(vbox, 3)
        hbox.addWidget(self.Tab, 1)
        #hbox.addLayout(AllTools,1)
        
        self.main_frame.setLayout(hbox)
        self.setCentralWidget(self.main_frame)
    
    def createStatusBar(self):
        sb = QStatusBar()
        sb.setFixedHeight(18)
        self.setStatusBar(sb)
        self.statusBar().showMessage(self.tr("Ready"))
    
    def PressClip(self):
        msg = "Do you want to clip the MRI (NO UNDO!!!!)?"
        reply = QMessageBox.question(self, 'Clip the MRI (NO UNDO!!!!)?',
                     msg, QMessageBox.Yes, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            NSym = floor(self.NumImages / 2)
            Dist = self.NumImages - (self.AmCut.value() + self.ApCut.value())
            if (Dist - 2 * floor(Dist / 2)) != 0:
                Dist -= 1
            AM = array([0, Dist]) + self.AmCut.value()
            BM = array([-1 * floor(Dist / 2), Dist - floor(Dist / 2)]) + self.BCut.value() + NSym
            CM = array([-1 * floor(Dist / 2), Dist - floor(Dist / 2)]) + self.CCut.value() + NSym
            self.data.MRIData = self.data.MRIData[AM[0]:(AM[1] + 1), BM[0]:(BM[1] + 1), CM[0]:(CM[1] + 1)]
            self.generateSupDataFromMri()
            
            self.ApCut.blockSignals(True)
            self.ApCut.setValue(0)
            self.ApCut.blockSignals(False)
            self.AmCut.blockSignals(True)
            self.AmCut.setValue(0)
            self.AmCut.blockSignals(False)
            self.BCut.blockSignals(True)
            self.BCut.setValue(0)
            self.BCut.blockSignals(False)
            self.CCut.blockSignals(True)
            self.CCut.setValue(0)
            self.CCut.blockSignals(False)
            
            self.plotData()
			
    def on_pick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        #
        
        #pdb.set_trace()
        for aa in range(0,len(self.data.ElectrodeMarkers)):
            if self.data.ElectrodeMarkers[aa].checkinclusion(event.artist):
                idx = aa
                break

        #pdb.set_trace()
        msg0 = 'You have selected file: %s.' % self.data.ElectrodeMarkers[idx].sp2comments[0]
        msg1 = '\n%s' % self.data.ElectrodeMarkers[idx].sp2comments[1]
        msg2 = '\n%s' % self.data.ElectrodeMarkers[idx].sp2comments[2]
        msg3 = '\n%s' % self.data.ElectrodeMarkers[idx].sp2comments[3]
        msg4 = '\n%s' % self.data.ElectrodeMarkers[idx].sp2comments[4]
        QMessageBox.information(self, "Click!", msg0+msg1+msg2+msg3+msg4)
		
    
    def setLinkedCFlag(self):                
        if self.PlaneCExternal.isChecked() or self.Sp2PlaneCExternal.isChecked() is True:
            self.memPos = array([self.AVPos.value(), self.BVPos.value(), self.CVPos.value()])
            self.memRot = array([self.AVRotO.value(), self.BVRotO.value(), self.CVRotO.value()])
            
            self.AVPos.blockSignals(True)
            self.AVPos.setValue(0)
            self.AVPos.setDisabled(True)
            self.AVPos.blockSignals(False)
            self.BVPos.blockSignals(True)
            self.BVPos.setValue(0)
            self.BVPos.setDisabled(True)
            self.BVPos.blockSignals(False)
            self.CVPos.blockSignals(True)
            self.CVPos.setValue(0)
            self.CVPos.setDisabled(True)
            self.CVPos.blockSignals(False)
            
            self.AVPos.setDisabled(True)
            self.BVPos.setDisabled(True)
            self.CVPos.setDisabled(True)
            
            self.PlaneExternal.blockSignals(True)
            self.PlaneExternal.setChecked(False)
            self.PlaneExternal.blockSignals(False)
            self.Sp2PlaneExternal.blockSignals(True)
            self.Sp2PlaneExternal.setChecked(False)
            self.Sp2PlaneExternal.blockSignals(False)       
        else:
            self.AVPos.blockSignals(True)
            self.AVPos.setValue(self.memPos[0])
            self.AVPos.setEnabled(True)
            self.AVPos.blockSignals(False)
            self.BVPos.blockSignals(True)
            self.BVPos.setValue(self.memPos[1])
            self.BVPos.setEnabled(True)
            self.BVPos.blockSignals(False)
            self.CVPos.blockSignals(True)
            self.CVPos.setValue(self.memPos[2])
            self.CVPos.setEnabled(True)
            self.CVPos.blockSignals(False)
            
            self.AVRotO.blockSignals(True)
            self.AVRotO.setValue(self.memRot[0])
            self.AVRotO.setEnabled(True)
            self.AVRotO.blockSignals(False)
            self.BVRotO.blockSignals(True)
            self.BVRotO.setValue(self.memRot[1])
            self.BVRotO.setEnabled(True)
            self.BVRotO.blockSignals(False)
            self.CVRotO.blockSignals(True)
            self.CVRotO.setValue(self.memRot[2])
            self.CVRotO.setEnabled(True)
            self.CVRotO.blockSignals(False)          
        
        self.plotData()
        
    def setLinkedFlag(self):
        if self.PlaneExternal.isChecked() or self.Sp2PlaneExternal.isChecked() is True:
            self.memPos = array([self.AVPos.value(), self.BVPos.value(), self.CVPos.value()])
            self.memRot = array([self.AVRotO.value(), self.BVRotO.value(), self.CVRotO.value()])
            
            self.PlaneCExternal.blockSignals(True)
            self.PlaneCExternal.setChecked(False)
            self.PlaneCExternal.blockSignals(False)
            self.Sp2PlaneCExternal.blockSignals(True)
            self.Sp2PlaneCExternal.setChecked(False)
            self.Sp2PlaneCExternal.blockSignals(False)
            
            self.AVPos.blockSignals(True)
            self.AVPos.setValue(self.data.coordChamber[0])
            self.AVPos.setDisabled(True)
            self.AVPos.blockSignals(False)
            self.BVPos.blockSignals(True)
            self.BVPos.setValue(self.data.coordChamber[1])
            self.BVPos.setDisabled(True)
            self.BVPos.blockSignals(False)
            self.CVPos.blockSignals(True)
            self.CVPos.setValue(self.data.coordChamber[2])
            self.CVPos.setDisabled(True)
            self.CVPos.blockSignals(False)
            
            self.AVRotO.blockSignals(True)
            self.AVRotO.setValue(self.data.rotChamber[1])
            self.AVRotO.setDisabled(True)
            self.AVRotO.blockSignals(False)
            self.BVRotO.blockSignals(True)
            self.BVRotO.setValue(self.data.rotChamber[0])
            self.BVRotO.setDisabled(True)
            self.BVRotO.blockSignals(False)
            self.CVRotO.blockSignals(True)
            self.CVRotO.setValue(self.data.rotChamber[2])
            self.CVRotO.setDisabled(True)
            self.CVRotO.blockSignals(False)
        else:
            self.AVPos.blockSignals(True)
            self.AVPos.setValue(self.memPos[0])
            self.AVPos.setEnabled(True)
            self.AVPos.blockSignals(False)
            self.BVPos.blockSignals(True)
            self.BVPos.setValue(self.memPos[1])
            self.BVPos.setEnabled(True)
            self.BVPos.blockSignals(False)
            self.CVPos.blockSignals(True)
            self.CVPos.setValue(self.memPos[2])
            self.CVPos.setEnabled(True)
            self.CVPos.blockSignals(False)
            
            self.AVRotO.blockSignals(True)
            self.AVRotO.setValue(self.memRot[0])
            self.AVRotO.setEnabled(True)
            self.AVRotO.blockSignals(False)
            self.BVRotO.blockSignals(True)
            self.BVRotO.setValue(self.memRot[1])
            self.BVRotO.setEnabled(True)
            self.BVRotO.blockSignals(False)
            self.CVRotO.blockSignals(True)
            self.CVRotO.setValue(self.memRot[2])
            self.CVRotO.setEnabled(True)
            self.CVRotO.blockSignals(False)
            
        self.plotData()
    
    def setExtFlag(self,pltNow=True):
        if shape(self.data.MRIData)[0] == 0:
            self.ExtCoordinate.setDisabled(True) 
        else:
            self.ExtCoordinate.setEnabled(True)
            if self.AddExternal.isChecked() is True:
                self.EXMLPos.setEnabled(True)
                self.EXAPPos.setEnabled(True)
                self.EXDPPos.setEnabled(True)
                self.PlaneExternal.setEnabled(True)
                self.PlaneCExternal.setEnabled(True)
                #self.Sp2PlaneExternal.setEnabled(True)
                #self.Sp2PlaneCExternal.setEnabled(True)
                self.BackTrackElect.setEnabled(True)
                self.SavePoint.setEnabled(True)
            else:
                self.EXMLPos.setDisabled(True)
                self.EXAPPos.setDisabled(True)
                self.EXDPPos.setDisabled(True)
                self.PlaneExternal.setChecked(False)
                self.PlaneExternal.setDisabled(True)
                self.PlaneExternal.setChecked(False)
                self.PlaneCExternal.setDisabled(True)
                self.PlaneCExternal.setChecked(False)
                #self.Sp2PlaneExternal.setChecked(False)
                #self.Sp2PlaneExternal.setDisabled(True)
                #self.Sp2PlaneExternal.setChecked(False)
                #self.Sp2PlaneCExternal.setDisabled(True)
                #self.Sp2PlaneCExternal.setChecked(False)
                self.BackTrackElect.setDisabled(True)
                self.SavePoint.setDisabled(True)
                
            if pltNow:
                self.plotData()
            
# RADU
    def setSp2Flag(self,pltNow=True):
        if shape(self.data.MRIData)[0] == 0:
            self.Sp2Coordinate.setDisabled(True) 
        else:
            self.Sp2Coordinate.setEnabled(True)
            if self.AddSp2External.isChecked() is True:
		#self.Sp2MLPos.setEnabled(True)
                #self.Sp2APPos.setEnabled(True)
                #self.Sp2DPPos.setEnabled(True)
                self.Sp2PlaneExternal.setEnabled(True)
                self.Sp2PlaneCExternal.setEnabled(True)
                #self.PlaneExternal.setEnabled(True)
                #self.PlaneCExternal.setEnabled(True)
                self.Sp2SavePoint.setEnabled(True)
            else:
                self.Sp2MLPos.setDisabled(True)
                self.Sp2APPos.setDisabled(True)
                self.Sp2DPPos.setDisabled(True)
                self.Sp2PlaneExternal.setChecked(False)
                self.Sp2PlaneExternal.setDisabled(True)
                self.Sp2PlaneExternal.setChecked(False)
                self.Sp2PlaneCExternal.setDisabled(True)
                self.Sp2PlaneCExternal.setChecked(False)
                #self.PlaneExternal.setChecked(False)
                #self.PlaneExternal.setDisabled(True)
                #self.PlaneExternal.setChecked(False)
                #self.PlaneCExternal.setDisabled(True)
                #self.PlaneCExternal.setChecked(False)
                self.Sp2SavePoint.setDisabled(True)
                
            if pltNow:
                self.plotData()
            
#End Radu
    
    def getSp2Coords(self):
        
        thefile = QFile(self.fs_mon_path)
        thefile.open(QIODevice.ReadOnly)
        thisdata = thefile.readData(256)
        if isinstance(thisdata,str):
            thisdata = thisdata.split('\t')
            ap = float(thisdata[0])
            ml = float(thisdata[1])
            dp = float(thisdata[2])
            self.Sp2APPos.setValue(ap)
            self.Sp2MLPos.setValue(ml)
            self.Sp2DPPos.setValue(dp)
            self.plotData()
        thefile.close()
        
    
    def setShowNeuronsFlags(self):
        if self.showNeuronsFlag is True:
            self.showNeuronsFlag = False
            self.CloseNeuron.setDisabled(True)
            self.MonkeyNum.setDisabled(True)
            self.TypeNeuron.setDisabled(True)
        else:
            self.showNeuronsFlag = True
            self.CloseNeuron.setEnabled(True)
            self.MonkeyNum.setEnabled(True)
            self.TypeNeuron.setEnabled(True)
            
        if self.data.MonkeyNum[0] == -1:
            self.MonkeyNum.setDisabled(True)
            self.TypeNeuron.setDisabled(True)
            self.ShowNeurons.setDisabled(True)
            self.CloseNeuron.setDisabled(True)
            
        if self.data.NeuronsType[0] == -1:
            self.TypeNeuron.setDisabled(True)
            self.MonkeyNum.setDisabled(True)
            self.ShowNeurons.setDisabled(True)
            self.CloseNeuron.setDisabled(True)
            
        self.plotData()
        
    def setClipFlag(self):
        if ((shape(self.data.MRIData)[0] == 0) or (self.ClipFlag.isChecked() is False)):
            self.ApCut.setDisabled(True)
            self.AmCut.setDisabled(True)
            self.BCut.setDisabled(True)
            self.CCut.setDisabled(True)
            self.ClipMRIBT.setDisabled(True)
        else:
            self.ApCut.setEnabled(True)
            self.AmCut.setEnabled(True)
            self.BCut.setEnabled(True)
            self.CCut.setEnabled(True)
            self.ClipMRIBT.setEnabled(True)        
        
    def setChamberFlags(self):
        if self.AlignChamber.isChecked() is True:
            self.APos.setEnabled(True)
            self.BPos.setEnabled(True)
            self.CPos.setEnabled(True)
            self.ARotO.setEnabled(True)
            self.BRotO.setEnabled(True)
            self.CRotO.setEnabled(True)
            self.LoadElecPosB.setEnabled(True)
            self.DepthCorr.setEnabled(True)
        else:
            self.APos.setDisabled(True)
            self.BPos.setDisabled(True)
            self.CPos.setDisabled(True)
            self.ARotO.setDisabled(True)
            self.BRotO.setDisabled(True)
            self.CRotO.setDisabled(True)
            self.LoadElecPosB.setDisabled(True)
            self.DepthCorr.setDisabled(True)
            
        if shape(self.data.MRIData)[0] == 0:
            self.MonkeyNum.setDisabled(True)
            self.TypeNeuron.setDisabled(True)
            self.ClipFlag.setDisabled(True)
        else:
            self.ClipFlag.setEnabled(True)
            
        if self.data.MonkeyNum[0] == -1:
            self.MonkeyNum.setDisabled(True)
            self.TypeNeuron.setDisabled(True)
            self.ShowNeurons.setDisabled(True)
            self.CloseNeuron.setDisabled(True)
            
        if self.data.NeuronsType[0] == -1:
            self.TypeNeuron.setDisabled(True)
            self.MonkeyNum.setDisabled(True)
            self.ShowNeurons.setDisabled(True)
            self.CloseNeuron.setDisabled(True)
            
        if self.data.NeuronsType[0] != -1 and self.data.MonkeyNum[0] != -1:
            self.ShowNeurons.setEnabled(True)
                    
        self.AlignChamber.setEnabled(True)
        self.plotData()
        
    def create_menu(self):        
        self.file_menu = self.menuBar().addMenu("&File")
        
        open_file_action = self.create_action("&Open",
            shortcut="Ctrl+O", slot=self.open_file,
            tip="Open pyElectrode file")
        
        load_file_action = self.create_action("&Load MRI",
            shortcut="Ctrl+L", slot=self.load_mri,
            tip="Load MRI file")
        
        save_file_action = self.create_action("&Save",
            shortcut="Ctrl+S", slot=self.save_data,
            tip="Save the data")
        
        export_plot_action = self.create_action("&Export plot",
            shortcut="Ctrl+E", slot=self.save_plot,
            tip="Export the plot")
        
        quit_action = self.create_action("&Quit", slot=self.close,
            shortcut="Ctrl+Q", tip="Close the application")
        
        self.add_actions(self.file_menu,
            (open_file_action , load_file_action, None, save_file_action, export_plot_action, None, quit_action))
        
        self.edit_menu = self.menuBar().addMenu("&Edit")
        
        add_grid_action = self.create_action("&Grid", slot=self.ChangeGridFlag,
            shortcut="Ctrl+G", tip="add a grid")
        
        add_rotA_action = self.create_action("rot 90 &A", slot=self.RotA90,
            shortcut="Ctrl+A", tip="Rotation of 90  deg around A")
        
        add_rotB_action = self.create_action("rot 90 &B", slot=self.RotB90,
            shortcut="Ctrl+B", tip="Rotation of 90  deg around B")
        
        add_rotC_action = self.create_action("rot 90 &C", slot=self.RotC90,
            shortcut="Ctrl+C", tip="Rotation of 90  deg around C")
        
        add_LogFile_action = self.create_action("Set record and comment files", slot=self.selectLogCommentFile,
            tip="Select the filename for log and record")
        
        '''add_chamber_action = self.create_action("Get chamber size", slot=self.getChamberSize,
            tip="get the size of the chamber")'''
        
        self.add_actions(self.edit_menu, (add_grid_action, None, add_rotA_action, add_rotB_action, add_rotC_action, None, add_LogFile_action,))
        
        self.view_menu = self.menuBar().addMenu("&View")
        
        increase_brightness_action = self.create_action("Increase brightness", slot=self.increase_brightness,
            shortcut="Ctrl++", tip="Increase brightness")
        
        decrease_brightness_action = self.create_action("Decrease brightness", slot=self.decrease_brightness,
            shortcut="Ctrl+-", tip="Decrease brightness")
        
        reset_brightness_action = self.create_action("Reset brightness", slot=self.reset_brightness,
            shortcut="Ctrl+R", tip="Reset brightness")
        
        self.add_actions(self.view_menu, (increase_brightness_action, decrease_brightness_action, reset_brightness_action,))

    def save_plot(self):
        path=str(self.data.Directory)
        text, ok = QInputDialog.getText(self, 'File 2 save the plot', 'Enter filename (extensions: {.png or .svg}) :')
        
        if ok:
            if path[-1]==sep:
                file2save=path+str(text)
            else:
                file2save=path+sep+str(text)
                
            self.canvas.print_figure(file2save, dpi=self.dpi)
                         
    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)
                
    def RotA90(self):
        self.data.MRIData = transpose(self.data.MRIData[:, :, ::-1], (0, 2, 1))
        self.plotData()
                
    def RotB90(self):
        self.data.MRIData = transpose(self.data.MRIData[:, :, ::-1], (2, 1, 0))
        self.plotData()
        
    def RotC90(self):
        self.data.MRIData = transpose(self.data.MRIData[:, ::-1, :], (1, 0, 2))
        self.plotData()
        
    def increase_brightness(self):
        self.MeanAddView -= (0.005 * self.MinMaxMRI)
        self.plotData()
        
    def decrease_brightness(self):
        self.MeanAddView += (0.005 * self.MinMaxMRI)
        self.plotData()
        
    def reset_brightness(self):
        self.MeanAddView = 0
        self.plotData()

    def create_action(self, text, slot=None, shortcut=None,
                        icon=None, tip=None, checkable=False,
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action
    
    def ChangeGridFlag(self):
        if self.grid is True:
            self.grid = False
        else:
            self.grid = True
        
        self.plotData()
        
    def SaveCoordinates(self):
        if ((len(self.LogFile) == 0) or (len(self.SaveElectFile) == 0)):
            msg = "Please select a log file and a record file before saving"
            QMessageBox.question(self, 'Select a log file and a record file',
                     msg, QMessageBox.Ok)
        else:
            dlg = StartAddPointDialog()
            if dlg.exec_():
                self.LogSTR=str(dlg.LogComment.toPlainText())
                self.TypeNeuronExt=dlg.BRotO.value()
                self.MonkeyNumExt=dlg.ARotO.value()
                if path.isfile(self.SaveElectFile):
                    tmp=loadtxt(self.SaveElectFile)
                    if len(shape(tmp))==1:
                        numN=2
                    else:
                        numN=shape(tmp)[0]+1
                    tmp=vstack((tmp,array([self.MonkeyNumExt,self.TypeNeuronExt,self.EXMLPos.value(),self.EXAPPos.value(),self.EXDPPos.value()*1000.0,numN])))
                    savetxt(self.SaveElectFile,tmp)
                    f = open(self.LogFile, 'a')
                    f.write(str(numN)+'. '+self.LogSTR+'\n')
                    f.close()
                else:
                    savetxt(self.SaveElectFile,array([[self.TypeNeuronExt,self.MonkeyNumExt,self.EXMLPos.value(),self.EXAPPos.value(),self.EXDPPos.value()*1000.0,1]]))
                    f = open(self.LogFile, 'w')
                    f.write('1. '+self.LogSTR+'\n')
                    f.close()
#Radu
    def SaveSp2Coordinates(self):
        if ((len(self.LogFile) == 0) or (len(self.SaveElectFile) == 0)):
            msg = "Please select a log file and a record file before saving"
            QMessageBox.question(self, 'Select a log file and a record file',
                     msg, QMessageBox.Ok)
        else:
            dlg = StartAddPointDialog()
            if dlg.exec_():
                self.LogSTR=str(dlg.LogComment.toPlainText())
                self.TypeNeuronExt=dlg.BRotO.value()
                self.MonkeyNumExt=dlg.ARotO.value()
                if path.isfile(self.SaveElectFile):
                    tmp=loadtxt(self.SaveElectFile)
                    if len(shape(tmp))==1:
                        numN=2
                    else:
                        numN=shape(tmp)[0]+1
                    tmp=vstack((tmp,array([self.MonkeyNumExt,self.TypeNeuronExt,self.Sp2MLPos.value(),self.Sp2APPos.value(),self.Sp2DPPos.value()*1000.0,numN])))
                    savetxt(self.SaveElectFile,tmp)
                    f = open(self.LogFile, 'a')
                    f.write(str(numN)+'. '+self.LogSTR+'\n')
                    f.close()
                else:
                    savetxt(self.SaveElectFile,array([[self.TypeNeuronExt,self.MonkeyNumExt,self.Sp2MLPos.value(),self.Sp2APPos.value(),self.Sp2DPPos.value()*1000.0,1]]))
                    f = open(self.LogFile, 'w')
                    f.write('1. '+self.LogSTR+'\n')
                    f.close()
#End Radu        
    def getChamberSize(self):
        dlg = StartChamberDialog()
        try:
            dlg.setInitValue(self.data.ChamberSize[0], self.data.ChamberSize[1])
        except:
            self.data.ChamberSize = [20.0, 20.0]
            dlg.setInitValue(self.data.ChamberSize[0], self.data.ChamberSize[1])            
        
        if dlg.exec_():
            w, l = dlg.getValues()
            self.data.ChamberSize[0] = l
            self.data.ChamberSize[1] = w
            if self.PlaneExternal.isChecked() or self.Sp2PlaneExternal.isChecked() is True:
                self.plotData()            
            
    
    def computeRotationMatrix(self, MatIN=array([0.0, 0.0, 0.0], dtype=float), deltaIN=array([0.0, 0.0, 0.0], dtype=float),NoTR=False):
        MatIN = MatIN * pi / 180.0
        
        ''''A = cos(MatIN[1]);
        B = sin(MatIN[1]);
        C = cos(MatIN[0]);
        D = sin(MatIN[0]);
        E = cos(MatIN[2]);
        F = sin(MatIN[2]);
        
        AD = A * D;
        BD = B * D;
        
        RotTot=zeros((3,3),dtype=float)
        
        RotTot[0,0]=C*E
        RotTot[0,1]=-1.0*C*F
        RotTot[0,2]=-1.0*D
        RotTot[1,0]=-1.0*BD * E + A * F
        RotTot[1,1]= BD * F + A * E
        RotTot[1,2]=-1.0*B*C
        RotTot[2,0]=AD * E + B * F
        RotTot[2,1]=-1.0*AD * F + B * E
        RotTot[2,2]=A*C'''
        
        RotX = array([[1, 0, 0], [0, cos(MatIN[1]), sin(MatIN[1])], [0, -sin(MatIN[1]), cos(MatIN[1])]], dtype=float)
        RotY = array([[cos(MatIN[0]), 0, -sin(MatIN[0])], [0, 1, 0], [sin(MatIN[0]), 0, cos(MatIN[0])]], dtype=float)
        RotZ = array([[cos(MatIN[2]), sin(MatIN[2]), 0], [-sin(MatIN[2]), cos(MatIN[2]), 0], [0, 0, 1]], dtype=float)
    
        RotTot=dot(RotX, dot(RotY, RotZ))
        
        if NoTR:
            MatrixTF=RotTot
        else:
            MatrixTF=zeros((4,4))
            
            MatrixTF[0:3,0:3]=RotTot
            MatrixTF[3,3]=1
            MatrixTF[0,3]=deltaIN[0]
            MatrixTF[1,3]=deltaIN[1]
            MatrixTF[2,3]=deltaIN[2]
        
        return MatrixTF
    
    def selectLogCommentFile(self):
        path = QFileDialog.getExistingDirectory(self, "Select saving directory")
        
        if path:
            text, ok = QInputDialog.getText(self, 'Filename 2 save electrode and comment', 'Enter filename (no extension):')

            if ok:
                if path[-1] == sep:
                    self.SaveElectFile = str(path + str(text) + '_ExtElect.txt')
                    self.LogFile = str(path + str(text) + '_ExtElectLog.txt')
                else:
                    self.SaveElectFile = str(path + sep + str(text) + '_ExtElect.txt')
                    self.LogFile = str(path + sep + str(text) + '_ExtElectLog.txt')
                    
                    
    def save_data(self):
        path = QFileDialog.getExistingDirectory(self, "Select saving directory")
        
        if path:
            self.data.Directory = path
            text, ok = QInputDialog.getText(self, 'Filename 2 save the data', 'Enter filename (no extension):')
            
            if ok:
                if path[-1] == sep:
                    file2save = path + str(text) + '.pye'
                else:
                    file2save = path + sep + str(text) + '.pye'
                    
                self.SaveToFile(file2save)
            
    def open_file(self):
        file_choices = "pyElectrode (*.pye)"
        
        path = unicode(QFileDialog.getOpenFileName(self,
                        'Open pyElectrode file', '.',
                        file_choices))
        if path:
            self.data = self.LoadFile(str(path))
            self.generateSupDataFromMri()
            self.plotData()
            

    def load_mri(self):
        path = QFileDialog.getExistingDirectory(self, "Select MRI Directory")
        
        if path:
            path += sep
            text, ok = QInputDialog.getText(self, 'File pattern of the MRI', 'Enter filename pattern:')
            if ok:
                self.data.Directory = path
                self.data.BaseFile = text
                self.data.readDicomFile(self.pb, self.statusBar())
                self.generateSupDataFromMri()
                self.plotData()
            
    def generateSupDataFromMri(self):
            p1 = floor(shape(self.data.MRIData)[0] / 2.0).astype(integer)
            self.StepImage = p1.astype(integer)
            self.NumImages = shape(self.data.MRIData)[0]
            self.range=arange(-p1,p1+1,dtype=float)
            
            self.APos.blockSignals(True)
            self.APos.setValue(self.data.coordChamber[0])
            self.APos.blockSignals(False)
            self.BPos.blockSignals(True)
            self.BPos.setValue(self.data.coordChamber[1])
            self.BPos.blockSignals(False)
            self.CPos.blockSignals(True)
            self.CPos.setValue(self.data.coordChamber[2])
            self.CPos.blockSignals(False)
            
            self.ARotO.blockSignals(True)
            self.ARotO.setValue(self.data.rotChamber[0])
            self.ARotO.blockSignals(False)
            self.BRotO.blockSignals(True)
            self.BRotO.setValue(self.data.rotChamber[1])
            self.BRotO.blockSignals(False)
            self.CRotO.blockSignals(True)
            self.CRotO.setValue(self.data.rotChamber[2])
            self.CRotO.blockSignals(False)
            self.CDepth.blockSignals(True)
            self.CDepth.setValue(self.data.depthCorrection)
            self.CDepth.blockSignals(False)  
            
            sizeIMG = floor(self.NumImages / 2)
            self.APos.setRange(-1 * sizeIMG, sizeIMG)
            self.AVPos.setRange(-1 * sizeIMG, sizeIMG)
            self.BPos.setRange(-1 * sizeIMG, sizeIMG)
            self.BVPos.setRange(-1 * sizeIMG, sizeIMG)
            self.CPos.setRange(-1 * sizeIMG, sizeIMG)
            self.CVPos.setRange(-1 * sizeIMG, sizeIMG) 
            self.ClipRange(False)
            
            self.MinMaxMRI = self.data.MRIData.max() - self.data.MRIData.min()
            
            if shape(self.data.MRIData)[0] != 0:
                self.ClipFlag.setEnabled(True)
            else:
                self.ClipFlag.setDisabled(True)
                
            self.setClipFlag()
            
            if ((self.data.MonkeyNum[0] != -1) and (self.data.NeuronsType[0] != -1)):
                cNorm = cl.Normalize(vmin=0, vmax=shape(self.data.NeuronsType)[0])
                self.MonkeyNum.blockSignals(True)
                self.TypeNeuron.blockSignals(True)
                # Clear the neurons type
                self.MonkeyNum.clear()
                self.TypeNeuron.clear()
                
                # Load the new type
                self.MonkeyNum.addItem('All')
                for ii in self.data.MonkeyNum:
                    self.MonkeyNum.addItem(str(ii))
                
                self.TypeNeuron.addItem('All')
                for ii in self.data.NeuronsType:
                    self.TypeNeuron.addItem(str(ii))
                    
                self.MonkeyNum.blockSignals(False)
                self.TypeNeuron.blockSignals(False)
                self.ShowNeurons.setEnabled(True)
            else:
                cNorm = cl.Normalize(vmin=0, vmax=1)
                self.ShowNeurons.setDisabled(True)
                
            jet = cm = get_cmap('jet') 
            self.scalarMap = cmm.ScalarMappable(norm=cNorm, cmap=jet)
            self.setExtFlag(False)
            self.setSp2Flag(False)      
    
    def ClipRange(self,pltNow=True):
        sizeIMG = floor(self.NumImages / 2)
        self.AmCut.setRange(0, sizeIMG) 
        self.ApCut.setRange(0, sizeIMG)
        deltaClip = floor((self.AmCut.value() + self.ApCut.value()) / 2)
        self.BCut.setRange(-1 * deltaClip, deltaClip)
        self.CCut.setRange(-1 * deltaClip, deltaClip)
        
        if pltNow:
            self.plotData()
        
    
    def LoadElecPos(self):
        file_choices = "text (*.txt)"
        
        path = unicode(QFileDialog.getOpenFileName(self,
                        'Load Electrode file', '.',
                        file_choices))
        if path:
            pathpos = path.rfind(sep)
            
            self.data.ElectrodeDirectory = path[0:(pathpos + 1)]
            self.data.ElectrodeFile = path[(pathpos + 1):]
            self.data.LoadElecPos()
            # Clear the neurons type
            self.MonkeyNum.clear()
            self.TypeNeuron.clear()
            
            # Load the new type
            self.MonkeyNum.addItem('All')
            for ii in self.data.MonkeyNum:
                self.MonkeyNum.addItem(str(ii))
            
            self.TypeNeuron.addItem('All')
            for ii in self.data.NeuronsType:
                self.TypeNeuron.addItem(str(ii))
                
            cNorm = cl.Normalize(vmin=0, vmax=shape(self.data.NeuronsType)[0])
            jet = cm = get_cmap('jet') 
            self.scalarMap = cmm.ScalarMappable(norm=cNorm, cmap=jet)
            self.setChamberFlags()
            
            self.plotData()
        
    def InterpolateRotation(self, RotTMP=array([0.0, 0.0, 0.0], dtype=float), shift=array([127, 127, 127]), shift2=array([0, 0, 0])):
        NewShift=array(shift,copy=True)
        NewShift2=array(shift2,copy=True)
        delta = array([NewShift]).T
        delta[0, 0] = shift[0]
        delta[1, 0] = shift[1]
        delta[2, 0] = shift[2]
        
        if sum(abs(shift2)) > 0:
            adSH = True
        else:
            adSH = False
            
        XMax = self.StepImage
        XMin = -self.StepImage
        dX = self.StepImage
        
        YMax = self.StepImage
        YMin = -self.StepImage
        dY = self.StepImage
        
        ZMax = self.StepImage
        ZMin = -self.StepImage
        dZ = self.StepImage
        
        MatRotAlign = self.computeRotationMatrix(RotTMP,NoTR=True)
                
        if adSH:
            NewShift += NewShift2
        
        XTMP=array((tile(self.range[NewShift[0] + self.StepImage],(self.NumImages,self.NumImages))).reshape(-1))
        YTMP=array((transpose(tile(self.range,(self.NumImages,1)))).reshape(-1))
        ZTMP=array((tile(self.range,(self.NumImages,1))).reshape(-1))
        
        TMPNew2=dot(MatRotAlign, array([XTMP,YTMP,ZTMP],dtype=float) - delta) + delta
        
        # find the boundaries around the studied point
        X0=floor(TMPNew2[0,:]).reshape((self.NumImages,self.NumImages)).astype(integer)
        Y0=floor(TMPNew2[1,:]).reshape((self.NumImages,self.NumImages)).astype(integer)
        Z0=floor(TMPNew2[2,:]).reshape((self.NumImages,self.NumImages)).astype(integer)
        
        X1 = X0 + 1
        Y1 = Y0 + 1
        Z1 = Z0 + 1
        
        # Check if the points are inside the boundaries of the image
        X0[where(X0 < XMin)] = XMin
        X1[where(X1 < XMin)] = XMin
        X0[where(X0 > XMax)] = XMax
        X1[where(X1 > XMax)] = XMax
        
        Y0[where(Y0 < YMin)] = YMin
        Y1[where(Y1 < YMin)] = YMin
        Y0[where(Y0 > YMax)] = YMax
        Y1[where(Y1 > YMax)] = YMax
        
        Z0[where(Z0 < ZMin)] = ZMin
        Z1[where(Z1 < ZMin)] = ZMin
        Z0[where(Z0 > ZMax)] = ZMax
        Z1[where(Z1 > ZMax)] = ZMax
        
        # Compute deltas
        xind = (TMPNew2[0,:].reshape((self.NumImages,self.NumImages))) - X0
        yind = (TMPNew2[1,:].reshape((self.NumImages,self.NumImages))) - Y0
        zind = (TMPNew2[2,:].reshape((self.NumImages,self.NumImages))) - Z0
        
        DataX = squeeze(self.data.MRIData[X0 + dX, Y0 + dY, Z0 + dZ] * (1 - xind) * (1 - yind) * (1 - zind) + self.data.MRIData[X1 + dX, Y0 + dY, Z0 + dZ] * xind * (1 - yind) * (1 - zind) + self.data.MRIData[X0 + dX, Y1 + dY, Z0 + dZ] * (1 - xind) * yind * (1 - zind) + self.data.MRIData[X0 + dX, Y0 + dY, Z1 + dZ] * (1 - xind) * (1 - yind) * (zind) + self.data.MRIData[X1 + dX, Y0 + dY, Z1 + dZ] * (xind) * (1 - yind) * (zind) + self.data.MRIData[X0 + dX, Y1 + dY, Z1 + dZ] * (1 - xind) * (yind) * (zind) + self.data.MRIData[X1 + dX, Y1 + dY, Z0 + dZ] * (xind) * (yind) * (1 - zind) + self.data.MRIData[X1 + dX, Y1 + dY, Z1 + dZ] * (xind) * (yind) * (zind))
        
        # find the boundaries around the studied point
        XTMP=array((transpose(tile(self.range,(self.NumImages,1)))).reshape(-1))
        YTMP=array((tile(self.range[(NewShift[1] + self.StepImage)],(self.NumImages,self.NumImages))).reshape(-1))
        ZTMP=array((tile(self.range,(self.NumImages,1))).reshape(-1))
        
        TMPNew2=dot(MatRotAlign, array([XTMP,YTMP,ZTMP],dtype=float) - delta) + delta
        
        X0=floor(TMPNew2[0,:]).reshape((self.NumImages,self.NumImages)).astype(integer)
        Y0=floor(TMPNew2[1,:]).reshape((self.NumImages,self.NumImages)).astype(integer)
        Z0=floor(TMPNew2[2,:]).reshape((self.NumImages,self.NumImages)).astype(integer)
                
        X1 = X0 + 1
        Y1 = Y0 + 1
        Z1 = Z0 + 1
        
        # Check if the points are inside the boundaries of the image
        X0[where(X0 < XMin)] = XMin
        X1[where(X1 < XMin)] = XMin
        X0[where(X0 > XMax)] = XMax
        X1[where(X1 > XMax)] = XMax
        
        Y0[where(Y0 < YMin)] = YMin
        Y1[where(Y1 < YMin)] = YMin
        Y0[where(Y0 > YMax)] = YMax
        Y1[where(Y1 > YMax)] = YMax
        
        Z0[where(Z0 < ZMin)] = ZMin
        Z1[where(Z1 < ZMin)] = ZMin
        Z0[where(Z0 > ZMax)] = ZMax
        Z1[where(Z1 > ZMax)] = ZMax
        
        # Compute deltas
        xind = (TMPNew2[0,:].reshape((self.NumImages,self.NumImages))) - X0
        yind = (TMPNew2[1,:].reshape((self.NumImages,self.NumImages))) - Y0
        zind = (TMPNew2[2,:].reshape((self.NumImages,self.NumImages))) - Z0
        
        DataY = squeeze(self.data.MRIData[X0 + dX, Y0 + dY, Z0 + dZ] * (1 - xind) * (1 - yind) * (1 - zind) + self.data.MRIData[X1 + dX, Y0 + dY, Z0 + dZ] * xind * (1 - yind) * (1 - zind) + self.data.MRIData[X0 + dX, Y1 + dY, Z0 + dZ] * (1 - xind) * yind * (1 - zind) + self.data.MRIData[X0 + dX, Y0 + dY, Z1 + dZ] * (1 - xind) * (1 - yind) * (zind) + self.data.MRIData[X1 + dX, Y0 + dY, Z1 + dZ] * (xind) * (1 - yind) * (zind) + self.data.MRIData[X0 + dX, Y1 + dY, Z1 + dZ] * (1 - xind) * (yind) * (zind) + self.data.MRIData[X1 + dX, Y1 + dY, Z0 + dZ] * (xind) * (yind) * (1 - zind) + self.data.MRIData[X1 + dX, Y1 + dY, Z1 + dZ] * (xind) * (yind) * (zind))
        
        # find the boundaries around the studied point
        XTMP=array((transpose(tile(self.range,(self.NumImages,1)))).reshape(-1))
        YTMP=array((tile(self.range,(self.NumImages,1))).reshape(-1))
        ZTMP=array((tile(self.range[(NewShift[2] + self.StepImage)],(self.NumImages,self.NumImages))).reshape(-1))
        
        TMPNew2=dot(MatRotAlign, array([XTMP,YTMP,ZTMP],dtype=float) - delta) + delta
        
        X0=floor(TMPNew2[0,:]).reshape((self.NumImages,self.NumImages)).astype(integer)
        Y0=floor(TMPNew2[1,:]).reshape((self.NumImages,self.NumImages)).astype(integer)
        Z0=floor(TMPNew2[2,:]).reshape((self.NumImages,self.NumImages)).astype(integer)
        
        X1 = X0 + 1
        Y1 = Y0 + 1
        Z1 = Z0 + 1
        
        # Check if the points are inside the boundaries of the image
        X0[where(X0 < XMin)] = XMin
        X1[where(X1 < XMin)] = XMin
        X0[where(X0 > XMax)] = XMax
        X1[where(X1 > XMax)] = XMax
        
        Y0[where(Y0 < YMin)] = YMin
        Y1[where(Y1 < YMin)] = YMin
        Y0[where(Y0 > YMax)] = YMax
        Y1[where(Y1 > YMax)] = YMax
        
        Z0[where(Z0 < ZMin)] = ZMin
        Z1[where(Z1 < ZMin)] = ZMin
        Z0[where(Z0 > ZMax)] = ZMax
        Z1[where(Z1 > ZMax)] = ZMax
        
        # Compute deltas
        xind = (TMPNew2[0,:].reshape((self.NumImages,self.NumImages))) - X0
        yind = (TMPNew2[1,:].reshape((self.NumImages,self.NumImages))) - Y0
        zind = (TMPNew2[2,:].reshape((self.NumImages,self.NumImages))) - Z0
        
        DataZ = squeeze(self.data.MRIData[X0 + dX, Y0 + dY, Z0 + dZ] * (1 - xind) * (1 - yind) * (1 - zind) + self.data.MRIData[X1 + dX, Y0 + dY, Z0 + dZ] * xind * (1 - yind) * (1 - zind) + self.data.MRIData[X0 + dX, Y1 + dY, Z0 + dZ] * (1 - xind) * yind * (1 - zind) + self.data.MRIData[X0 + dX, Y0 + dY, Z1 + dZ] * (1 - xind) * (1 - yind) * (zind) + self.data.MRIData[X1 + dX, Y0 + dY, Z1 + dZ] * (xind) * (1 - yind) * (zind) + self.data.MRIData[X0 + dX, Y1 + dY, Z1 + dZ] * (1 - xind) * (yind) * (zind) + self.data.MRIData[X1 + dX, Y1 + dY, Z0 + dZ] * (xind) * (yind) * (1 - zind) + self.data.MRIData[X1 + dX, Y1 + dY, Z1 + dZ] * (xind) * (yind) * (zind))
        
        return DataX, DataY, DataZ
            
    def plotData(self, input= -1, figIN=array([])):
        # Set to the good graph
        if shape(figIN)[0] == 0:
            plA = self.axesA
            plB = self.axesB
            plC = self.axesC
            plD = self.axesD
        else:
            plA = figIN[0]
            plB = figIN[1]
            plC = figIN[2]
            plD = figIN[3]     
        
        # Read the positions for the translations of the calibration
        self.data.coordChamber[0] = self.APos.value()
        self.data.coordChamber[1] = self.BPos.value()
        self.data.coordChamber[2] = self.CPos.value()
        
        self.data.depthCorrection = self.CDepth.value()
        
        # Read the angles for the rotations of the calibration
        self.data.rotChamber[0] = self.BRotO.value()
        self.data.rotChamber[1] = self.ARotO.value()
        self.data.rotChamber[2] = self.CRotO.value()
        
        self.rotView[0] = self.BVRotO.value()
        self.rotView[1] = self.AVRotO.value()
        self.rotView[2] = self.CVRotO.value()
        
        self.CoordView[0] = self.AVPos.value()
        self.CoordView[1] = self.BVPos.value()
        self.CoordView[2] = self.CVPos.value()
        
        if shape(self.data.MRIData)[0] != 0:
            plA.clear()
            plC.clear()
            plD.clear()
            plB.clear()
            plA.set_axis_off()
            plB.set_axis_off()
            plC.set_axis_off()
            plD.set_axis_off()    
            
            # Check if there is an electrode file
            if ((self.data.MonkeyNum[0] != -1) and (self.showNeuronsFlag is True)):
                AllUniqueType=unique(self.data.ElectrodeMonkeyData[:, 1])
                # Load in the raw matrix the neurons corresponding to a specific monkey and a particular type
                if self.TypeNeuron.currentText() != 'All':
                    if self.MonkeyNum.currentText() != 'All':
                        indXElect=intersect1d(nonzero(self.data.ElectrodeMonkeyData[:, 0] == float(self.MonkeyNum.currentText()))[0], nonzero(self.data.ElectrodeMonkeyData[:, 1] == float(self.TypeNeuron.currentText()))[0])
                        UniqueType=array([float(self.TypeNeuron.currentText())])
                        UniquePos=array([squeeze(nonzero(AllUniqueType==float(self.TypeNeuron.currentText()))[0])])
                    else:
                        indXElect=nonzero(self.data.ElectrodeMonkeyData[:, 1] == float(self.TypeNeuron.currentText()))[0]
                        UniqueType=array([float(self.TypeNeuron.currentText())]) 
                        UniquePos=array([squeeze(nonzero(AllUniqueType==float(self.TypeNeuron.currentText()))[0])])              
                else:
                    if self.MonkeyNum.currentText() != 'All':
                        indXElect=nonzero(self.data.ElectrodeMonkeyData[:, 0] == float(self.MonkeyNum.currentText()))[0]
                        UniqueType=unique(self.data.ElectrodeMonkeyData[:, 1])
                        UniquePos=arange(0,shape(AllUniqueType)[0])
                    else:
                        indXElect=arange(0,(shape(self.data.ElectrodeMonkeyData)[0]))
                        UniqueType=unique(self.data.ElectrodeMonkeyData[:, 1])
                        UniquePos=arange(0,shape(AllUniqueType)[0])
                    
                ElectrodeRaw = self.data.ElectrodeData[indXElect, :]   
                ElectrodeRaw += array([[0.0, 0.0, self.data.depthCorrection * (1.0 / self.data.PixSize)]], dtype=float) 
                ElectrodeRaw[:,[0,1,2]]=ElectrodeRaw[:,[2,0,1]]
            else:
                indXElect=(array([]),)
                UniqueType=array([])
                UniquePos=array([])
                ElectrodeRaw = zeros((1, 3)) * NAN
                
            if self.AddExternal.isChecked() is True:
                ExtPT = array([[self.EXDPPos.value() + self.data.depthCorrection, self.EXMLPos.value(), self.EXAPPos.value()]], dtype=float) * (1.0 / self.data.PixSize)
            else:
                ExtPT = zeros((1, 3)) * NAN

# Radu
            if self.AddSp2External.isChecked() is True:
                ExtSp2PT = array([[self.Sp2DPPos.value() + self.data.depthCorrection, self.Sp2MLPos.value(), self.Sp2APPos.value()]], dtype=float) * (1.0 / self.data.PixSize)
            else:
                ExtSp2PT = zeros((1, 3)) * NAN

# End Radu
                
            Electrode = ElectrodeRaw.copy()
            dlt = array([[0, 0, 0]], dtype=float)
            
            if self.AlignChamber.isChecked() is True:
                if sum(self.data.rotChamber * self.data.rotChamber) > 0:                
                    RotTMP = array([0.0, 0.0, 0.0], dtype=float)
                    RotTMP[0] = self.data.rotChamber[0]
                    RotTMP[1] = self.data.rotChamber[1]
                    RotTMP[2] = self.data.rotChamber[2]
                    DataX, DataY, DataZ = self.InterpolateRotation(RotTMP, self.data.coordChamber)
                else:
                    MatRotAlign = eye(3)
                    DataX = squeeze(self.data.MRIData[self.data.coordChamber[0] + self.StepImage, :, :])
                    DataY = squeeze(self.data.MRIData[:, self.data.coordChamber[1] + self.StepImage, :])
                    DataZ = squeeze(self.data.MRIData[:, :, self.data.coordChamber[2] + self.StepImage])
                    
                delta = array([self.data.coordChamber]).T
                delta[0, 0] = -self.data.coordChamber[0]
                delta[1, 0] = -self.data.coordChamber[1]
                delta[2, 0] = -self.data.coordChamber[2]
                
                Electrode[:, 0] += (-delta[0, 0] + self.StepImage)
                Electrode[:, 1] += (-delta[1, 0] + self.StepImage)
                Electrode[:, 2] += (-delta[2, 0] + self.StepImage)
                
                ExtPT[:, 0] += (-delta[0, 0] + self.StepImage)
                ExtPT[:, 1] += (-delta[1, 0] + self.StepImage)
                ExtPT[:, 2] += (-delta[2, 0] + self.StepImage)
        
#Radu
                
                ExtSp2PT[:, 0] += (-delta[0, 0] + self.StepImage)
                ExtSp2PT[:, 1] += (-delta[1, 0] + self.StepImage)
                ExtSp2PT[:, 2] += (-delta[2, 0] + self.StepImage)

#End Radu       
            else:
                MatRotAlign = eye(4)
                
                # compute the transformation to place the electrodes in the MRI reference frame              
                RotTMP = array([0.0, 0.0, 0.0], dtype=float)
                if sum(self.data.rotChamber * self.data.rotChamber) > 0:  
                    RotTMP[0] = self.data.rotChamber[0]
                    RotTMP[1] = self.data.rotChamber[1]
                    RotTMP[2] = self.data.rotChamber[2]
                
                MatRotAlign = self.computeRotationMatrix(RotTMP,self.data.coordChamber)
                
                CorrectCenterMR=zeros((4,1))
                CorrectCenterMR[0:3,0]=self.StepImage
                
                # place the electrode marks in the normal MRI reference frame
                Electrode = transpose(dot(MatRotAlign, vstack((Electrode.T,ones((1,shape(Electrode)[0]))))))
                
                # place the external point in the normal MRI reference frame
                ExtPT = transpose(dot(MatRotAlign, vstack((ExtPT.T,1))))
        
                # place the external point in the normal MRI reference frame
                ExtSp2PT = transpose(dot(MatRotAlign, vstack((ExtSp2PT.T,1))))
                    
                deltaVisual = array([[self.AVPos.value()],[self.BVPos.value()], [self.CVPos.value()]])                    
                
                # Read the angles for the rotations of the view point
                RotViewAngles = array([0.0, 0.0, 0.0], dtype=float)
                RotViewAngles[0] = self.rotView[0]
                RotViewAngles[1] = self.rotView[1]
                RotViewAngles[2] = self.rotView[2]
                    
                MatRotView = self.computeRotationMatrix(RotViewAngles,self.CoordView)
                    
                if self.PlaneExternal.isChecked() is True:
                    delta3 = array([[self.AVPos.value()], [self.BVPos.value()], [self.CVPos.value()]])
                    dlt = array([[self.EXDPPos.value() + self.data.depthCorrection, self.EXMLPos.value(), self.EXAPPos.value()]], dtype=float) * (1.0 / self.data.PixSize)
                    DataX, DataY, DataZ = self.InterpolateRotation(RotViewAngles, squeeze(delta3), squeeze(dlt))
                    delta3+=dlt.T
                elif self.PlaneCExternal.isChecked() is True:
                    dlt = transpose(dot(inv(MatRotView), ExtPT.T))
                    DataX, DataY, DataZ = self.InterpolateRotation(RotViewAngles, squeeze(zeros((1,3))), squeeze(dlt[:,0:3]))
                    delta3 = dlt[:,0:3].T
                elif self.Sp2PlaneExternal.isChecked() is True:
                    delta3 = array([[self.AVPos.value()], [self.BVPos.value()], [self.CVPos.value()]])
                    dlt = array([[self.Sp2DPPos.value() + self.data.depthCorrection, self.Sp2MLPos.value(), self.Sp2APPos.value()]], dtype=float) * (1.0 / self.data.PixSize)
                    DataX, DataY, DataZ = self.InterpolateRotation(RotViewAngles, squeeze(delta3), squeeze(dlt))
                    delta3+=dlt.T
                elif self.Sp2PlaneCExternal.isChecked() is True:
                    dlt = transpose(dot(inv(MatRotView), ExtSp2PT.T))
                    DataX, DataY, DataZ = self.InterpolateRotation(RotViewAngles, squeeze(zeros((1,3))), squeeze(dlt[:,0:3]))
                    delta3 = dlt[:,0:3].T

                else:
                    if sum(RotViewAngles * RotViewAngles) > 0:
                        delta3 = array([[self.AVPos.value()], [self.BVPos.value()], [self.CVPos.value()]])
                        DataX, DataY, DataZ = self.InterpolateRotation(RotViewAngles, squeeze(delta3))
                    else:
                        DataX = squeeze(self.data.MRIData[ self.CoordView[0] + self.StepImage, :, :])
                        DataY = squeeze(self.data.MRIData[:, self.CoordView[1] + self.StepImage, :])
                        DataZ = squeeze(self.data.MRIData[:, :, self.CoordView[2] + self.StepImage])
                    
                    delta3 = deltaVisual
                           
                delta=-1*delta3   
                  
                # Rotate the electrodes marks with the view
                Electrode = transpose(dot(inv(MatRotView), (Electrode.T)))
                Electrode+= tile(transpose(CorrectCenterMR),(shape(Electrode)[0],1))  #  have MRI based coordinates
                Electrode+= tile(transpose(vstack((deltaVisual,0))),(shape(Electrode)[0],1)) # Correct to ensure that the points are moving in the good direction in the view
                
                # Rotate the external point with the view
                ExtPT = transpose(dot(inv(MatRotView), ExtPT.T))
                ExtPT+= transpose(CorrectCenterMR) # Correct to have MRI based coordinates
                ExtPT+= transpose(vstack((deltaVisual,0))) # Correct to ensure that the points are moving in the good direction in the view
                
        # Rotate the external point with the view
                ExtSp2PT = transpose(dot(inv(MatRotView), ExtSp2PT.T))
                ExtSp2PT+= transpose(CorrectCenterMR) # Correct to have MRI based coordinates
                ExtSp2PT+= transpose(vstack((deltaVisual,0))) # Correct to ensure that the points are moving in the good direction in the view
           
            TRBack = dot(eye(3), delta) + self.StepImage
            
            plA.imshow(DataX, cmap=cmm.bone, origin='upper', vmin=self.MeanAddView)
            plA.axis('image')
            autoAxis = plA.axis()
            plA.plot([0, autoAxis[2]], [self.NumImages - TRBack[1] - 1, self.NumImages - TRBack[1] - 1], lw=2, color='r')
            plA.plot([self.NumImages - TRBack[2] - 1, self.NumImages - TRBack[2] - 1], [0, autoAxis[2]], lw=2, color='g')
            
            if self.AlignChamber.isChecked() is True:
                plA.plot([autoAxis[2]*0.975,autoAxis[2],autoAxis[2]*0.975], [self.NumImages - TRBack[1] - 1+(self.NumImages/2.0)*0.0125, self.NumImages - TRBack[1] - 1, self.NumImages - TRBack[1] - 1-(self.NumImages/2.0)*0.0125], lw=2, color='r')
                plA.text(autoAxis[2]*0.975,self.NumImages - TRBack[1] - 1-(self.NumImages/2.0)*0.0125-2,'Ch AP',fontsize=12, color='red',horizontalalignment='right',verticalalignment='bottom')
                plA.plot([self.NumImages - TRBack[2] - 1+(self.NumImages/2.0)*0.0125, self.NumImages - TRBack[2] - 1, self.NumImages - TRBack[2] - 1-(self.NumImages/2.0)*0.0125], [autoAxis[2]*0.975,autoAxis[2],autoAxis[2]*0.975], lw=2, color='g')
                plA.text(self.NumImages - TRBack[2] - 1+(self.NumImages/2.0)*0.0125+2,autoAxis[2]*0.975,'Ch ML',fontsize=12, color='green',horizontalalignment='left',verticalalignment='bottom')
                
            
            if self.CloseNeuron.value() == 0:
                MxPos=-10.0
                for zz in arange(0,shape(UniqueType)[0]):
                    idd=nonzero(self.data.ElectrodeMonkeyData[indXElect, 1] == UniqueType[zz])[0]
                    if sum(shape(idd))>0:
                        MxPos=max(array([max(abs(Electrode[idd, 0]-(self.NumImages - TRBack[0] - 1))),MxPos]))
                        plA.plot(Electrode[idd, 2], Electrode[idd, 1], '.',color=self.scalarMap.to_rgba(UniquePos[zz]))
                        #pdb.set_trace()
                        for aa in idd:
                            self.data.ElectrodeMarkers[indXElect[aa]].plAc.set_xdata(Electrode[aa, 2])
                            self.data.ElectrodeMarkers[indXElect[aa]].plAc.set_ydata(Electrode[aa, 1])
                            self.data.ElectrodeMarkers[indXElect[aa]].plAc.set_color(self.scalarMap.to_rgba(UniquePos[zz]))
                            plA.add_line(self.data.ElectrodeMarkers[indXElect[aa]].plAc)
                
                if MxPos==-10.0:
                    MxPos=NAN
                
                if shape(UniqueType)[0]>0:
                    self.DistALbl.setText('Mx A: '+ str(round(MxPos*self.data.PixSize*100)/100))
            else:
                MxPos=-10.0
                ord = argsort(abs((TRBack[0]) - Electrode[:, 2]))
                for zz in arange(0,shape(UniqueType)[0]):
                    idd=intersect1d(nonzero(self.data.ElectrodeMonkeyData[indXElect, 1] == UniqueType[zz])[0],ord[0:(self.CloseNeuron.value())])
                    if sum(shape(idd))>0:
                        MxPos=max(array([max(abs(Electrode[idd, 0]-(self.NumImages - TRBack[0] - 1))),MxPos]))
                        plA.plot(Electrode[idd, 2], Electrode[idd, 1], '.',color=self.scalarMap.to_rgba(UniquePos[zz]))
                        for aa in idd:
                            #pdb.set_trace()
                            self.data.ElectrodeMarkers[indXElect[aa]].plAc.set_xdata(Electrode[aa, 2])
                            self.data.ElectrodeMarkers[indXElect[aa]].plAc.set_ydata(Electrode[aa, 1])
                            self.data.ElectrodeMarkers[indXElect[aa]].plAc.set_color(self.scalarMap.to_rgba(UniquePos[zz]))
                            plA.add_line(self.data.ElectrodeMarkers[indXElect[aa]].plAc)
                

                
                if MxPos==-10.0:
                    MxPos=NAN
                
                if shape(UniqueType)[0]>0:
                    self.DistALbl.setText('Mx A: '+ str(round(MxPos*self.data.PixSize*100)/100))

            #pdb.set_trace()            
            plA.plot(ExtPT[:, 2], ExtPT[:, 1], 'm.')
            plA.plot(ExtSp2PT[:, 2], ExtSp2PT[:, 1], 'c*')
            
            plB.imshow(DataY, cmap=cmm.bone, origin='upper', vmin=self.MeanAddView)
            plB.axis('image')
            autoAxis = plB.axis()
            plB.plot([0, autoAxis[2]], [self.NumImages - TRBack[0] - 1, self.NumImages - TRBack[0] - 1], lw=2, color='b')
            plB.plot([self.NumImages - TRBack[2] - 1, self.NumImages - TRBack[2] - 1], [0, autoAxis[2]], lw=2, color='g')
            
            if self.AlignChamber.isChecked() is True:
                plB.plot([autoAxis[2]*0.975,autoAxis[2],autoAxis[2]*0.975], [self.NumImages - TRBack[0] - 1+(self.NumImages/2.0)*0.0125, self.NumImages - TRBack[0] - 1, self.NumImages - TRBack[0] - 1-(self.NumImages/2.0)*0.0125], lw=2, color='b')
                plB.text(autoAxis[2]*0.975,self.NumImages - TRBack[0] - 1-(self.NumImages/2.0)*0.0125-2,'Ch AP',fontsize=12, color='b',horizontalalignment='right',verticalalignment='bottom')
                plB.plot([self.NumImages - TRBack[2] - 1+(self.NumImages/2.0)*0.0125, self.NumImages - TRBack[2] - 1, self.NumImages - TRBack[2] - 1-(self.NumImages/2.0)*0.0125], [autoAxis[2]*0.975,autoAxis[2],autoAxis[2]*0.975], lw=2, color='g')
                plB.text(self.NumImages - TRBack[2] - 1+(self.NumImages/2.0)*0.0125+2,autoAxis[2]*0.975,'Ch Depth',fontsize=12, color='green',horizontalalignment='left',verticalalignment='bottom')
            
            
            if self.CloseNeuron.value() == 0:
                MxPos=-10.0
                for zz in arange(0,shape(UniqueType)[0]):
                    idd=nonzero(self.data.ElectrodeMonkeyData[indXElect, 1] == UniqueType[zz])[0]
                    if sum(shape(idd))>0:
                        MxPos=max(array([max(abs(Electrode[idd, 1]-(self.NumImages - TRBack[1] - 1))),MxPos]))
                        plB.plot(Electrode[idd, 2], Electrode[idd, 0], '.',color=self.scalarMap.to_rgba(UniquePos[zz]))
                        for aa in idd:
                            #pdb.set_trace()
                            self.data.ElectrodeMarkers[indXElect[aa]].plBc.set_xdata(Electrode[aa, 2])
                            self.data.ElectrodeMarkers[indXElect[aa]].plBc.set_ydata(Electrode[aa, 0])
                            self.data.ElectrodeMarkers[indXElect[aa]].plBc.set_color(self.scalarMap.to_rgba(UniquePos[zz]))
                            plB.add_line(self.data.ElectrodeMarkers[indXElect[aa]].plBc)
                

                
                if MxPos==-10.0:
                    MxPos=NAN
                    
                if shape(UniqueType)[0]>0:
                    self.DistBLbl.setText('Mx B: '+ str(round(MxPos*self.data.PixSize*100)/100))
            else:
                MxPos=-10.0
                ord = argsort(abs((self.NumImages - TRBack[1] - 1) - Electrode[:, 0]))
                for zz in arange(0,shape(UniqueType)[0]):
                    idd=intersect1d(nonzero(self.data.ElectrodeMonkeyData[indXElect, 1] == UniqueType[zz])[0],ord[0:(self.CloseNeuron.value())])
                    if sum(shape(idd))>0:
                        MxPos=max(array([max(abs(Electrode[idd, 1]-(self.NumImages - TRBack[1] - 1))),MxPos]))
                        plB.plot(Electrode[idd, 2], Electrode[idd, 0], '.',color=self.scalarMap.to_rgba(UniquePos[zz]))
                        for aa in idd:
                            #pdb.set_trace()
                            self.data.ElectrodeMarkers[indXElect[aa]].plBc.set_xdata(Electrode[aa, 2])
                            self.data.ElectrodeMarkers[indXElect[aa]].plBc.set_ydata(Electrode[aa, 0])
                            self.data.ElectrodeMarkers[indXElect[aa]].plBc.set_color(self.scalarMap.to_rgba(UniquePos[zz]))
                            plB.add_line(self.data.ElectrodeMarkers[indXElect[aa]].plBc)
                

                
                if MxPos==-10.0:
                    MxPos=NAN
                
                if shape(UniqueType)[0]>0:
                    self.DistBLbl.setText('Mx B: '+ str(round(MxPos*self.data.PixSize*100)/100))
                
            plB.plot(ExtPT[:, 2], ExtPT[:, 0], 'm.')
            plB.plot(ExtSp2PT[:, 2], ExtSp2PT[:, 0], 'c*')
            
            plC.imshow(DataZ, cmap=cmm.bone, origin='upper', vmin=self.MeanAddView)
            plC.axis('image')
            autoAxis = plC.axis()
            plC.plot([0, autoAxis[2]], [self.NumImages - TRBack[0] - 1, self.NumImages - TRBack[0] - 1], lw=2, color='b')
            plC.plot([self.NumImages - TRBack[1] - 1, self.NumImages - TRBack[1] - 1], [0, autoAxis[2]], lw=2, color='r')
            
            if self.AlignChamber.isChecked() is True:
                plC.plot([autoAxis[2]*0.975,autoAxis[2],autoAxis[2]*0.975], [self.NumImages - TRBack[0] - 1+(self.NumImages/2.0)*0.0125, self.NumImages - TRBack[0] - 1, self.NumImages - TRBack[0] - 1-(self.NumImages/2.0)*0.0125], lw=2, color='b')
                plC.text(autoAxis[2]*0.975,self.NumImages - TRBack[0] - 1-(self.NumImages/2.0)*0.0125-2,'Ch ML',fontsize=12, color='b',horizontalalignment='right',verticalalignment='bottom')
                plC.plot([self.NumImages - TRBack[1] - 1+(self.NumImages/2.0)*0.0125, self.NumImages - TRBack[1] - 1, self.NumImages - TRBack[1] - 1-(self.NumImages/2.0)*0.0125], [autoAxis[2]*0.975,autoAxis[2],autoAxis[2]*0.975], lw=2, color='r')
                plC.text(self.NumImages - TRBack[1] - 1+(self.NumImages/2.0)*0.0125+2,autoAxis[2]*0.975,'Ch Depth',fontsize=12, color='r',horizontalalignment='left',verticalalignment='bottom')
                        
            if self.CloseNeuron.value() == 0:
                MxPos=-10.0
                for zz in arange(0,shape(UniqueType)[0]):
                    idd=nonzero(self.data.ElectrodeMonkeyData[indXElect, 1] == UniqueType[zz])[0]
                    if sum(shape(idd))>0:
                        MxPos=max(array([max(abs(Electrode[idd, 2]-(self.NumImages - TRBack[2]))),MxPos]))
                        plC.plot(Electrode[idd, 1], Electrode[idd, 0], '.',color=self.scalarMap.to_rgba(UniquePos[zz]))
                        for aa in idd:
                            #pdb.set_trace()
                            self.data.ElectrodeMarkers[indXElect[aa]].plCc.set_xdata(Electrode[aa, 1])
                            self.data.ElectrodeMarkers[indXElect[aa]].plCc.set_ydata(Electrode[aa, 0])
                            self.data.ElectrodeMarkers[indXElect[aa]].plCc.set_color(self.scalarMap.to_rgba(UniquePos[zz]))
                            plC.add_line(self.data.ElectrodeMarkers[indXElect[aa]].plCc)
                

                
                if MxPos==-10.0:
                    MxPos=NAN
                    
                if shape(UniqueType)[0]>0:
                    self.DistCLbl.setText('Mx C: '+ str(round(MxPos*self.data.PixSize*100)/100))
            else:
                MxPos=-10.0
                ord = argsort(abs((self.NumImages - TRBack[2] - 1) - Electrode[:, 1]))
                for zz in arange(0,shape(UniqueType)[0]):
                    idd=intersect1d(nonzero(self.data.ElectrodeMonkeyData[indXElect, 1] == UniqueType[zz])[0],ord[0:(self.CloseNeuron.value())])
                    if sum(shape(idd))>0:
                        MxPos=max(array([max(abs(Electrode[idd, 0]-(self.NumImages - TRBack[2] - 1))),MxPos]))
                        plC.plot(Electrode[idd, 1], Electrode[idd, 0], '.',color=self.scalarMap.to_rgba(UniquePos[zz]))
                        for aa in idd:
                            #pdb.set_trace()
                            self.data.ElectrodeMarkers[indXElect[aa]].plCc.set_xdata(Electrode[aa, 1])
                            self.data.ElectrodeMarkers[indXElect[aa]].plCc.set_ydata(Electrode[aa, 0])
                            self.data.ElectrodeMarkers[indXElect[aa]].plCc.set_color(self.scalarMap.to_rgba(UniquePos[zz]))
                            plC.add_line(self.data.ElectrodeMarkers[indXElect[aa]].plCc)
                

                
                if MxPos==-10.0:
                    MxPos=NAN
                    
                if shape(UniqueType)[0]>0:
                    self.DistCLbl.setText('Mx C: '+ str(round(MxPos*self.data.PixSize*100)/100))
                
            plC.plot(ExtPT[:, 1], ExtPT[:, 0], 'm.')
            plC.plot(ExtSp2PT[:, 1], ExtSp2PT[:, 0], 'c*')
                
            if self.grid is True:
                if self.data.PixSize != -1:
                    DeltaDist = 10 / self.data.PixSize
                    distList = union1d(-1 * arange(0, (self.NumImages / 2), DeltaDist), arange(0, (self.NumImages / 2), DeltaDist)) + (self.NumImages / 2)
                    for ds in distList:
                        plA.plot([0, autoAxis[2]], [ds, ds], color='0.6')
                        plA.plot([ds, ds], [0, autoAxis[2]], color='0.6')
                        plB.plot([0, autoAxis[2]], [ds, ds], color='0.6')
                        plB.plot([ds, ds], [0, autoAxis[2]], color='0.6')
                        plC.plot([0, autoAxis[2]], [ds, ds], color='0.6')
                        plC.plot([ds, ds], [0, autoAxis[2]], color='0.6')
            
            
            if self.ClipFlag.isChecked() is True:
                NSym = floor(self.NumImages / 2)
                Dist = self.NumImages - (self.AmCut.value() + self.ApCut.value())
                AM = array([0, Dist]) + self.AmCut.value()
                BM = array([-1 * floor(Dist / 2), Dist - floor(Dist / 2)]) + self.BCut.value() + NSym
                CM = array([-1 * floor(Dist / 2), Dist - floor(Dist / 2)]) + self.CCut.value() + NSym
                plA.plot([AM[0], AM[1], AM[1], AM[0], AM[0]], [BM[0], BM[0], BM[1], BM[1], BM[0]], color='0.9')
                plB.plot([AM[0], AM[1], AM[1], AM[0], AM[0]], [CM[0], CM[0], CM[1], CM[1], CM[0]], color='0.9')
                plC.plot([BM[0], BM[1], BM[1], BM[0], BM[0]], [CM[0], CM[0], CM[1], CM[1], CM[0]], color='0.9')
                        
            autoAxis = plA.axis()
            rec = Rectangle((autoAxis[0], autoAxis[2]), (autoAxis[1] - autoAxis[0]), (autoAxis[3] - autoAxis[2]), fill=False, lw=3, color='b')
            rec = plA.add_patch(rec)
            #rec.set_clip_on(False)
            
            autoAxis = plB.axis()
            rec = Rectangle((autoAxis[0], autoAxis[2]), (autoAxis[1] - autoAxis[0]), (autoAxis[3] - autoAxis[2]), fill=False, lw=3, color='r')
            rec = plB.add_patch(rec)
            #rec.set_clip_on(False)
            
            autoAxis = plC.axis()
            rec = Rectangle((autoAxis[0], autoAxis[2]), (autoAxis[1] - autoAxis[0]), (autoAxis[3] - autoAxis[2]), fill=False, lw=3, color='g')
            rec = plC.add_patch(rec)
            #rec.set_clip_on(False)
            
            self.canvas.draw()
    
    def BackTrackElectFind(self):
        RotViewElect = array([0.0, 0.0, 0.0], dtype=float)
        RotViewElect[0] = self.rotView[0]
        RotViewElect[1] = self.rotView[1]
        RotViewElect[2] = self.rotView[2]
        
        deltaVisual = array([[self.AVPos.value()],[self.BVPos.value()], [self.CVPos.value()]])  
        
        MatRotView = self.computeRotationMatrix(RotViewElect,deltaVisual)
                
        ExtPT = array([[self.AVPos.value()], [self.BVPos.value()], [self.CVPos.value()]])
        ExtPT -=deltaVisual
        
        ExtPT = dot(MatRotView, vstack((ExtPT,1)))
        
        delta = array([[0.0], [0.0], [0.0]])
        MatRotAlign = eye(4)
        
        # compute the transformation to place the electrodes in the MRI reference frame
        if sum(self.data.rotChamber * self.data.rotChamber) > 0:                
            RotTMP = array([0.0, 0.0, 0.0], dtype=float)
            RotTMP[0] = self.data.rotChamber[0]
            RotTMP[1] = self.data.rotChamber[1]
            RotTMP[2] = self.data.rotChamber[2]
            
            delta = array([self.data.coordChamber]).T
            delta[0, 0] = (self.data.coordChamber[0])
            delta[1, 0] = (self.data.coordChamber[1])
            delta[2, 0] = (self.data.coordChamber[2])
            
            MatRotAlign = self.computeRotationMatrix(RotTMP,delta)
        
            
        ExtPT = dot(inv(MatRotAlign), ExtPT)
                
        
        self.EXMLPos.blockSignals(True)
        self.EXMLPos.setValue(ExtPT[1, 0] * self.data.PixSize)
        self.EXMLPos.blockSignals(False)
        
        self.EXAPPos.blockSignals(True)
        self.EXAPPos.setValue(ExtPT[2, 0] * self.data.PixSize)
        self.EXAPPos.blockSignals(False)
        
        self.EXDPPos.blockSignals(True)
        self.EXDPPos.setValue((ExtPT[0, 0] * self.data.PixSize) - self.data.depthCorrection)
        self.EXDPPos.blockSignals(False)
        
        self.plotData()

    def SaveToFile(self, fileSTR):
        f = open(str(fileSTR), 'wb')
        dump(self.data, f, HIGHEST_PROTOCOL)
        f.close()
            
    def LoadFile(self, fileSTR):
        if find(platform, 'win') != -1:
            fileSTR = replace(fileSTR, '/', sep)
            
        f = open(fileSTR, 'rb')
        myNewObject = load(f)
        self.ShowNeurons.setChecked(False)
        f.close()
        return myNewObject
    
class DialogChamber(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 150)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(130, 100, 200, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        
        ARotOLbl = QLabel('Chamber width', Dialog)
        ARotOLbl.setGeometry(QRect(20, 20, 110, 31))
        self.ARotO = QDoubleSpinBox(Dialog)
        self.ARotO.setGeometry(QRect(20, 45, 150, 31))
        self.ARotO.setRange(0, 180)
        self.ARotO.setValue(0)
        self.ARotO.setDecimals(2)
        APlane = QVBoxLayout()
        APlane.addWidget(ARotOLbl)
        APlane.addWidget(self.ARotO)
        APlane.addStretch()
        
        BRotOLbl = QLabel('Chamber length', Dialog)
        BRotOLbl.setGeometry(QRect(180, 20, 110, 31))
        self.BRotO = QDoubleSpinBox(Dialog)
        self.BRotO.setGeometry(QRect(180, 45, 150, 31))
        self.BRotO.setRange(0, 180)
        self.BRotO.setValue(0)
        self.BRotO.setDecimals(2)
        BPlane = QVBoxLayout()
        BPlane.addWidget(BRotOLbl)
        BPlane.addWidget(self.BRotO)
        BPlane.addStretch()
        
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), Dialog.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"), Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)
    
    def setInitValue(self, width=20.0, length=20.0):
        self.ARotO.setValue(length)
        self.BRotO.setValue(width)
        
    def getDimensions(self):
        return self.ARotO.value(), self.BRotO.value()

class StartChamberDialog(QDialog, DialogChamber):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
    def getValues(self):
        return self.getDimensions()    
    
    
class DialogAddPoint(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 300)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(10, 250, 300, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        
        ARotOLbl = QLabel('Classification 1', Dialog)
        ARotOLbl.setGeometry(QRect(20, 10, 110, 31))
        self.ARotO = QSpinBox(Dialog)
        self.ARotO.setGeometry(QRect(20, 35, 150, 31))
        self.ARotO.setRange(1, 1000)
        self.ARotO.setValue(1)
        APlane = QVBoxLayout()
        APlane.addWidget(ARotOLbl)
        APlane.addWidget(self.ARotO)
        APlane.addStretch()
        
        BRotOLbl = QLabel('Classification 2', Dialog)
        BRotOLbl.setGeometry(QRect(180, 10, 110, 31))
        self.BRotO = QSpinBox(Dialog)
        self.BRotO.setGeometry(QRect(180, 35, 150, 31))
        self.BRotO.setRange(1, 1000)
        self.BRotO.setValue(1)
        BPlane = QVBoxLayout()
        BPlane.addWidget(BRotOLbl)
        BPlane.addWidget(self.BRotO)
        BPlane.addStretch()
        
        CommentLbl = QLabel('Comment', Dialog)
        CommentLbl.setGeometry(QRect(10, 70, 110, 31))
        self.LogComment = QTextEdit(Dialog)
        self.LogComment.setAcceptRichText(False)
        self.LogComment.setGeometry(QRect(10, 95, 330, 145))
        
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), Dialog.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"), Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)
    
    def setInitValue(self, width=20.0, length=20.0):
        self.ARotO.setValue(length)
        self.BRotO.setValue(width)
        
    def getDimensions(self):
        return self.ARotO.value(), self.BRotO.value()
		
class Neuron(object):
    def __init__(self):
        self.plAc = Line2D([0],[0],marker = 'D', markersize = 6, picker = 'boolean', pickradius = 6) #plane A tick mark
        self.plBc = Line2D([0],[0],marker = 'D', markersize = 6, picker = 'boolean', pickradius = 6)
        self.plCc = Line2D([0],[0],marker = 'D', markersize = 6, picker = 'boolean', pickradius = 6)
        self.path = ""
        self.sp2comments = array(['','','','','','',''], dtype = str)
    def checkinclusion(self,lineobj):
        if lineobj == self.plAc or lineobj == self.plBc or lineobj == self.plCc:
            return 1
        else:
            return 0
        
class StartAddPointDialog(QDialog, DialogAddPoint):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
    def getValues(self):
        return self.getDimensions()

class MRIData:
    def __init__(self):
        self.MRIData = []
        self.ElectrodeData = []
        self.ElectrodeMonkeyData = []
        self.BaseFile = ''
        self.Directory = ''
        self.ElectrodeFile = ''
        self.ElectrodeDirectory = ''
        self.PixSize = -1.0
        self.SliceSize = -1.0
        self.ChamberSize = [20.0, 20.0]
        self.VoxelSize = [-1.0]
        self.MonkeyNum = [-1.0]
        self.NeuronsType = [-1.0]
        self.depthCorrection = 0.0
        self.coordChamber = array([0, 0, 0])
        self.rotChamber = array([0.0, 0.0, 0.0], dtype=float)
        self.ElectrodeMarkers = []
                
    def get_PGM_bytedata_string(self, arr):
        '''Given a 2D numpy array as input write gray-value image data in the PGM 
        format into a byte string and return it.
        
        arr: single-byte unsigned int numpy array
        note: Tkinter's PhotoImage object seems to accept only single-byte data
        '''
        
        if arr.dtype != uint8:
            raise ValueError
        if len(arr.shape) != 2:
            raise ValueError
        
        # array.shape is (#rows, #cols) tuple; PGM input needs this reversed
        col_row_string = ' '.join(reversed(map(str, arr.shape)))
    
        bytedata_string = '\n'.join(('P5',
                                     col_row_string,
                                     str(arr.max()),
                                     arr.tostring()))
        return bytedata_string
    
    
    def get_PGM_from_numpy_arr(self, arr, window_center, window_width,
                               lut_min=0, lut_max=255):
        '''real-valued numpy input  ->  PGM-image formatted byte string
        
        arr: real-valued numpy array to display as grayscale image
        window_center, window_width: to define max/min values to be mapped to the
                                     lookup-table range. WC/WW scaling is done
                                     according to DICOM-3 specifications.
        lut_min, lut_max: min/max values of (PGM-) grayscale table: do not change
        '''
    
        if isreal(arr).sum() != arr.size:
            raise ValueError
    
        # currently only support 8-bit colors
        if lut_max != 255:
            raise ValueError
    
        if arr.dtype != float64:
            arr = arr.astype(float64)
        
        # LUT-specific array scaling
        # width >= 1 (DICOM standard)
        window_width = max(1, window_width)
        
        wc, ww = float64(window_center), float64(window_width)
        lut_range = float64(lut_max) - lut_min
    
        minval = wc - 0.5 - (ww - 1.0) / 2.0
        maxval = wc - 0.5 + (ww - 1.0) / 2.0
    
        min_mask = (minval >= arr)
        to_scale = (arr > minval) & (arr < maxval)
        max_mask = (arr >= maxval)
        
        if min_mask.any(): arr[min_mask] = lut_min
        if to_scale.any(): arr[to_scale] = ((arr[to_scale] - (wc - 0.5)) / 
                                            (ww - 1.0) + 0.5) * lut_range + lut_min
        if max_mask.any(): arr[max_mask] = lut_max
        
        # round to next integer values and convert to unsigned int
        arr = rint(arr).astype(uint8)
            
        # return PGM byte-data string
        return arr#get_PGM_bytedata_string(arr)
    
    def readDicomFile(self, pb, st):
        FileListRaw = sorted(listdir(self.Directory))
        
        FileList = []
        
        for File in FileListRaw:
            if find(File, self.BaseFile) == 0:
                FileList.append(str(self.Directory + File))
        
        FileList = sorted(FileList)
        
        if len(FileList):
            AllData = array([], dtype=float64)
            h = 0
            pb.show()
            pb.setRange(0, len(FileList))
            st.showMessage("Reading DICOM files...")
            for File in FileList:
                data = dcm.read_file(File)
                arr = data.pixel_array.astype(float)
                    
                if self.SliceSize == -1:
                    self.SliceSize = float(data.SliceThickness)
                    
                if self.VoxelSize[0] == -1:
                    self.VoxelSize = array([float(data.PixelSpacing[0]), float(data.PixelSpacing[1])])
                    
                if self.PixSize == -1:
                    self.PixSize = min(concatenate((array([self.SliceSize]), self.VoxelSize), 0))
                
                # pixel_array seems to be the original, non-rescaled array.
                # If present, window center and width refer to rescaled array
                # -> do rescaling if possible.
                if ('RescaleIntercept' in data) and ('RescaleSlope' in data):
                    intercept = data.RescaleIntercept  # single value
                    slope = data.RescaleSlope          # 
                    arr = slope * arr + intercept
                                    
                if shape(AllData)[0] == 0:
                    AllData = arr
                else:
                    AllData = dstack((AllData, arr))
                pb.setValue(h)
                h += 1
            pb.hide()
            
            if (self.VoxelSize[0] != self.SliceSize):
                AllData=self.NormalizeMRI(AllData,pb,st)
            
            # Fill the MRI to obtain a square MRI
            si = shape(AllData)
            siM = max(si)
            dsi = zeros((3,))
            for ii in arange(0, len(si)):
                if si[ii] < siM:
                    dsi[ii] = siM - si[ii]
            
            if (dsi[0] > 0):
                AllData = concatenate((zeros((floor(dsi[0] / 2), si[1], si[2])), AllData, zeros((dsi[0] - floor(dsi[0] / 2), si[1], si[2]))), axis=0)
                si = shape(AllData)
            
            if (dsi[1] > 0):
                AllData = concatenate((zeros((si[0], floor(dsi[1] / 2), si[2])), AllData, zeros((si[0], dsi[1] - floor(dsi[1] / 2), si[2]))), axis=1)
                si = shape(AllData)
            
            if (dsi[2] > 0):
                AllData = concatenate((zeros((si[0], si[1], floor(dsi[2] / 2))), AllData, zeros((si[0], si[1], dsi[2] - floor(dsi[2] / 2)))), axis=2)
                si = shape(AllData)
            
            if (shape(AllData)[0]-floor(shape(AllData)[0]/2)*2)==0:
                self.MRIData = AllData[:0:-1, :0:-1, :0:-1]
            else:
                self.MRIData = AllData[::-1, ::-1, ::-1]
            
            st.showMessage("Ready")
            
    def NormalizeMRI(self,AllData,pb,st):
        # Need to reshape the data
        FinalX=tile(arange(0,shape(AllData)[0],dtype=float),[shape(AllData)[1],1])
        FinalY=transpose(tile(arange(0,shape(AllData)[1],dtype=float),[shape(AllData)[0],1]))
        X0 = floor(FinalX).astype(integer)
        Y0 = floor(FinalY).astype(integer)
        AllZ=arange(0,(shape(AllData)[2]),(self.VoxelSize[0] / self.SliceSize))
        FinalZ=ones(shape(X0))
        
        AllData2 = zeros((shape(FinalX)[0],shape(FinalX)[1],shape(AllZ)[0]))
        pb.show()
        pb.setRange(0, shape(AllZ)[0])
        st.showMessage("Normalizing data...")
        
        for ii in arange(0, shape(AllZ)[0]):
            Z0 = floor(FinalZ*AllZ[ii]).astype(integer)

            X1 = X0 + 1
            Y1 = Y0 + 1
            Z1 = Z0 + 1
            
            X1[nonzero(X1 > (shape(AllData)[0] - 1))] = (shape(AllData)[0] - 1)
            Y1[nonzero(Y1 > (shape(AllData)[1] - 1))] = (shape(AllData)[1] - 1)
            Z1[nonzero(Z1 > (shape(AllData)[2] - 1))] = (shape(AllData)[2] - 1)
            
            # Compute deltas
            xind = FinalX - X0
            yind = FinalY - Y0
            zind = (FinalZ*AllZ[ii]) - Z0
            
            dX = 0
            dY = 0
            dZ = 0
            
            AllData2[:, :, ii] = squeeze(AllData[X0 + dX, Y0 + dY, Z0 + dZ] * (1 - xind) * (1 - yind) * (1 - zind) + AllData[X1 + dX, Y0 + dY, Z0 + dZ] * xind * (1 - yind) * (1 - zind) + AllData[X0 + dX, Y1 + dY, Z0 + dZ] * (1 - xind) * yind * (1 - zind) + AllData[X0 + dX, Y0 + dY, Z1 + dZ] * (1 - xind) * (1 - yind) * (zind) + AllData[X1 + dX, Y0 + dY, Z1 + dZ] * (xind) * (1 - yind) * (zind) + AllData[X0 + dX, Y1 + dY, Z1 + dZ] * (1 - xind) * (yind) * (zind) + AllData[X1 + dX, Y1 + dY, Z0 + dZ] * (xind) * (yind) * (1 - zind) + AllData[X1 + dX, Y1 + dY, Z1 + dZ] * (xind) * (yind) * (zind))
            
            pb.setValue(ii)
        pb.hide()
                
        return AllData2
        
    def LoadElecPos(self):
        TMPData = loadtxt(self.ElectrodeDirectory + self.ElectrodeFile, dtype=float)
        TMPLog = loadtxt(self.ElectrodeDirectory + self.ElectrodeFile.replace('.txt','Log.txt'), dtype = str,delimiter = ';')

                
        self.ElectrodeData = (1.0 / self.PixSize) * array([TMPData[:, 2], TMPData[:, 3], (TMPData[:, 4] / 1000.0)], dtype=float).T
        self.ElectrodeMonkeyData = array([TMPData[:, 0], TMPData[:, 1]], dtype=float).T
        
        for ii in range(0,TMPData.shape[0]):
            tmpnr = Neuron()
            tmpnr.sp2comments = TMPLog[ii,:].T
            self.ElectrodeMarkers.append(tmpnr)

        #pdb.set_trace()
        self.MonkeyNum = sort(unique(TMPData[:, 0]))
        self.NeuronsType = sort(unique(TMPData[:, 1]))

def main():
    app = QApplication(argv)
    form = Form()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
