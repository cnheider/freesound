from Crypto.Cipher import AES
from django.conf import settings
import base64
import md5
import os

class File:
    id = 0
    
    def __init__(self, name, full_path, is_dir):
        self.name = name
        self.full_path = full_path
        self.is_dir = is_dir
        self.children = [] if is_dir else None

        self.id = "file%d" % File.id
        File.id += 1
    
    def recursive_print(self, spacer=""):
        print spacer + self.name
        if self.is_dir:
            for child in self.children:
                child.recursive_print(spacer + "  ")        

def generate_tree(path):
    all_files = []

    lookups = {path: File(path, path, True)}
    files = {} 
    
    for (root, dirnames, filenames) in os.walk(path):
        parent = lookups[root]
    
        for dirname in dirnames:
            full_path = os.path.join(root, dirname)
            file_object = File(dirname, full_path, True)
            lookups[full_path] = file_object
            parent.children.append(file_object)
            
        for filename in filenames:
            full_path = os.path.join(root, filename)
            file_object = File(filename, full_path, False)
            files[file_object.id] = filename
            parent.children.append(file_object)
            

    return lookups[path], files

def md5file(filename):
    """Return the hex digest of a file without loading it all into memory"""
    fh = open(filename, "rb")
    digest = md5.new()
    while 1:
        buf = fh.read(4096)
        if buf == "":
            break
        digest.update(buf)
    fh.close()
    return digest.hexdigest()
