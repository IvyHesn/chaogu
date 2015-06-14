import urllib.request
import json
import time
import codecs
from collections import OrderedDict
import csv


def get_html(url):
    '''
    加header，访问url得到网页html代码
    '''
    send_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'xueqiu.com',
        'Cookie': r's=iadygnff.g98ms6; xq_a_token=7e06ebb83c8d925cb776b5eb4fe87b09369d7c6e; xq_r_token=f90b576a98f834873eae35246026eff163237a0a; __utma=1.277142738.1433166723.1433166839.1433258555.4; __utmb=1.3.10.1433258555; __utmc=1; __utmz=1.1433166723.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E9%9B%AA%E7%90%83; Hm_lvt_1db88642e346389874251b5a1eded6e3=1433166723,1433258555; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1433258610',
    }
    req = urllib.request.Request(url, headers=send_headers)
    resp = urllib.request.urlopen(req)
    html = resp.read()
    html = html.decode('utf-8')
    return html


def get_dic(html):
    '''
    在得到的网页代码中，提取有用的信息，并转为dict
    '''
    pos_start = html.find('SNB.cubeInfo = ') + len('SNB.cubeInfo = ')
    pos_end = html.find('SNB.cubePieData')
    data = html[pos_start:pos_end]
    dic = json.loads(data, object_pairs_hook=OrderedDict)
    return dic


def get_stock_list(dic):
    '''
    对提取出来的dict进一步筛选，得到股票组合
    '''
    stock_info = dic['view_rebalancing']['holdings']
    stock_info = stock_info
    new_key_seq = ('stock_name', 'segment_name', 'stock_symbol', 'weight')
    stock_list = [None] * len(stock_info)
    for i in range(0, len(stock_info)):
        stock = [] * len(new_key_seq)
        for key in new_key_seq:
            value = stock_info[i][key]
            stock.append(value)
        symbol_url = 'http://xueqiu.com/P/' + dic['symbol']
        stock.append(symbol_url)
        stock_list[i] = stock
    #print (stock_list)
    return stock_list


def get_data(html):
    '''
    暂时没用到的股票组合信息
    '''
    pos_start = html.find('SNB.cubePieData = ') + len('SNB.cubePieData = ')
    pos_end = html.find('SNB.cubeTreeData ')
    data = html[pos_start:pos_end]
    return data


def get_all_stock_info(url_list):
    '''
    得到url_list中的所有股票组合
    '''
    all_stock_list = []
    for url in url_list:
        html = get_html(url)
        dic = get_dic(html)
        stock_list = get_stock_list(dic)
        all_stock_list.append(stock_list)
        print (url, 'get_stock_list successful!')
    return all_stock_list


def write_csv(all_stock_list, file_name):
    '''
    写入csv文件
    '''
    with open(file_name, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, dialect='excel')
        spamwriter.writerow(['股票名称', '行业板块', '股票代码', '持仓比例', '链接地址'])
        for stock_list in all_stock_list:
            for stock in stock_list:
                spamwriter.writerow(stock)
    print ('write_csv successful!')

url_list = [
    'http://xueqiu.com/P/ZH161584',
    'http://xueqiu.com/P/ZH000826',
    'http://xueqiu.com/P/ZH115767',
    'http://xueqiu.com/P/ZH003288',
    'http://xueqiu.com/P/ZH228157',
    'http://xueqiu.com/P/ZH079629',
    'http://xueqiu.com/P/ZH217723',
    'http://xueqiu.com/P/ZH157153',
]


def main():
    all_stock_list = get_all_stock_info(url_list)
    file_name = 'stock_list-' + \
        time.strftime('%Y-%m-%d', time.localtime()) + '.csv'
    print (file_name)
    write_csv(all_stock_list, file_name)

main()
