'''
Created on May 26, 2018

Data extraction from OPENFLIGHTMAPS AIXM embedded file, which is available at
https://openflightmaps.org/live/lk-czech-republic/

@author: ibisek
'''

import sys
import json

from bs4 import BeautifulSoup
from html2json import removeDiacritic

'''
@return list of runways [direction, dimensions], e.g. ["14-32", "700x100"]
'''
def getRunways(soup, regionCode): 
    rwys = soup.find_all('rwy')
    
    runways = dict()
    
    for rwy in rwys:
        code=rwy.find('codeid').text
        if not code.startswith(regionCode): continue
        directions = rwy.find('txtdesig').text.replace(' ', '').replace('/', '-')
        length = rwy.find('vallen').text
        width = rwy.find('valwid').text
        
        if code not in runways:
            runways[code] = list()
        
        runways[code].append((directions, "{}x{}".format(length, width)))
        
    return runways

def getAirfields(soup, regionCode):
    records = soup.find_all('ahp')
    
    airfields = dict()
    
    for record in records:
        code=record.find('codeid').text
        if not code.startswith(regionCode): continue
        
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
        
        airfields[code] = (name, lat, lon, (elevFt, elevM))
         
    return airfields

'''
@return dict of uni ID -> code; e.g. 30196 -> LKKA
'''
def _getUniIds(soup, regionCode):
    records = soup.find_all('uni')  
    
    uniIds = dict()
    
    for record in records:
        code=record.find('codeid').text
        if not code or not code.startswith(regionCode): continue
        
        uniId = record.uniuid['mid']
        
        uniIds[uniId] = code
         
    return uniIds

'''
@return dict (key = code) of lists of tuples (callSign, freq)
'''
def getFrequencies(soup, regionCode):
    uniIds = _getUniIds(soup, regionCode)
    
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


def doProcess(filename, workingDir, regionCode='LK'):

    f = open(filename, 'r')
    text = f.read()
    f.close()

    soup = BeautifulSoup(text, 'html.parser')
    
    runways = getRunways(soup, regionCode)
    print("runways:", runways)
    
    airfields = getAirfields(soup, regionCode)
    print("airfields:", airfields)
    
    frequencies = getFrequencies(soup, regionCode)
    print("frequencies:", frequencies)
    
#     sys.exit(0)
    
    for code in airfields.keys():
        af = airfields[code]              # (name, lat, lon, (elevFt, elevM))
        freq = frequencies[code]    # (callSign, freq)
        rwys = runways[code]        # [(directions, dimensions)]
        
        #try to locate existing file or start new if not present
        filename = "{}/{}.json".format(workingDir, code.lower())
        
        try:
            f = open(filename, 'r')
            jsonStr = f.read()
            f.close()
            j = json.loads(jsonStr)

            # add fields which are missing:
            if 'rwy' not in j:
                j['rwy'] = rwys
            
            if 'elev' not in j:
                j['elev'] = af[3]
        
        
        except FileNotFoundError:
            # create a completely new record + file:
            j = dict()
            j['code'] = code
            j['name'] = af[0]
            j['alias'] = removeDiacritic(af[0])
            j['coords'] = (af[1], af[2]) 
            j['elev'] = af[3]
            
            j['freq'] = [("{} {}".format(af[0], f[0]), f[1]) for f in freq]
            j['rwy'] = rwys
            
        
        # save the json:
        s = json.dumps(j, separators=(',',':'))
        f = open(filename, 'w')
        f.write(s)
        f.close()
    

TEST = True    
if __name__ == '__main__':

    if TEST:
        filename = '/home/ibisek/wqz/download/vfrManual/openflightmaps.org/aixm_lk.xml'
        workingDir = '/tmp/00'
        regionCode = 'LK'
              
    else:
        if len(sys.argv) != 3:
            print("Usage: openflightmaps.py <aixm-filename> <outPath> <regionCode>\n where\n  filename is from the embedded folder and\n  regionCode is LK/LZ/..")
            sys.exit(0)
      
        filename = sys.argv[1]
        workingDir = sys.argv[2]
        regionCode = sys.argv[3]

 
    doProcess(filename, workingDir, regionCode)
    
    print("KOHEU.")
    
    
