from pathlib import Path
import numpy as np
import Markov as mk
import os
from time import time

#Main script for the Markov modeling part. Inputs are explained in MaMaStat.py. Generates a csv file with the features per each row.
def main(WHICHSAMPLES,wf,WHICHCLASS,dbs=None,appslist=None):
    with Path(f'{WHICHCLASS}Occ.txt').open() as packseq:
        PACKETS = [line.strip() for line in packseq]

    allnodes = PACKETS + ['selfdefined', 'obfuscated']
    
    Header = ['filename'] + [
        f'{i}To{j}' for i in allnodes for j in allnodes
    ]
    print(f'Header is long {len(Header)}')

    dbcounter = 0
    checks = list(range(0, 13000, 1000))
    
    for v, sample in enumerate(WHICHSAMPLES):
        numApps = os.listdir(f'graphs/{sample}/')
        DatabaseRes = [Header]
        leng = len(numApps)

        for i in range(len(numApps)):
            if i in checks:
                print(f'starting {i+1} of {leng}')
                
            if wf == 'Y':
                with open(f'{WHICHCLASS}/{sample}/{numApps[i]}') as callseq:
                    specificapp = callseq.readlines()
            else:
                specificapp = dbs[dbcounter][i]

            MarkMat = mk.main(specificapp, allnodes, wf)
            
            MarkRow = [
                numApps[i] if wf == 'Y' else appslist[dbcounter][i]
            ] + [
                MarkMat[i][j] 
                for i in range(len(MarkMat)) 
                for j in range(len(MarkMat))
            ]
            
            DatabaseRes.append(MarkRow)
            
        dbcounter += 1
        
        output_file = Path(f'Features/{WHICHCLASS}/{sample}.csv')
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            for line in DatabaseRes:
                f.write(f"{line}\n")

