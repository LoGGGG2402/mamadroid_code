'''
info: This script parses the call egdes extracted from apps into caller and callee
''' 

from collections import defaultdict
from pathlib import Path

def parse_graph(app, _dir):
    caller = []
    callee = []
    edges = defaultdict(list)
    filename = Path(app).name
    _newFile = filename.replace(".apk", "") if '.apk' in filename else filename

    with open(app) as lines:
        for line in lines:
            line = line.rpartition(" ==> ")
            callee.append(line[2])
            
            if line[0].count(" in ") > 1:
                calls = line[0].split(" in ")
                if calls[1].startswith("<"):
                    _index = calls[1].index("<")
                    if calls[1][int(_index) + 1].isalnum():
                        caller.append(calls[1])
                else:
                    _call = line[0].rpartition(" in ")
                    if _call[2].startswith("<"):
                        _index = _call[2].index("<")
                        if _call[2][int(_index) + 1].isalnum():
                            caller.append(_call[2])
            else:
                calls = line[0].split(" in ")
                try:
                    caller.append(calls[1])
                except:
                    print(f"{line[0]}%%{line[1]}")

    for c, n in zip(caller, callee):
        edges[c].append(n)

    newfile = f"{_dir}/graphs/{_newFile}"
    with open(newfile, 'w') as out:
        for edge, targets in edges.items():
            out.write(f"{edge} ==> {targets}\n")

    return newfile

