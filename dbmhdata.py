#coding=utf-8
import sys
import MySQLdb
import short_url
import os
import chardet
import uuid
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from xpinyin import Pinyin
reload(sys)
sys.setdefaultencoding('utf-8')


dataname = "test"

conn= MySQLdb.connect(
    host='localhost',
    port = 3306,
    user='root',
    passwd='12345',
    db = dataname ,
)

def getDate():
    loadfile = [u'.']
    mydict = {}
    mylist = []
    while(loadfile):
        try:
            path = loadfile.pop()
            #
            #print path
            for x in os.listdir(path):

                if os.path.isfile(os.path.join(path,x)):
                    if os.path.splitext(x)[1]=='.jpg' or os.path.splitext(x)[1]=='.png':
                        # 这里这样写是因为读取海贼王路径 会出现在海贼 和 王 中间的\\\分割 目前不知道解决的方式
                        try:
                            pass
                            #temp_path = path.decode("GBK")
                            #temp_x = x.decode("GBK")
                        except Exception,e:
                            #gb18030TypeStr = strs.encode('GB18030')
                            temp_path = path.decode("GB18030")
                            temp_x = x.decode("GB18030")
                        #templist = test3(temp_path.split('\\')[-1],temp_x,temp_path.split('\\')[-2])
                        templist = test3(path.split('\\')[-1],x,path.split('\\')[-2])
                        #templist = test3(path.split('\\')[-1].decode("GBK"),x,path.split('\\')[-2].decode("GBK"))
                        #print chardet.detect(path.split('\\')[-1])

                        mydict[templist[0]] = templist
                else:
                    loadfile.append(os.path.join(path,x))

        except Exception,e:
            print str(e) + path


    #InsertData('mhpic',mydict)
    for key in mydict:
        mylist.append(mydict[key])
        #print mydict


    #print mydict
    #updata_mhchapter_todb(mylist)

    updata_mhdata_todb(mylist)

def test1():
    for i in range(10):
        url = short_url.encode_url(123)
        print url
        print short_url.decode_url(url)


def test2():
    p = Pinyin()
    print p.get_pinyin(u"上海", '')
#test2()

def InsertData(TableName,dic):

    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='12345',db='test',port=3306)  #链接数据库
        cur=conn.cursor()
        COLstr=''   #列的字段
        ROWstr=''  #行字段

        ColumnStyle=' VARCHAR(20)'
        for key in dic.keys():
            COLstr=COLstr+' '+key+ColumnStyle+','
            ROWstr=(ROWstr+'"%s"'+',')%(dic[key])

            #判断表是否存在，存在执行try，不存在执行except新建表，再insert
        try:
            cur.execute("SELECT * FROM  %s"%(TableName))
            cur.execute("INSERT INTO %s VALUES (%s)"%(TableName,ROWstr[:-1]))

        except MySQLdb.Error,e:
            cur.execute("CREATE TABLE %s (%s)"%(TableName,COLstr[:-1]))
            cur.execute("INSERT INTO %s VALUES (%s)"%(TableName,ROWstr[:-1]))
        conn.commit()
        cur.close()
        conn.close()

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def test3(chaptername,check_str,mhname):
    str_type = check_str.split('.')[-1]
    str_name = chaptername

    pattern = re.compile(u'(.+)\.+(.+)')
    match = pattern.match(check_str)
    str_id =  match.group(1)

    str_nums = str_id.replace(chaptername,'')
    if str_nums.find('num')!=-1:
        str_nums = check_str.split('.')[0].replace('num','')



    #str_id = check_str.split('.')[-2:]
    return [str_id,str_type,mhname,str_name,str_nums,mhname + '/' + str_name + '/' + check_str]

def updata_mhdata_todb(mylist):
    conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='12345',
        db = dataname ,
        charset='utf8'
    )
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS mhdata")
    cur.execute("CREATE TABLE mhdata(id varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',type varchar(32) COLLATE utf8_bin DEFAULT NULL,mhname varchar(100) COLLATE utf8_bin DEFAULT NULL,chaptername varchar(100)  COLLATE utf8_bin DEFAULT NULL,pages int(11) COLLATE utf8_bin  DEFAULT NULL,mhurl varchar(100)  COLLATE utf8_bin DEFAULT NULL,KEY `chapter_id` (`id`),CONSTRAINT `chapter_id` FOREIGN KEY (`id`) REFERENCES `mhchapter` (`chapterid`))")

    #list = [mylist[0][0],mylist[0][1],mylist[0][2],mylist[0][3],mylist[0][4]]
    #cur.executemany(sqli,[('2','1','1','1','1')])

    # 进行判读 按照章节名称添加主键 其他的不用变化 需要从数据库中取出章节的id
    #漫画章节的表并不大  完全可以一次性查出 同时也可以分多次来查询

    #sqli = "insert into mhdata(id,type,mhname,chaptername,pages,mhurl)values(%s,%s,%s,%s,%s,%s)"
    #cur.executemany(sqli,mylist)

    conn_in= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='12345',
        db = dataname ,
        charset='utf8',

    )
    cur_in = conn_in.cursor()
    kkk = cur_in.execute("select * from  mhchapter")
    info = cur_in.fetchmany(kkk)

    chapterdict = {}

    for i,j,z,f,k in info:
        chapterdict[z+'|'+f] = j

    for cell in mylist:
        checks_str = cell[2] + '|' + cell[3]

        change_id = chapterdict[checks_str]
        cell[0] = change_id


    cur_in.close()
    conn_in.commit()
    conn_in.close()


    sqli = "insert into mhdata(id,type,mhname,chaptername,pages,mhurl)values(%s,%s,%s,%s,%s,%s)"
    cur.executemany(sqli,mylist)

    cur_in.close()
    conn.commit()
    conn.close()

