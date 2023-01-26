import logging
import sys
import urllib.request, urllib.error, urllib.parse
import os
import json
import struct
import blowfish
import shutil
from shutil import copyfile, move, rmtree
import subprocess 
import unpacker_pak
from os.path import join
IPF_BLACKLIST = []
region = ""
error_ipf = [] #the somehow error patch
            

def copyfiles(output):
    if not os.path.exists(output):
        os.mkdir(output)
    files = ['shared.ipf', 
             'ies_ability.ipf',
             'ies_client.ipf',
             'ies_drop.ipf',
             'ies_mongen.ipf',
             'ui.ipf',
             'bg.ipf',
             'language.ipf',
             'ies.ipf',
             'xml.ipf',]
    for i in files:
        if os.path.exists (join('extract',i)):
            #try:
            #move(join('extract',i), join(output, i))
            subprocess.run(['cp', '-r', join('extract',i), output])
            logging.warning("copying to {}".format(join(output,i)))
            # except:
            #     logging.warning("copying {} failed".format(i))
            #     pass

    # move(join('extract','ies_ability.ipf'), output)
    # move(join('extract','ies_client.ipf'), output)
    # move(join('extract','ies_drop.ipf'), output)
    # move(join('extract','ies_mongen.ipf'), output)
    # move(join('extract','ui.ipf'), output)
    # move(join('extract','bg.ipf'), output)
    # move(join('extract','language.ipf'), output)
    # move(join('extract','ies.ipf'), output)
    # move(join('extract','xml.ipf'), output)

def unpack():
    IPF_PATH    = join("..", "{}_patch".format(region))
    OUTPUT_PATH = join("..", "{}_unpack".format(region))
    unpacker    = join("..", 'IPFUnpacker', 'ipf_unpack')
    cwd = os.getcwd()
    search_dir = IPF_PATH
    os.chdir(search_dir)
    files = filter(os.path.isfile, os.listdir())
    files = [ f for f in files] # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    
    os.chdir(cwd)
    files.sort()
    extension_needed = ['ies', 'xml', 'lua','png', 'jpg', 'tga', 'json','tok', 'colmesh', 'tsv'   ]
    for f in files:
        if f.split(".")[-1]!= "ipf":
            logging.warning("ignoring {}..".format(f))
            continue
        else:
            logging.warning("patching {}".format(f))
            cur_file = join(IPF_PATH, f)
            copyfile(cur_file, f)
            subprocess.run ([unpacker, f, 'decrypt'])
            subprocess.run([unpacker, f, 'extract']+ extension_needed)
            os.remove(f) 
            os.remove(cur_file) 
            copyfiles(join("..","{}_unpack").format(region))
            rmtree('extract')



def revision_decrypt(revision):
    # Thanks to https://github.com/celophi/Arboretum/blob/master/Arboretum.Lib/Decryptor.cs
    size_unencrypted = struct.unpack_from('@i', revision, 0)[0]
    size_encrypted = struct.unpack_from('@i', revision, 4)[0]

    revision = [ord(chr(c)) for c in revision]               # Convert to binary
    blowfish.Decipher(revision, 8, size_encrypted)      # Decrypt with blowfish
    revision = [chr(c) for c in revision]            # Convert back to unicode characters

    # Clean and split into a list
    #revision = ''\
    #    .join(revision[8:])\
    #    .encode('ascii', 'ignore')\
    #    .split('\r\n')
    revision = ''\
        .join(revision[8:])\
        .split('\r\n')
    return revision[:-1]


def getRegion(reg):
    try:
        region = reg[1]
        region = region.lower()
        accepted = ['itos','ktos','ktest', 'jtos']
        if region not in accepted:
            logging.warning("region unsupported")
            quit()
    except:
        logging.warning("need 1 positional argument; region")
        quit()
    return region
    
def write(l,file):
    with open(file, 'w', encoding= 'utf-8') as f:
        json.dump(l,f)
        
def read(file):
    with open(file, 'r', encoding= 'utf-8') as f:
        return json.load(f)

  
def patch_full(patch_path, patch_url, patch_ext, patch_unpack, revision_url,repatch):
    logging.warning('Patching %s...', revision_url)
    revision_list = urllib.request.urlopen(revision_url).read()
    revision_list = revision_decrypt(revision_list)

    for revision in revision_list:
        # Download patch
        patch_name = revision + patch_ext
        patch_file = os.path.join(patch_path, patch_name)
        if (not os.path.exists(os.path.join(patch_path, patch_name)) or repatch==1  )and patch_name not in IPF_BLACKLIST :
            logging.warning('Lets Downloading %s...', patch_url + patch_name)
            patch_process(patch_file, patch_name, patch_unpack, patch_url, patch_path)



