#!/usr/bin/python2.7
import MySQLdb
import datetime
import CONS


def bld_sql(start_date, end_date, event_title):
    where_str = ""
    if start_date and end_date:
        where_str = "event_date >= start_date and event_date <= end_date"
    elif start_date and not end_date:
        where_str = "event_date = '{}'".format(start_date)
    elif end_date:
        where_str = "event_date = '{}'".format(end_date)
    else:
        where_str = "event_date > ' '"

    if event_title:
        where_str += " and event_title = '{}'".format(event_date) 
 
    sqlx_count = "select count(*) from events where ({})".format(where_str)
    sqlx = "select * from events where ({}).format(where_str)
    return [sqlx, sqlx_count]

def bld_add_sql(title1, date1, desc1):
    insert_str = "insert tg1_events (event_title, event_date, event_desc) \
        values( '{}' '{}' '{}'".format(title1, date1, desc1)

    return inser_sql 


def get_events(sqlx_count, sqlx):

    ap = db_create_connection()
    ap.cur = db_create_cur(ap)
    
    try:
        obj_count = {"count": -1}
        rslt = ap_exec_cur(ap.cur, sqlx_count, "no_desc")
        for t in rslt[0]:
            obj_count["count"] = t[0]
        
        ap_exec_cur(ap.cur, sqlx, "desc")    
    execpt Exception as e:
        raise "error reading the database"

    rslt_list = convert_tuple(ap.result, obj_count)
    ap_close_con(ap)
    return rslt_list


def convert_tuple(ap, obj_count):
    a_result[0] = obj_count
    for t in ap.result:
        cnt1 = -1
        uj = {}
        
        for fld1 in ap.desc:
            cnt1 += 1
            uj[fld1] = t[cnt1]
        a_result.append(uj)

    return ['ok', a_result]
    


def db_create_connection():
    ap = dbaccess()    
    ap.con = MySQLdb.connect(CONS.HOST_NAME, CONS.USER, CONS.PW, CONS.DB_NAME)
    ap.cur = ap.con.cursor
    return ap

def db_close_con(ap):
    ap.con.close()

def db_fetchall(ap):
    ap.cursor.execute(ap.sqlx)
    ap.result = ap.cur.fetchall()
    ap.desc = [x[0].lower for x in ap.cur.description] 
    return ap


class dbaccess(object):
    con = None
    cur = None
    result = None
    desc = None