def updata_mhchapter_todb(mylist):
    conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='12345',
        db = dataname ,
        charset='utf8',

    )
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS mhchapter")
    cur.execute("CREATE TABLE mhchapter(mhid varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',chapterid varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',mhname varchar(100)  COLLATE utf8_bin DEFAULT NULL,chaptername varchar(100)  COLLATE utf8_bin DEFAULT NULL,pages int(11) COLLATE utf8_bin  DEFAULT NULL,primary key(chapterid))")

    mhdict = {}
    chapterdict = {}

    for key in mylist:
        if key[2] not in mhdict:
            mhdict[key[2]] =  uuid.uuid1()


        str_first = unicode("第", "utf8")
        str_seconde = unicode("话", "utf8")

        mypage = 0
        if key[3].find(str_first)!=-1 and key[3].find(str_seconde)!=-1:
            mypage = int(key[3][key[3].find(str_first) + 1:key[3].find(str_seconde)])
        chapterdict[key[3]] = [mhdict[key[2]],uuid.uuid1(),key[2],key[3],mypage]


    ttlist = []
    for key in chapterdict:
        ttlist.append(chapterdict[key])

    sqli = "insert into mhchapter(mhid,chapterid,mhname,chaptername,pages)values(%s,%s,%s,%s,%s)"
    #cur.executemany(sqli,[('2','1','1','1','1')])
    cur.executemany(sqli,ttlist)

    cur.close()
    conn.commit()
    conn.close()

def test5():
    list = [['9','1','1','1','1'],['12','1','1','1','1'],['31','1','1','1','1']]
    conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='12345',
        db = dataname ,
    )
    cursor=conn.cursor()
    sql = "insert into t1(id,type,hmname,chaptername,page)values(%s,%s,%s,%s,%s)"
    cursor.executemany(sql,list)
    conn.commit()
    conn.close()
    print("ok")


def str_splite():
    mystr = "家庭教师/第304话 世川了平VS.青叶红叶/第304话 世川了平VS.青叶红叶9.jpg"
    str_type = mystr.split('.')[-1]
    print str_type.encode('GBK')
    #print mystr.split('\\')[1].encode('GBK')

def test_check_str():
    strs = '7³'

    print repr(strs)

    strs1 = "xb3"
    strs2 = "xc2"
    gbkTypeStr = strs.encode('GBK', 'ignore')
    gb18030TypeStr = strs.encode('GB18030')
    print gbkTypeStr
    print gb18030TypeStr
    #print strs1.encode("GBK")
    #print strs1.decode("GBK")


def test_read_file():
    file = "第114话 库洛姆•骷髅VS.玛蒙"
    #file = "家庭教师"
    gb18030TypeStr = file.encode('GB18030')
    ddd = unicode('./家庭教师/第114话 库洛姆•骷髅VS.玛蒙','utf-8')
    print repr(ddd)
    #print os.listdir(ddd)

    strkkk = u'.\\\u7b2c114\u8bdd \u5e93\u6d1b\u59c6?\u9ab7\u9ac5VS.\u739b\u8499'

    print repr(strkkk)
    print repr(os.path.realpath(strkkk))
    print repr(os.path.split(os.path.realpath(strkkk))[1])
    print repr(unicode('第114话 库洛姆•骷髅VS.玛蒙','utf-8') )
    print os.listdir(unicode('第114话 库洛姆•骷髅VS.玛蒙','utf-8'))


    #file = open("123")


def test_utf_GBK():
    path = '.\\\xb5\xda114\xbb\xb0 \xbf\xe2\xc2\xe5\xc4\xb7?\xf7\xbc\xf7\xc3VS.\xc2\xea\xc3\xc9'
    print repr(path)
    ddd = unicode(path,'GBK')
    print repr(ddd)

    loadfile = ['.']
    mydict = {}
    mylist = []
    print os.listdir(loadfile[0])
    #for x in os.listdir(path):


def test_uuid():
    name = "test_name"
    namespace = "test_namespace"

    print uuid.uuid1()  # 带参的方法参见Python Doc
    print(uuid.uuid3(uuid.NAMESPACE_DNS, namespace))


def split_strs():
    soierjo = "世川了平VS.jpg"
    str5 = unicode(soierjo, "utf8")
    pattern = re.compile(u'(.+)\.+(.+)')
    match = pattern.match(str5)
    print match.group(1)
    return match

# 把字典插入数据库中 其中字典的键作为主键
#test4([])
#str_splite()
#test_uuid()
getDate()
#str_splite()
#split_strs()

#test_utf_GBK()

#test_check_str()
#dic={"a":["1","2"],"c":["1","2"]}
#InsertData('testtable',dic)
#test3("广岛之鲛".encode('GBK'),"广岛之鲛1.jpg".encode('GBK'))
# 包括 直接的id名称 类型 漫画名称 章节 页数
# 处理 插入的时候会进行查询 如果有重复 更新数据库 并生成对应日志