import functools
import os
import platform
import shutil


def strcmp(stra, strb) -> bool:
    import re

    stra = re.sub('[\u4e00-\u9fa5]', '', stra)  # 去除字符串之中的中文
    strb = re.sub('[\u4e00-\u9fa5]', '', strb)  # 去除字符串之中的中文

    i, j = 0, 0
    while i < len(stra) and j < len(strb):
        if stra[i] < strb[j]:
            return False
        elif stra[i] > strb[j]:
            return True
        else:
            pass

        i += 1
        j += 1

    if i == len(stra):
        return True

    if j == len(strb):
        return False


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

    # dirlist = sorted(dirlist, key=functools.cmp_to_key(strcmp))
    # filelist = sorted(filelist, key=functools.cmp_to_key(strcmp))
    result = []

    for dir in dirlist:
        print(basepath)
        new_basepath = basepath + [dir]
        print(new_basepath)
        item = (dir, '/'.join(new_basepath) + '/', lev)

        result.append(item)

        result += tree(new_basepath, os.path.join(path, dir), lev + 1)

    for file in filelist:
        new_basepath = basepath + [file]
        item = (file[:-3], '/'.join(new_basepath), lev)
        result.append(item)

    return result


def writesidebar(path, ans):
    if platform.system().lower() == 'windows':
        with open(os.path.join(path, '_sidebar.md'), 'w', encoding='utf-8') as sider:
            for item in ans:
                sider.write('  ' * item[2] + '- ' + '[%s](%s)' % (item[0], item[1]))
                sider.write('\n')
                # print('  ' * item[2] + '- ' + '[%s](%s)' % (item[0], file_path))
        # print(item[1].split('\\'))

    elif platform.system().lower() == 'linux':
        pass


def main(path):
    writesidebar(path, tree([], path, 0))

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

    # dirlist = sorted(dirlist, key=functools.cmp_to_key(strcmp))
    # filelist = sorted(filelist, key=functools.cmp_to_key(strcmp))

    for dir in dirlist:
        # print(dir)
        main(os.path.join(path, dir))
    for file in filelist:
        pass
        # print(file)


def updatereadme(path):
    item_list = os.listdir(path)
    # print(item_list)
    if path != '.\\':
        shutil.copyfile("C:\\Users\DELL\\Desktop\\MyWebsite\\CBWeb\\README.md", os.path.join(path, 'README.md'))

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

    # dirlist = sorted(dirlist, key=functools.cmp_to_key(strcmp))
    # filelist = sorted(filelist, key=functools.cmp_to_key(strcmp))

    for dir in dirlist:
        updatereadme(os.path.join(path, dir))
    for file in filelist:
        pass


if __name__ == '__main__':
    updatereadme('.\\')
    # main('.\\')