def patch_process(patch_file, patch_name, patch_unpack, patch_url, patch_destination = ""):
    if patch_name in error_ipf:
        return
    # Ensure patch_file destination exists
    if not os.path.exists(os.path.dirname(patch_file)):
        os.makedirs(os.path.dirname(patch_file))
    def request_as_fox(url):
        headers={"User-Agent":"tos"}
        return urllib.request.Request(url,None,headers)

    filesize = 0
    if os.path.exists(patch_file):
        filesize = os.path.getsize(patch_file)

    if not os.path.isfile(patch_file) or filesize==0:
        # Download patch
        print('Downloading %s ...', patch_url + patch_name)
        patch_response = urllib.request.urlopen(request_as_fox(patch_url + patch_name))

        with open(patch_file, 'wb') as file:
            file.write(patch_response.read())
    else:
        logging.debug("Reusing cache %s...",patch_name)

    if os.path.isfile(patch_file):
        filesize = os.path.getsize(patch_file)

    if filesize == 0:
        logging.warning('Filesize is ZERO %s...', patch_file)
    else:
        pass
    # Extract patch
    if(patch_unpack):
        unpacker_pak.unpack(patch_name,patch_destination)
    else:
        unpack()
    # Delete patch
    # os.remove(patch_file)



def revision_txt_read(revision_txt):
    if os.path.isfile(revision_txt):
        with open(revision_txt, 'r') as file:
            return file.readline()
    else:
        return 0


def revision_txt_write(revision_txt, revision):
    with open(revision_txt, 'w') as file:
        file.write(revision)
        

def read_version(filename):
    rev = {}
    with open(filename, 'r') as f:
        w = csv.reader(f)
        for lines in w:
            if len(lines)<2:
                continue
            rev[lines[0]] = lines[1]
    return rev
    
def patch_partial(patch_path, patch_url, patch_ext, patch_unpack, revision_path, revision_url,repatch):
    logging.debug('Patching %s...', revision_url)
    revision_list = urllib.request.urlopen(revision_url).read()
    revision_list = revision_decrypt(revision_list)
    revision_old = read_version(revision_path)
    revision_new = revision_old

    for revision in revision_list:
        revision = revision.split(' ')[0]
     
        if (int(revision) > int(revision_old) or repatch==1) and revision not in ['147674']:
            # Process patch
            patch_name = revision + '_001001' + patch_ext
            patch_file = os.path.join(patch_path, patch_name)
            filesize = 0
            if os.path.isfile(patch_file):
                filesize = os.path.getsize(patch_file)
            
            patch_process(patch_file, patch_name, patch_unpack, patch_url, patch_path)

            # Update revision
            revision_txt_write(revision_path, revision)
            revision_new = revision

    return revision_old, revision_new


def do_patch_full(patch_output, url_patch):   
    patch_full(
        os.path.join("..", "{}_patch".format(region)),  url_patch + 'full/data/', '.ipf', False,
        url_patch + 'full/data.file.list.txt',True
    )
    

def move_language(region):
    if region not in ['itos', 'jtos']:
        return 
    output_path = {'itos' : os.path.join('..', 'Translation', 'English'),
                   'jtos' : os.path.join('..', 'Translation', 'Japanese'),}
    input_path  = {'itos' : os.path.join('..', 'itos_patch', 'languageData', 'English'),
                   'jtos' : os.path.join('..', 'jtos_patch', 'languageData', 'Japanese'),}

    output_path = output_path[region]
    input_path  = input_path[region]
    if os.path.exists(input_path):
        try:
            shutil.move(input_path, output_path)
        except:
            pass



if __name__ == "__main__":
    logging.warning('Patching...')
    region
    region = getRegion(sys.argv)
    #region = "itos"
    url_patch = {'itos' : 'http://drygkhncipyq8.cloudfront.net/toslive/patch/',
                 'jtos' : 'http://d3bbj7hlpo9jjy.cloudfront.net/live/patch/',
                 'ktos' : 'http://d31k064uwo645x.cloudfront.net/patchkor/',
                 'ktest' : 'http://tosg.dn.nexoncdn.co.kr/patch/test/'} # FIXME
    
    
    
    url_patch = url_patch[region]
    output = os.path.join("..", "{}_patch".format(region))
    
    if ('full' in sys.argv ):
        do_patch_full(output, url_patch)
    else:
        version_data, version_data_new = patch_partial(
            output , url_patch + 'partial/data/', '.ipf', False,
            'revision.csv', url_patch + 'partial/data.revision.txt' ,0
        )
        version_release, version_release_new = patch_partial(
            output, url_patch + 'partial/release/', '.pak', True,
            'release.csv', url_patch + 'partial/release.revision.txt',0
        )

        move_language(region)
    
    
    
    
