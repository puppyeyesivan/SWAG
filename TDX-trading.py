from struct import *

import os
import sys


    
def day2csv_data(dirname,fname,targetDir):
    ofile=open(dirname+os.sep+fname,'rb')
    buf=ofile.read()
    ofile.close()
     
    ifile=open(targetDir+os.sep+fname+'.csv','w')
    num=len(buf)
    no=num/32
    b=0
    e=32
    line='' 
    linename=str('date')+','+str('open')+', '+str('high')+' ,'+str('low')+', '+str('close')+' ,'+str('amout')+', '+str('vol')+' ,'+str('str07')+''+'\n'
      # print line
    ifile.write(linename)
    for i in xrange(no):
       a=unpack('IIIIIfII',buf[b:e])
       line=str(a[0])+','+str(a[1]/100.0)+', '+str(a[2]/100.0)+' ,'+str(a[3]/100.0)+', '+str(a[4]/100.0)+' ,'+str(a[5]/10.0)+', '+str(a[6])+' ,'+str(a[7])+''+'\n'
      # print line
       ifile.write(line)
       b=b+32
       e=e+32
    ifile.close()
    


pathdir='/vipdoc/sh/lday'
targetDir='/_python_gp_tdx/data_gupiao/sh/lday'

 
listfile=os.listdir(pathdir)
 

for f in listfile:
   
    day2csv_data(pathdir,f,targetDir)
else:
    print 'The for '+pathdir+' to '+targetDir+'  loop is over'
    





