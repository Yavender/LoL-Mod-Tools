import subprocess
from subprocess import PIPE, STDOUT, CREATE_NO_WINDOW
import os
import shutil
from zipfile import ZipFile

import numpy
import PIL.Image
import PIL.ImageEnhance

from settings import *

from lolpytools.convert import lolinibin2ini, lolluaobj2lua, loltroybin2troy


def convert_inibin2ini(filepath):
    inname = filepath
    outname = inname[:-6] + "ini"
    with open(inname, 'rb') as infile:
        with open(outname, 'w', encoding='utf-8', newline='\r\n') as outfile:
            lolinibin2ini(infile, outfile)


def convert_luaobj2lua(filepath):
    inname = filepath
    outname = inname[:-6] + "lua"
    with open(inname, 'rb') as infile:
        with open(outname, 'w', encoding='utf-8', newline='\r\n') as outfile:
            lolluaobj2lua(infile, outfile)
            
            
def convert_troybin2troy(filepath):
    inname = filepath
    outname = inname[:-7] + "troy"
    with open(inname, 'rb') as infile:
        with open(outname, 'w', encoding='utf-8', newline='\r\n') as outfile:
            loltroybin2troy(infile, outfile)


def gradient(list_trgba=[[0.0, 1, 1, 1.0, 0],[0.300000012, 1, 1, 1.0, 0.35],[0.5, 1, 1, 1.0, 0.35],[1.0, 0.33, 1, 1.0, 0]], width=100, height=500):
    image = PIL.Image.new('RGBA', (width, height), (255,255,255,0))
    image = numpy.array(image)
    list_range_p = []
    pre_range = 0
    for i in range(len(list_trgba)-1):
        range_p = [pre_range, round(list_trgba[i+1][0]*height)]
        pre_range = range_p[-1]
        list_range_p.append(range_p)
    for i in range(len(list_range_p)):
        for row in range(list_range_p[i][0], list_range_p[i][1]):
            for index in range(width):
                r =  int((list_trgba[i][1] + (list_trgba[i+1][1] - list_trgba[i][1])/(list_range_p[i][1]-list_range_p[i][0])*(row-list_range_p[i][0])) * 255)
                g =  int((list_trgba[i][2] + (list_trgba[i+1][2] - list_trgba[i][2])/(list_range_p[i][1]-list_range_p[i][0])*(row-list_range_p[i][0])) * 255)
                b =  int((list_trgba[i][3] + (list_trgba[i+1][3] - list_trgba[i][3])/(list_range_p[i][1]-list_range_p[i][0])*(row-list_range_p[i][0])) * 255)
                a =  int((list_trgba[i][4] + (list_trgba[i+1][4] - list_trgba[i][4])/(list_range_p[i][1]-list_range_p[i][0])*(row-list_range_p[i][0])) * 255)
                image[row][index] = [r, g, b, a]
    
    image = PIL.Image.fromarray(image)
    image = image.rotate(90, expand=True)
    return image

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

# wad-extract
def wad_extract(filepath):
    if '.client' in filepath:
        try:
            subprocess.run([WAD_EXTRACT, filepath],creationflags=CREATE_NO_WINDOW)
        except:
            pass


# wad-make
def wad_make(filepath):
    if os.path.exists(filepath):
        try:
            subprocess.run([WAD_MAKE, filepath],creationflags=CREATE_NO_WINDOW)
        except:
            pass


# ritobin
def ritobin(filepath):
    if '.bin' in filepath or '.py' in filepath or '.' not in filepath:
        try:
            subprocess.run([RITO_BIN, filepath],creationflags=CREATE_NO_WINDOW)
        except:
            pass

# skl-convert
def skl_convert(filepath):
    if '.skl' in filepath:
        try:
            subprocess.run([SKL_CONVERT, filepath],creationflags=CREATE_NO_WINDOW)
            os.remove(filepath)
            os.rename(filepath.replace('skl', 'new.skl'), filepath)
        except:
            pass

# tex2dss
def tex2dds(filepath):
    if '.tex' in filepath or '.dds' in filepath:
        try:
            subprocess.run([TEX2DDS, filepath],creationflags=CREATE_NO_WINDOW)
        except:
            pass

# luaobj2lua
def luaobj2lua(filepath):
    if '.luaobj' in filepath:
        convert_luaobj2lua(filepath)

# inibin2ini
def inibin2ini(filepath):
    if '.inibin' in filepath:
        convert_inibin2ini(filepath)

# troybin2troy
def troybin2troy(filepath):
    if '.troybin' in filepath:
        convert_troybin2troy(filepath)
            
