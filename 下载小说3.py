import requests
import re
import concurrent.futures
import threading
import os
from time import sleep
path_dir = os.path.dirname(__file__)
if not os.path.exists(path_dir+"\\文件\\"):
    os.makedirs(path_dir+"\\文件\\")
print("开始运行")
session = requests.Session()
heders = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    #"accept-language":"zh-CN,zh;q=0.9"
}
url_main = "https://www.zjsw.org/read/230800/"
response_main  = session.get(url=url_main,headers=heders)
text_main = response_main.text
book_title = re.search(r'<h1 class="f20h">(?P<name>.*?)<em>',text_main).group("name")
print(book_title)
print("开始下载：",book_title)
pattern_book_title=r'<div class="link_14">(.|\s)*?</div>(?P<text>(.|\s)*?)</div>'
text_lib = re.search(pattern_book_title,text_main).group("text")
pattern_it = r'<a href=".*?">.*?</a>'
list_its = re.findall(pattern_it,text_lib)
def download(url:str,title:str) -> str:
    response_zhang = session.get(url=url,headers=heders)
    text_zhang = response_zhang.text
    pattern_zhang_gettext = r'<div id="content">(?P<text>(.|\s)*?)</div>'
    match_zhang = re.search(pattern_zhang_gettext,text_zhang)
    if not match_zhang:
        return ""
    content = match_zhang.group("text")
    content = content.replace("<p>","\n").replace("</p>","\n")
    print(title)
    return title +"\n"+content+"\n"
pattern_iteam = r'<a href="(?P<href>(.|\s)*?)">(?P<title>(.|\s)*?)</a>'
futures = []
executor = concurrent.futures.ThreadPoolExecutor(max_workers=700)
with open (path_dir+"\\文件\\"+book_title+".txt","w",encoding="utf-8") as book:
    for item in list_its:
        match_it = re.search(pattern_iteam,item)
        title = match_it.group("title")
        url_zhang ='https://www.zjsw.org/'+ match_it.group("href")
        book.write(download(url=url_zhang,title=title))
