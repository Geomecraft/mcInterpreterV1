import shutil
from os import listdir, path, unlink


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