# change color
def change_color(filepath, color):
    if '.dds' in filepath:
        a_raw = PIL.Image.open(filepath)
        a = PIL.ImageEnhance.Color(a_raw)
        a = a.enhance(0)
        a = numpy.array(a)
        a = a.astype(float)/255

        width, height = a_raw.size
        b = PIL.Image.new('RGBA', (width, height), color)
        b = numpy.array(b)
        b = b.astype(float)/255
        
        mask = a >= 0.5
        ab = numpy.zeros_like(a)
                
        ab[~mask] = (2*a*b)[~mask]
        ab[mask] = (1-2*(1-a)*(1-b))[mask]

        x=(ab*255).astype(numpy.uint8)
        x = PIL.Image.fromarray(x)
        x.save(filepath)

    
def get_lol_path():
    with open("path.txt", 'r+') as pa:
        line_pa = pa.readlines()
    return line_pa[0][:-(len("cslol-manager.exe"))] + 'installed'


def extract_folder(path):
    basename = os.path.basename(path)
    
    if not os.path.exists('Projects'):
        os.makedirs('Projects')
        
    
    if 'WAD' == basename:
        modname = os.listdir(path)[0].split('.')[0]
        
        i = 0
        new_path = 'Projects/' + modname
        while os.path.exists(new_path):
            i += 1
            new_path = 'Projects/' + modname + f'{i}'
            
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        if not os.path.exists(new_path+"/META"):
            os.makedirs(new_path+"/META")
            shutil.copy('Default/info.json', new_path+"/META/info.json")
            
        shutil.copytree(path, new_path + '/' + basename)
    
    elif '.wad' in (basename):
        modname = basename.split('.wad')[0]
        
        i = 0
        new_path = 'Projects/' + modname + '/WAD'
        while os.path.exists(new_path):
            i += 1
            new_path = 'Projects/' + modname + f'{i}/WAD'
            
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        if not os.path.exists(new_path[:-3]+"META"):
            os.makedirs(new_path[:-3]+"META")
            shutil.copy('Default/info.json', new_path[:-3]+"META/info.json")
            
        shutil.copytree(path, new_path + '/' + basename.capitalize())
    
    elif 'assets' == basename or 'data' == basename:
        modname = 'Untitled'
        
        if 'data' == basename:
            if os.path.exists(path + '/characters'):
                modname = os.listdir(path + '/characters')[0].capitalize()
            else:
                onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
                if onlyfiles:
                    modname = onlyfiles[0].split('_')[0]
        else:
            if os.path.exists(path + '/characters'):
                modname = os.listdir(path + '/characters')[0].capitalize()
                        
        
        i = 0
        new_path = 'Projects/' + modname + '/WAD'
        while os.path.exists(new_path):
            i += 1
            new_path = 'Projects/' + modname + f'{i}/WAD'
            
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        if not os.path.exists(new_path[:-3]+"META"):
            os.makedirs(new_path[:-3]+"META")
            shutil.copy('Default/info.json', new_path[:-3]+"META/info.json")
            
        os.makedirs(new_path + f'/{modname}.wad')
        shutil.copytree(path, new_path + f'/{modname}.wad/' + basename)
    
    else:
        shutil.copytree(path, 'Projects/' + basename)
        

def extract_file(file_path):
    # Extract zip/fantome
    
    
    if not os.path.exists('Projects'):
        os.makedirs('Projects')
        
    if '.fantome' in file_path or '.zip' in file_path or '.wad.client' in file_path:
        modname = file_path.split('/')[-1].replace('.fantome', '').replace('.zip', '').replace('.wad.client', '')
        
        i = 0
        new_path = 'Projects/' + modname + '/WAD'
        while os.path.exists(new_path):
            i += 1
            new_path = 'Projects/' + modname + f'{i}/WAD'
            
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        if not os.path.exists(new_path[:-3]+"META"):
            os.makedirs(new_path[:-3]+"META")
            shutil.copy('Default/info.json', new_path[:-3]+"META/info.json")
            
        if '.client' in file_path:
            file_name = file_path.split('/')[-1]
            shutil.copyfile(file_path, new_path + '/' + file_name.capitalize())
        else:  
            with ZipFile(file_path, 'r') as zObject:
                zObject.extractall(path = new_path[:-3])
        
        # Extract .wad.client
        for root, dirs, files in os.walk(new_path):
            for file in files:
                if '.client' in file:
                    wad_extract(root + '/' + file)
                                
        if os.path.exists(new_path.replace('WAD', 'DATA')):
            files = os.listdir(new_path.replace('WAD', 'DATA')+"/Characters")
            file = files[0] + ".client"

            os.rename(new_path.replace('WAD', 'DATA'), new_path.replace('WAD', 'assets'))
            os.makedirs(new_path + "/" + file.replace(".client", ""))
            shutil.move(new_path.replace('WAD', 'assets'), new_path + "/" + file.replace(".client", ""))
    else:
        modname = file_path.split('/')[-1]
        
        i = 0
        new_path = 'Projects/' + modname
        while os.path.exists(new_path):
            i += 1
            new_path = 'Projects/' + modname + f'{i}'
            
        if not os.path.exists(new_path):
            os.makedirs(new_path)
            
        shutil.copyfile(file_path, new_path + '/' + os.path.basename(file_path))

