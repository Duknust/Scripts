#!/usr/bin/python
class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

import base64
from Crypto.Cipher import AES
from Crypto import Random
import getpass
import sys
import os

# init global vars ################################################################
monthScheduleDate = ""                                                            #
tagDescription = {}                                                               #
monthSchedule = []                                                                #
allAvailMonths = []                                                               #
tagfile = "tag_description.txt"                                                   #
tagDescription['xx']="xx ## nothing"                                              #
tagDescription['yy']="yy ## nothing"                                              #
## end global vars ################################################################

# init crypto vars ################################################################
BS = 16 #default                                                                  #
pad = lambda s: s+(BS-len(s)%BS)*chr(BS-len(s)%BS)                                #
unpad = lambda s : s[:-ord(s[len(s)-1:])]                                         #
key = b'Sixteen byte key' #default                                                #
## end crypto vars ################################################################

# init crypto #####################################################################
def readKey():                                                                    #
  global key                                                                      #
  my_str = getpass.getpass()                                                      #
  key = bytes.encode(my_str)                                                      #                 
                                                                                  #  
def encodeString(s):                                                              #
  return base64.b32encode(s)                                                      # 
                                                                                  #
def decodeString(s):                                                              #
  return base64.b32decode(s)                                                      #
                                                                                  #
def readScheduleFromFileDECRYPT(filename):                                        #
  global matrix                                                                   #
  i = 0                                                                           #
  lines = [line.strip() for line in open(filename)]                               #
  for line in lines:                                                              #
    decLine = decrypt(decodeString(line))                                         #
    matrix[i] = decLine.split(' ')                                                #
    i = i+1                                                                       #
                                                                                  #
def writeScheduleToFileENCRYPT(output):                                           #
  global matrix                                                                   #
  f = open(output,'a')                                                            #
  for line in matrix:                                                             #
    s = ' '.join(str(x) for x in line)                                            #
    s = encodeString(encrypt(s))                                                  #
    f.write(s+'\n')                                                               #
  f.close()                                                                       #
                                                                                  #
def encrypt(raw):                                                                 #
  global key                                                       #
  raw = pad(raw)                                                   #
  iv = Random.new().read( AES.block_size )                         #
  cipher = AES.new(key, AES.MODE_CBC, iv )                         #   
  return base64.b64encode(iv+cipher.encrypt(raw))                  #
                                                                   #
def decrypt(enc):                                                                 #
  global key                                                                      #
  enc = base64.b64decode(enc)                                                     #  
  iv = enc[:16]                                                                   #
  cipher = AES.new(key, AES.MODE_CBC, iv)                                         #
  return unpad(cipher.decrypt(enc[16:]))                                          #
## end crypto #####################################################################

# init crypto specific ############################################################
def tagDescriptionRead_CRYPTO(filename="tag_description.txt"):                    #
  global tagDescription                                                           #
  lines = [line.strip() for line in open(filename)]                               #
  for line in lines:                                                              #
    decline = decrypt(decodeString(line))                                         #
    tag = decline.split(" ")                                                      #
    tagDescription[tag[0]]=tag[1]                                                 #
                                                                                  #
def tagDescriptionWrite_CRYPTO(filename="tag_description.txt"):                   #
  global tagDescription                                                           #
  f = open(filename,'a')                                                          #
  for line in lines:                                                              #
    s = ' '.join(str(x) for x in line)                                            #
    s = encodeString(encrypt(s))                                                  #
    f.write(s+'\n')                                                               #
  f.close                                                                         #
                                                                                  #
def monthScheduleWrite_CRYPTO(filename):                                          #
  global monthSchedule                                                            #
  global monthScheduleDate                                                        #
  f = open("months/"+filename,'a')                                                #
  f.write(encodeString(encrypt(monthScheduleDate))+"\n")                          #
  for line in monthSchedule:                                                      #
    s = ' '.join(str(x) for x in line)                                            #
    s = encodeString(encrypt(s))                                                  #
    f.write(s+'\n')                                                               #
  f.close                                                                         #
                                                                                  #
