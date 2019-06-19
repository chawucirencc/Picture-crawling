import time
import requests
import pymysql
from lxml import etree


def get_response(url):
    '''
        得到网页的相应
    '''
    try:
        r = requests.get(url=url)
        r.status_code == 200
        r.encoding = 'utf-8'
        return r.text
    except:
        print("get error")


def getpage_html(url_text):
    '''
    得到二级网页的信息以及图片的地址信息.....
    '''
    html = etree.HTML(url_text)
    page_info = html.xpath("//a[@class='preview']/@href")
    return page_info


def deal_pageinfo(page_url, page_url_all):
    '''
    得到图片地址，将图片信息存放到一个list中...
    '''
    try:
        for res in page_url:
            page_res = requests.get(res)
            time.sleep(1)
            if page_res.status_code != 200:
                continue
            else:
                page_res.encoding = 'utf-8'
                page_html = etree.HTML(page_res.text)
                photo_address = page_html.xpath("//img[@id='wallpaper']/@src")
                page_url_all.extend(photo_address)
    except:
        print("page_info get error")
    return page_url_all


def save_photo(page_url_all, save_path, i):
    '''
    通过requests的get请求图片的网址，通过2进制写入到文件中...
    '''
    a = 1
    print("总共{0}张照片".format(len(page_url_all)))
    try:
        for x in page_url_all:
            time.sleep(1)
            img = requests.get(x)
            if img.status_code != 200:
                print("{0}不能获取...".format(x))
                continue
            print("正在下载第{0}张照片...".format(a))
            with open(save_path+str(a)+'.jpg', 'wb') as f:
                f.write(img.content)
            a += 1
        f.close
        print("图片下载完成...")
    except:
        print('图片获取失败...')


def connection_sql():
    '''
    连接数据库的的函数
    '''
    conn = pymysql.connect(host='localhost', user='root', password='password', database='world')
    cur = conn.cursor()
    sql = "SELECT Population, Name FROM city\
            WHERE Population > 2000000;"
    result = cur.execute(sql)
    print(result)
    for t in cur.fetchall():
        print(t)
    conn.close()


def main():
    '''
    主函数，定义全局变量，调用函数...
    '''
    time_1 = time.time()
    save_path = 'C:\\Users\\NaOH\\Desktop\\photo\\'
    # 保存地址可自定义
    print("注意：若输入较大的数值可能会使得最终结果失败，会耗费较大的电脑性能和网络，请合理选择数值...")
    page_end = int(input("请输入想要爬取的页数："))
    time.sleep(2)
    print("开始爬取...")
    page_url_all = []
    for i in range(2, page_end+2):
        url = "https://wallhaven.cc/toplist?page=" + str(i)
        url_text = get_response(url)
        page_url = getpage_html(url_text)
        page_url_all = deal_pageinfo(page_url, page_url_all=page_url_all)
    print("已经完成50%...")
    # print(len(page_url_all))
    # print(page_url_all)
    save_photo(page_url_all, save_path, i)
    time_2 = time.time() - time_1
    print("时长为", time_2)


if __name__ == "__main__":
    main()

