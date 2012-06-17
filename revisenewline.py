import codecs
import getopt
import os
import sys

import fileworker

def revisefileend(filename, end):
    if not checkfileend(filename, end):
        f = open(filename, "a")
        f.write(end)
        f.close()
        print("    revised!")

def checkfileend(filename, end):
    lines = reverseread(filename, 2)
    return len(lines) > 0 and lines[-1].endswith(end)

def reverseread(filename, linecount = 1, stepcount = 82):
    f = codecs.open(filename, "r", "utf-8", "ignore")
    f.seek(0, 2)
    bytecount = f.tell()
    lines = []
    while bytecount > 0 and linecount > len(lines) - 1:
        readcount = min(bytecount, stepcount)
        f.seek(bytecount - readcount, 0)
        chunk = f.read(readcount)
        curlines = chunk.split(os.linesep)
        if not lines:
            lines = curlines
        elif len(lines) > 0 and len(curlines) > 0:
            # last read may truncate 'os.linesep', we merge it here
            mergelines = (curlines[-1] + lines[0]).split()
            lines = curlines[0:-1] + mergelines + lines[1:]
        bytecount -= readcount

    if linecount > len(lines):
        return lines
    else:
        return lines[len(lines) - linecount]

class Job:
    def __init__(self):
        pass

    def Process(self):
        pass

class ReviseJob:
    def __init__(self):
        pass

    def Process(self, filename):
        print("deal with '" + os.path.basename(filename) + "'")
        revisefileend(filename, "\n")

if __name__ == "__main__":
    worker = fileworker.FileWorker()
    opts, args = getopt.getopt(sys.argv[1:], "s:p:rh", ["help"])
    for op, value in opts:
        if op == "-s":
            worker.SetSuffixs(value)
        elif op == "-p":
            worker.SetPath(value)
        elif op == "-r":
            worker.SetRecursive(value=="yes")
        elif op == "-h" or op == "--help":
            worker.PrintUsage()
            sys.exit()

    print("Start...")
    job = ReviseJob()
    worker.Work(job)
    print("Finished!")

