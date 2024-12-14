import requests
import re
import concurrent.futures
import threading
from json import dumps
import os
from time import sleep
print("开始运行")
path_dir = os.path.dirname(__file__)
session = requests.Session()
heders = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "accept-language":"zh-CN,zh;q=0.9"
}
url_main = "https://www.511wx4.com/wenxue/25459/"
response_main  = session.get(url=url_main,headers=heders)
text_main = response_main.text
book_title = re.search(r'<div id="info">(.|\s)*?<h1>(?P<name>(.|\s)*?)</h1>',text_main).group("name")
print(book_title)
print("开始下载：",book_title)

if not os.path.exists(path_dir+"\\文件\\"):#文件夹不存在，就创建这个文件夹
    os.makedirs(path_dir+"\\文件\\")
    pass
text_lib = re.search(r'<div id="list">(?P<dt>(.|\s)*?)</div>',text_main).group("dt")
pattern = r'<a href="(?P<href>.*?)">.*?</a>'
#网站编写者把一章分成好几节，只能一章一章爬了

def download(url:str) -> str:
    try:
        global session
        pattern_content=r'<div id="content">(?P<content>(.|\s)*?)</div>'
        pattern_title=r'<div class="bookname">(.|\s)*?<h1>(?P<title>(.|\s)*?)</h1>(.|\s)*?</div>'
        response_jie = session.get(url=url,headers=heders)
        text_jie = response_jie.text
        resel_title = re.search(pattern_title, text_jie)
        title = resel_title.group("title")
        print(title)
        content = re.search(pattern_content, text_jie).group("content").replace(
            "&nbsp;",""
            ).replace(
            "<br>","\n"
            ).replace(
            "<br/>","\n"
            )
        sleep(0.5)
        return title,content
    except:
        return ""
executor = concurrent.futures.ThreadPoolExecutor(max_workers=500)
#用列表推导式将任务提交到线程池并将结果储存到futures列表中
futures = [executor.submit ( download,"https://www.511wx4.com"+match.group('href')) for match in re.finditer(pattern, text_lib)]
concurrent.futures.wait(futures)
with open (path_dir+"\\文件\\"+book_title+".txt","w",encoding="utf-8") as book:
    for future in futures:
        result ="{}\n{}".format(future.result()[0],future.result()[1])
        book.write(result+"\n")