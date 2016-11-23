# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 09:02:21 2016

@author: mathieu boily
"""

import getopt
import sys
import subprocess
import os
import datetime
from os.path import isfile, isdir, join, listdir

"""
Takes a number, in bytes, as argument.
Converts this number in kb, mb, gb or tb ans returns it with the corresponding unit as string.
"""
def formatSize(size):
    units = ["Bytes", "Kb", "Mb", "Gb", "Tb"]
    count = 0
    
    while size > 1024:
        size /= 1024
        count += 1
        
    return str(round(size, 1)) + " " + units[count]
    
"""
Iterates through all folders and writes their size, creation date and version.
Creates a file in each folder describing these metadata.
"""
def folderSize(folderName, fileName):
    #Current date for the creation date.
    today = datetime.datetime.now().strftime("%d-%m-%Y")
    """
    Recursive function. Goes to the deepest folder and comes back.
    """
    def aux(path):
        folderSize = 0
        for subdir in os.listdir(path):
            #For each files in the current one.
            current = join(path, subdir)
            if isdir(current):
                #If the file is a directory, calls himself to go deeper.
                subfoldersSize = aux(current)
                folderSize += subfoldersSize
            else:
                #If it's a normal file, get its size.
                tmp = os.stat(current).st_size
                folderSize += tmp
                
        metadata = {}
        if isfile(os.path.join(path, fileName)):
            #if the metadata file already exists
            with open(join(path, fileName)) as file:
                #Open it and retreive each metadata.
                for line in file:
                    tmp = line.split(":")
                    metadata[tmp[0]] = tmp[1]
            metadata["size"] = formatSize(folderSize)
            metadata["version"] = int(metadata["version"]) + 1
            metadata["creation date"] = today
        else:
            #If it doesn't exist, we create it.
            metadata["size"] = formatSize(folderSize)
            metadata["creation date"] = today
            metadata["version"] = 1
            
        with open(join(path, fileName), "w") as file:
            #Writes the new metadata for this folder
            for key, value in metadata.items():
                file.write(key + ":" + str(value).strip() + "\n")
        
        return folderSize
    
    aux(folderName)
    
def getNextHundred(number):
    return number if number % 100 == 0 else number + 100 - number % 100
    
def moveOutput(projectPath, scenario, iteration):
    try:
        if not isdir(join(projectPath, scenario)):
            os.mkdir(join(projectPath, scenario))
            
        if iteration == 0:
            os.rename(join(projectPath, "Summary.gz"), join(projectPath, scenario, "0_Summary.gz"))
            
        os.rename(join(projectPath, "Output.gz"), join(projectPath, scenario, str(iteration) + "_Output.gz"))
    except OSError as ex:
        print("An error occurred while moving the Output.gz at iteration " + str(iteration) + " of scenario '" + scenario + "'.")
        print("Project directory contains : ")
        print([f for f in listdir(projectPath) if os.path.isfile(join(projectPath, f))])
        print("Error is : ", ex.errno, ex.strerror)

def main(argv):
    projectName = ""
    projectPath = ""
    advParameters = ""
    rapId = ""
    scenarios = []
    mode = 0
    task = 0 # Running task. Equivalent of the index in the jobs' list
    iterations = 0
    
    try:
        #Accepted arguments
        options, arguments = getopt.getopt(argv, "p:m:t:o:r:i:s:", ["project=", "mode=", "task=", "iterations=", "options=", "rap-id=", "scenario="])
    except getopt.GetoptError as error:
        print(error)
        sys.exit(2)
    
    #Parsing all the options
    for opt, arg in options:
        if opt in ('-p', '--project'):
            projectName = arg
        elif opt in ("-t", "--task"):
            task = int(arg)
        elif opt in ("-m", "--mode"):
            mode = int(arg)
        elif opt in ("-o", "--options"):
            advParameters = " -p " + arg
        elif opt in ("-r", "--rap-id"):
            rapId = arg
        elif opt in ("-s", "--scenario"):
            scenarios.append(arg)
        elif opt in ("-i", "--iterations"):
            iterations = int(arg)
            
    # Required fields
    if not projectName or not mode or not rapId or task < 0 or not scenarios or not iterations:
        print("Missing arguments. Received : " + str(options))
        sys.exit(2)
        
    projectPath = join("/scratch", rapId, projectName)
   
    print("Mode : ", mode, "Task : ", task)
    schnapsOutput = open(join(projectPath, "schnapsOutput.txt"), "a")
    if mode == 1:
        # 1 job per simulation (Ex. 5 scenarios with 100 simulations = 500 jobs)
        scenario = scenarios[getNextHundred(task) / 100]
        configFile = "parameters_" + str(task % iterations) + ".xml"
        subprocess.call(["schnaps", "-c", configFile, "-d", projectPath, "-s", scenario, "-p", advParameters], stdout=schnapsOutput)
        moveOutput(projectPath, scenario, task)
    elif mode == 2:
        # 1 job per iteration
        for scenario in scenarios:
            configFile = "parameters_" + str(task) + ".xml"
            subprocess.call(["schnaps", "-c", configFile, "-d", projectPath, "-s", scenario, "-p", advParameters], stdout=schnapsOutput)
            moveOutput(projectPath, scenario, task)
    elif mode == 3:
        # 1 job per scenario
        for i in range(0, iterations):
            scenario = scenarios[task]
            configFile = "parameters_" + str(i) + ".xml"
            subprocess.call(["schnaps", "-c", configFile, "-d", projectPath, "-s", scenario, "-p", advParameters], stdout=schnapsOutput)
            moveOutput(projectPath, scenario, i)
    else:
        # 1 job for all
        for scenario in scenarios:
            for j in range(0, iterations):
                configFile = "parameters_" + str(j) + ".xml"
                subprocess.call(["schnaps", "-c", configFile, "-d", projectPath, "-s", scenario, "-p", advParameters], stdout=schnapsOutput)
                moveOutput(projectPath, scenario, j)
    
    schnapsOutput.close()
    #Creates the metadata file in each directory of the project.
    #Do not modify the metadata's filename, unless you modify it also in the configuration file of Koksoak's website (/var/www/html/conf.php)
    folderSize(os.path.join("/scratch", rapId, projectName), ".meta")


main(sys.argv[1:])