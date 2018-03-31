#coding=utf-8
import sys
import MySQLdb
import os
import re
import uuid

reload(sys)
sys.setdefaultencoding('utf-8')
dataname = "leodb"

def updata_mhdata_todb(list):
    conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='12345',
        db = dataname ,
        charset='utf8'
    )
    cur = conn.cursor()
    # kkk = cur.execute("select * from  mhname")
    # info = cur.fetchmany(kkk)
    # print info
    # print type(info)
    sqli =  "insert into mhchapter(id,mhname_id,data,chapter_nums,pics_nums,chapter_name)values(%s,%s,%s,%s,%s,%s)"
    cur.executemany(sqli,list)
    conn.commit()
    conn.close()




def updata_mhname_todb(list):
    conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='12345',
        db = dataname ,
        charset='utf8'
    )
    cur = conn.cursor()
    sqli =  "insert into mhname(id,mhname)values(%s,%s)"
    cur.executemany(sqli,list)
    conn.commit()
    conn.close()


def get_chapter_bydb():
    conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='12345',
        db = dataname ,
        charset='utf8'
    )
    cur = conn.cursor()
    names = cur.execute("select * from  mhchapter")
    info = cur.fetchmany(names)
    for key in info:
        print  key[2]

def get_mhname_bydb(mhname):
    conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='12345',
        db = dataname ,
        charset='utf8'
    )
    cur = conn.cursor()
    names = cur.execute("select * from  mhname")
    info = cur.fetchmany(names)
    has_name = False
    has_id = ""
    for key in info:
        if key[1] == mhname:
            has_name =  True
            has_id =  key[0]

    return has_name,has_id


def getDate():
    loadfile = [u'./app/static']
    temp_mhname = ""
    mhdict = {}
    chapter_url_lists = []
    while(loadfile):
        try:
            path = loadfile.pop()
            for x in os.listdir(path):
                if os.path.isfile(os.path.join(path,x)):
                    if os.path.splitext(x)[1]=='.jpg' or os.path.splitext(x)[1]=='.png':
                        # 记录上一个图片的路径 如果章节的名称不变 视为一个章节 同时生成章节id 以章节id作为字典的key 最后把数据放入一个大的数组中
                        try:
                            if(path.split('/')[-2]!=temp_mhname):
                                if(mhdict!={} or mhdict=={} and chapter_url_lists!=[]):
                                    chapter_id = uuid.uuid1()
                                    mhdict[chapter_id] = [temp_chaptername,chapter_url_lists,temp_mhname]
                                    checkdict(mhdict)
                                chapter_url_lists = []
                                mhdict = {}
                                temp_chaptername = ""
                                temp_mhname = path.split('/')[-2]
                            #如果章节的名称不同 就创建数组装起来
                            if(path.split('/')[-1]!=temp_chaptername):
                                # list  这里不管排序 创建chapterid 漫画的名称和里面的内容分开处理这样才符合逻辑
                                if temp_chaptername!="":
                                    chapter_id = uuid.uuid1()
                                    mhdict[chapter_id] = [temp_chaptername,chapter_url_lists,temp_mhname]
                                temp_chaptername = path.split('/')[-1]
                                chapter_url_lists = []
                                chapter_url_lists.append(x)
                            else:
                                chapter_url_lists.append(x)
                        except Exception,e:
                            pass
                    else:
                        pass
                else:
                    loadfile.append(os.path.join(path,x))

        except Exception,e:
            print str(e) + path

    chapter_id = uuid.uuid1()
    mhdict[chapter_id] = [temp_chaptername,chapter_url_lists,temp_mhname]
    checkdict(mhdict)


# 改进test3 目前我的格式应该都能够用test3 切割 包含 漫画名称 漫画id 章节名称 章节id 章节页数 漫画第几话 （难点是章节id和漫画id的关联）
# 最后是data 数据 这里面包括
def test3(chaptername,check_str,mhname):
    str_type = check_str.split('.')[-1]
    str_name = chaptername

    pattern = re.compile(u'(.+)\.+(.+)')
    match = pattern.match(check_str)
    str_id =  match.group(1)

    str_nums = str_id.replace(chaptername,'')
    if str_nums.find('num')!=-1:
        str_nums = check_str.split('.')[0].replace('num','')

    return [str_id,str_type,mhname,str_name,str_nums,mhname + '/' + str_name + '/' + check_str]

def test4(chaptername,check_strs,mhname):
    db_list =  [-1 for i in range(len(check_strs))]
    #print check_strs
    for list in check_strs:
        # print chaptername
        #print list
        # print mhname
        temp_list = test3(chaptername,list,mhname)
        db_list[int(temp_list[4])] = temp_list[5]


    temp_strs = ""
    for temp_str in db_list:
        temp_strs  = temp_strs + temp_str + '\n'

    #print db_list[1]

    has_name,has_id = get_mhname_bydb(mhname)
    if(not has_name):
        has_id = uuid.uuid1()
        updata_mhname_todb([[has_id,mhname]])

    chapterid = uuid.uuid1()
    updata_mhdata_todb([[chapterid,has_id,temp_strs,0,len(check_strs),chaptername]])

    #print db_list
    # chapter_id,chapter_type,mhname,chapter_name,chapter_nums,chapter_data_list



def test_uuid():
    print uuid.uuid1()

def checkdict(dict):
    for key in dict:
        test4(dict[key][0],dict[key][1],dict[key][2])

# 漫画名称的数组 同时有个同名的问题
#print get_mhname_bydb("123")

get_chapter_bydb()
#updata_mhname_todb([[3,"钢"]])
#print get_mhname_bydb('钢之炼金术师')

# 漫画章节的数组 包含漫画章节的信息
#updata_mhchapter_todb

