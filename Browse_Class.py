import ftplib
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import stat

qt_app = QApplication(sys.argv)
 
class browse_Class(QWidget):

    #Constructor
    def __init__(self, ftpObj):

        #Initialize the object as a QWidget
        QWidget.__init__(self)

        #Get our ftp object
        self.ftp = ftpObj
        self.baseDir = os.getcwd() #Store based directory

        #Setup the window
        self.setup_Window(800, 400, 'FTP: Browse Files', QIcon(self.baseDir + '\\FolderIcon.png'))

        #Create Local and server path text boxes
        self.localPathLineEdit = QLineEdit(self)
        self.serverPathLineEdit = QLineEdit(self)

        #Create Local and server path labels
        self.create_Path_Labels()
        self.create_Path_Line_Edits()

        #Create Local and server list widgets for browsing
        self.localListWidget = QListWidget(self)
        self.serverListWidget = QListWidget(self)

        #Initialize the list widgets
        self.refresh_Local_Files_List_Widget()
        self.refresh_Server_Files_List_Widget()

        #Initialize buttons
        self.create_Up_Dir_Btns()
        self.create_Change_To_Curr_Dir_Btns()
        self.create_Change_Dir_Btns()
        self.create_Permissions_Btns()
        self.create_Delete_Dir_Btns()

        #Connect server click and double click events to navigation and setting the path
        self.serverListWidget.itemClicked.connect(self.set_Server_Path)
        self.serverListWidget.itemDoubleClicked.connect(self.server_Navigate)

        #Connect local click and double click events to navigation and setting the path
        self.localListWidget.itemClicked.connect(self.set_Local_Path)
        self.localListWidget.itemDoubleClicked.connect(self.local_Navigate)
    
    #*********************
    #shows and runs the BrowseFiles widget
    #*********************
    def run(self):
        self.show() #Show the form
        qt_app.exec_() #Run the Qt application

    #*********************
    #sets up the window 
    #width is the desired width of the window
    #height is the desired height of the window
    #title is the desired title that will display along the top of the window
    #icon is the QIcon to display along the top of the window
    #*********************
    def setup_Window(self, width, height, title, icon):
        self.setWindowTitle(title) #Set the title
        self.setWindowIcon(icon) #Set the icon
        self.setFixedSize(width, height) #Set the width/height

    #*********************
    #creates the file path labels for the server and local files
    #*********************
    def create_Path_Labels(self):
        # The label for the local path
        self.localPathLabel = QLabel('Local Path:', self)
        self.localPathLabel.move(110, 12)

        # The label for the server path
        self.serverPathLabel = QLabel('Server Path:', self)
        self.serverPathLabel.move(455, 12)

    #*********************
    #moves the file path line edit (text boxes) for the server and local files
    #*********************
    def create_Path_Line_Edits(self):
        # The line edit for the local path
        self.localPathLineEdit.move(170, 10)

        # The line edit for the server path
        self.serverPathLineEdit.move(525,10)

    #*********************
    #creates the delete directory buttons for both local and server
    #*********************
    def create_Delete_Dir_Btns(self):
        self.deleteLocalDirBtn = QPushButton('Delete\nDirectory', self)
        self.deleteLocalDirBtn.setIcon(QIcon('img\\FolderDelete.png'))
        self.deleteLocalDirBtn.setToolTip('Delete directory')
        self.deleteLocalDirBtn.move(10, 145)

        #TODO: delete local directory
        #self.deleteLocalDirBtn.clicked.connect(self.delete_Local_Dir)

        self.deleteServerDirBtn = QPushButton('Delete\nDirectory', self)
        self.deleteServerDirBtn.setIcon(QIcon('img\\FolderDelete.png'))
        self.deleteServerDirBtn.setToolTip('Delete directory')
        self.deleteServerDirBtn.move(715, 145)
        self.deleteServerDirBtn.clicked.connect(self.delete_Server_Dir)


    #*********************
    #Deletes a directory from the server
    #RETURN is False if error occurs else true
    #*********************
    def delete_Server_Dir(self):

        # TODO: FIX THIS, this is broken
        dirName = self.serverPathLineEdit.text().split('/')[-1];

        try:
            if self.dir_Exists(dirName): #if the directory exists
                self.ftp.rmd(dirName) #remove the directory
                print("Directory: ", dirName, " deletion successful ") #print successful deletion message
                self.refresh_Server_Files_List_Widget()
            else: #otherwise, the directory does not exist
                print("Directory: ", dirName, " does not exist") #print directory DNE message
                return False
        except ftplib.all_errors: #an error occurred
            print("Directory: ", dirName, " deletion failed") #print failed deletion message
            return False #return false indicates deletion did not occur
        return True
  

    #*********************
    #Checks if directory exists (in current location)
    #dir is the directory you want to check for existence
    #THIS ASSUMES YOU ARE IN THE CORRECT DIR
    #RETURN is True if the directory exists, False if it does not
    #*********************
    def dir_Exists(self, dirName):

        # TODO: FIX THIS, this only works in certain cases

        fileList = [] #list object to store all files
        self.ftp.retrlines('LIST', fileList.append) #append to list
    
        for file in fileList: #for every file/directory in the list (current location)
            if file.split()[-1] == dirName and file.upper().startswith('D'): # If the name matches and is a directory
                return True #directory found, return True
        return False #otherwise, directory not found, return False

    #*********************
    #creates the permissions buttons for both local and server
    #*********************
    def create_Permissions_Btns(self):
        self.rwxLocalBtn = QPushButton('RWX', self)
        self.rwxLocalBtn.setToolTip('Read-Write-Execute')
        self.rwxLocalBtn.move(10,195)
        self.rwxLocalBtn.clicked.connect(lambda: self.set_Local_Permissions('','rwx'))

        self.rwLocalBtn = QPushButton('RW', self)
        self.rwLocalBtn.setToolTip('Read-Write')
        self.rwLocalBtn.move(10,220)
        self.rwLocalBtn.clicked.connect(lambda: self.set_Local_Permissions('','rw-'))

        self.rwxServerBtn = QPushButton('RWX', self)
        self.rwxServerBtn.setToolTip('Read-Write-Execute')
        self.rwxServerBtn.move(715,195)
        self.rwxServerBtn.clicked.connect(lambda: self.set_Remote_Permissions('','rwx'))

        self.rwServerBtn = QPushButton('RW', self)
        self.rwServerBtn.setToolTip('Read-Write')
        self.rwServerBtn.move(715,220)
        self.rwServerBtn.clicked.connect(lambda: self.set_Remote_Permissions('','rw-'))

        self.rServerBtn = QPushButton('R', self)
        self.rServerBtn.setToolTip("Read-Only")
        self.rServerBtn.move(715,245)
        self.rServerBtn.clicked.connect(lambda: self.set_Remote_Permissions('','r--'))

    #*********************
    #set remote file permissions
    #*********************
    def set_Remote_Permissions(self, path, perm):
        permNum = self.switch_Remote_Perm.get(perm, '0000')
        try:
            self.ftp.sendcmd('SITE CHMOD {0} {1}'.format(permNum, self.serverPathLineEdit.text()))
        except ftplib.all_errors:
            return None

    #*********************
    #set local file permissions
    #*********************
    def set_Local_Permissions(self, path, perm):
        permNum = self.switch_Remote_Perm.get(perm, '0000')

        #TODO: This does not work yet

    #*********************
    #remote permissions dictionary
    #*********************
    switch_Remote_Perm = {
        "rwx": "0777", #Read, write, execute
        "rw-": "0666", #Read, write
        "r--": "0444", #Read only
        }

    #*********************
    #refresh the list widget for the local navigation
    #*********************
    def refresh_Local_Files_List_Widget(self):
        self.localListWidget.clear()
        self.localListWidget.setFixedSize(250, 300)

        localFiles = os.listdir()
 
        for localFile in localFiles:
            localItem = QListWidgetItem(localFile)

            if os.path.isdir(localFile):
                localItem.setIcon(QIcon(self.baseDir + '\\img\\FolderIcon.png'))
            elif os.path.isfile(localFile):
                localItem.setIcon(QIcon(self.baseDir + '\\img\\FileIcon.png'))

            self.localListWidget.addItem(localItem)

        self.localListWidget.move(100, 50)

    #*********************
    #refresh the list widget for the server navigation
    #*********************
    def refresh_Server_Files_List_Widget(self):
        self.serverListWidget.clear()
        self.serverListWidget.setFixedSize(250, 300)

        serverFiles = self.ftp.nlst()

        for serverFile in serverFiles:
            serverItem = QListWidgetItem(serverFile)

            startingDir = self.ftp.pwd()

            try:
                self.ftp.cwd(serverFile)
                self.ftp.cwd(startingDir)
                serverItem.setIcon(QIcon(self.baseDir + '\\img\\FolderIcon.png'))
            except ftplib.error_perm:
                serverItem.setIcon(QIcon(self.baseDir + '\\img\\FileIcon.png'))
            
            self.serverListWidget.addItem(serverItem)

        self.serverListWidget.move(450, 50)

    #*********************
    #sets the server path in the line edit text box
    #*********************
    def set_Server_Path(self, item):
        self.serverPathLineEdit.clear()

        prepender = self.ftp.pwd()
        
        if prepender == "/":
            self.serverPathLineEdit.setText(self.ftp.pwd() + item.text())
        else:
            self.serverPathLineEdit.setText(self.ftp.pwd() + "/" + item.text())

    #*********************
    #navigates to the item clicked if it is a server directory
    #*********************
    def server_Navigate(self, item):
        if self.dir_Exists(item.text()):
            self.ftp.cwd(item.text())
        self.refresh_Server_Files_List_Widget()

    #*********************
    #sets the local path in the line edit text box
    #*********************
    def set_Local_Path(self, item):
        self.localPathLineEdit.clear()
        self.localPathLineEdit.setText(os.getcwd() + "\\" + item.text())

    #*********************
    #navigates to the item clicked if it is a local directory
    #*********************
    def local_Navigate(self, item):
        if os.path.isdir(item.text()):
            os.chdir(item.text())

        self.refresh_Local_Files_List_Widget()

    #*********************
    #creates the "up directory" buttons for local/server
    #*********************
    def create_Up_Dir_Btns(self):
        self.upLocalDirBtn = QPushButton('Go Up a\nDirectory', self)
        self.upLocalDirBtn.setIcon(QIcon('img\\UpDir.png'))
        self.upLocalDirBtn.setToolTip("Go back a directory")
        self.upLocalDirBtn.move(10,50)
        self.upLocalDirBtn.clicked.connect(self.up_Local_Dir)

        self.upServerDirBtn = QPushButton('Go Up a\nDirectory', self)
        self.upServerDirBtn.setIcon(QIcon('img\\UpDir.png'))
        self.upServerDirBtn.setToolTip("Go back a directory")
        self.upServerDirBtn.move(715,50)
        self.upServerDirBtn.clicked.connect(self.up_Server_Dir)

    #*********************
    #creates the change to current directory buttons for local/server
    #*********************
    def create_Change_To_Curr_Dir_Btns(self):
        self.changeToCurrLocalDirBtn = QPushButton('Current\nDirectory', self)
        
        self.changeToCurrLocalDirBtn.setIcon(QIcon('img\\FolderIcon.png'))
        self.changeToCurrLocalDirBtn.setToolTip("Go to the Current Directory")
        self.changeToCurrLocalDirBtn.move(10,100)
        self.changeToCurrLocalDirBtn.clicked.connect(self.change_To_Curr_Local_Dir)

        self.changeToCurrServerDirBtn = QPushButton('Current\nDirectory', self)
        self.changeToCurrServerDirBtn.setIcon(QIcon('img\\FolderIcon.png'))
        self.changeToCurrServerDirBtn.setToolTip("Go to the Current Directory")
        self.changeToCurrServerDirBtn.move(715,100)
        self.changeToCurrServerDirBtn.clicked.connect(self.change_To_Curr_Server_Dir)

    #*********************
    #creates the change to directory buttons for local/server
    #*********************
    def create_Change_Dir_Btns(self):
        self.changeLocalDirBtn = QPushButton('', self)
        self.changeLocalDirBtn.setIcon(QIcon('img\\GreenArrow.png'))
        self.changeLocalDirBtn.setToolTip("Change Directory")
        self.changeLocalDirBtn.move(310,8)
        self.changeLocalDirBtn.clicked.connect(self.change_Local_Dir)

        self.changeServerDirBtn = QPushButton('', self)
        self.changeServerDirBtn.setIcon(QIcon('img\\GreenArrow.png'))
        self.changeServerDirBtn.setToolTip("Change Directory")
        self.changeServerDirBtn.move(665,8)
        self.changeServerDirBtn.clicked.connect(self.change_Server_Dir)

    #*********************
    #changes the local directory to ..
    #*********************
    def up_Local_Dir(self):
        os.chdir("..")
        self.localPathLineEdit.setText(os.getcwd())
        self.refresh_Local_Files_List_Widget()
        print("Going up a directory to: " + os.getcwd())

    #*********************
    #changes the server directory to ..
    #*********************
    def up_Server_Dir(self):
        self.ftp.cwd("..")
        self.serverPathLineEdit.setText(self.ftp.pwd())
        self.refresh_Server_Files_List_Widget()
        print("Going up a directory to: " + self.ftp.pwd())

    #*********************
    #sets the path of the text box to the current local directory
    #*********************
    def change_To_Curr_Local_Dir(self):
        self.localPathLineEdit.setText(os.getcwd())
        print("Current directory is: " + os.getcwd())

    #*********************
    #sets the path of the text box to the current server directory
    #*********************
    def change_To_Curr_Server_Dir(self):
        self.serverPathLineEdit.setText(self.ftp.pwd())
        self.refresh_Server_Files_List_Widget()
        print("Current directory is: " + self.ftp.pwd())

    #*********************
    #changes to the local directory specified in the path
    #*********************
    def change_Local_Dir(self):
        #TODO: NEEDS TO BE MORE ROBUST
        os.chdir(self.localPathLineEdit.text())
        self.refresh_Local_Files_List_Widget()
        print("Current directory is: " + os.getcwd())

    #*********************
    #changes to the local directory specified in the path
    #*********************
    def change_Server_Dir(self):
        #TODO: NEEDS TO BE MORE ROBUST
        self.ftp.cwd(self.serverPathLineEdit.text())
        self.refresh_Server_Files_List_Widget()
        print("Current directory is: " + self.ftp.pwd())