def monthScheduleRead_CRYPTO(filename):                                           #
  global monthSchedule                                                            #
  global monthScheduleDate                                                        #
  lines = [line.strip() for line in open("months/"+filename)]                     #
  i=0                                                                             #
  for line in lines:                                                              #
    decLine = decrypt(decodeString(line))                                         #
    if (i>1):                                                                     #
      decLine = decLine.split(" ")                                                #
      monthSchedule.append(decLine)                                               #
    elif i==0:                                                                    #   
      monthScheduleDate=decLine                                                   #
    i+=1                                                                          #
## end crypto specific ############################################################

# init functions ##################################################################
def getMonthsInDB():#verified                                                     #
  global allAvailMonths                                                           #
  allAvailMonths = os.listdir("months/")                                          #
                                                                                  #
def printMonthsInDB():#verified                                                   #
  global allAvailMonths                                                           #
  for month in allAvailMonths:                                                    #
    print month                                                                   #
                                                                                  #
def printDescriptions():                                                          #
  global tagDescription                                                           #
  for key in tagDescription:                                                      #
    print key+" "+tagDescription[key]                                             #
                                                                                  #
def tagDescriptionRead(filename="tag_description.txt"):#verified                  #
  global tagDescription                                                           #
  lines = [line.strip() for line in open(filename)]                               #
  for line in lines:                                                              #
    tag = line.split(" ")                                                         #
    tagDescription[tag[0]]=tag[1]                                                 #
                                                                                  #
def tagDescriptionWrite(filename="tag_description.txt", new=True):#verified       #
  global tagDescription                                                           #
  val = ""                                                                        #
  if new:                                                                         #
    val = 'w'                                                                     #
  else:                                                                           #
    val = 'a'                                                                     #
  f = open("months/"+filename,val)                                                #
  for key in tagDescription:                                                      #
    f.write(key+" "+tagDescription[key]+"\n")                                     #
  f.close()                                                                       #
                                                                                  #
def monthScheduleRead(filename):#verified                                         #
  global monthSchedule                                                            #
  global monthScheduleDate                                                        #
  lines = [line.strip() for line in open("months/"+filename)]                     #
  i = 0                                                                           #
  for line in lines:                                                              #
    if (i>1):                                                                     #
      line = line.split(" ")                                                      #
      monthSchedule.append(line)                                                  #
    elif i==0:                                                                    #
      monthScheduleDate=line                                                      #
    i+=1                                                                          #
                                                                                  #
def monthScheduleWrite(filename, new):                                            #
  global monthSchedule                                                            #
  global monthScheduleDate                                                        #
  val = ""                                                                        #
  if new:                                                                         #
    val = 'w'                                                                     #
  else:                                                                           #
    val = 'a'                                                                     #
  f = open("months/"+filename,val)                                                #
  f.write(monthScheduleDate+"\n")                                                 #
  firstLine="xxxxx "                                                              #
  value=""                                                                        #
  for i in range(1,32):                                                           #
    if i<10:                                                                      #
      value="0"+str(i)                                                            #
    else:                                                                         #
      value=str(i)                                                                #
    firstLine+=value+" "                                                          #
  f.write(firstLine+"\n")                                                         #
  for line in monthSchedule:                                                      #
    s = ' '.join(str(x) for x in line)                                            #
    f.write(s+'\n')                                                               #
  f.close                                                                         #
                                                                                  #
def monthScheduleWrite(filename, date, new):                                      #
  global monthSchedule                                                            #
  val = ""                                                                        #
  if new:                                                                         #
    val = 'w'                                                                     #
  else:                                                                           #
    val = 'a'                                                                     #
  f = open("months/"+filename,val)                                                #
  f.write(date+"\n")                                                              #
  firstLine="xxxxx "                                                              #
  value=""                                                                        #
  for i in range(1,32):                                                           #
    if i<10:                                                                      #
      value="0"+str(i)                                                            #
    else:                                                                         #
      value=str(i)                                                                #
    firstLine+=value+" "                                                          #
  f.write(firstLine+"\n")                                                         #
  for line in monthSchedule:                                                      #
    s = ' '.join(str(x) for x in line)                                            #
    f.write(s+'\n')                                                               #
  f.close                                                                         #
                                                                                  #
def printDaySchedule(day=1):#verified                                             #
  global monthSchedule                                                            #
  print "day:  "+str(day)                                                         #
  for i in range(0,24):                                                           #
    print str((monthSchedule[i])[0])+" "+str((monthSchedule[i])[int(day)])        #
                                                                                  #
