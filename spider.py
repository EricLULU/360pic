import requests
from urllib import parse
import csv
import time
import os
import random
import threading
import settings

current_path =  os.getcwd()  #获取当前工作目录
File_Path = current_path + '\\' + 'picture'  #创建新的文件夹
if not os.path.exists(File_Path):
        os.makedirs(File_Path)               #创建的大的文件夹

s = requests.Session()  
headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cookie':'__guid=15484592.93573937038302720.1533650849383.2432; soid=(!_bra0*Ue*w2zwC6Ux5vcZBZ3zgXTxS1TO-dt94; __gid=9114931.532307051.1533651857277.1533717712405.10; __DC_gid=9114931.532307051.1533651857277.1534175731659.15; Q=u%3D%25OO%25N8_%25PS%25R3%25PO%25P4%25OP%25OR%26n%3D%25Q3%25RN%25QQ%25N1%25P0%25Q6%25Q4%25O0%26le%3DZwH4BGZlAGLlAlH0ZUSkYzAioD%3D%3D%26m%3D%26qid%3D876649536%26im%3D1_t01386b81c31e58d8dd%26src%3D360se%26t%3D1; T=s%3D84cc5aed0672118e130eb24c5afec615%26t%3D1531440507%26lm%3D%26lf%3D1%26sk%3Dc0f4d3338fec7e2f2ccf0826684a8b50%26mt%3D1531440507%26rc%3D1%26v%3D2.0%26a%3D1; count=1; erules=ecl-9%7Cp2-11; __huid=11haPiIpSt4WlBnXh2jvJl2KFXdXr0KVQNmgrv0y5ZbjY%3D; _S=7f5d2a1c7e33542955e284e46393a61d; test_cookie_enable=null; tracker=; lightbox_thumb_visible=1; imgnumber=42',
    'DNT':'1',
    'Host':'image.so.com',
    'Proxy-Connection':'keep-alive',
    'Referer':'http://image.so.com/z?ch=go',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE',
    'X-Requested-With':'XMLHttpRequest',
    }

s.headers.update(headers)

csvfile = open('360img.csv', 'a', newline='', encoding='utf-8')
fieldnames = ['id','cover_imgurl','group_title','tag','qhimg_thumb_url','qhimg_url','total_count']
writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
writer.writeheader()

lock = threading.RLock()   #设置锁 
local = threading.local() 
item_list = []      #item存储列表


def download(url, num_retries=2):
    """
        下载html，并将结果以json格式返回
    """
    print("正在爬取",url)
    try:
        time.sleep(3)
        r = s.get(url, timeout=30)
    except:
        if num_retries > 0:
            print("重新连接")
            print("第",3-num_retries,'次')    
            download(url, num_retries-1)
    else:
        if len(r.text) < 10000:
            if num_retries > 0:
                download(url, num_retries-1)
            else:
                return None
        else:
            print(len(r.text))
            return r.json()



def url_cre(start_url): 
    """
        生成 ajax 请求时的 url
    """
    for i in range(1):
        #print("现在在爬",i,'页')
        #start_url = "http://image.so.com/zj?ch=go"
        data = {
            #'t1':'396',          #这个链接也已经拿到了
            'sn': str(i*30),
            'listtype':'new',
            'temp':'1',
        }
        
        url_s = start_url + '&' + parse.urlencode(data)
        url_list = url_s.split('?')
        url = url_list[0] + 'j?' + url_list[1]
        yield url



def img_down(item, big_tag, small_tag, num_retries=2):
    """
        图片下载
    """
    global lock
    global local

    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Host':'p0.so.qhimg.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        } 
    
    url = item['qhimg_thumb_url']


    #文件夹建立
    lock.acquire()
    try:
        big_tag_path = File_Path + '\\' + big_tag
    except:
        new_file_path = File_Path
    if not os.path.exists(big_tag_path):
        os.makedirs(big_tag_path)

    try:
        small_tag_path = big_tag_path + "\\" + small_tag
    except:
        small_tag_path = big_tag_path
    if not os.path.exists(small_tag_path):
        os.makedirs(small_tag_path)
    lock.release()

    #print('图片链接:',url)
    try:
        time.sleep(3)
        local.r = requests.get(url,headers=headers, timeout=30)
    except:
        if num_retries > 0:
            print("重新下载图片")
            img_down(item, num_retries-1)
    else:
        try:
            title = item['group_title'].replace('/','_')
        except:
            title = item['group_title']
        filename = small_tag_path + "\\" + title + item['id'] + '.jpg'
        #filename = item['id'] + '.jpg'
        try:
            lock.acquire()
            with open(filename,'wb') as f:   #保存图片
                f.write(local.r.content)
                #print("图片保存成功")
        except:
            pass
        finally:
            lock.release()


def info_get(result):
    """
        解析信息
    """
    item = {}
    items = result.get('list')
    length = len(items)
    for i in range(length):
        item = {
            'id':items[i].get('id'),
            'cover_imgurl': items[i].get('cover_imgurl'),
            'group_title':items[i].get('group_title'),
            'tag':items[i].get('tag'),
            'qhimg_thumb_url':items[i].get("qhimg_thumb_url"),
            'qhimg_url':items[i].get('qhimg_url'),
            'total_count':items[i].get('total_count'),
        }
        #print(item)
        yield item
        #writer.writerow(item)




def save_to_csv(item):
    """
        将结果存入到csv中
    """
    global lock
    try:
        lock.acquire()
        if writer.writerow(item):
            #print("csv保存成功")
            pass
        else:
            print("保存失败")
    except:
        pass
    finally:
        lock.release()  #释放锁


def worker(item_list,big_tag,small_tag):
    while  item_list:
        try:
            lock.acquire()
            item = item_list.pop()
            lock.release()
            save_to_csv(item)
            img_down(item, big_tag, small_tag)
        except:
            try:
                lock.release()
            except:
                pass
    
    """
    for item in item_list:
        save_to_csv(item)
        img_down(item, big_tag, small_tag)
    """
def main(start_url, big_tag, small_tag): 
    """
        args: start_url
        调度程序
    """
    global item_list
    for url in url_cre(start_url):
        result = download(url)
        
        if result == None:
            continue

        for item in info_get(result):
            item_list.append(item)       #生产者已经完成
    threads = []   #线程存储列表
    for i in range(settings.THREAD_NUM):
        t = threading.Thread(target=worker, args=(item_list, big_tag, small_tag))
        threads.append(t)

    for i in range(settings.THREAD_NUM):
        threads[i].start()

    for i in range(settings.THREAD_NUM):
        threads[i].join()
    #接下来是消费者

    #save_to_csv(item)
    #img_down(item, big_tag, small_tag)
"""
if __name__ == '__main__':
    print("开始")
    main()
    print("结束")
"""