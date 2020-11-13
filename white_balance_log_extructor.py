# -*- coding: utf-8 -*-
import os
import re
import csv
from tqdm import tqdm

def createEveryTVLog(readedFile):
        newText = ''
        for log in readedFile:
            if 'WBA_RESULT' in log: 
                log = log + '\n' + "###################\n"
                newText += log
                print("newtext : ",newText)
            else:
                newText += log
        splittedLogs = newText.split('###################')
        returnedLogs = clearLogList(splittedLogs)
        return returnedLogs

def clearLogList(logList): 
    for log in logList:
        if 'WBA_RESULT= NOK' in log:
            del logList[logList.index(log)]
    return logList

def createFolder(folderPath):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

def calculateX(u,v):
    x = (9*u)/((6*u)-(16*v)+12)
    return x;

def calculateY(u,v):
    y = (4*v)/((6*u)-(16*v)+12)
    return y;

def calculateCCT(x,y):
    n = (x-0.3320)/(0.1858-y)
    CCT = (437*(pow(n,3))) + (3601*(pow(n,2))) + (6861*n) + 5517
    return round(CCT)

class stWBALog:
    projectName = ''
    panelName = ''    
    seriNo = ''
    firstValues = dict()
    rgbValuesForCool = dict()
    rgbValuesForStandard = dict()
    rgbValuesForWarm = dict()
    
folder_path = "/home/byesilbag/Projects/WBA/latestWBALogs"
all_files = os.listdir(folder_path)

listOfEveryThing = list()
for file in tqdm(all_files):
#for file in all_files:
    f = open(folder_path + '/' + file,'r')
    all_logs_in_a_file = f.readlines()
    splitted_log_list = createEveryTVLog(all_logs_in_a_file)

    for l in splitted_log_list:
        firstValueIndex = -1
        l = l.split('\n')
        tempSt = stWBALog()
        tempDict = dict()
        colorTemp = ''
        
        tempDictForCool = dict()
        tempDictForCool['0'] = '128'
        tempDictForCool['1'] = '128'
        tempDictForCool['2'] = '128'
        tempDictForCool['3'] = '128'
        tempDictForCool['4'] = '128'
        tempDictForCool['5'] = '128'
        
        tempDictForStandard = dict()
        tempDictForStandard['0'] = '128'
        tempDictForStandard['1'] = '128'
        tempDictForStandard['2'] = '128'
        tempDictForStandard['3'] = '128'
        tempDictForStandard['4'] = '128'
        tempDictForStandard['5'] = '128'
        
        tempDictForWarm = dict()
        tempDictForWarm['0'] = '128'
        tempDictForWarm['1'] = '128'
        tempDictForWarm['2'] = '128'
        tempDictForWarm['3'] = '128'
        tempDictForWarm['4'] = '128'
        tempDictForWarm['5'] = '128'
        
        
        for idx, val in enumerate(l):
            if 'TACT' in val:
                val = val.split('\t')
                tempSt.projectName = val[6]
                tempSt.panelName = val[8]
                tempSt.seriNo = val[7]
            if val == '[ SET_WBA_ColorTemp= 0 ]':
                colorTemp = 'cool'
            if val == '[ SET_WBA_ColorTemp= 1 ]':
                colorTemp = 'standard'
            if val == '[ SET_WBA_ColorTemp= 2 ]':
                colorTemp = 'warm'
            if val == '[ SET_OP2InternalRGB= 204 ]' or (colorTemp == 'cool' and val == '[ SET_OP2InternalRGB= 178 ]'):
                firstValueIndex = idx + 1
            if idx == firstValueIndex:
                val = re.sub('[\s+]', ' ', val)
                firstValues = val.split(':')[-1]
                firstValues = firstValues.split()
                u = int(firstValues[1])
                v = int(firstValues[3])
                Lv = int(firstValues[5])
                tempDict[colorTemp] = dict({'u':u,'v':v,'Lv':Lv})
                tempSt.firstValues = tempDict
            if 'SET_RgbGainOffset' in val:
                val = val.replace('[ ','|')
                val = val.replace(' ]','|')
                val = val.replace(': \t','|')
                val = val.replace('\t','|')
                val = val.replace('= ','=')
                component = val.split('|')[3].split('=')[1]
                value = val.split('|')[4].split('=')[1]
                if colorTemp == 'warm':
                    tempDictForWarm[component] = value
                if colorTemp == 'standard':
                    tempDictForStandard[component] = value
                if colorTemp == 'cool':
                    tempDictForCool[component] = value
        tempSt.rgbValuesForCool = tempDictForCool
        tempSt.rgbValuesForStandard = tempDictForStandard
        tempSt.rgbValuesForWarm = tempDictForWarm
        listOfEveryThing.append(tempSt)


