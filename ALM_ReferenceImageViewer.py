import sys, os, inspect
from PySide import QtGui, QtCore


images = []
pix = []
scale = []
LOCK = -1
REMOVE = False
ICONPATH = "Dapino-Summer-Holiday-Photo.ico"
TITLE = "Image Viewer"


class ScrollArea(QtGui.QScrollArea):
    """
        Small change to the default scroll area,
        that makes scrolling the mouse wheel re-scale the image
        instead of scrolling around in the window.
        Also, holding left button down while moving the mouse pans the
        image.
    """

    def __init__(self):
        # add all the goodies from QScrollArea
        super(ScrollArea, self).__init__()
        self.scaleF = 1
        self.factor = .10

    # click to focus an image. store this widget. if store, continue
    def wheelEvent(self, e):
        """Define mouse wheel events here"""
        for i in xrange(len(images)):
            if images[i].underMouse():
                if e.delta() < 0:
                    if self.scaleF > 0.19999:
                        self.ZoomOut(images[i], i)
                if e.delta() > 0:
                    if self.scaleF < 2.98999:
                        self.ZoomIn(images[i], i)

    def mouseReleaseEvent(self, e):
    	global REMOVE
    	if self.childAt(e.pos()) and REMOVE == True:
    		self.close()
    		self.destroy()
    		REMOVE = False

    def mouseMoveEvent(self, e):
    	x1, y1 = e.pos().toTuple()
    	x = x1 - self.mousePosX
    	y = y1 - self.mousePosY
    	self.horizontalScrollBar().setValue(self.currentPosH - x)
    	self.verticalScrollBar().setValue(self.currentPosV - y)

    def mousePressEvent(self, e):
    	self.mousePosX, self.mousePosY = e.pos().toTuple()
    	self.currentPosH = self.horizontalScrollBar().value()
    	self.currentPosV = self.verticalScrollBar().value()

    def ResizeImage(self, widget, pix_index):
        image = pix[pix_index]
        if image:
            image = image.scaled(image.size() * self.scaleF, QtCore.Qt.KeepAspectRatio)
        widget.setPixmap(image)

    def ZoomOut(self, image, pix_index):
        print "Zooming Out"
        self.scaleF -= self.factor
        self.ResizeImage(image, pix_index)
        print self.scaleF

    def ZoomIn(self, image, pix_index):
        print "Zooming In"
        self.scaleF += self.factor
        self.ResizeImage(image, pix_index)
        print self.scaleF
        

class Window(QtGui.QWidget):

    def __init__(self):
        # add all the goodies from QWidget
        super(Window, self).__init__()

        # support for custom right click menu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.ShowMenu)

        self.vbox = QtGui.QVBoxLayout(self)
        self.setLayout(self.vbox)
        self.scaleF = 1
        self.factor = .10
        self.opacity = self.windowOpacity()

        # image grid
        self.mainGroup = QtGui.QGroupBox("Right-click to load an image", self)
        self.grid = QtGui.QGridLayout(self.mainGroup)
        self.mainGroup.setLayout(self.grid)

        # control panel
        self.cpGroup = QtGui.QGroupBox("Control Panel", self)
        self.cpLayout = QtGui.QVBoxLayout()
        self.cpGroup.setLayout(self.cpLayout)

        self.vbox.addWidget(self.mainGroup)
        self.vbox.addWidget(self.cpGroup)

        # adjust properties after adding widgets/layouts to the layout
        self.mainGroup.setAlignment(QtCore.Qt.AlignRight)
        self.mainGroup.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        self.cpGroup.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Maximum))
        self.grid.setSpacing(1)

        self.InitUI()

    def InitUI(self):

        # build the main window and center on the screen
        # then show
        self.setGeometry(300, 300, 500, 500)
        self.InitCenter()
        self.InitOpacitySlider()
        self.InitCheckbox()
        QtGui.QToolTip.setFont(QtGui.QFont("SansSerif", 10))
        self.setWindowTitle(TITLE)
        self.setWindowIcon(QtGui.QIcon(ICONPATH))
        self.show()

    def InitOpacitySlider(self):
    	lbl = QtGui.QLabel("Opacity Slider")
        sld = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.cpLayout.addWidget(lbl)
        self.cpLayout.addWidget(sld)
        sld.setMinimum(15) # don't go too low otherwise we lose the window!
        sld.setValue(100)  # init slider to max on load

        # when slider value is changed, update the image opacity
        sld.valueChanged.connect(self.ChangeOpacity)

    def ChangeOpacity(self, i):
        self.setWindowOpacity(self.opacity * i/100)

    def InitCheckbox(self):
        """Define checkboxes here"""
        stayOnTop = QtGui.QCheckBox("Stay On Top?", self)
        stayOnTop.move(100, 20)

        # call StayOnTop() when clicked
        stayOnTop.stateChanged.connect(self.StayOnTop)
        self.cpLayout.addWidget(stayOnTop)

    def StayOnTop(self):
        """set window lock"""
        global LOCK
        LOCK = -LOCK
        if LOCK == 1:
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
            self.show()

    def LoadImage(self):
        try:
            fname, _ = QtGui.QFileDialog.getOpenFileName(self, "Open Image", os.getcwd())
            if fname[len(fname) - 3:] in ("jpg", "png", "tif", "gif", "bmp"):
                f = open(fname, 'r')
                self.ShowImage(QtGui.QImage(f.name))
                f.close()
            else:
                QtGui.QMessageBox.warning(self,
                    "Error!",
                    "I cannot open that!")
        except IOError:
            pass

    def ShowImage(self, image):
        """Create a pixmap from an image on disk"""
        pm = QtGui.QPixmap.fromImage(image)
        lbl = QtGui.QLabel()
        scroller = ScrollArea()

        scroller.setWidget(lbl)
        self.grid.addWidget(scroller)

        lbl.setPixmap(pm)
        lbl.setScaledContents(False)  # leave as False so the images dont break!

        scroller.setBackgroundRole(QtGui.QPalette.Dark)
        scroller.setWidgetResizable(True)

        # store the label and pixmap at the same time,
        # so the index matches
        images.append(lbl)
        pix.append(pm)

    def RemoveImage(self):
    	global REMOVE
    	REMOVE = True

    def ShowMenu(self, pos):
        """Define Context Menu Actions here"""
        cMenu = QtGui.QMenu(self)

        # Exit
        exitAct = QtGui.QAction("Exit", cMenu)
        exitAct.triggered.connect(self.close)

        # Load Image
        loadAct = QtGui.QAction("Load Image", cMenu)
        loadAct.triggered.connect(self.LoadImage)

        # Remove Image
        removeAct = QtGui.QAction("Remove Image", cMenu)
        removeAct.triggered.connect(self.RemoveImage)

        # add actions to menu - order matters
        cMenu.addAction(loadAct)
        cMenu.addAction(removeAct)
        cMenu.addAction(exitAct)

        # .popup is asynchronous - .exec_ is blocking
        cMenu.popup(self.mapToGlobal(pos))

    def InitCenter(self):
        """Center the window on load"""
        qr = self.frameGeometry()
        center = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(center)
        self.move(qr.topLeft())

    # - KEYPRESS EVENTS
    def keyPressEvent(self, e):
        """Define What Keys Do Here"""
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

    def Help(self, obj):
        """Simple method to find properties of any object

            For when I can't find the docs fast enough
        """
        for prop, val in inspect.getmembers(obj):
            print prop, ": ", val, "\n"

def main():
    app = QtGui.QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
