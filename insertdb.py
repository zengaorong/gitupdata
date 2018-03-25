#coding=utf-8
import sys
import MySQLdb
import os
import re

reload(sys)
sys.setdefaultencoding('utf-8')
dataname = "leodb"

def updata_mhdata_todb():
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
    sqli = "insert into mhname(id,mhname)values(%s,%s)"
    cur.executemany(sqli,[[2,"123"]])
    conn.commit()
    conn.close()

def getDate():
    loadfile = [u'./app/static']
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
                        try:
                            pass
                        except Exception,e:
                            pass
                        templist = test3(path.split('\\')[-1],x,path.split('\\')[-2])
                        mydict[templist[0]] = templist
                else:
                    loadfile.append(os.path.join(path,x))

        except Exception,e:
            print str(e) + path


    #InsertData('mhpic',mydict)
    url_list = []
    for key in mydict:
        print mydict[key][0]
        print mydict[key][1]
        print mydict[key][2]
        print mydict[key][3]
        print mydict[key][4]
        print mydict[key][5]
        break
        mylist.append(mydict[key])
        url_list.append(mydict[key][5].replace('./app/static/',""))

    return url_list

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

getDate()