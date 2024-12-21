from pathlib import Path
from multiprocessing import Process, Queue
import numpy as np
import PackAbs as Pk

# This script does the abstraction to packages of the API calls.


# This function is called when -wf flag is set to Y to operate the abstraction.
def fileextract(fileitem, numApps, WHICHSAMPLES, v, PACKETS, pos):
    Packetsfile = []
    
    input_path = Path('Calls') / WHICHSAMPLES[v] / fileitem
    output_path = Path('Packages') / WHICHSAMPLES[v] / fileitem
    
    with input_path.open(encoding='utf-8') as callseq:
        specificapp = []
        
        for line in callseq:
            Packetsline = []
            
            for j in line.split('\t')[:-1]:
                match = None
                j = j.replace('<', '')
                j = j.replace(' ', '')
                
                match = Pk.PackAbs(j, pos)
                
                if match is None:
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

    with output_path.open('w', encoding='utf-8') as f:
        for j in range(0, len(Packetsfile)):
            eachline = '\t'.join(Packetsfile[j])
            f.write(f"{eachline}\n")

def main(WHICHSAMPLES, wf, CORES, callsdatabase=None):
    PACKETS = []
    
    with Path('Packages.txt').open(encoding='utf-8') as packseq:
        PACKETS = [line.strip() for line in packseq]
    
    allpacks = [i.split('.')[1:] for i in PACKETS]
    pos = [[] for _ in range(9)]
    
    for i in allpacks:
        k = len(i)
        for j in range(0, k):
            if i[j] not in pos[j]:
                pos[j].append(i[j])

    packdb = []
    if wf == 'Y':
        for v in range(0, len(WHICHSAMPLES)):
            numApps = os.listdir(os.path.join('Calls', WHICHSAMPLES[v]))
            
            queue = Queue()
            for i in range(0, len(numApps)):
                queue.put(numApps[i])
            
            ProcessList = []
            numfor = min(len(numApps), CORES)
            
            for rr in range(0, numfor):
                fileitem = queue.get()
                process = Process(target=fileextract, args=(fileitem, numApps, WHICHSAMPLES, v, PACKETS, pos))
                ProcessList.append(process)
                process.daemon = True
                process.start()

            while not queue.empty():
                for rr in range(0, CORES):
                    if not ProcessList[rr].is_alive():
                        ProcessList[rr].terminate()
                        
                        if not queue.empty():
                            fileitem = queue.get()
                            process = Process(target=fileextract, args=(fileitem, numApps, WHICHSAMPLES, v, PACKETS, pos))
                            ProcessList[rr] = process
                            process.daemon = True
                            process.start()

            for process in ProcessList:
                process.join()

    else:
        for db in callsdatabase:
            appdb = []
            for app in db:
                Packetsfile = []
                for line in app:
                    Packetsline = []
                    for j in line.split('\t')[:-1]:
                        match = None
                        j = j.replace('<', '').replace(' ', '')
                        
                        match = Pk.PackAbs(j, pos)
                        
                        if match is None:
                            splitted = j.split('.')
                            obfcount = sum(1 for k in splitted if len(k) < 3)
                            match = 'obfuscated' if obfcount >= len(splitted)/2 else 'selfdefined'
                        Packetsline.append(match)
                    Packetsfile.append(Packetsline)
                appdb.append(Packetsfile)
            packdb.append(appdb)
            
    return packdb

