import requests
import json
import time

future_member_str = '''80108379A 安粮期货
80024680B 倍特期货
80103748B 渤海期货
80107843B 宝城期货
80066672C 长江期货
80066673C 财信期货
80007037C 创元期货
80108179C 长安期货
80108055C 长城期货
80108168C 财达期货
80107847D 东方期货
80107735D 大陆期货
80055436D 大有期货
80134835D 第一创业期货
80102887D 东海期货
80107997D 东航期货
80104009D 大越期货
80108370D 道通期货
80045628D 东华期货
80108180D 东亚期货
80104015D 大地期货
80108070D 东兴期货
80108224D 东证期货
80111760D 东方财富期货
80101066D 东吴期货
80108200D 大通期货
80108197F 福能期货
80066668F 方正中期期货
80101065G 国泰期货
80066666G 国元期货
80102927G 国联期货
80066669G 国投安信期货
80103744G 光大期货
80108400G 广州期货
80108375G 国海良时期货
80102946G 国金期货
80004615G 国贸期货
80100056G 国都期货
80107031G 冠通期货
80107033G 广金期货
80095998G 国信期货
80069367G 格林期货
80107846G 国盛期货
80108177G 国富期货
80052362G 广发期货
80108093H 华金期货
80108678H 华鑫期货
80021496H 华龙期货
80055521H 华泰期货
80061244H 宏源期货
80071840H 海通期货
80107733H 红塔期货
80108192H 华联期货
80058848H 华闻期货
80108051H 徽商期货
80108653H 海证期货
80104005H 华融融达期货
80058162H 华安期货
80107995H 华融期货
80108169H 和合期货
80108394H 恒洋贸易
80107034H 和融期货
80055515H 海航期货
80107731H 华西期货
80078479H 恒泰期货
80108095H 汇金期货
80066667H 恒力期货
80108385H 华创期货
80114350H 混沌天成
80044916H 弘业期货
80076361H 恒银期货
80108390J 京都期货
80055497J 津投期货
80055522J 金源期货
80074415J 锦泰期货
80101049J 建信期货
80108380J 金信期货
80053800J 金石期货
80039956J 金瑞期货
80052272J 金汇期货
80108178J 金鹏期货
80103800J 金元期货
80108378J 九州期货
80068441J 江海汇鑫期货
80102903L 鲁证期货
80108381L 路易达孚中国
80066674M 摩根大通期货
80103391M 迈科期货
80019274M 美尔雅期货
80108373M 民生期货
80107032N 宁证期货
80080089N 南华期货
80010572P 平安期货
80104011Q 前海期货
80104013Q 乾坤期货
80103804R 瑞达期货
80108189R 瑞银期货
80103599R 瑞奇期货
80055499S 盛达期货
80108195S 上海中期
80108386S 山金期货
80066675S 首创期货
80108171S 三立期货
80055520S 神华期货
80004835S 申银万国期货
80107732S 晟鑫期货
80108186T 天鸿期货
80093548T 天富期货
80055086T 通惠期货
80373309T 天风期货
80055516W 五矿期货
80108191X 新晟期货
80101060X 新世纪期货
80108087X 西南期货
80104008X 先融期货
80107993X 信达期货
80103802X 兴证期货
80106526X 鑫鼎盛期货
80020521X 兴业期货
80104012X 新纪元期货
80108377X 西部期货
80030099X 新湖期货
80980919X 先锋期货
80145758Y 永商期货
80102901Y 永安期货
80108185Y 英大期货
80102904Y 一德期货
80009079Y 云晨期货
80057675Y 云财富期货
80103797Y 银河期货
80108218Z 招金期货
80128238Z 中银国际期货
80108049Z 中金期货
80055519Z 中航期货
80128239Z 中融汇信
80027560Z 中钢期货
80050220Z 中信期货
80098329Z 中粮期货
80108374Z 中衍期货
80096453Z 中国国际期货
80075388Z 中财期货
80023426Z 中大期货
80055517Z 招商期货
80098340Z 中信建投期货
80108203Z 中原期货
80108383Z 中州期货
80104007Z 中投期货
80091157Z 浙商期货
80103801Z 中天期货
80066665Z 浙石期货
80103644Z 中辉期货'''

