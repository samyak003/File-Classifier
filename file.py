from datetime import datetime 
import os 
import tkinter as tk
from tkinter import filedialog
import numpy as np
import re


version = "1.0.0"

os.system("cd /")
if "file_classifier" not  in os.listdir("/"):
    os.mkdir("/file_classifier")
file_c = "C:/file_classifier"
os.system("cd {}".format(file_c))
log = open("{}/log.txt".format(file_c),"w")
copied = []
verified = []

def logging(level, message):
    log.write("{} :{} : {}\n".format(datetime.today(),level, message))

logging("Debug","Program started")



def exten(directory,folder):
    logging("Debug","Using extension function")
    files = []
    extentions = []
    classified = {}
    for file in folder:
        try :
            os.listdir(directory+"/"+file)
        except :
            files.append(file)
    for file in files:
        extentions.append(file.split(".")[-1])
    extentions = np.unique(extentions)
    for extention in extentions :
        s = []
        for file in files:
            if file.split(".")[-1] == extention :
                s.append(file)
        classified[extention] = s
    logging("Debug","Classification of extensions completed with {} extensions".format(len(classified)))
    return classified

def folder_creation(v,directory):
    folder = os.listdir(directory)
    for check in v :
        if check in folder:
            print("No need of {} folder".format(check))
            logging("Debug","No need of {} folder".format(check))
        else :
            os.mkdir(directory+"\{}".format(check))
            print("{} folder created".format(check))
            logging("Debug","{} folder created".format(check))
  


def about():
    file = open(file_c+"/about.txt", "w")
    file.write("-"*60+"\n This program is created by Samyak Jain(@Samyak003)\n"+"-"*60
               +"\nVersion - {}".format(version)+ "\nIf you faced any bugs, email the logs.txt to samyakjain003@gmail.com or Send the file to @samyak003 on telegram ")
    file.close()
    
def copy_verification(e,copied,directory):
    print("-"*10+"\n Verifying\n"+"-"*10)
    for a in e :
        for z in os.listdir(directory+"/"+a) :
            verified.append(z)
    different = set(copied).difference(verified)
    if len(different) == 0 :
        print("All files transfered!")
        logging("Info","All files transfered!")
    else :
        print("Cannot copy ",len(different)," files")
        logging("Error","Cannot copy "+"{}".format(len(different))+" files")
        print("Files are- ")
        for f in different:
            print(f)
    return copied

def copy(e,directory,listOffile):
    folder_creation(e,directory)
    print("-"*10)
    print("Copying files")
    logging("Debug","Copying files")
    print("-"*10)
    listOffile.write("-"*60+"\n Files coiped are \n"+"-"*60)
    for extension in e :
        for file in e[extension]:
                print(file)
                v = directory+"\{}".format(file)
                command = "copy \"{}\" \"{}\"".format(v,directory+"/{}".format(extension))
                os.system(command)
                logging("Debug","{} copied".format(file))
                listOffile.write("\n"+file)
                copied.append(file)
    print("Done copying")
    logging("Info", "Done copying")
    
    
def delete(directory,listOffile,diff):
    logging("Info","User selected to delete the files ")
    listOffile.write("\n"+"-"*60+"\nDeleted Files are \n"+"-"*60)
    print("-"*10)
    print("Deleting files")
    logging("Debug","Deleting files")
    print("-"*10)
    for file in copied:
        if file not in diff:
            print(file+"no")
            continue
        else:
            try:
                os.chmod(directory+"/{}".format(file),-1)
                os.remove(directory+"/{}".format(file))
                logging("Debug","{} deleted".format(file))
                print(file)
                listOffile.write("\n"+file)
            except:
                logging("Error","Cannot delete "+file)
    logging("Info","Done Deleting")
    
    
    
def main():
    print("""  _____ _ _         ____ _               _  __ _           
 |  ___(_) | ___   / ___| | __ _ ___ ___(_)/ _(_) ___ _ __ 
 | |_  | | |/ _ \ | |   | |/ _` / __/ __| | |_| |/ _ \ '__|
 |  _| | | |  __/ | |___| | (_| \__ \__ \ |  _| |  __/ |   
 |_|   |_|_|\___|  \____|_|\__,_|___/___/_|_| |_|\___|_|  
 
 By Samyak Jain (@samyak003)""")
    root = tk.Tk()
    root.withdraw()
    print()
    while True:
        try :
            directory = filedialog.askdirectory()
            folder = os.listdir(directory)
        except :
            logging("Error","User entered wrong directory")
            print("Sorry you entered wrong/invalid directory\nPlease enter a valid one")
        else : 
            break
    logging("Info", "Directory entered - {}".format(directory))
    os.system("cd "+directory)
    logging("Debug", "Current directory set to {}".format(directory))
    e = exten(directory,folder)
    print("Found files of {} extensions ".format(len(e)))
    excep_input = input("Any Exceptions ?[f/e/n]")
    if excep_input == "f":
        logging("Debug", "Files are exempted")
        l = []
        exempted_files = filedialog.askopenfilenames()
        for a in exempted_files:
            if re.search("^"+directory,a) :
                for q in a.split("/"):
                    continue
                l.append(q)
            else :
                print("File(s) are not present in the current directory")
                logging("Error","File(s) are not present in the current directory")
                break
        for f in l:
            for ex in e.values():
                if f in ex :
                    ex.remove(f)
    elif excep_input == "e":
        logging("Debug", "Extensions are exempted")
        extensions = (input("Enter the extentions -> ").split(","))
        for extension in extensions :
            if extension in e:
                e.pop(extension)
                logging("Debug", "{} exempted".format(extension))
            else :
                print("No extension named {} found".format(extension))
                logging("Error", "No extension named {} found".format(extension))
    proceed  = input("Proceed ? [Y//N]")
    listOffile = open("{}/list.txt".format(file_c),"w")
    if proceed.lower() == "y":
        copy(e,directory,listOffile)
        diff = copy_verification(e,copied,directory)
        delete_input = input("Do you want to delete the copied files ? [Y/n] -> ")
        if delete_input == "Y":
            delete(directory,listOffile,diff)
        else :
            logging("Info","User selected not to delete files")
    else :
        logging("Info", "User selected not to proceed")
    
    print("-"*10)
    print("Thank You")
    about()
    logging("Info","About file saved")
    print("Logs,info and about saved in "+file_c)
    input("Press enter to close the program") 


main()
        

log.close()