def printDayScheduleWithTagDescription(day=1):#verified                           #
  global monthSchedule                                                            #
  print "day:  "+str(day)                                                         #
  for i in range(0,24):                                                           #
    hour=str((monthSchedule[i])[0])+" "                                           #
    tagValue=str((monthSchedule[i])[day])                                         #
    tagDesc=tagDescription.get(tagValue, "## unknown")                            #
    print hour+tagDesc                                                            #
                                                                                  #
def printMonthSchedule():#verified                                                #
  global monthSchedule                                                            #
  strDays="      "                                                                #
  for i in range(0,31):                                                           #
    if i<9:                                                                       #
      strDays+=" "+str(i+1)+" "                                                   #
    else:                                                                         #
      strDays+=str(i+1)+" "                                                       #
  print strDays                                                                   #
  for i in range(0,24): #days                                                     #
    toPresent=""                                                                  #
    for j in range(0,32):                                                         #
      toPresent+=str((monthSchedule[i])[j])+" "                                   #
    print toPresent                                                               #
                                                                                  #
def monthScheduleUpdate(day, hour, tag):                                          #
  global monthSchedule                                                            #
  monthSchedule[hour][day]=tag                                                    #
## end functions ##################################################################
def menu0():
  print bcolors.OKBLUE+"<1> List months"+bcolors.ENDC
  print bcolors.OKBLUE+"<2> Add new month"+bcolors.ENDC
  print bcolors.OKBLUE+"<3> Months"+bcolors.ENDC
  print bcolors.OKBLUE+"   <31> Day Schedule"+bcolors.ENDC
  print bcolors.OKBLUE+"   <32> Day Schedule With Tag Description"+bcolors.ENDC
  print bcolors.OKBLUE+"   <33> Set description to day"+bcolors.ENDC
  print bcolors.OKBLUE+"<4> Descriptions"+bcolors.ENDC
  print bcolors.OKBLUE+"   <41> Add description"+bcolors.ENDC
  print bcolors.OKBLUE+"   <42> Set new value to key"+bcolors.ENDC
  return input()

def main():
  while True:
    opt = menu0()
    if opt==1: #list months
      getMonthsInDB()
      printMonthsInDB()
    elif opt==2: #new month
      print "insert yyyymm:"
      date = raw_input()
      monthScheduleRead("monthSchedule.txt")
      monthScheduleWrite(date+".txt",date)
    elif opt==3: #months
      print "insert yyyymm:"
      date = raw_input()
      date=date+".txt"
      monthScheduleRead(date)
      printMonthSchedule()
    elif opt==31: #day schedule
      print "insert yyyymm:"
      date = raw_input()
      print "insert dd"
      day = raw_input()
      date=date+".txt"
      monthScheduleRead(date)
      printDaySchedule(day)
    elif opt==32: #day schedule with tags
      print "insert yyyymm:"
      date = raw_input()
      print "insert dd"
      day = raw_input()
      monthScheduleRead(date+".txt")
      printDayScheduleWithTagDescription(day)
    elif opt==33: #set tag to day
      print "insert yyyymm:"
      date = raw_input()
      monthScheduleRead(date+".txt")
      print "insert dd"
      day = int(raw_input())
      print "insert hour"
      hour = int(raw_input())
      print "insert tag"
      tag = raw_input()
      monthScheduleUpdate(day, hour, tag)
      monthScheduleWrite(date,True)
    elif opt==4: #descriptions
      tagDescriptionRead()
      printDescriptions()
    elif opt==41: #add description
      tagDescriptionRead()
      print "insert tag"
      tag = raw_input()
      print "insert description"
      description = raw_input()
      tagDescriptionWrite(True)
    elif opt==42: #new value to key
      tagDescriptionRead()
      global tagDescription
      print "insert tag:"
      tag = raw_input()
      print tagDescription[tag]
      print "insert new description:"
      description = raw_input()
      tagDescription[tag]=description
    else:
      print bcolors.WARNING+"something wrong"+bcolors.ENDC

# main ############################################################################
if __name__ == "__main__":
  try:
    main()
    monthScheduleDate = None                               
    tagDescription = None
    monthSchedule = None
    allAvailMonths = None
  except:
    monthScheduleDate = None                               
    tagDescription = None
    monthSchedule = None
    allAvailMonths = None
    print "Unexpected error:", sys.exc_info()[0]
    raise
