# -*- coding: utf-8 -*-
"""
Created on June 13th, 2023
Author: Zhengyuan Dong
Email: zydong122@gmail.com
"""

import requests, re, os
from urllib.parse import urlparse, unquote


def parse_url(url):
    """
    aim: Parse the source of a URL.
    """
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    if hostname and 'github.com' in hostname:
        return 'github'
    return None
def change_name(filereadme_name_list):
    """aim: Create a new list of filenames, replacing duplicate filenames with new names."""
    name_count = {}
    for name in filereadme_name_list:
        if name not in name_count:
            name_count[name] = 1
        else:
            name_count[name] += 1
    new_name_list = []
    for name in filereadme_name_list:
        if name_count[name] > 1:
            ext = os.path.splitext(name)[1]
            new_name = f"README{name_count[name]}{ext}"
            new_name_list.append(new_name)
            name_count[name] -= 1
        else:
            new_name_list.append(name)
    return new_name_list
def get_readme_from_github(url):
    txt2 = url.split('/')[4].split('.')[0]# remove .git
    txt1 = url.split('/')[3]
    folder_path = "./Github/"+txt1+"/"+txt2
    
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)
        print("Build filepath")
    else:
        print("Filepath exists!")
    r = requests.get('/'.join(url.split('/')[:5]))

    readme_links = re.findall(r'href="(.*/blob/.*?\.(md|rst))"', r.text)
    filereadme_name_list =  [i[0].split('/')[-1] for i in readme_links]
    filereadme_name_list = change_name(filereadme_name_list)
    filereadme_name_list = [unquote(i) for i in filereadme_name_list]

    readme_list = [folder_path+'/'+i for i in filereadme_name_list]
    
    for i,link in enumerate(readme_links):
        raw_link = link[0].replace("blob", "raw")
        readme_url = "https://github.com" + raw_link
        readme_response = requests.get(readme_url)

        txt = readme_response.text
        txt = substitute(readme_url, txt)

        with open(readme_list[i], "a") as f:
            f.write(txt)
        f.close()
    if len(readme_links)>0:
        reback=True
    else:
        reback=False
    return reback
def substitute(repo_url, content):
    # remove last readme
    repo_url = '/'.join(repo_url.split('/')[:-1])
    pattern = r'<img src="(.+?)"'
    matches = re.findall(pattern, content)

    for match in matches:
        parsed_url = urlparse(match)
        if not parsed_url.scheme and not parsed_url.netloc:
            img_path = parsed_url.path.replace("./", "")
            img_url = f"{repo_url}/{img_path}"
            print(img_url)
        else:
            # if use url link to show img
            img_url = match
        content = content.replace(match, img_url)
    return content
def save_readme_from_url(url):
    if parse_url(url)=='github':
        reback = get_readme_from_github(url)
        if not reback:
            return 'No readme under the link!'
        else:
            return 'Added Successfully!'
    else:
        return 'Unsupport type of link, please enter Github Link now!'
if __name__=='__main__':
    url = "https://github.com/DoraDong-2023/DocLocal"
    save_readme_from_url(url)
    
    