def read(file_path):
    file = open(file_path, 'r+')
    lines = file.readlines()
    file.close()
    return lines

def read_py(file_path):
    py = open(file_path, 'r+')
    lines_py = py.readlines()
    py.close()
    return lines_py

def read_json(file_path):
    json = open(file_path, 'r+')
    lines_json = json.readlines()
    json.close()
    return lines_json

def read_troy(file_path):
    troy = open(file_path, 'r+')
    lines_troy = troy.readlines()
    troy.close()
    return lines_troy

def save(file_path, lines):
    file = file_path.split('/')[-1]
    with open(file, 'a') as py:
        py.writelines(lines)
    if os.path.exists(file):
        os.remove(file_path)
        shutil.move(file, file_path.replace(file, ''))



def update_bin(file_path):

    old_py = open(file_path, 'r+')
    lines_old_py = old_py.readlines()
    old_py.close()
    new_py = open(file_path.replace('Yours', 'Riot'), 'r+')
    lines_new_py = new_py.readlines()
    
    file = file_path.split('/')[-1]

    # Updating vfx champion
    
    for l_no, line in enumerate(lines_new_py):
        if "SkinAnimationProperties: embed = SkinAnimationProperties".lower() in line.lower():
            with open(file, 'a') as data:
                data.writelines(lines_new_py[:l_no])
                break
    for l_no, line in enumerate(lines_old_py):
        if "SkinAnimationProperties: embed = SkinAnimationProperties".lower() in line.lower():
            start = l_no
        if "IconSquare: option[string]".lower() in line.lower():
            end = l_no + 3
            with open(file, 'a') as data:
                data.writelines(lines_old_py[start:end])
                break
    for l_no, line in enumerate(lines_new_py):
        if "IconSquare: option[string]".lower() in line.lower():
            start = l_no + 3
            with open(file, 'a') as data:
                data.writelines(lines_new_py[start:start+3])
                break
    for l_no, line in enumerate(lines_old_py):
        if "mResourceResolver".lower() in line.lower():
            with open(file, 'a') as data:
                data.writelines(lines_old_py[l_no:])
                break
    
    if os.path.exists(file):
        os.remove(file_path)
        shutil.move(file, file_path.replace(file, ''))
        ritobin(file_path)
        

def update_all_bin():
    # Read old .py and new .py
    for root, dirs, files in os.walk('WAD'):
        for file in files:
            if '.py' in file:
                old_py = open(root +'/'+ file, 'r+')
                lines_old_py = old_py.readlines()
                old_py.close()
                new_py = open('NEW/' + root +'/'+ file, 'r+')
                lines_new_py = new_py.readlines()

                # Updating vfx champion
                for l_no, line in enumerate(lines_new_py):
                    if "SkinAnimationProperties: embed = SkinAnimationProperties" in line:
                        with open(file, 'a') as data:
                            data.writelines(lines_new_py[:l_no])
                            break
                for l_no, line in enumerate(lines_old_py):
                    if "SkinAnimationProperties: embed = SkinAnimationProperties" in line:
                        start = l_no
                    if "IconSquare: option[string]" in line:
                        end = l_no + 3
                        with open(file, 'a') as data:
                            data.writelines(lines_old_py[start:end])
                            break
                for l_no, line in enumerate(lines_new_py):
                    if "IconSquare: option[string]" in line:
                        start = l_no + 3
                        with open(file, 'a') as data:
                            data.writelines(lines_new_py[start:start+3])
                            break
                for l_no, line in enumerate(lines_old_py):
                    if "mResourceResolver" in line:
                        with open(file, 'a') as data:
                            data.writelines(lines_old_py[l_no:])
                            break
                
                if os.path.exists(file):
                    os.remove(root +'/'+ file)
                    shutil.move(file, root)
                    subprocess.run([RITO_BIN, root +'/'+ file],creationflags=CREATE_NO_WINDOW)