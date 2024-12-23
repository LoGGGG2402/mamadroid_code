from pathlib import Path
import argparse
import sys
import multiprocessing
import math
import TxtToCallsCSV as TTC
import callsToFamilies as cTF
import callsToPack as cTP
import MarkovCall as MC
import os
from multiprocessing import freeze_support

def writelists(tbwritten, filepath):
    Path(filepath).write_text('\n'.join(map(str, tbwritten)) + '\n')

# This script manages the scripts related to the whole statistical model. Starting from the result of the static analysis, arrives to the generation of the csv file per database of samples.
# The script requires as input a python array of the names of the folders in the graph folder related to the databases which samples we want to extract the features. These folders must contain the files created by the static analysis. The python array structure has to be mantained even if there is only one database.
# It requires as well a flag (Y or N) if you desire to write the files during the intermediate steps (from the graph folder to the call to the families/package one). If the flag is set on N it will only write the final csv. When the flag is set on Y the script is a lot slowert output part.
# Indicate first the databases folders in this format: database1:database2:database3. Then indicate Y or N (--writefiles) as second argument.
# The features files (one per indicated database) will be created as "name_of_the_database".csv files in the folders Features/Families and Features/Packages.

if __name__ == '__main__':
    freeze_support()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--database", help="specify the databases folder in graphs/ in which the samples are in this format: database1:database2:database3",
                        type=str)
    parser.add_argument("-wf","--writefiles", help="flag to write intermediate files or not, write -wf followed by Y or N",type=str)
    parser.add_argument("-c","--cores", type=int, help="Part of the scripts fork in more processes. default cores number is 75% of the cores of the machine, please specify if you want a different number.")
    args = parser.parse_args()
    if args.database:
        dbs = args.database.split(':')
    else:
        sys.exit("no database input. Please, check the help.")
    if args.writefiles:
        wflag = args.writefiles
    else:
        wflag = 'N'
        print("no writefiles option used, the default option is not writing the intermediate files.")
    if wflag == 'Y':
        for i in dbs:
            try:
                os.mkdir('Calls/'+i)
                os.mkdir('Families/'+i)
                os.mkdir('Packages/'+i)
            except:
                print('folders creation failed, probably the folders are already in place!')

    if args.cores:
        cores = args.cores
    else:
        cores = int(math.ceil(0.75*multiprocessing.cpu_count()))
        print("no cores option used, the default option is 75% cores.")
        
    print("starting rearranging the files")    
    callsdatabase, appslist = TTC.main(dbs, wflag)

    try:
        # Check if required files exist
        required_files = ['FamiliesOcc.txt', 'PackagesOcc.txt', 'Families.txt', 'Packages.txt']
        for file in required_files:
            if not os.path.exists(file):
                print(f"Error: Required file {file} not found")
                sys.exit(1)
                
        # Create required directories if they don't exist
        for i in dbs:
            for dir in ['Calls', 'Families', 'Packages', 'Features/Families', 'Features/Packages']:
                try:
                    os.makedirs(f'{dir}/{i}', exist_ok=True)
                except Exception as e:
                    print(f'Warning: Could not create directory {dir}/{i}: {e}')
                    
        if wflag == 'Y':
            callsdatabase = None
            print("starting the abstraction to families")
            _ = cTF.main(dbs, wflag, cores)
            print("abstraction to families is finished")
            print("starting the abstraction to packages")
            _ = cTP.main(dbs, wflag, cores)
            print("abstraction to packages is finished")
            print("starting the Markov model creation in families abstraction")
            MC.main(dbs, wflag, 'Families')
            print("Markov model in families abstraction finished, features file created in Features/Families/")
            print("starting the Markov model creation in packages abstraction")
            MC.main(dbs, wflag, 'Packages')
            print("Markov model in packages abstraction finished, features file created in Features/Packages/")
        else:
            print("starting the abstraction to families")
            famdatabase = cTF.main(dbs, wflag, cores, callsdatabase)
            print("abstraction to families is finished")
            print("starting the abstraction to packages")
            packdatabase = cTP.main(dbs, wflag, cores, callsdatabase)
            callsdatabase = None
            print("abstraction to packages is finished")
            print("starting the Markov model creation in families abstraction")
            MC.main(dbs, wflag, 'Families', famdatabase, appslist)
            famdatabase = None
            print("Markov model in families abstraction finished, features file created in Features/Families/")
            print("starting the Markov model creation in packages abstraction")
            MC.main(dbs, wflag, 'Packages', packdatabase, appslist)
            packdatabase = None
            print("Markov model in packages abstraction finished, features file created in Features/Packages/")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
