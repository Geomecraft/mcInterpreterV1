
import shutil
from os import listdir, path, unlink

from model.Exceptions import NamespaceError


def stripEachItem(lst):
    for i in range(0, len(lst)):
        lst[i] = lst[i].strip()  # get rid of spaces attached to parameters from splicing


def assertExistNamespace(memory):
    try:
        memory.currentNamespace
    except: #what error?
        raise NamespaceError("no current namespace is set")

def clearDirectory(dirPath):
    for filename in listdir(dirPath):
        file_path = path.join(dirPath, filename)
        try:
            if path.isfile(file_path) or path.islink(file_path):
                unlink(file_path)
            elif path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
