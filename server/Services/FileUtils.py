'''
Created on May 31, 2016

@author: PDINDA
'''


import glob
import json
from os.path import join, dirname
import os.path
import shutil
import traceback
import zipfile

from PIL import Image


def fileToJson(file_path=None):
    if file_path is None:
        raise ValueError("No File to read:" + str(file_path))
    if os.path.isfile(file_path):
        with open(file_path) as json_data:
            d = json.load(json_data)
            json_data.close()
            return d
    else:
        raise ValueError("File not found:" + str(file_path))


def jsontoFile(filename_with_path=None, data=None):
    if filename_with_path is None:
        raise ValueError("No path set for file :" + str(filename_with_path))
    if data is None:
        raise ValueError("No data is provided to write to file")
    if os.path.exists(filename_with_path):
        raise ValueError("File already exists in path :" + str(filename_with_path))
    if not os.access(os.path.dirname(filename_with_path), os.W_OK):
        raise ValueError(
            "The directory does not have write access :" + str(filename_with_path))
    with open(filename_with_path, 'w') as outfile:
        json.dump(data, outfile)
        return filename_with_path


def addFolderToZip(myZipFile, folder_to_zip):
    # convert path to ascii for ZipFile Method
    folder_to_zip = folder_to_zip.encode('ascii')
    for file in glob.glob(folder_to_zip + "/*"):
        if os.path.isfile(file):
            myZipFile.write(file, os.path.basename(file), zipfile.ZIP_STORED)
        elif os.path.isdir(file):
            addFolderToZip(myZipFile, file)


def createZipFile(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w",
                         zipfile.ZIP_STORED, allowZip64=True)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname, filename),
                                        arcname)
            zf.write(absname, arcname)
    zf.close()
    if not os.path.isfile(dst + ".zip"):
        raise ValueError("The file: " + dst + ".zip was not created")


def renameFile(old_name_with_path, new_name):
    if old_name_with_path is None:
        raise ValueError("No path set for file")
    if new_name is None:
        raise ValueError("No new_name is provided to rename the file")
    if not os.access(os.path.dirname(old_name_with_path), os.W_OK):
        raise ValueError("The directory does not have write access")
    if os.path.exists(new_name):
        if os.path.isfile(new_name):
            os.remove(new_name)
        elif os.path.isdir(new_name):
            shutil.rmtree(new_name)
    os.rename(old_name_with_path, new_name)


def returnJsonFromFiles(file_path, file_name):
    json_files = [pos_json for pos_json in os.listdir(
        file_path) if pos_json.endswith('.json')]
    if json_files is None:
        raise ValueError("No file " + file_name + " found.Invalid zip file")
    for file in json_files:
        if file in [file_name]:
            return fileToJson(file_path + '/' + file)


def thumbnail(image_details, thumbnail_file_path):
    #
    size = 86, 86

    outfile = thumbnail_file_path
    if image_details != outfile:
        try:
            print 'FileUtils :thumbnail: Trying to create thumbnail for ' + image_details
            im = Image.open(image_details)
            im.thumbnail(size)
            im.save(outfile)
            print "Thumbnail Created at  '%s'" % outfile
            return outfile
            # im.save(file_path)
        except IOError as e:  # catch *all* exceptions
            print 'Error :' + str(e)
            traceback.print_exc()
            return None
            # return jsonify({"result":"failed","message":str(e)}), 404


def unzipImportFile(file_path):
    file_name_without_ext = os.path.basename(file_path).split(".")[0]
    extract_to_dir = os.path.normpath(
        join(os.path.dirname(file_path), file_name_without_ext))
    zip_ref = zipfile.ZipFile(file_path, 'r')
    zip_ref.extractall(os.path.normpath(
        join(os.path.dirname(file_path), file_name_without_ext)))
    zip_ref.close()
    return extract_to_dir


def check_if_exists(path):
    if path and not os.path.exists(path):
        raise Exception("Path:" + path + " is invalid or does not exists")
    return True


def mkdirs(dirs_to_create, overwrite=False):
    if type(dirs_to_create) is not list:
        dirs_to_create = [dirs_to_create]
    for path in dirs_to_create:
        if not os.path.exists(path):
            os.makedirs(path)
        elif os.path.exists(path) and overwrite:
            shutil.rmtree(path)
            os.makedirs(path)
