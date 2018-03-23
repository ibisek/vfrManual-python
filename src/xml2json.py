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


PATTERN_CMT = '<cmt>(.*?)[\[](.+?)\s([0-9.,]+)[\]]<[\/]cmt>'
cmtPattern = re.compile(PATTERN_CMT, re.IGNORECASE)

def doProcess(filename, outPath):
    
    f = open(filename, 'r')
    xml = f.read()
    f.close()
    
    lines = xml.split('\n')
    
    for line in lines:
        j = dict()
        
        print("line:", line)
        if not line or '' == line: continue

        soup = BeautifulSoup(line, 'html.parser')
        print(soup)
        
        wpt = soup.find("wpt")
        lat = "{:.5f}".format(float(wpt['lat']))
        lon = "{:.5f}".format(float(wpt['lon']))
        elevation = wpt.find('ele').string  # [m]
        code = wpt.find('name').string
        
        cmt =  wpt.find('cmt').string
        print("cmt:", cmt)
        m = cmtPattern.findall(line)
        if m:
            print(m)
            name = m[0][0].strip()  # often empy
            callSign = m[0][1]  # gives just 'RADIO'
            if name: callSign = "{} {}".format(name, callSign) # to be in the same format as from vfrManual
            freq = m[0][2]
            
        print("lat", lat)
        print("lon", lon)
        print("elevation", elevation)
        print("code", code)
        print("name", name)
        print("callSign", callSign)
        print("freq", freq)
        
        j["freq"] = [freq]
        j["coords"] = (float(lat), float(lon))
        j["elev"] = elevation
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
        filename = '../data/ulonly.xml'
        outPath = '/tmp/00/'
             
    else:
        if len(sys.argv) != 3:
            print("Usage: html2json <filename> <outPath>\n where filename is ulonly.xml")
            sys.exit(0)
     
        filename = sys.argv[1]
        outPath = sys.argv[2]
 
    doProcess(filename, outPath)
    
    print("KOHEU.")
    
    
