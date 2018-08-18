headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cookie':'__guid=15484592.93573937038302720.1533650849383.2432; soid=(!_bra0*Ue*w2zwC6Ux5vcZBZ3zgXTxS1TO-dt94; __gid=9114931.532307051.1533651857277.1533717712405.10; __DC_gid=9114931.532307051.1533651857277.1534175731659.15; lightbox_thumb_visible=1; imgnumber=1; erules=p1-1%7Cp4-2; Q=u%3D%25OO%25N8_%25PS%25R3%25PO%25P4%25OP%25OR%26n%3D%25Q3%25RN%25QQ%25N1%25P0%25Q6%25Q4%25O0%26le%3DZwH4BGZlAGLlAlH0ZUSkYzAioD%3D%3D%26m%3D%26qid%3D876649536%26im%3D1_t01386b81c31e58d8dd%26src%3D360se%26t%3D1; T=s%3D84cc5aed0672118e130eb24c5afec615%26t%3D1531440507%26lm%3D%26lf%3D1%26sk%3Dc0f4d3338fec7e2f2ccf0826684a8b50%26mt%3D1531440507%26rc%3D1%26v%3D2.0%26a%3D1; __huid=11haPiIpSt4WlBnXh2jvJl2KFXdXr0KVQNmgrv0y5ZbjY%3D; count=12; test_cookie_enable=null; _S=aad5a1137ce6913150764571ecce0ee0',
    'DNT':'1',
    'Host':'image.so.com',
    'Proxy-Connection':'keep-alive',
    'Referer':'http://image.so.com/z?ch=go',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE',
    'X-Requested-With':'XMLHttpRequest',
    }

START_URL = "http://image.so.com/"
NUM_RETRIES = 2

#url列表
TAG_URL_LIST = []   #大的标签的链接
Tag_SMALL_URL_LIST = [] #小的标签的链接
THREAD_NUM = 10