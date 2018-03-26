# -*- coding: utf-8 -*-
'''
Created on Mar 17, 2018

Imports data from VFR manual. [http://lis.rlp.cz/vfrmanual/]

@author: ibisek
'''

import re
import sys
import json

from bs4 import BeautifulSoup


PATTERN_FREQ = '<span>(.*?)<\/span>([0-9,.]+)'
freqPattern = re.compile(PATTERN_FREQ, re.IGNORECASE)
'''
@return list of tuples (callSign, freq)
'''        
def listFreq(soup):
    retVal = list()
    
    freqTag = soup.find('div', id='aerodrome-frekvence')

    items = freqTag.find_all('div')
    for item in items:  # Tag in ResultSet
        
        line = str(item).replace('\n', '')
        
        m = freqPattern.findall(line)
        if m:
            callSign = m[0][0]
            freq = m[0][1]
            #print("{} : {}".format(callSign, freq))
            retVal.append((callSign, freq))
        
    return retVal


PATTERN_GPS = '^.+?([0-9]+).+?([0-9]+).+?([0-9]+).+?([NS]).+?([0-9]+).+?([0-9]+).+?([0-9]+).+?([EW]+)'
PATTERN_ELEV = 'ELEV.+?([0-9]+).+?([0-9]+)'
PATTERN_ELEV_CIRCLE = 'Okruh.+?([0-9]+).+?([0-9]+)'
gpsPattern = re.compile(PATTERN_GPS, re.IGNORECASE)
elevPattern = re.compile(PATTERN_ELEV, re.IGNORECASE)
circleAltPattern = re.compile(PATTERN_ELEV_CIRCLE, re.IGNORECASE)
'''
@return (gps (lat, lon), elevation ([ft], [m]), circleAlt ([ft], [m])
'''
def getGpsElevationCircle(soup):
    gps = None
    elevation = None
    circleAlt = None
    
    tag = soup.find('div', id='aerodrome-poloha')
    line = str(tag).replace('\n', '')
    
    m = gpsPattern.findall(line)
    if m:
        latDeg = int(m[0][0])
        latMin = int(m[0][1])
        latSec = int(m[0][2])
        latSign = m[0][3]
        
        lat = latDeg + latMin/60 + latSec / 3600
        if latSign == 'S': lat = -1 * lat
        
        lonDeg = int(m[0][4])
        lonMin = int(m[0][5])
        lonSec = int(m[0][6])
        lonSign = m[0][7]
        
        lon = lonDeg + lonMin/60 + lonSec / 3600
        if lonSign == 'W': lon = -1 * lon
  
        gps = (lat, lon)

    
    m = elevPattern.findall(line)
    if m:
        elevFt = m[0][0]
        elevM = m[0][1]
        elevation = (int(elevFt), int(elevM))
        
    m = circleAltPattern.findall(line)
    if m:
        ft = m[0][0]
        m = m[0][1]
        circleAlt = (int(ft), int(m))

    return (gps, elevation, circleAlt)


PATTERN_RWY = '.+?([0-9]+[LR]{0,1}).+<td>([0-9]+).+?x.+?([0-9]+)'
rwyPattern = re.compile(PATTERN_RWY, re.IGNORECASE)
'''
@return list of [('16-32', dimensions)]
'''
def listRunways(soup):
    rwys = list()
    
    tag = soup.find('table', id='aerodrome-drahy')
    if tag:
        rwyDir1 = None
        rows = tag.find_all('tr')
        for row in enumerate(rows[1:]):
            i = row[0]
            line = str(row[1]).replace('\n', '')
            
            if i % 2 == 0:
                m = rwyPattern.findall(line)
                if m:
                    rwyDir1 = m[0][0]
            else:
                m = rwyPattern.findall(line)
                if m:
                    rwyDir2 = m[0][0]
                    rwyDim = "{}x{}".format(m[0][1], m[0][2])
                    
                    rwys.append(("{}-{}".format(rwyDir1, rwyDir2), rwyDim))
    
    return rwys


'''
@return (name, code)
'''
def getNameCode(soup):
    tag = soup.find('div', id='admenubar')
    tag = tag.find('h2')
    
    items = str(tag.string).split('-')

    code = items[0].strip()
    name = items[1].strip()
    
    return (name, code)


'''
@return: list of texts
'''
def getProcedures(soup):
    procedures = []
    
    tag = soup.find('div', id='aerodrome-postupy')
    pTags = tag.find_all("p")
    for p in pTags:
        if 'NIL' in p.text: continue
        t = p.text.replace('\n', '').replace('\t', '')
        while t.find('  ') >= 0: t = t.replace('  ', ' ')    # remove long spaces
        
        procedures.append(t.strip())
    
    return procedures


