'''
Created on May 26, 2018

Data extraction from OPENFLIGHTMAPS AIXM embedded file, which is available at
https://openflightmaps.org/live/lk-czech-republic/

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


def getRunways(soup, codePrefix): 
    rwys = soup.find_all('rwy')
    
    runways = dict()
    
    for rwy in rwys:
        code=rwy.find('codeid').text
        if not code.startswith(codePrefix): continue
        directions = rwy.find('txtdesig').text
        length = rwy.find('vallen').text
        width = rwy.find('valwid').text
        
        if code not in runways:
            runways[code] = list()
        
        runways[code].append((directions, "{}x{}".format(length, width)))
        
    return runways

def getAirfields(soup, codePrefix):
    records = soup.find_all('ahp')
    
    airfields = dict()
    
    for record in records:
        code=record.find('codeid').text
        if not code.startswith(codePrefix): continue
        
        lat = record.find('geolat').text
        latLetter = lat[len(lat)-1]
        latSign = 1 if latLetter == "N" else -1
        lat = latSign * float(lat[:len(lat)-1]) 
        lat = "{:.5f}".format(lat)
        
        lon = record.find('geolong').text
        lonLetter = lon[len(lon)-1]
        lonSign = 1 if lonLetter == "E" else -1
        lon = lonSign * float(lon[:len(lon)-1]) 
        lon= "{:.5f}".format(lon)
        
        elevFt = int(record.find('valelev').text)
        elevM = int(float(elevFt) * 0.3048)
        
        names = record.find_all('txtname')
        
        # there are multiple (typically two) txt name fields - the shorter one contains name of the place:
        name = min([name.text for name in names], key=len)
        
        if code not in airfields:
            airfields[code] = list()
         
        airfields[code].append((name, lat, lon, (elevFt, elevM)))
         
    return airfields

'''
@return dict of uni ID -> code; e.g. 30196 -> LKKA
'''
def _getUniIds(soup, codePrefix):
    records = soup.find_all('uni')  
    
    uniIds = dict()
    
    for record in records:
        code=record.find('codeid').text
        if not code or not code.startswith(codePrefix): continue
        
        uniId = record.uniuid['mid']
        
        uniIds[uniId] = code
         
    return uniIds

'''
@return dict (key = code) of lists of tuples (callSign, freq)
'''
def getFrequencies(soup, codePrefix):
    uniIds = _getUniIds(soup, codePrefix)
    
    records = soup.find_all('fqy')  
     
    frequencies = dict()
     
    for record in records:
        freq = record.find('valfreqrec').text
        uniId = record.find('uniuid')['mid']
        
        if uniId in uniIds:
            code = uniIds[uniId]
            
            callSign = record.find('txtcallsign').text
            callSign = callSign[callSign.rfind(' ')+1:] # just the last item.. 'RADIO' / 'TOWER' / etc.
         
            if code not in frequencies:
                frequencies[code] = list()
              
            frequencies[code].append((callSign, freq))
          
    return frequencies


def doProcess(filename, outPath, codePrefix="LK"):

    f = open(filename, 'r')
    text = f.read()
    f.close()

    soup = BeautifulSoup(text, 'html.parser')
    
    runways = getRunways(soup, codePrefix)
    print("runways:", runways)
    
    airfields = getAirfields(soup, codePrefix)
    print("airfields:", airfields)
    
    frequencies = getFrequencies(soup, codePrefix)
    print("frequencies:", frequencies)
    
    
if __name__ == '__main__':

#     if TEST:
#         filename = '/tmp/00/ulonly.xml'
#         outPath = '/tmp/00/'
#              
#     else:
#         if len(sys.argv) != 3:
#             print("Usage: html2json <filename> <outPath>\n where filename is ulonly.xml")
#             sys.exit(0)
#      
#         filename = sys.argv[1]
#         outPath = sys.argv[2]

    filename = "/home/ibisek/wqz/download/vfrManual/openflightmaps.org/aixm_lk.xml"
    outPath = "/tmp/00"
 
    doProcess(filename, outPath)
    
    print("KOHEU.")
    
    
