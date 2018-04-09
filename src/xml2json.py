'''
Created on Mar 17, 2018

Data extraction from DATABAZE LETIST file, which is available at
http://www.aerobaze.cz/gps/

@author: ibisek
'''

import re
import sys
import json

from bs4 import BeautifulSoup


PATTERN_CMT1 = '<cmt>(.*?)[\[](.+?)\s([0-9.,]+)[\]]<[\/]cmt>'
PATTERN_CMT2 = '<cmt>(.+?)\s([0-9.,]+)<\/cmt>'
cmtPattern1 = re.compile(PATTERN_CMT1, re.IGNORECASE)
cmtPattern2 = re.compile(PATTERN_CMT2, re.IGNORECASE)

def doProcess(filename, outPath):
    
    f = open(filename, 'r')
    xml = f.read()
    f.close()
    
    lines = xml.split('\n')
    
    for line in lines:
        #print("line:", line)
        if not line or '' == line: continue

        soup = BeautifulSoup(line, 'html.parser')
        
        wpt = soup.find("wpt")
        lat = "{:.5f}".format(float(wpt['lat']))
        lon = "{:.5f}".format(float(wpt['lon']))
        elevation = int(wpt.find('ele').string)  # [m]
        code = wpt.find('name').string
        
        name = None
        callSign = None
        freq = None

        if code == "LKKOTV" or code == "LKBYST":
            print("TED!", code)
            
        m = cmtPattern1.findall(line)
        if m:
            name = m[0][0].strip()  # often empy
            callSign = m[0][1]  # gives just 'RADIO'
            if name: callSign = "{} {}".format(name, callSign) # to be in the same format as from vfrManual
            freq = m[0][2]
            
        if not name:
            m = cmtPattern2.findall(line)
            if m:
                callSign = m[0][0]  # gives just 'RADIO'
                freq = m[0][1]
                        
#         print("lat", lat)
#         print("lon", lon)
#         print("elevation", elevation)
#         print("code", code)
#         print("name", name)
#         print("callSign", callSign)
#         print("freq", freq)
        
        
        freqList = list()
        if callSign and freq: freqList.append((callSign, freq))
        
        j = dict()
        
        if len(freqList) > 0: j["freq"] = freqList 
        j["coords"] = (float(lat), float(lon))
        j["elev"] = (int("{:0.0f}".format(elevation * 3.2808399).rstrip('0').rstrip('.')), elevation)   # [ft], [m]
        #j["rwy"] = runways
        j["code"] = code
        if name: j["name"] = name
      
        s = json.dumps(j, separators=(',',':'))

        outFilename = "{}/{}.json".format(outPath, code.lower())
        f = open(outFilename, 'w')
        f.write(s)
        f.close()
    

TEST = False
if __name__ == '__main__':

    if TEST:
        filename = '/tmp/00/ulonly.xml'
        outPath = '/tmp/00/'
             
    else:
        if len(sys.argv) != 3:
            print("Usage: html2json <filename> <outPath>\n where filename is ulonly.xml")
            sys.exit(0)
     
        filename = sys.argv[1]
        outPath = sys.argv[2]
 
    doProcess(filename, outPath)
    
    print("KOHEU.")
    
    
