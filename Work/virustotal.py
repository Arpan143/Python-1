# -*- coding: utf-8 -*-

import argparse
import hashlib
import os
import sqlite3
import requests
import time


def sqlite_create(): # 判断;创建数据库和表
    conn = sqlite3.connect('virustotal.db')
    sql = '''CREATE TABLE IF NOT EXISTS "virustotal" (
        "ID"  INTEGER NOT NULL,
        "MD5"  TEXT NOT NULL,
        "FileName"  TEXT,
        "Submit_time"  TEXT,
        "Scan_date"  TEXT,
        "File_size"  TEXT,
        "Sha1"  TEXT,
        "Sha256"  TEXT,
        "Scan_id"  TEXT,
        "Resource"  TEXT,
        "Response_code"  TEXT,
        "Permalink"  TEXT,
        "Verbose_msg"  TEXT,
        "Positives"  TEXT,
        "Total"  TEXT,
        "Result"  TEXT,
        "Adaware"  TEXT,
        "Aegislab"  TEXT,
        "Agnitum"  TEXT,
        "Ahnlabv3"  TEXT,
        "AntiVir"  TEXT,
        "Antiyavl"  TEXT,
        "Avast"  TEXT,
        "Avg"  TEXT,
        "Baiduinternational"  TEXT,
        "Bitdefender"  TEXT,
        "Bkav"  TEXT,
        "Bytehero"  TEXT,
        "Catquickheal"  TEXT,
        "Clamav"  TEXT,
        "Cmc"  TEXT,
        "Commtouch"  TEXT,
        "Comodo"  TEXT,
        "DrWeb"  TEXT,
        "Emsisoft"  TEXT,
        "Esetnod32"  TEXT,
        "Fortinet"  TEXT,
        "Fprot"  TEXT,
        "Fsecure"  TEXT,
        "Gdata"  TEXT,
        "Ikarus"  TEXT,
        "Jiangmin"  TEXT,
        "K7antivirus"  TEXT,
        "K7gw"  TEXT,
        "Kaspersky"  TEXT,
        "Kingsoft"  TEXT,
        "Malwarebytes"  TEXT,
        "Mcafee"  TEXT,
        "Mcafeegwedition"  TEXT,
        "Microsoft"  TEXT,
        "Microworldescan"  TEXT,
        "Nanoantivirus"  TEXT,
        "Norman"  TEXT,
        "Nprotect"  TEXT,
        "Panda"  TEXT,
        "Qihoo360"  TEXT,
        "Rising"  TEXT,
        "Sophos"  TEXT,
        "Superantispyware"  TEXT,
        "Symantec"  TEXT,
        "Tencent"  TEXT,
        "Thehacker"  TEXT,
        "Totaldefense"  TEXT,
        "Trendmicro"  TEXT,
        "Trendmicrohousecall"  TEXT,
        "Vba32"  TEXT,
        "Vipre"  TEXT,
        "Virobot"  TEXT,
        "Zillya"  TEXT,
        PRIMARY KEY ("MD5" ASC)
        );''' # 创建av表
    conn.execute(sql)
    sql = '''CREATE TABLE IF NOT EXISTS "no_virustotal" (
        "id"  INTEGER NOT NULL,
        "MD5"  TEXT NOT NULL,
        "FileName"  TEXT,
        "Submit_time"  TEXT,
        "File_size"  TEXT,
        "Response_code"  TEXT,
        "Resource"  TEXT,
        "Verbose_msg"  TEXT,
        PRIMARY KEY ("MD5" ASC)
        );''' # 创建no-av表
    conn.execute(sql)
    conn.commit()
    sql = 'SELECT MAX(id) from virustotal;'
    cur = conn.execute(sql)
    if cur.fetchone()[0] is None:
        sql = '''insert into virustotal (id,md5) values (0,'Sample');'''
        conn.execute(sql)
    sql = 'SELECT MAX(id) from no_virustotal;'
    cur = conn.execute(sql)
    if cur.fetchone()[0] is None:
        sql = '''insert into no_virustotal (id,md5) values (0,'Sample');'''
        conn.execute(sql)
    conn.commit()
    return conn


