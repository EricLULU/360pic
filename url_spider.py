import requests
from bs4 import BeautifulSoup
import settings

#url_start = "http://image.so.com/"   #这是首页
class Url_Get(object):
    def __init__(self):
        #self.num_retries = settings.NUM_RETRIES
        self.url_start = settings.START_URL
        self.url_list = [self.url_start]
        self.tag_url_list = []  #大标签的 url集合
        self.tag_small_list=[]  #小标签的url集合
        self.headers = settings.headers
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def downloader(self, url, num_retries=2):
        """

        """
        try:
            html = self.session.get(url).content
            return html
        except:
            if num_retries > 0:
                print("重新下载")
                self.downloader(url, num_retries-1)
    """
    def downloader(self, url, num_retries=self.num_retries):
        
            #只是用来下载html页面
        
        try:
            html = self.session.get(url).text
            return html
        except:
            print("重新下载")
             self.downloader(url, num_retries-1)
    """
    def tag_url_get(self):
        """
            这里获取的都是每个标签的url， 比如美女，图解天下等的
        """
        html = self.downloader(self.url_start)   #这里使用首页作为种子页面
        soup = BeautifulSoup(html,'lxml')
        nav = soup.find(id='hd_nav')
        li_list = nav.find_all('li')
        le = len(li_list)
        for i in range(1, le-1):
            link = li_list[i].find('a').attrs['href']
            big_tag = li_list[i].find('a').string

            #print(big_tag)
            
            url = self.normalize_link(link)
            yield url, big_tag
        """
        for li in nav.find_all('li'):
            link = li.find('a').attrs['href']
           #print(link)s
            #self.tag_url_list.append(url)   #tag_url_list 怎加url
            url = self.normalize_link(link)
            settings.TAG_URL_LIST.append(url)
        settings.TAG_URL_LIST.pop(0)
        settings.TAG_URL_LIST.pop(-1)
        print("TAG_URL_LIST：", settings.TAG_URL_LIST)
        """
    def small_tag_url_get(self, url):
        """
            获得每个打标签下的小标签，注意在使用的时候，应该使用pop，if setting.Tag_SMALL_URL_LIST 的方式
        """
        #url = settings.TAG_URL_LIST.pop() 
        try:
            html = self.downloader(url)
            soup = BeautifulSoup(html, 'lxml')
            bd = soup.find(id='bd')
            for li in bd.find_all('li'):
                link = li.find('a').attrs['href']
                small_tag = li.find('a').string
                if small_tag != None:    #链接清洗
                    url = self.normalize_link(link)
                yield url, small_tag

                #settings.Tag_SMALL_URL_LIST.append(url)   #小标签下的url获取
        except:
            print("失败")


    def normalize_link(self, link):
        #规范化url
        #url 是公共的
        #link 是后main的参数
        return self.url_start + link
