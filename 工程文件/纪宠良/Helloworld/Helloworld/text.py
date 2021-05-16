# -*- coding:utf-8 -*-
import pymysql
import math
conn = pymysql.Connect(
    host='127.0.0.1',  #连接IP地址，如果是本地就是localhost
    user='root',       #数据库用户名
    passwd='jclgogogo.',   #据库密码
    db='test',         #要查询的数据库名
    charset='utf8'    #码
)
museum=['抗美援朝纪念馆','旅顺博物馆','沈阳故宫博物院','大连现代博物馆','吉林省自然博物馆','吉林省博物院','伪满皇宫博物院','东北烈士纪念馆','铁人王进喜纪念馆','瑷珲历史陈列馆','黑龙江省博物馆','大庆博物馆','上海博物馆','上海鲁迅纪念馆','中共一大会址纪念馆','上海科技馆','陈云纪念馆','南京博物院','侵华日军南京大屠杀遇难同胞纪念馆','南通博物苑','苏州博物馆','扬州博物馆','常州博物馆','南京市博物总馆','浙江省博物馆','浙江自然博物馆','中国丝绸博物馆']
for name in museum:
    c = conn.cursor()      #标，上一行数据查完后，游标移至下一行继续查询
    c.execute('SELECT mus_id from text_museum where  mus_name="'+name+'"')    #行这条查询语句
    row = c.fetchone()     #etchone查询一行
    mid=row[0]
    c.execute('select new_id from test_m where title="'+"旅顺博物馆文物保护修复基地成立!"+'"')
    flag=c.fetchone()
    if(flag):
        print([flag,"yes"])
    else:
        print([flag,"no"])

    print(mid)