def get_md5(): # 获取sample文件夹下所有文件的MD5值
    file_info = {}
    # file_md5_list = []
    for root, root2, filename in os.walk(os.getcwd() + '\sample'):
        for i in filename:
            file_size = os.path.getsize(os.path.join(root, i))
            with open(os.path.join(root, i), 'rb') as f:
                file_read = f.read()
                md5_str = hashlib.md5(file_read).hexdigest()
                sha1_str = hashlib.sha1(file_read).hexdigest()
                sha256_str = hashlib.sha256(file_read).hexdigest()
                file_info[md5_str] = {u'file_name': i, u'Submit_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                      u'file_size': file_size, u'Sha1': sha1_str, u'Sha25': sha256_str}
    # print file_info
    return file_info


def db_query(conn, file_info): # 根据文件MD5查询数据库,存在则不进入后续操作
    result_md5_db = []
    for i in file_info:
        sql = "SELECT MD5 FROM virustotal where MD5 ='" + i + "';"
        sql_no = "SELECT MD5 FROM no_virustotal where MD5 ='" + i + "';"
        cur = conn.execute(sql)
        cur_no = conn.execute(sql_no)
        result = cur.fetchone()
        result_no = cur_no.fetchone()
        if result is not None:
            result_md5_db.append(result[0])
        if result_no is not None:
            result_md5_db.append(result_no[0])
    for i in result_md5_db:
        del file_info[i]
    print "Select over!"
    # print file_info
    return file_info


def vt_sample_query_into_db(file_info, vt_apikey): # 根据文件MD5检测(virustotal)
    del_file_info_list = []
    no_virustotal_db = {}
    url = "https://www.virustotal.com/vtapi/v2/file/report"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' +
                             ' Chrome/55.0.2883.75 Safari/537.36'}
    for i in file_info:
        parameters = {"resource": i, "apikey": vt_apikey}
        response = requests.get(url, params=parameters, headers=headers, timeout=300)
        try:
            json_response = response.json()
            if json_response['response_code'] == 1:
                # file_info[i],  = list_append(file_info[i], json_response)
                del json_response['md5']
                file_info[i] = dict(file_info[i], **json_response)
            elif json_response['response_code'] == 0:
                del_file_info_list.append(i)
                no_virustotal_db[i] = dict(file_info[i], **json_response)
        except:
            print i
            del_file_info_list.append(i)
        time.sleep(15)
    for i in del_file_info_list:
        del file_info[i]
    print 'Url over'
    return file_info, no_virustotal_db


def update_av_scan(conn, md5_str, av_result): # 用于更新数据库中扫描引擎字段
    av_list = ["Ad-Aware", "AegisLab", "Agnitum", "AhnLab-V3", "AntiVir", "Antiy-AVL", "Avast", "AVG",
               "Baidu-International", "BitDefender", "Bkav", "ByteHero", "CAT-QuickHeal", "ClamAV", "CMC", "Commtouch",
               "Comodo", "DrWeb", "Emsisoft", "ESET-NOD32", "Fortinet", "F-Prot", "F-Secure", "GData", "Ikarus",
               "Jiangmin", "K7AntiVirus", "K7GW", "Kaspersky", "Kingsoft", "Malwarebytes", "McAfee",
               "McAfee-GW-Edition", "Microsoft", "MicroWorld-eScan", "NANO-Antivirus", "Norman", "nProtect", "Panda",
               "Qihoo-360", "Rising", "Sophos", "SUPERAntiSpyware", "Symantec", "Tencent", "TheHacker", "TotalDefense",
               "TrendMicro", "TrendMicro-HouseCall", "VBA32", "VIPRE", "ViRobot", "Zillya"]
    av_dict = {
        "Ad-Aware": "Adaware",
        "AegisLab": "Aegislab",
        "Agnitum": "Agnitum",
        "AhnLab-V3": "Ahnlabv3",
        "AntiVir": "Antivir",
        "Antiy-AVL": "Antiyavl",
        "Avast": "Avast",
        "AVG": "Avg",
        "Baidu-International": "Baiduinternational",
        "BitDefender": "Bitdefender",
        "Bkav": "Bkav",
        "ByteHero": "Bytehero",
        "CAT-QuickHeal": "Catquickheal",
        "ClamAV": "Clamav",
        "CMC": "Cmc",
        "Commtouch": "Commtouch",
        "Comodo": "Comodo",
        "DrWeb": "Drweb",
        "Emsisoft": "Emsisoft",
        "ESET-NOD32": "Esetnod32",
        "Fortinet": "Fortinet",
        "F-Prot": "Fprot",
        "F-Secure": "Fsecure",
        "GData": "Gdata",
        "Ikarus": "Ikarus",
        "Jiangmin": "Jiangmin",
        "K7AntiVirus": "K7antivirus",
        "K7GW": "K7gw",
        "Kaspersky": "Kaspersky",
        "Kingsoft": "Kingsoft",
        "Malwarebytes": "Malwarebytes",
        "McAfee": "Mcafee",
        "McAfee-GW-Edition": "Mcafeegwedition",
        "Microsoft": "Microsoft",
        "MicroWorld-eScan": "Microworldescan",
        "NANO-Antivirus": "Nanoantivirus",
        "Norman": "Norman",
        "nProtect": "Nprotect",
        "Panda": "Panda",
        "Qihoo-360": "Qihoo360",
        "Rising": "Rising",
        "Sophos": "Sophos",
        "SUPERAntiSpyware": "Superantispyware",
        "Symantec": "Symantec",
        "Tencent": "Tencent",
        "TheHacker": "Thehacker",
        "TotalDefense": "Totaldefense",
        "TrendMicro": "Trendmicro",
        "TrendMicro-HouseCall": "Trendmicrohousecall",
        "VBA32": "Vba32",
        "VIPRE": "Vipre",
        "ViRobot": "Virobot",
        "Zillya": "Zillya"
    }
    for av in av_list:
        try:
            update_sql = "UPDATE virustotal SET '%s'='%s' WHERE MD5='%s';" % (av_dict[av],
                                                                av_result[md5_str]['scans'][av]['result'], md5_str)
            cur = conn.execute(update_sql)
            conn.commit()
        except:
            continue
    # scan_result = {} #将各个扫描引擎的结果加到av_result中
    # for i in av_result:
    #     for y in av_result[i]['scans']:
    #         scan_result[y] = av_result[i]['scans'][y]['result']
    #         av_result[i] = dict(av_result[i], **scan_result)
    # return av_result


