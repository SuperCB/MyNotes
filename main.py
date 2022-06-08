# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os


def generateMenu(path):
    dir_list = os.listdir(path)

    with open(os.path.join(path, '_sidebar.md'), 'w', encoding='utf-8') as slider:
        for cur_file in dir_list:
            cur_path = os.path.join(path, cur_file)
            if os.path.isfile(cur_path):
                # name = cur_file.split(".")[0]
                type_ = cur_file.split(".")[-1]
                print(type_)
                if type_ != 'md':
                    continue

                if cur_file[0]=='_':
                    continue
                if cur_file == '_sidebar.md' or cur_file == "RAEDME.md":
                    continue
                slider.write('- [%s](%s)\n' % (cur_file[:-3], cur_file))
                print("{0} : is file!".format(cur_path))
            elif os.path.isdir(cur_path):
                if cur_file[0] == '_':
                    continue
                if cur_file == 'img' or cur_file == 'src' or cur_file == '.git':
                    continue
                slider.write('- [%s](%s/)\n' % (cur_file, cur_file))
                generateMenu(cur_path)
                print("{0} : is dir!".format(cur_file))
    # with open(os.path.join(path, 'README.md'), 'w', encoding='utf-8') as readme:
    #     readme.write(path)


if __name__ == '__main__':
    generateMenu('D:\docsify')
    # path='D:\docsify'
    # dir_list = os.listdir(path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
