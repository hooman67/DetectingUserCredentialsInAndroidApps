import time, subprocess, socket, re


##########getting ready for split###########################################
srcFile=open("AFTT.txt", "r")
outFile=open("segmentedFile.txt","w")

#you  want  android.widget.EditText at the begining of the line
outFile.write(srcFile.read().replace(r' \n  ',"\n\n\n\n"))

srcFile.close()
outFile.close()
############################################################################

###########SPLITING THE FILE INTO AN STRING ARRAY###########################
f=open("segmentedFile.txt", "r")

wholeFile = ""
for line in f:
	wholeFile += line;
f.close()

wholeFileArr = re.split('\n\s{4,}',wholeFile)


outFile=open("outputFile.txt","w")
for ind in range(len(wholeFileArr)):
	if "android.widget.EditText" in wholeFileArr[ind]: 
		#outFile.write(wholeFileArr[ind] +"\n\n")
		#print(str(len(wholeFileArr)))
		widg_type = re.compile(r'android.widget\S*', re.MULTILINE).findall(wholeFileArr[ind])
		widg_id=re.compile(r'mID=\S*', re.MULTILINE).findall(wholeFileArr[ind])
		widg_xloc = re.compile(r'getLocationOnScreen_x\S*', re.MULTILINE).findall(wholeFileArr[ind])
		widg_yloc = re.compile(r'layout:getLocationOnScreen_y\S*', re.MULTILINE).findall(wholeFileArr[ind])

		for index in range(len(widg_id)):
			outFile.write("\n\n")
			if index < len(widg_type):
				outFile.write(widg_type[index] + "\n")
			else:
				outFile.write("type:Other\n")
			outFile.write(widg_id[index] + "\n")
			outFile.write(widg_xloc[index] + "\n")
			outFile.write(widg_yloc[index] + "\n")

outFile.close()


#outFile=open("outputFile.txt","w")
#ttt =""
#for line in f:
#	widg_type = re.compile(r'android.widget\S*', re.MULTILINE).findall(line)
#	widg_id=re.compile(r'mID=\S*', re.MULTILINE).findall(line)
#	widg_xloc = re.compile(r'getLocationOnScreen_x\S*', re.MULTILINE).findall(line)
#	widg_yloc = re.compile(r'layout:getLocationOnScreen_y\S*', re.MULTILINE).findall(line)
	
#	ttt += line;
#	kk = re.split('\n\s{4,}',ttt)

#	for ind in range(len(kk)):
#		outFile.write(kk[ind] +"\n\n")

#	print("id: "+str(len(widg_id))+"\n")
#	print("id: "+str(len(widg_type))+"\n")
#	print("x: "+str(len(widg_xloc))+"\n")
#	print("y: "+str(len(widg_yloc))+"\n")

#	for index in range(len(widg_id)):
#		outFile.write("\n\n")
#		outFile.write(widg_type[index] + "\n")
#		outFile.write(widg_id[index] + "\n")
#		outFile.write(widg_xloc[index] + "\n")
#		outFile.write(widg_yloc[index] + "\n")

            
