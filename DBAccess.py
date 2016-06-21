# import mysql.connector as mariadb     # mysqldb   # MySQLdb
# import mysqldb
import mysql.connector
import datetime
import CONS


def bld_sql(start_date, end_date, event_title):
    where_str = None
    if start_date and end_date:
        where_str = "event_date >= start_date and event_date <= end_date"
    elif start_date and not end_date:
        where_str = "event_date = '{}'".format(start_date)
    elif end_date:
        where_str = "event_date = '{}'".format(end_date)
    else:
        where_str = "event_date > ' '"

    if event_title:
        where_str += " and event_title = '{}'".format(event_title)
 
    sqlx_count = "select count(*) from events where ({})".format(where_str)
    sqlx = "select * from events where ({})".format(where_str)
    return [sqlx, sqlx_count]


def bld_add_sql(title1, date1, desc1):
    insert_str = "insert tg1_events (event_title, event_date, event_desc) \
        values( '{}' '{}' '{}'".format(title1, date1, desc1)

    return insert_str


def add_event(sqlx):

    ap = db_create_connection()
    rmsg = ""
    try:
        db_exec_cur(ap.cur, sqlx, "desc")

    except Exception as e:
        rmsg =  ["error", "error adding event"]

    db_close_con(ap)
    if not rmsg:
        rmsg = ["success", "event added succesfully"]
    return rmsg


def get_events(sqlx_count, sqlx):

    ap = db_create_connection()

    try:
        obj_count = {"count": -1}
        rslt = db_exec_cur(ap.cur, sqlx_count, "no_desc")
        for t in rslt[0]:
            obj_count["count"] = t[0]
        
        db_exec_cur(ap.cur, sqlx, "desc")
    except Exception as e:
        raise "error reading the database"

    rslt_list = convert_tuple(ap.result, obj_count)
    db_close_con(ap)
    return rslt_list


def convert_tuple(ap, obj_count):
    a_result = [obj_count]
    for t in ap.result:
        cnt1 = -1
        uj = {}
        
        for fld1 in ap.desc:
            cnt1 += 1
            uj[fld1] = t[cnt1]
        a_result.append(uj)

    return ['ok', a_result]
    

def db_create_connection():
    ap = DBAccess()
    cnx = mysql.connector.connect(user='scott', password='tiger',
                                  host='127.0.0.1',
                                  database='employees')

    ap.con = mysql.connector.connect(user=CONS.USER, password=CONS.PW,
                                     database=CONS.DB_NAME, host=CONS.HOST)
    ap.cur = ap.con.cursor()
    return ap


def db_close_con(ap):
    ap.con.close()


def db_exec_cur(ap):
    ap.cursor.execute(ap.sqlx)
    ap.result = ap.cur.fetchall()
    ap.desc = [x[0].lower for x in ap.cur.description] 
    return ap


class DBAccess(object):
    con = None
    cur = None
    result = None
    desc = None