main_folder = 'excel_files'
for ll in tqdm(listOfEveryThing):
    project_path = main_folder + '/' + ll.projectName
    createFolder(project_path)
    panel_path = project_path + '/' + ll.panelName
    createFolder(panel_path)
    if not os.path.isfile(panel_path + '/' + ll.panelName + '.csv'):
        with open(panel_path + '/' + ll.panelName + '.csv', 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['PROJECT NAME','PANEL NAME','SERI NO','COOL-u','COOL-v','COOL-Lv','COOL-x','COOL-y','COOL-CCT','COOL-RedGain','COOL-GreenGain','COOL-BlueGain','COOL-RedOffset','COOL-GreenOffset','COOL-BlueOffset','STANDARD-u','STANDARD-v','STANDARD-Lv','STANDARD-x','STANDARD-y','STANDARD-CCT','STANDARD-RedGain','STANDARD-GreenGain','STANDARD-BlueGain','STANDARD-RedOffset','STANDARD-GreenOffset','STANDARD-BlueOffset','WARM-u','WARM-v','WARM-Lv','WARM-x','WARM-y','WARM-CCT','WARM-RedGain','WARM-GreenGain','WARM-BlueGain','WARM-RedOffset','WARM-GreenOffset','WARM-BlueOffset'])
        
for ll in tqdm(listOfEveryThing):
    project_path = main_folder + '/' + ll.projectName
    panel_path = project_path + '/' + ll.panelName
    with open(panel_path + '/' + ll.panelName + '.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        if ll.firstValues:
            coolDict = ll.firstValues.get('cool')
            standardDict = ll.firstValues.get('standard')
            warmDict = ll.firstValues.get('warm')
            
            standardRedGain = ll.rgbValuesForStandard
            warmRedGain = ll.rgbValuesForWarm
  
            if bool(coolDict) and bool(standardDict) and bool(warmDict):
                cool_u = coolDict['u']/10000
                cool_v = coolDict['v']/10000
                cool_x = calculateX(cool_u,cool_v)
                cool_y = calculateY(cool_u,cool_v)
                cool_CCT = calculateCCT(cool_x,cool_y)
            
                standard_u = standardDict['u']/10000
                standard_v = standardDict['v']/10000
                standard_x = calculateX(standard_u,standard_v)
                standard_y = calculateY(standard_u,standard_v)
                standard_CCT = calculateCCT(standard_x,standard_y)
            
                warm_u = warmDict['u']/10000
                warm_v = warmDict['v']/10000
                warm_x = calculateX(warm_u,warm_v)
                warm_y = calculateY(warm_u,warm_v)
                warm_CCT = calculateCCT(warm_x,warm_y)
                
                writer.writerow([ll.projectName,ll.panelName,ll.seriNo,
                                 cool_u,cool_v,coolDict['Lv'],cool_x,cool_y,cool_CCT,
                                 ll.rgbValuesForCool.get('0'),ll.rgbValuesForCool.get('1'),ll.rgbValuesForCool.get('2'),ll.rgbValuesForCool.get('3'),ll.rgbValuesForCool.get('4'),ll.rgbValuesForCool.get('5'),
                                 standard_u,standard_v,standardDict['Lv'],standard_x,standard_y,standard_CCT,
                                 ll.rgbValuesForStandard.get('0'),ll.rgbValuesForStandard.get('1'),ll.rgbValuesForStandard.get('2'),ll.rgbValuesForStandard.get('3'),ll.rgbValuesForStandard.get('4'),ll.rgbValuesForStandard.get('5'),
                                 warm_u,warm_v,warmDict['Lv'],warm_x,warm_y,warm_CCT,
                                 ll.rgbValuesForWarm.get('0'),ll.rgbValuesForWarm.get('1'),ll.rgbValuesForWarm.get('2'),ll.rgbValuesForWarm.get('3'),ll.rgbValuesForWarm.get('4'),ll.rgbValuesForWarm.get('5')])
    

