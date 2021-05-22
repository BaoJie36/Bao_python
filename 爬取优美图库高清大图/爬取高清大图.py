import requests
import time
from bs4 import BeautifulSoup

url = "https://www.umei.net/bizhitupian/weimeibizhi/"
resp = requests.get(url)
resp.encoding = 'utf-8'  # 处理乱码


# 把源代码交给 bs分析

main_page = BeautifulSoup(resp.text, "html.parser")  # 指明是网页html

# 从网页源代码中找到需要内容的大范围和存放高清大图所在的子网页链接

alist = main_page.find("div", class_="TypeList").find_all("a")

for a in alist:

    href = 'https://www.umei.net/'+a.get('href')  # 通过get直接拿取href的值

    # 拿到子页面的源代码
    child_page_resp = requests.get(href)
    child_page_resp.encoding = 'utf-8'
    child_page_text = child_page_resp.text

    # 从子页面中拿到图片的下载路径
    child_page = BeautifulSoup(child_page_text, "html.parser")

    # 实际发现center在网页中是唯一，此处采取用center来确定图片链接
    p = child_page.find("p", align="center")
    img = p.find("img")
    src = img.get("src")

    # 下载图片
    img_resp = requests.get(src)
    # img_resp.content  # 这里拿到的是字节

    img_name = src.split("/")[-1]  # 拿到url中的最后一个/以后的内容

    # 因为是图片所以用wb,其次最好设置个文件夹发图片
    with open("img/"+img_name, mode="wb") as f:
        
        f.write(img_resp.content)  # 图片内容写入文件

    print("图片下载完成",img_name)

    # 防止访问过快，设置个时间延迟
    time.sleep(1)

print("结束")
