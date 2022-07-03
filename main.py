from asyncio import streams
import functools
import os
import platform
import shutil
from requests import patch
import yaml



def tree(basepath: list, path, lev):




    item_list = os.listdir(path)
    # print(item_list)
    dirlist = []
    filelist = []
    for item_name in item_list:
        item_path = os.path.join(path, item_name)
        if os.path.isfile(item_path):
            # markdown文件
            # print(item_path)
            type_ = item_name.split(".")[-1]
            if type_ != 'md':
                continue
            if item_name[0] == '_':
                continue
            if item_name == 'README.md':
                continue
            filelist.append(item_name)
        elif os.path.isdir(item_path):
            if item_name[0] == '_' or item_name[0] == '.':
                continue
            dirlist.append(item_name)

    result = []

    for dir in dirlist:
        # print(basepath)
        new_basepath = basepath + [dir]
        # print(new_basepath)
        item = (dir, '/'.join(new_basepath) + '/', lev,1)

        result.append(item)

        result += tree(new_basepath, os.path.join(path, dir), lev + 1)

    for file in filelist:
        new_basepath = basepath + [file]
        item = (file[:-3], '/'.join(new_basepath), lev,0)
        result.append(item)

    return result




def main(path):
    

    item_list = os.listdir(path)
    # print(item_list)
    dirlist = []
    filelist = []
    for item_name in item_list:
        item_path = os.path.join(path, item_name)
        if os.path.isfile(item_path):
            # markdown文件
            # print(item_path)
            type_ = item_path.split(".")[-1]
            if type_ != 'md':
                continue
            if item_path[0] == '_':
                continue
            if item_path == 'README.md':
                continue
            filelist.append(item_path)
        elif os.path.isdir(item_path):
            if item_name[0] == '_' or item_name[0] == '.':
                continue
            dirlist.append(item_name)

    for dir in dirlist:
        # print(dir)
        main(os.path.join(path, dir))
    for file in filelist:
        pass
        # print(file)


if __name__ == '__main__':
    path='./docs'

    with open("basic.yml","r")as basic:
        basiclines=basic.readlines()
    
    ans = tree([], path, 1)
    
    with open(os.path.join('./', 'mkdocs.yml'), 'w', encoding='utf-8') as sider:
        
    
        for line in basiclines:
            sider.write(line)
        
        
        sider.write('nav: \n')
        sider.write("  - Home:\n")
        sider.write("    - Getting Started : index.md\n")
        sider.writable()
        for item in ans:
            if item[3]==1:
                sider.write('  ' * item[2] + '- ' + '%s :' % item[0])
            else:
                sider.write('  ' * item[2] + '- ' +'%s : %s' % (item[0], item[1]))
            sider.write('\n')
    
    
    # if platform.system().lower() == 'windows':
    #     main('.\\')
    # elif platform.system().lower() == 'linux':
    #     main('./')
    

