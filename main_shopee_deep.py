# coding=utf-8
import pygsheets
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
import tools
import time

def shopee_deep():
    # shopee
    url_main = 'https://shopee.tw/search?keyword=%E5%86%B7%E5%87%8D%E7%99%BD%E8%9D%A6'
    key_str = '冷凍白蝦'

    headers = {
        'User-Agent': 'Googlebot',
    }

    r = requests.get(url_main,headers=headers,allow_redirects=True)
    print("查看連線狀況: " + str(r.status_code)) #查看連線狀況
    print("連線網址: " + str(r.url)) #查看連線的網址

    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")

    '''
    contents 標題
    prices 價錢
    links 連結
    page 頁數
    '''
    contents = soup.find_all("div", class_="_1NoI8_ A6gE1J _1co5xN")
    prices = soup.find_all("span", class_="_1xk7ak")
    all_items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
    links = [['= HYPERLINK ("https://shopee.tw'+i.find('a').get('href')+'"),"賣場連結"'] for i in all_items]
    page = int(soup.find("span", class_="shopee-mini-page-controller__total").getText())

    # 報表寫入 GCP
    gc = pygsheets.authorize(service_file='valid-xxxx-xxxx-xxxxxxx.json')
    survey_url = 'https://docs.google.com/'

    t = time.localtime()
    time_str = time.strftime("%Y%m%d", t)

    sh = gc.open_by_url(survey_url)
    sheet_title = time_str+"_"+key_str

    try:
        sh.worksheets('title',sheet_title)
    except:
        sh.add_worksheet(sheet_title, 500, 15, None, None, 0)

    wks = sh.worksheet_by_title(sheet_title)
    header = wks.cell('A1') #選取起始儲存格

    wks.update_values(crange='A1',values=[
        [
            '品名',
            '項目',
            '價錢',
            '已出售',
            '商品數量',
            '產地',
            '重量',
            '出貨地',
            '網址',
        ]])

    print("分頁數量: "+ str(page))

    j = 2
    k = 0
    page_str = 0

    while k <= page:
        url = url_main+'&page=' + str(page_str)
        print("當頁網址: "+str(url))
        r = requests.get(url, headers=headers, allow_redirects=True)
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")

        contents = soup.find_all("div", class_="_1NoI8_ A6gE1J _1co5xN")
        prices = soup.find_all("span", class_="_1xk7ak")
        all_items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
        links = [['https://shopee.tw'+i.find('a').get('href')] for i in all_items]

        number_i = 1
        for c, p, l in zip(contents, prices, links):
            print("c: " + c.contents[0])
            print("p: " + p.contents[0])
            print("page: "+str(k))
            print("number_i: "+str(number_i))

            url_sub = l[0]

            # 已售出
            for loop_num in range(50):
                try:
                    r_sub = requests.get(url_sub, headers=headers, allow_redirects=True)
                    soup_sub = BeautifulSoup(r_sub.text, 'html.parser')
                    sell_qu = [soup_sub.find("div", class_="_2gcR05").getText()]
                    is_loop_num = False
                    break
                except:
                    print("'已售出'沒有抓到數值")

            buy_data = soup_sub.find_all("div", class_="_2gVYdB")
            buy_detail = soup_sub.find("div", class_="_36_A1j").find('span')

            print('*---------------------------------*')

            '''
            _Product_name           品名
            _Weight                 重量
            _Brand                  品牌
            _Origin                 產地
            _Products_num           商品數量
            _Shipping_place	        出貨地
            _Shipping_restrictions  運送限制
            _Shelf_life             保存期限
            _Species                種類
            _Pork_origin            豬肉產地
            _Specification          規格
            _Specification_v2       規格 V2
            _Contents               內容物/成分
            _Effective_date         有效日期/剩餘保存期限
            _Food_business          食品業者登錄字號
            _Telephone              國內負責廠商電話
            _Product_Insurance      產品責任險
    
            '''
            _Product_name = ['']
            _Weight = ['']
            _Brand = ['']
            _Origin = ['']
            _Products_num = ['']
            _othen = ''
            _Shipping_place = ['']
            _Shipping_restrictions = ['']
            _Shelf_life = ['']
            _Species = ['']
            _Pork_origin = ['']
            _Specification = ['']
            _Specification_v2 = ['']
            _Contents = ['']
            _Effective_date = ['']
            _Food_business = ['']
            _Telephone = ['']
            _Product_Insurance = ['']

            for bu in buy_data:
                title = bu.find("label",class_="_1-gNZm").getText()

                if title == '品牌':
                    _Brand = [tools.getValueGogo(bu)]

                elif title == '產地':
                    _Origin = [tools.getValueGogo(bu)]

                elif title == '商品數量':
                    _Products_num = [tools.getValueGogo(bu)]

                elif title == '出貨地':
                    _Shipping_place = [tools.getValueGogo(bu)]

                elif title == '運送限制':
                    _Shipping_restrictions = [tools.getValueGogo(bu)]

                elif title == '保存期限':
                    _Shelf_life = [tools.getValueGogo(bu)]

                elif title == '種類':
                    _Species = [tools.getValueGogo(bu)]

                elif title == '豬肉產地':
                    _Pork_origin = [tools.getValueGogo(bu)]

                elif title == '規格':
                    _Specification = [tools.getValueGogo(bu)]

                elif title == '內容物/成分':
                    _Contents = [tools.getValueGogo(bu)]

                elif title == '有效日期/剩餘保存期限':
                    _Effective_date = [tools.getValueGogo(bu)]

                elif title == '食品業者登錄字號':
                    _Food_business = [tools.getValueGogo(bu)]

                elif title == '國內負責廠商電話':
                    _Telephone = [tools.getValueGogo(bu)]

                elif title == '產品責任險':
                    _Product_Insurance = [tools.getValueGogo(bu)]


                else:
                    try:
                        _othen += "{title_out} : {value_out} || ".format(title_out=title, value_out=bu.find("div").getText())
                    except:
                        print(bu)
                        print(title)

            if _othen !='':
                _othen = [_othen]
            else:
                _othen = ['']

            # 產品品名抓取
            if _Product_name == ['']:
                for _Product_name_num in range(10):
                    try:
                        _Product_name = [tools.getSpecification(c.contents[0])]
                        break
                    except:
                        _Product_name = ['']

            #規格如果是空的抓取
            if _Specification == ['']:
                try:
                    regex = regex = r"^(?:內容物|產品規格)\W{1,3}(.*)"
                    _Specification = [tools.getStringGogoWeight(buy_detail.getText(), regex)]
                except:
                    _Specification = ['']

            # 重量抓取
            try:
                regex = r"^(?:重量|產品規格|規格|草蝦淨重|\s+內容量 \( g/ml \))\W{1,3}(.*)"
                _Weight = [tools.getStringGogoWeight(buy_detail.getText(), regex)]
            except:
                _Weight = ['']

            #重量特殊處理
            if _Weight == ['']:
                try:
                    regex = regex = r"^每包(.*)"
                    _Weight = [tools.getStringGogoWeight(buy_detail.getText(), regex)]
                except:
                    _Weight = ['']

            #重量title處理
            if _Weight == ['']:
                try:
                    regex = regex = r"(\d+g)|(\d+\.\d+kg)"
                    _Weight = [tools.getStringGogoWeight(c.contents[0], regex)]
                except:
                    _Weight = ['']


            #有效期限抓取
            if _Shelf_life == ['']:
                try:
                    regex = regex = r"^有效期限(.*)"
                    _Shelf_life = [tools.getStringGogoWeight(buy_detail.getText(), regex)]
                except:
                    _Shelf_life = ['']

            #產地抓取
            if _Origin == ['']:
                try:
                    regex = regex = r"^(?:\*產地|產地|★ 產地|◎原產地\(國家\)|原產地\(國\))\W{1,3}(.*)"
                    _Origin = [tools.getStringGogoWeight(buy_detail.getText(), regex)]
                except:
                    _Origin = ['']

            wks.update_values(crange="A" + str(j), values=
            (list(map(list, zip(*[
                _Product_name,
                c.contents,
                p.contents,
                sell_qu,
                _Products_num,
                _Origin,
                _Weight,
                _Shipping_place,
                l,
            ])))))

            j += 1
            number_i +=1

        k += 1
        page_str += 1

    return 'OKOK'

for is_pass_num in range(10):
    try:
        is_pass = shopee_deep()
        if is_pass == 'OKOK':
            print("結束囉~~")
            break
    except:
        print("老爺，不好拉，失敗 {num} 次 !!".format(num=is_pass_num))

time.sleep(3)
quit()
