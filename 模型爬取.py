import re
from lxml import etree
import requests
import csv
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
file = open('./模型_top300.csv',mode='w',encoding='utf-8-sig',newline='')
column = ['名字','图片','厂商','出荷时间','游览人数','定价','比例','评分']
csv.writer(file).writerow(column)
# URL = 'https://www.hpoi.net/hobby/all?order=hits&r18=-1&company=2551&workers=&view=3&category=102&jobId=1'
header ={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76'
}
for page in tqdm(range(1,11)):
    print(f'.................正在爬取第{page}页.................')
    URL = f'https://www.hpoi.net/hobby/all?order=hits&r18=-1&company=2551&workers=&view=3&category=102&jobId=1&page={page}'
    time.sleep(1)
    response = requests.get(url=URL, headers=header)
    if response.status_code != 200:
        print(f'爬取失败，状态码为{response.status_code}')
    else:
        response.encoding = 'utf-8'
    # print(response.text)
    time.sleep(1)
    soup = BeautifulSoup(response.text, 'html.parser')  #
    li_list = soup.select('html > body > div.container > div.row > div.col-md-17 >div.hpoi-database-ibox > div#content > ul.hpoi-glyphicons-list > li')
    # print(li_list)
    j = 1
    for i in li_list:
        name_top = i.select_one('li > div.hpoi-detail-grid-right > div.hpoi-detail-grid-title > a').text #名字
        # print(name_top)
        changshan_top_1 = re.findall("<span><em>厂商：</em>(.*)</span>",str(i))
        changshan_top = ','.join(changshan_top_1)                                                       #厂商
        # print(changshan_top)
        chuhe_top_1 = re.findall("<span><em>出荷：</em>(.*)</span>",str(i))
        chuhe_top = ','.join(chuhe_top_1)                                                               #出荷
        # print(chuhe_top)
        youlan_top_1 = re.findall("<span><em>浏览：</em>(.*)</span>",str(i))
        youlan_top = ','.join(youlan_top_1)                                                             #游览
        tree = etree.HTML(response.text)
        net = tree.xpath(f'//*[@id="content"]/ul/li[{j}]/a/@href')[0]
        # print(net)
        j = j + 1
        url_top = 'https://www.hpoi.net/' + net
        respone = requests.get(url=url_top,headers=header)
        soup_1 = BeautifulSoup(respone.text,'html.parser')
        trees = etree.HTML(respone.text)
        try:
            price = trees.xpath('/html/body/div[2]/div[3]/div/div[2]/div/div[2]/div[3]/span[text()="定价"]/following-sibling::*[1]')[0].text
        except:
            price = None
        if price == None:
            price = trees.xpath('/html/body/div[2]/div[3]/div/div[2]/div/div[2]/div[4]/span[text()="定价"]/following-sibling::*[1]')[0].text
        # print(price)                                                                                                            #  价格
        bili_top = trees.xpath('////div[contains(@class, "hpoi-infoList-item")]//a/text()')[4]
        if bili_top not in ['1/60','1/48','1/144','1/100']:
            bili_top = '1/100'
        # print(bili_top)                                                                                                          #比例
        pingfen_top_1 = trees.xpath('//div[contains(text(), "评分：")]/span/text()')
        pingfen_top = ','.join(pingfen_top_1)                                                                                      #评分
        if pingfen_top == '�':
            pingfen_top = 4.5
        # print(pingfen_top)
        image_top_1 = trees.xpath('/html/body/div[2]/div[3]/div/div[2]/div/div[1]/div[1]/div/img/@src')
        image_top = ','.join(image_top_1)
        # print(image_top)
        # xilie_top = trees.xpath('////div[contains(@class, "hpoi-infoList-item")]//a/text()')
        # print(xilie_top)

        #     time.sleep(1)
        # list = soup_1.select('html > body > div.container-fluid > div.container > div.row')
        # for l in list:
        #     list_1 = l.select_one('div.row > div.col-md-18 > div.hpoi-ibox-content > div.hpoi-ibox-box > div.hpoi-ibox-img > div.isotope-img')
        #     image_top = list_1.find('img').get('src')                          #图片
        #     print(image_top)
            #
            #     list_2 = l.select_one(
            #         'div.row > div.col-md-18 > div.hpoi-ibox-content > div.infoList-box')
            #     # print(list_2)
            #
            #     shuxing_top_1 = list_2.find_all('a',target="_blank")
            #     # print(shuxing_top_1)
            #     shuxing_top = ','.join([i.text for i in shuxing_top_1[0:3]])
            #     # print(shuxing_top)                                    #属性
            #     pingfen_top_1 = re.findall('<div>评分：<span>(.*)</span></div>',str(l))
            #     pingfen_top = ','.join(pingfen_top_1)
                # print(pingfen_top_1)                                                     #评分
                # tree = etree.HTML(respone.text)
                # price = tree.xpath('/html/body/div[2]/div[3]/div/div[2]/div/div[2]/div[5]/p/text()')[0].text
                # print(price)
                # print(price)
        top_data = [name_top,image_top,changshan_top,chuhe_top,youlan_top,price,bili_top,pingfen_top]
        # column = ['名字', '图片', '厂商', '出荷时间', '游览人数', '定价', '比例', '评分']
        print(top_data)
        time.sleep(1)
        csv.writer(file).writerow(top_data)
file.close()
print('采集完毕')
