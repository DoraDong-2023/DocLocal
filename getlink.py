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
        
        with open(readme_list[i], "a") as f:
            f.write(readme_response.text)
        f.close()
    if len(readme_links)>0:
        reback=True
    else:
        reback=False
    return reback
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
    url = "https://github.com/openai/openai-cookbook"
    save_readme_from_url(url)
    
    