PATTERN_CONTACT_NAME = '<strong>(.+?)<\/strong>'
PATTERN_CONTACT_PHONE = '([+][0-9]+.[0-9]+.[0-9]+.[0-9]+)'
PATTERN_CONTACT_MAIL = 'mailto:(.+?)"'
contactNamePattern = re.compile(PATTERN_CONTACT_NAME, re.IGNORECASE)
contactPhonePattern = re.compile(PATTERN_CONTACT_PHONE, re.IGNORECASE)
contactMailPattern = re.compile(PATTERN_CONTACT_MAIL, re.IGNORECASE)
'''
@return list of dicts (name, phone, mail)
'''
def getContacts(soup):
    contacts = []
    
    tag = soup.find('div', id='aerodrome-kontakty')
    pTags = tag.find_all("p")
    for p in pTags:
        line = p.prettify().replace('\n', '').replace('\t', '').replace('\u00a0', ' ')
        #print("line:", line)

        name = None
        phone = None
        mail = None
        
        m = contactNamePattern.findall(line)
        if m: name = m[0].strip()
            
        m = contactPhonePattern.findall(line)
        if m: phone = m[0].strip()

        m = contactMailPattern.findall(line)
        if m: mail = m[0].strip()
        
        #print("contact:\n {}\n {}\n {}".format(name, phone, mail))
        m = dict()
        if name: m["name"] = name
        if phone: m["phone"] = phone
        if mail: m["mail"] = mail
        
        contacts.append(m)
    
    return contacts

DIA1 = 'áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ'
DIA2 = 'acdeeinorstuuyzACDEEINORSTUUYZ'
def removeDiacritic(s):
    l=[]
    for c in s:
        if c in DIA1:
            i = DIA1.find(c)
            l.append(DIA2[i])
            
        else:
            l.append(c)
    
    return ''.join(l)


def doTest():
    filename = '../data/lkka_text_cz.html'
#     filename = '../data/lktb_text_cz.html'
#     filename = '../data/lksu_text_cz.html'  
    
    f = open(filename, 'r')
    html = f.read()
    f.close()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    freqList = listFreq(soup)
    print("freq:", freqList)

    (gps, elevation, circleAlt) = getGpsElevationCircle(soup)
    print("gps:", gps)
    print("elev:", elevation)
    print("circle", circleAlt)
    
    runways = listRunways(soup)
    print("rwys:",runways)
    
    (name, code) = getNameCode(soup)
    print("name:", name)
    print("code:", code)
    

def doProcess(filename, outPath):
    j = dict()
    
    f = open(filename, 'r')
    html = f.read()
    f.close()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    freqList = listFreq(soup)
    j["freq"] = freqList

    (gps, elevation, circleAlt) = getGpsElevationCircle(soup)
    j["coords"] = (float("{:.5f}".format(gps[0])), float("{:.5f}".format(gps[1])))
    j["elev"] = elevation
    if circleAlt: j["circleAlt"] = circleAlt    # some don't have it 
    
    runways = listRunways(soup)
    j["rwy"] = runways
    
    (name, code) = getNameCode(soup)
    j["code"] = code
    j["name"] = name
    
    nameAlias = removeDiacritic(name)
    if name != nameAlias:
        j["nameAlias"] = nameAlias

    contacts = getContacts(soup)
    j["contacts"] = contacts
        
    procedures = getProcedures(soup)
    j["txt"] = dict()
    j["txt"]["cz"] = dict()
    j["txt"]["cz"]["proc"] = procedures
    
    s = json.dumps(j, separators=(',',':'))
    
    outFilename = "{}/{}.json".format(outPath, code.lower())
    f = open(outFilename, 'w')
    f.write(s)
    f.close()
    

TEST = False
if __name__ == '__main__':

    if not TEST:
        if len(sys.argv) != 3:
            print("Usage: html2json <filename> <outPath>\n where filename is lk**_text_[cz|en].html")
            sys.exit(0)
    
        filename = sys.argv[1]
        outPath = sys.argv[2]
    
    else:
        filename = '../data/lkka_text_cz.html'
#         filename = '../data/lksu_text_cz.html'
#         filename = '../data/lkmt_text_cz.html'
#         filename = '../data/lktb_text_cz.html'
        outPath = '/tmp/00/'
        

    doProcess(filename, outPath)
    
    print("KOHEU.")
    
    
