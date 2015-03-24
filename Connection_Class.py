import ftplib
from multiprocessing import Process, Queue

class connection_Class(ftplib.FTP):
    
    #constructor
    def __init__(self, url):
        self.isOpen = False
        super().__init__()
        self.connect(url)
        self.queue = Queue()
        self.proc = Process(target = None)

    def __del__(self):
        self.disconnect()
        self.queue.close()
        self.proc.join()

    #*********************
    #connects a new ftp obj to the given url
    #url is a valid string containing the file servers url
    #If error returns None
    #return a bool
    #*********************
    def connect(self, url):
        try:
            super().connect(url)
        except ftplib.all_errors:
            self.isOpen = False
            #What should be returned if we have an error? we can't just return the ftp obj... maybe None?
            return False
        self.isOpen = True
        return True


    #*********************
    #logs into the file server using the provided userName and password
    #ftpObj is the current working ftp server object
    #userName is a str containing the user name
    #password is the password
    #RETURN is False if error occurs else true
    #*********************
    def login(self, userName, Password):
        try:
            super().login(str(userName), Password)
        except ftplib.all_errors:
            return False
        return True


    #*********************
    #Downloads binary version of file 
    #This should be faster then the ASCII version
    #ftpObj is the current working ftp server object
    #fileName is the file you want downloaded
    #blockSize is the size of the packets being sent (default is 8Kb)
    #callBackMethod is a function such as "update progress bar"
    #THIS ASSUMES YOU ARE IN THE CORRECT DIR
    #RETURN is False if error occurs else true
    #*********************
    def download_BIN(self, fileName, blockSize = 8192, callBackMethod = None):
        try:                            #we need some way to monitor the progress... 
            self.retrbinary('RETR '.join(fileName), open(fileName, 'wb').write, blockSize, callBackMethod )
        except ftplib.all_errors:
            return False                #we should change this to actuall tell the error
        return True

    #*********************
    #uploads binary version of file 
    #This should be faster then the ASCII version.
    #ftpObj is the current working ftp server object
    #fileName is the file you want uploaded
    #blockSize should not be changed unless you know the network can handle it (so not at liberty lol)
    #callBackMethod is a function such as "update progress bar"
    #THIS ASSUMES YOU ARE IN THE CORRECT DIR
    #RETURN is False if error occurs else true
    #*********************
    def upload_BIN(self, fileName, blockSize = 8192, callBackMethod = None):
        try:                            #we need some function to monitor the progress to pass to callBackMethod
            self.storbinary("STOR ".join(fileName), open(fileName), blockSize, callBackMethod )
        except ftplib.all_errors:
            return False                #we should change this to actuall tell the error
        return True

    #*********************
    #Deletes a directory from the server
    #ftpObj is the current working ftp server object
    #directoryName is the directory you want deleted
    #RETURN is False if error occurs else true
    #*********************
    def delete_Dir(self, dirName):
        try:
            if dir_Exists(self, dirName): #if the directory exists
                self.rmd(dirName) #remove the directory
                print("Directory: ", dirName, " deletion successful ") #print successful deletion message
            else: #otherwise, the directory does not exist
                print("Directory: ", dirName, " does not exist") #print directory DNE message
                return False
        except ftplib.all_errors: #an error occurred
            print("Directory: ", dirName, " deletion failed") #print failed deletion message
            return False #return false indicates deletion did not occur
        return True


    #*********************
    #Checks if directory exists (in current location)
    #ftpObj is the current working ftp server object
    #dir is the directory you want to check for existence
    #THIS ASSUMES YOU ARE IN THE CORRECT DIR
    #RETURN is True if the directory exists, False if it does not
    #*********************
    def dir_Exists(self, dirName):
        fileList = [] #list object to store all files
        self.retrlines('LIST', fileList.append) #append to list
    
        for file in fileList: #for every file/directory in the list (current location)
            if file.split()[-1] == dirName and file.upper().startswith('D'): # If the name matches and is a directory
                return True #directory found, return True
        return False #otherwise, directory not found, return False


    #*********************
    #Remote file permissions
    #*********************
    def set_Remote_Permissions(self, path, perm):
        permNum = self.switch_Remote_Perm.get(perm, "0000")
        self.sendcmd("SITE CHMOD {0} {1}".format(permNum, path))


    #********************* 
    #Disconnects from the ftp server, steralizes ftpObj
    #Should be called whenever switching servers or closing the program
    #ftpObj is a active ftp connection object
    #if there is an error return False
    #if successful, sets ftpObj to None and returns true
    #*********************
    def disconnect(self):
        if self.is_Open():
            try:
                self.close()
            except ftplib.all_errors:
                return False
            self
            return True

    #********************* 
    #Is connection closed?
    #*********************
    def is_Open(self):
        return self.isOpen

    switch_Remote_Perm = {
        "rwx": "0777", #Read, write, execute
        "rw-": "0666", #Read, write
        "r--": "0444", #Read only
        }


    #*******************
    # multiprocessing!
    # NOT DONE YET DO NOT TRY TO USE!!!!!!!!!!!!
    #*******************
    def ftp_Manager(self, function, args = None):
        if self.queue.empty():
            #check and see if there is process
            if not self.proc.is_alive():
                self.proc = multiprocessing.Process(target=None)
                self.proc
        else:
            self.queue.put((function, args))