future_member_list = future_member_str.split('\n')

future_member_map = {}
for members in future_member_list:
    member = members.split(' ')
    future_member_map[member[0][:-1]] = member[1]


def data_to_params(datas):
    arr = []
    for key, value in datas.items():
        arr.append(key + '=' + str(value))
    return '&'.join(arr)


# type=QHCC&sty=QHSYCC&stat=4&mkt=069001008&sc=MA&code=ma2201&cmd=80102901&name=3
# &cb=jQuery1123042189815451714097_1629702488253&_=1629702488254

# http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?
# type=QHCC&sty=QHSYCC&stat=4&mkt=069001008&sc=PK&code=pk2110&cmd=80102901&name=3&
# cb=jQuery1123036098349030214427_1629790389700&_=1629790389701

cost_str = ''
for k, v in future_member_map.items():
    data = {
        'type': 'QHCC',
        'sty': 'QHSYCC',
        'stat': '4',
        'mkt': '069001008',
        'sc': 'PK',
        'code': 'pk2110',
        'cmd': k,
        'name': 3
    }
    url = 'https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?'
    url = url + data_to_params(data) + '&_=' + str(time.time())
    res = requests.get(url).content.decode('utf8')

    # res_b = b'([{"series1": {"categories":["7-27","7-28","7-29","7-30","8-02","8-03","8-04","8-05","8-06","8-09",
    # "8-10","8-11","8-12","8-13","8-16","8-17","8-18","8-19","8-20","8-23"],"series": [{"name":
    # "\xe7\xbb\x93\xe7\xae\x97\xe4\xbb\xb7","data": [2747,2725,2757,2814,2813,2751,2742,2751,2737,2727,2728,2792,
    # 2824,2831,2843,2846,2864,2824,2792,2841]},{"name": "\xe5\xa4\x9a\xe5\x8d\x95\xe5\x9d\x87\xe4\xbb\xb7",
    # "data": [2694.19,2695.00,2695.00,2711.02,2711.02,2711.02,2724.34,2733.58,2734.50,2733.17,2733.17,2745.49,
    # 2771.88,2771.88,2778.47,2784.26,2787.98,2787.98,2787.98,2794.40]},{"name":
    # "\xe7\xa9\xba\xe5\x8d\x95\xe5\x9d\x87\xe4\xbb\xb7","data": [2720.21,2720.21,2721.61,2731.11,2733.20,2738.49,
    # 2739.10,2741.73,2740.81,2740.44,2740.44,2749.09,2765.59,2770.30,2779.03,2779.03,2785.18,2785.18,2785.18,
    # 2787.29]}]},"series2": {"categories":["7-27","7-28","7-29","7-30","8-02","8-03","8-04","8-05","8-06","8-09",
    # "8-10","8-11","8-12","8-13","8-16","8-17","8-18","8-19","8-20","8-23"],"series": [{"name":
    # "\xe5\xa4\x9a\xe5\x8d\x95\xe9\x87\x8f","data": [7596,7800,7390,8540,7208,5827,10219,15645,21401,26031,24847,
    # 31431,47340,45166,49779,54454,57113,46112,41634,47373]},{"name": "\xe7\xa9\xba\xe5\x8d\x95\xe9\x87\x8f",
    # "data": [12108,9434,9807,10931,11218,15957,19304,24780,30705,31571,30712,36905,47332,51002,57966,55462,59789,
    # 59629,56223,58431]}]},"series3": {"categories":["7-27","7-28","7-29","7-30","8-02","8-03","8-04","8-05","8-06",
    # "8-09","8-10","8-11","8-12","8-13","8-16","8-17","8-18","8-19","8-20","8-23"],"series": [{"name":
    # "\xe5\x87\x80\xe5\xa4\x9a\xe9\x87\x8f","data": [null,null,null,null,null,null,null,null,null,null,null,null,8,
    # null,null,null,null,null,null,null]},{"name": "\xe5\x87\x80\xe7\xa9\xba\xe9\x87\x8f","data": [4512,1634,2417,
    # 2391,4010,10130,9085,9135,9304,5540,5865,5474,null,5836,8187,1008,2676,13517,14589,11058]}]}}])'

    if res == '': continue
    res = res.replace("(", '').replace(')', '')
    # if (data && data[0] && data[0].stats != false)
    if 'stats' in res: continue
    now_time = time.strftime('%m-%d', time.localtime()).replace('0', '')
    # if now_time not in res: continue
    if '8-23' not in res: continue
    text = json.loads(res)
    last_date = text[0]['series1']['categories'][-1]
    average_call_price = text[0]['series1']['series'][1]['data'][-1]
    average_put_price = text[0]['series1']['series'][2]['data'][-1]
    print(future_member_map[k], last_date, average_call_price, average_put_price)
    # print(type(last_date), last_date, type(average_call_price), type(average_put_price))
    cost_str = v + ' ' + last_date + ' ' + str(average_call_price) + ' ' + str(average_put_price) + '\n'
    time.sleep(2)