def insert_av_scan_db(conn, av_scan_result, md5_str): # 以扫描引擎为表名，添加各个表
    for i in av_scan_result:
        try:
            create_sql = "CREATE TABLE IF NOT EXISTS '" + i.encode('utf-8') + "'('MD5' Text PRIMARY KEY," \
                                                "'detected' Text,'version' Text,'result' Text,'update' Text);"
            cur = conn.execute(create_sql)
            conn.commit()
        except:
            print "Table", i, "already exists!"
        insert_sql = "INSERT INTO '" + i + "' VALUES" + " ('%s','%s', '%s', '%s', '%s');" % (md5_str,
                            av_scan_result[i]['detected'], av_scan_result[i]['version'], av_scan_result[i]['result'],
                            av_scan_result[i]['update'])
        cur = conn.execute(insert_sql)
        conn.commit()


def insert_av_info_db(conn, av_result): # 插入病毒信息
    if av_result:
        sql = 'SELECT max(id) FROM virustotal'
        cur = conn.execute(sql)
        now_id = cur.fetchone()[0]
        for i in av_result:
            now_id += 1
            sql = "INSERT INTO virustotal VALUES (%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" \
                  ",'%s','%s','None','None','None','None','None','None','None','None','None','None','None','None'," \
                  "'None','None','None','None','None','None','None','None','None','None','None','None','None','None'," \
                  "'None','None','None','None','None','None','None','None','None','None','None','None','None','None'," \
                  "'None','None','None','None','None','None','None','None','None','None','None','None','None');"\
                  % (now_id, i, av_result[i]['file_name'], av_result[i]['Submit_time'], av_result[i]['scan_date'],
                     av_result[i]['file_size'], av_result[i]['sha1'], av_result[i]['sha256'], av_result[i]['scan_id'],
                     av_result[i]['resource'], av_result[i]['response_code'], av_result[i]['permalink'],
                     av_result[i]['verbose_msg'], av_result[i]['positives'], av_result[i]['total'],
                     round(av_result[i]['positives']/float(av_result[i]['total']), 2))
            conn.execute(sql)
            conn.commit()
            update_av_scan(conn, i, av_result)
            # insert_av_scan_db(conn, av_result[i]['scans'], i) #创建各个扫描引擎结果表
        conn.commit()
        print "Insert av over!"


def insert_nvirus_db(conn, nvirus_result): # 插入非病毒信息
    if nvirus_result:
        sql_all = ''
        sql = 'SELECT max(id) FROM no_virustotal'
        cur = conn.execute(sql)
        now_id = cur.fetchone()[0]
        for i in nvirus_result:
            now_id += 1
            sql = "INSERT INTO no_virustotal VALUES (%d,'%s','%s','%s','%s','%s','%s','%s');" % (now_id, i,
                    nvirus_result[i]['file_name'], nvirus_result[i]['Submit_time'], nvirus_result[i]['file_size'],
                    nvirus_result[i]['response_code'], nvirus_result[i]['resource'], nvirus_result[i]['verbose_msg'])
            sql_all += sql
        cur.executescript(sql_all)
        conn.commit()
        print 'Select over'


if __name__ == '__main__':
    file_info = get_md5()
    conn = sqlite_create()
    print "Connection Success!"
    result_file_info = db_query(conn, file_info)
    parser = argparse.ArgumentParser(description='Virustotal')
    parser.add_argument('-a', dest='Virustotal_API_Key', required=True, help='Virustotal API Key')
    args = parser.parse_args()
    if result_file_info:
        # apikey_list = []
        vt_apikey = args.Virustotal_API_Key
        av_result, nvirus_result = vt_sample_query_into_db(result_file_info, vt_apikey)
        insert_av_info_db(conn, av_result)
        insert_nvirus_db(conn, nvirus_result)
    conn.close()
    print 'Done'
    # search_number = 1
    # api_number = 0
    # while True:
    #     if search_number <= 3000:
    #         vt_apikey = apikey_list[api_number]
    #         av_result, nvirus_result = vt_sample_query_into_db(result_file_md5_list, vt_apikey)
    #         search_number += 1
    #     else:
    #         api_number += 1
    #         search_number = 1