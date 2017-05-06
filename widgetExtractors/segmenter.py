import time, subprocess, socket, re


srcFile=open("PackageNames.txt", "r")
outFile=open("segmentedFile2.txt","w")

#you  want  android.widget.EditText at the begining of the line
outFile.write(srcFile.read().replace(r' \n  ',"\n\n\n\n"))

srcFile.close()
outFile.close()
