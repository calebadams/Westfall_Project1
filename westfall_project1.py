import urllib3
from Connection_Class import connection_Class

def main():
    ftp = connection_Class("drwestfall.net")
    ftp.login("ftp05", "student")
    print(ftp.getwelcome())
    ftp.download_BIN("newFile")
    ftp.disconnect()





#MAKE SURE THIS IS THE END OF THE DOCUMENT. DO NOT MOVE OR ADD AFTER THIS POINT*********************************************************************
if __name__ == '__main__':
    main()