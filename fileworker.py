import os

class FileWorker:
    def __init__(self, path=os.getcwd(), suffixs="h,c,hpp,cpp,proto,py", recursive=True):
        self.SetPath(path)
        self.SetSuffixs(suffixs)
        self.SetRecursive(recursive)

    def SetPath(self, path):
        self.__path = path

    def SetSuffixs(self, suffixs):
        self.__suffixs = []
        self.__emptysuffix = False
        self.__ignoresuffix = False

        words = suffixs.split(",")
        for word in words:
            if word == "":
                self.__emptysuffix = True
            elif word == "*":
                self.__ignoresuffix = True
            else:
                self.__suffixs.append("." + word)

    def SetRecursive(self, recursive):
        self.__recursive = recursive

    def Work(self, job):
        if os.path.isdir(self.__path):
            self.__WorkDir(self.__path, job)
        elif os.path.isfile(self.__path):
            self.__WorkFile(self.__path, job)

    def PrintUsage(self):
        print("revisenewline.py [-p path] [-s suffixs] [-r yes|no] [-h|--help]")

    def __WorkDir(self, dirname, job):
        assert(os.path.isdir(dirname))
        for child in os.listdir(dirname):
            childpath = os.path.join(dirname, child)
            if self.__recursive and os.path.isdir(childpath):
                self.__WorkDir(childpath, job)
            elif os.path.isfile(childpath):
                self.__WorkFile(childpath, job)

    def __WorkFile(self, filename, job):
        assert(os.path.isfile(filename))
        job.Process(filename)

    def __CheckSuffix(self, filename):
        if self.__ignoresuffix:
            return True
        elif self.__emptysuffix and not filename.endswith("."):
            return True
        else:
            for suffix in self.__suffixs:
                if filename.endswith(suffix):
                    return True
        
        return False

