import glob
import os
from shutil import copyfile
from os import remove, close
from tempfile import mkstemp

import sys

wrk = "/Users/louiscastricato/Google Drive/Notes/"
wrk2 = "/Users/louiscastricato/'Google Drive'/Notes/"
subjects = os.listdir(wrk)
files = glob.glob(wrk+"*")
subjects.remove('.DS_Store')


def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    copyfile(abs_path, file_path)

class Subject:
    def __init__(self, n, d):
        self.name = n
        self.directory = d

        self.classes = os.listdir(self.directory)
        self.classes.remove('.DS_Store')
    def print_classes(self):
        print self.classes
    def add_new_class(self, n):
        if os.path.exists(self.directory + "/"+n):
            print "Error, class already taken."
        else:
            os.makedirs(self.directory + "/" + n)
            os.makedirs(self.directory + "/" + n + "/Notes")
            self.classes.append(n)
            print "Successfully added new class: " + n
    def add_new_assignment(self, n):
        if os.path.exists(self.directory + "/"+n):
            cdir = self.directory + "/" + n + "/"
            subdir = os.listdir(cdir)
            max_num = 1
            print "Making directory."
            for files in subdir:
                delimit = files.split(" ")
                if delimit[0] == "Assignment":
                    if int(delimit[1]) >= max_num:
                        max_num = int(delimit[1])+1
            os.mkdir(cdir + "Assignment " + str(max_num))
            print "Copying LaTeX Template."
            ddir = cdir+"Assignment " + str(max_num) +"/assignment"+str(max_num)+".tex"
            copyfile(cdir+"../../../template.tex", ddir)
            replace(ddir, "\\title{Title}", "\\title{"+n +", Assignment " + str(max_num) + "}")
            os.chdir(str(wrk + self.name + "/"+n+"/Assignment "+str(max_num)))
            os.system("pdflatex assignment" + str(max_num) +".tex")
            print "Assignment "+ str(max_num) +" successfully created. Goodluck. :)" 
            if sys.argv[3] == "vim":
                os.systemc("vim assignment"+ str(max_num)+".tex")

subj =[None] * len(files)
for i in range(0, len(files)):
    subj[i] = Subject(subjects[i], files[i])
# New Assignment
if sys.argv[1] == "na":
    for s in subj:
        #Only add the assignment to the proper class obviously
        s.add_new_assignment(sys.argv[2])
#New Class
else if sys.argv[1] == "nc":
    for s in subj:
        if s.name == sys.argv[2]:
            s.add_new_class(sys.argv[3])
            break 
