# Python爬蟲之蝦皮爬爬樂_windows版本
## 動機

幫別人弄的，結果居然跟我說，這些資料還沒想到要做啥，要我每天都爬一下，還不給我DB，只給我 'google 報表'。

當作練功玩玩

## 參數說明

```python
url_main = '搜尋網址'
key_str = '關鍵字，拿來當 sheet title'

# GCP api，google 報表，權限部分去搜尋google 大神吧
gc = pygsheets.authorize(service_file='valid-xxxx-xxxx-xxxxxxx.json')
# 要把權限打開，認真!!
survey_url = '報表網址'

# 新創 sheet 的一行資料
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
```

## 運作方式

執行就是了，結果 :

```
查看連線狀況: 200
連線網址: https://shopee.tw/search?keyword=%E5%86%B7%E5%87%8D%E7%99%BD%E8%9D%A6
分頁數量: 8
當頁網址: https://shopee.tw/search?keyword=%E5%86%B7%E5%87%8D%E7%99%BD%E8%9D%A6&page=0
c: 【貝蛤蛤】南美生白蝦40/50／生白蝦／白蝦／蝦子／冷凍白蝦／冷凍蝦子／冷凍食品／海鮮／
p: 270
page: 0
number_i: 1
*---------------------------------*
```

c : 網址標題

p: 多少錢

page: 頁面，通常都是從0，不知道哪天會從1開始數

number_i: 第0頁的第1筆資料



報表部分: https://docs.google.com/spreadsheets/d/1y4RNIrpryeLPylnUS3YDcnUxLMWLOK2GKa809vOWeWQ/edit#gid=2087910786

## 結論

還是認真上班好了~