# cost_str = '''创元期货 8-23 None 2800.09
# 东证期货 8-23 2812.54 2809.13
# 东方财富期货 8-23 None None
# 东吴期货 8-23 2796.24 2779.9
# 方正中期期货 8-23 None None
# 国泰期货 8-23 2799.19 2791.9
# 国投安信期货 8-23 2799.84 None
# 光大期货 8-23 2824.34 2822.77
# 广发期货 8-23 2803.12 2789.54
# 华泰期货 8-23 2819.13 2799.34
# 海通期货 8-23 2833.61 2822.53
# 华闻期货 8-23 None 2805.45
# 徽商期货 8-23 None None
# 海证期货 8-23 2813.03 None
# 华安期货 8-23 None None
# 混沌天成 8-23 2822.96 None
# 弘业期货 8-23 None 2815.7
# 恒银期货 8-23 None None
# 南华期货 8-23 2762.43 None
# 平安期货 8-23 2779.23 None
# 瑞达期货 8-23 2836.61 2794.43
# 申银万国期货 8-23 2785.13 None
# 兴业期货 8-23 None 2778.56
# 新湖期货 8-23 2781.32 2793.77
# 永安期货 8-23 2794.4 2787.29
# 银河期货 8-23 2846.3 2815.12
# 中银国际期货 8-23 None 2773.83
# 中信期货 8-23 2801.74 2791.66
# 中粮期货 8-23 2821.4 None
# 中信建投期货 8-23 None 2777.01
# 中投期货 8-23 None 2831.82
# 中辉期货 8-23 2802.96 2848.07'''

cost_list = cost_str.split('\n')
count_put_price = 0
put_nums = 0
min_put_price = 0
max_put_price = 0
count_call_price = 0
call_nums = 0
min_call_price = 0
max_call_price = 0
min_put_name = ''
max_put_name = ''
min_call_name = ''
max_call_name = ''

for c in cost_list:
    price = c.split(' ')
    # 空单平均价格不为0
    if price[-1] == 'None' or price[-1] == '':
        continue
    else:
        # 转换字符串为数字类型
        put_price = float(price[-1])
        # 最低空单价
        if min_put_price == 0:
            min_put_price = put_price
        if min_put_price > put_price:
            min_put_price = put_price
            min_put_name = price[0]
        # 最高空单价
        if max_put_price < put_price:
            max_put_price = put_price
            max_put_name = price[0]
        put_nums += 1
        count_put_price += put_price

    if price[-2] == 'None':
        continue
    else:
        # 转换字符串为数字类型
        call_price = float(price[-2])
        # 最低空单价
        if min_call_price == 0:
            min_call_price = call_price
        if min_call_price > call_price:
            min_call_price = call_price
            min_call_name = price[0]
        # 最高空单价
        if max_call_price < call_price:
            max_call_price = call_price
            max_call_name = price[0]
        call_nums += 1
        count_call_price += call_price
print(count_put_price / put_nums if put_nums > 0 else 0, max_put_price, min_put_price, min_put_name, max_put_name)
print(count_call_price / call_nums if call_nums > 0 else 0, max_call_price, min_call_price, min_call_name,
      max_call_name)
