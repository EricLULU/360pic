"""
调度程序
"""
import spider
import url_spider
import settings
import threading


app = url_spider.Url_Get()   #s实例化

for url, big_tag in app.tag_url_get():
    print("开始抓取:",big_tag)
    for link, small_tag in app.small_tag_url_get(url):
        print("开始爬:",small_tag)
        spider.main(link, big_tag, small_tag)
        print("完毕")
"""
app.tag_url_get()     #获取tag_url

for url in settings.TAG_URL_LIST:
    print("小标签的url:",url)
    app.small_tag_url_get(url)  #获取小标签的url

for url in settings.Tag_SMALL_URL_LIST:
    spider.main(url)
"""