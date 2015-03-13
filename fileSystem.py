import sys
from random import randint



class FileSystem:
    
    listOfFiles = list()
    
    def __init__(self):
        print "class Initialized"
        f = open('filenames.txt', 'r')
        line = (f.read()).split('\n')
        
        for i in range(5):
            self.listOfFiles.append(line[randint(0,19)] + " ") #Inclusive
            
        print len(self.listOfFiles)
        
    def printFiles(self):
        print "My files are:", self.listOfFiles
        
    def hasFile(self, name):
        for file in self.listOfFiles:
            if (name + " ") in file:
                return True
            
        return False
    
    def getFile(self, name):
        listOfFiles = ""
        for file in self.listOfFiles:
            if (name + " ") in file:
                listOfFiles += file[:len(file)-1] + ","
                
        return listOfFiles[:len(listOfFiles)-1]
        

if __name__ == '__main__':
    fileSystem = FileSystem()
    fileSystem.printFiles()
    to_search = "The"
    print fileSystem.hasFile(to_search)
    print fileSystem.getFile(to_search)
