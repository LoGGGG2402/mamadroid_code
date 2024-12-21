from time import time
import csv
import os
import subprocess
import numpy as np

def main(WHICHSAMPLES, wf):
    alldb = []
    allapps = []
    
    for sample in WHICHSAMPLES:
        onedb = []
        apps = os.listdir(f'graphs/{sample}/')
        allapps.append(apps)
        leng = len(apps)
        
        checks = list(range(0, 13000, 1000))
        for i, app in enumerate(apps):
            if i in checks:
                print(f'starting {i+1} of {leng}')
                
            with open(f'graphs/{sample}/{app}') as callseq:
                specificapp = callseq.readlines()

            call = []
            nextblock = []
            nextcall = []
            start_time = time()
            
            for line in specificapp:
                if line[0] == '<' and (line[1] == "'" or line[1].isalpha()):
                    call.append(line.split('(')[0])
                    nextblock.append(line.split('==>')[1])

            for block in nextblock:
                supporto = block.translate({ord(c): None for c in '[]\'\\n'})
                nextcall.append(supporto.split(','))

            wholefile = [
                f"{call[j]}\t{''.join(nc.split('(')[0] + '\t' for nc in nextcall[j])}"
                for j in range(len(call))
            ]

            if wf == 'Y':
                with open(f'Calls/{sample}/{app}', 'w') as f:
                    f.write('\n'.join(wholefile) + '\n')
                    
            onedb.append(wholefile)
            
        alldb.append(onedb)
        
    return alldb, allapps

