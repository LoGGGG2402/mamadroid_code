import csv
import time
import os
import subprocess
from multiprocessing import Pool, Process, Queue
import numpy as np

# This script does the abstraction to families of the API calls.


# This function is called when -wf flag is set to Y to operate the abstraction.
def fileextract(fileitem, numApps, WHICHSAMPLES, v, PACKETS):
    Packetsfile = []
    
    # Updated file handling with context manager
    with open(os.path.join('Calls', WHICHSAMPLES[v], str(fileitem)), 'r', encoding='utf-8') as callseq:
        specificapp = []
        for line in callseq:
            Packetsline = []
            
            for j in line.strip().split('\t')[:-1]:
                match = False
                for y in PACKETS:
                    x = y.partition('.')[2]
                    
                    j = j.replace('<', '').replace(' ', '')
                    
                    if j.startswith(x):
                        match = x
                        break
                if match == False:
                    splitted = j.split('.')
                    obfcount = 0
                    for k in range(0, len(splitted)):
                        if len(splitted[k]) < 3:
                            obfcount += 1
                    if obfcount >= len(splitted)/2:
                        match = 'obfuscated'
                    else:
                        match = 'selfdefined'
                Packetsline.append(match)
            Packetsfile.append(Packetsline)

    # Updated file writing with context manager
    with open(os.path.join('Families', WHICHSAMPLES[v], str(fileitem)), 'w', encoding='utf-8') as f:
        for j in range(0, len(Packetsfile)):
            eachline = '\t'.join(Packetsfile[j])
            f.write(f"{eachline}\n")

# The main function. Inputs are explained in MaMaStat.py. In case -wf is set to N the abstraction is operated in the else and not multiprocessed.
def main(WHICHSAMPLES, wf, CORES, callsdatabase=None):
    PACKETS = []
    with open('Families.txt', 'r', encoding='utf-8') as packseq:
        PACKETS = [line.strip() for line in packseq]

    famdb = []
    if wf == 'Y':
        for v in range(0, len(WHICHSAMPLES)):
            numApps = os.listdir(os.path.join('Calls', WHICHSAMPLES[v]))

            queue = Queue()
            for i in range(0, len(numApps)):
                queue.put(numApps[i])
                
            appslist = []
            leng = len(numApps)
            ProcessList = []
            numfor = min([leng, CORES])
            
            for rr in range(0, numfor):
                fileitem = queue.get()
                ProcessList.append(Process(target=fileextract, args=(fileitem, numApps, WHICHSAMPLES, v, PACKETS)))
                ProcessList[rr].daemon = True
                ProcessList[rr].start()
                
            while not queue.empty():
                for rr in range(0, CORES):
                    if not ProcessList[rr].is_alive():
                        ProcessList[rr].terminate()
                        if not queue.empty():
                            fileitem = queue.get()
                            ProcessList[rr] = Process(target=fileextract, args=(fileitem, numApps, WHICHSAMPLES, v, PACKETS))
                            ProcessList[rr].daemon = True
                            ProcessList[rr].start()
            
            for rr in range(0, len(ProcessList)):
                ProcessList[rr].join()

    else:
        for db in callsdatabase:
            appdb = []
            for app in db:
                Packetsfile = []
                for line in app:
                    Packetsline = []
                    
                    for j in line.split('\t')[:-1]:
                        match = False
                        for y in PACKETS:
                            x = y.partition('.')[2]
                            
                            j = j.replace('<', '').replace(' ', '')
                            
                            if j.startswith(x):
                                match = x
                                break

                        if match == False:
                            splitted = j.split('.')
                            obfcount = 0
                            for k in range(0, len(splitted)):
                                if len(splitted[k]) < 3:
                                    obfcount += 1
                            if obfcount >= len(splitted)/2:
                                match = 'obfuscated'
                            else:
                                match = 'selfdefined'
                        Packetsline.append(match)
                    Packetsfile.append(Packetsline)
                appdb.append(Packetsfile)
            famdb.append(appdb)
    return famdb

