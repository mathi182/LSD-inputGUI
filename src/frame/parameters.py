"""
.. module:: parameters

.. codeauthor::  Mathieu Gagnon <mathieu.gagnon.10@ulaval.ca>

:Created on: 2010-08-10

"""

from PyQt4 import QtCore
from PyQt4 import QtGui
import Definitions

class Ui_parameters(object):
    '''
    This class is an automatically generated python file using the pyuic4 program and .ui file generated by Qt_Designer.
    This class is the mainWindow's tab containing the parameters information of the simulation.
    '''
    def __init__(self, parent):
        '''
        Constructor
        :param parent: application's mainWindow
        '''
        self.parent = parent
        
    def setupUi(self, parameters):
        """
        Creates the widgets that will be displayed on the frame.
        
        :param parameters: Visual frame.
        :type parameters: :class:`.MyWidgetTabParameters`
        """
        parameters.setObjectName("parameters")
        #Creating Layouts
        #Creating Layout for theAdd and Delete Buttons
        self.layoutControls = QtGui.QHBoxLayout()
        #Creating mainLayout
        self.mainLayout = QtGui.QVBoxLayout()
        
        #Label at top of the widget
        self.tableLabel = QtGui.QLabel()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.tableLabel.setFont(font)
        self.tableLabel.setObjectName("tableLabel")
        
        #Creating TableView
        self.tableView = ArrowsAwareTableView()
        self.tableView.setObjectName("tableView")
        # My preferences
        self.tableView.setDragEnabled(True)
        self.tableView.setAcceptDrops(True)
        self.tableView.setDropIndicatorShown(True)
        self.tableView.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.tableView.setDefaultDropAction(QtCore.Qt.DropAction(QtCore.Qt.MoveAction))
        self.tableView.setDragDropOverwriteMode(True)
        self.tableView.horizontalHeader().setSortIndicatorShown(True)
        self.tableView.setSortingEnabled(True)
        
        #Adding child widgets/layouts to the main layout
        self.mainLayout.addWidget(self.tableLabel)
        self.mainLayout.addWidget(self.tableView)
        self.mainLayout.addLayout(self.layoutControls)
        
        #Buttons Add and Delete
        self.add = QtGui.QPushButton()
        self.add.setFixedSize(QtCore.QSize(77,25))
        self.add.setObjectName("add")
        self.delete = QtGui.QPushButton()
        self.delete.setFixedSize(QtCore.QSize(77,25))
        self.delete.setObjectName("delete")
        #Adding these widgets to their layout
        self.layoutControls.addWidget(self.add)
        self.layoutControls.addWidget(self.delete)  
        self.layoutControls.addItem(QtGui.QSpacerItem(100, 30, QtGui.QSizePolicy.Expanding))


        #Setting MainLayout to environment
        parameters.setLayout(self.mainLayout)
        #Setting the spacings
        self.layoutControls.setSpacing(10)
        #Setting the margins
        self.mainLayout.setMargin(50)
        #Pyuic4 auto-generated code and connections
        self.retranslateUi(parameters)
        QtCore.QMetaObject.connectSlotsByName(parameters)
        
        self.connect(self.add, QtCore.SIGNAL("clicked()"), self.addRow)
        self.connect(self.delete, QtCore.SIGNAL("clicked()"), self.deleteRow)
        self.connect(self.tableView, QtCore.SIGNAL("deleteParam()"), self.deleteRow)
        
    def retranslateUi(self, parameters):
        '''
        Function allowing naming of the different labels regardless of app's language.
        
        :param Form: Visual frame to translate.
        :type Form: :class:`.MyWidgetTabParameters`
        '''
        parameters.setWindowTitle(QtGui.QApplication.translate("parameters", "Population", None, QtGui.QApplication.UnicodeUTF8))
        self.tableLabel.setText(QtGui.QApplication.translate("parameters", "Baseline parameters :", None, QtGui.QApplication.UnicodeUTF8))
        self.add.setText(QtGui.QApplication.translate("parameters", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.delete.setText(QtGui.QApplication.translate("parameters", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        
    def deleteRow(self):
        '''
        Delete parameter(s) in model
        '''
        if len(self.tableView.selectedIndexes()) > 1:
            self.tableView.model().specialRemove([index.row() for index in self.tableView.selectedIndexes()])
            self.tableView.clearSelection()
        
        elif len(self.tableView.selectedIndexes()):
            index = self.tableView.selectedIndexes()[0]
            self.tableView.model().removeRow(index.row(),self.tableView.rootIndex())
            self.tableView.clearSelection()
            
    def addRow(self):
        '''
        Add parameter in model
        '''
        newWidget = Widget_AddVar(self)
        newWidget.exec_()
        #If user cancelled the operation, do nothing
        if not newWidget.result():
            return
        
        #Else user entered parameter information, so create new parameter
        newVarName = newWidget.lineEditName.text()
        newType = newWidget.comboBoxType.currentText()
        if newWidget.radioButtonScalar.isChecked():
            newValue = [newWidget.lineEditScalar.text()]
        else:
            newValue = [ item.text() for item in [newWidget.listWidgetVector.item(i) for i in range(newWidget.listWidgetVector.count())]]
        
        if self.tableView.selectedIndexes() and len(self.tableView.selectedIndexes()) == 1:
            self.tableView.model().insertRow(self.tableView.selectedIndexes()[0].row(), self.tableView.rootIndex(), newVarName, newValue, newType)
            return
       
        self.tableView.model().insertRow(self.tableView.model().rowCount()-1, self.tableView.rootIndex(), newVarName, newValue, newType)
    
class Widget_AddVar(QtGui.QDialog):
    '''
    Dialog allowing the user to create a new Parameter
    '''
    def __init__(self, parent):
        '''
        Constructor.
        
        :param parent: parameters Tab
        '''
        QtGui.QDialog.__init__(self, parent)
        self.resize(450, 340)
        self.setObjectName("paramManager")
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(10, 300, 430, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        
        self.labelName = QtGui.QLabel("Name : ", self)
        self.labelName.setGeometry(QtCore.QRect(20, 20, 100, 22))
        
        self.lineEditName = QtGui.QLineEdit(self)
        self.lineEditName.setGeometry(QtCore.QRect(150, 20, 150, 22))
        
        self.labelType = QtGui.QLabel("Type : ", self)
        self.labelType.setGeometry(QtCore.QRect(20, 50, 100, 22))
        
        self.comboBoxType = QtGui.QComboBox(self)
        self.comboBoxType.setGeometry(QtCore.QRect(150, 50, 150, 22))
        self.comboBoxType.addItems(Definitions.baseTypes)
        self.radioButtonScalar = QtGui.QRadioButton("Scalar", self)
        self.radioButtonScalar.setGeometry(QtCore.QRect(20, 80, 100, 22))
        
        self.radioButtonVector = QtGui.QRadioButton("Vector", self)
        self.radioButtonVector.setGeometry(QtCore.QRect(150, 80, 100, 22))
        
        self.lineEditScalar = QtGui.QLineEdit(self)
        self.lineEditScalar.setGeometry(QtCore.QRect(30, 130, 100, 22))
        
        self.listWidgetVector = QtGui.QListWidget(self)
        self.listWidgetVector.setGeometry(QtCore.QRect(160, 130, 140, 100))
        
        self.pushButtonAdd = QtGui.QPushButton("Add", self)
        self.pushButtonAdd.setGeometry(QtCore.QRect(320, 150, 100, 25))
        
        self.pushButtonDelete = QtGui.QPushButton("Delete", self)
        self.pushButtonDelete.setGeometry(QtCore.QRect(320, 185, 100, 25))
        
        self.connect(self.radioButtonScalar, QtCore.SIGNAL("toggled(bool)"), self.rbManager)
        self.connect(self.pushButtonAdd, QtCore.SIGNAL("clicked()"), self.addData)
        self.connect(self.pushButtonDelete, QtCore.SIGNAL("clicked()"), self.removeData)
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.commitParameter)
        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        
        self.radioButtonScalar.setChecked(True)
        self.setWindowTitle(QtGui.QApplication.translate("paramManager", "Add parameter", None, QtGui.QApplication.UnicodeUTF8))

    def rbManager(self, state):
        '''
        Enables or disables widgets depending of the currently selected radio Button.
        
        :param state: Boolean telling the new state od the widget.
        '''
        self.lineEditScalar.setEnabled(state)
        self.listWidgetVector.setDisabled(state)
        self.pushButtonAdd.setDisabled(state)
        self.pushButtonDelete.setDisabled(state)
        
    def addData(self):
        '''
        Asks the user to enter a value if we are in vector mode.
        '''
        result, status = QtGui.QInputDialog.getText(self, "Enter Data", "Value : ")
        if status:
            self.listWidgetVector.addItem(result)
    
    def removeData(self):
        '''
        Removes a value from the list if we are in vector mode.
        '''
        self.listWidgetVector.takeItem(self.listWidgetVector.currentRow())
        
    def commitParameter(self):
        '''
        Checks if all fields were entered before closing dialog.
        '''
        if not self.lineEditName.text():
            QtGui.QMessageBox.warning(self, "Empty Name!", "Cannot add a parameter with an empty name!")
            return
        elif self.radioButtonScalar.isChecked():
            if not self.lineEditScalar.text():
                QtGui.QMessageBox.warning(self, "Empty Value!", "Cannot add a parameter with an empty value!")
                return
        elif not self.listWidgetVector.count():
            QtGui.QMessageBox.warning(self, "Empty Value!", "Cannot add a vector parameter with no value")
            return
            
        self.accept()

class ArrowsAwareTableView(QtGui.QTableView):
    '''
    This class slightly modify Qt's QTableView class.
    Navigating the TableView with arrows will generate the same signal as if the user was using the mouse buttons.
    This way, previews will be generated when the user clicks in the table view.
    '''
    def __init__(self):
        '''
        Constructor 
        '''
        QtGui.QTableView.__init__(self)
        
    def keyPressEvent(self,event):
        '''
        Reimplementation of QTableView's keyPressEvent function.
        
        :param event: see QTableView's documentation for more information
        '''
        super(ArrowsAwareTableView, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Delete and not self.state() == QtGui.QAbstractItemView.EditingState:
            self.emit(QtCore.SIGNAL("deleteParam()"))
