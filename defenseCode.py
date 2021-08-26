import io
import os.path
import psutil
import sys
import re
import asyncio
import time

from io import TextIOWrapper

blacklist = ["listener", "pynput", "keylogger", "email", "smtp"]
list = []
matches = []
stop = True
counter = 0

# chars = r"A-Za-z0-9/\-:.,_$%'()[\]<> "
chars = r"A-Za-z./\' "
shortest_run = 4
regexp = '[%s]{%d,}' % (chars, shortest_run)
pattern = re.compile(regexp)


def process(path_to_file):
    #print(path_to_file)
    with open(path_to_file, 'r', encoding='utf-8', errors='ignore') as s:
        data = s.read()
        return pattern.findall(data)

#print("mypid = " + str(os.getpid()))
#print("parent pid = " + str(os.getppid()))
while stop:
    time.sleep(1)
    for proc in psutil.process_iter():
        try:
            if proc.name().__contains__("py"):
                #print("proc.name = " + proc.name())
                #print("proc.pid = " + str(proc.pid))
                #print("ppid = " + str(proc.ppid()))
                if proc.pid == os.getpid() or proc.pid == os.getppid() or list.__contains__(proc.pid):
                    continue
                else:               
                    list.append(proc.pid)
                    path = proc.exe()
                    for found_str in process(path):
                        matches.append(blck for blck in blacklist if blck in found_str)
                        #print(matches)
                        if len(matches) > 2:
                            print("-------------------")
                            print("Killing process = "+ proc.name())
                            print("Cmdline = "+' '.join(proc.cmdline()))
                            #print("len = " + len(matches).__format__(""))
                            #stop = False
                            matches = []
                            proc.kill()
                            #break
        except psutil.NoSuchProcess:
            print("The process you are trying to kill dose not exist...")
            pass