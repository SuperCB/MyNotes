import os

import requests
import lxml.html


def readmecontent():
    URL = "https://en.wikipedia.org/wiki/Wikipedia:Picture_of_the_day"

    README = """
    
<div style="display:flex;justify-content: center; align-items:center;">
<h1>   欢迎来到CB的博客网站 👋</h1>
</div>

 
<h2> Picture of the day</h2>


<div style="display:flex;justify-content: center; align-items:center;">
    <img width=400px src="{wiki_link}"/>
</div>



      
> {wiki_content}
  """

    print("download image...")
    content = requests.get(URL).content
    html = lxml.html.fromstring(content)
    presentation_table = html.xpath("//table[@role='presentation']")[0]
    a_tag = presentation_table.xpath(".//a[@class='image']")[0]
    relative_link = a_tag.get("href")
    title = a_tag.get("title")
    image_src = a_tag.xpath("./img/@srcset")[0]
    best_image = image_src.split(" ")[0]
    print(f"{relative_link} {title}, image srcset:{image_src}")
    print(f"best image: {best_image}")

    content = requests.get(URL).content
    html = lxml.html.fromstring(content)
    presentation_table = html.xpath("//table[@role='presentation']")[0]
    content = presentation_table.xpath('.//tbody/tr/td')[1]
    ptext = content.xpath('.//p')[0]

    contenttext = ptext.xpath('.//text()')

    new_readme = README.format(
        wiki_link="https://" + best_image[2:],
        wiki_content=' '.join(contenttext)
    )
    return new_readme


new_readme = readmecontent()


def generatereadme(path):
    item_list = os.listdir(path)

    with open(os.path.join(path, 'README.md'), 'w') as f:
        f.write(new_readme)

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
        print(dir)
        generatereadme(os.path.join(path, dir))
    for file in filelist:
        pass


if __name__ == '__main__':
    generatereadme('./')
