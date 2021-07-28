import pymysql

def  storeCommentInf(comment):#存储评论
    db = pymysql.connect("localhost", "root", "root", "dfcf")
    cur=db.cursor()
    sql = 'INSERT INTO TB_COMMENT(comment_id,content,like_count,date ,user_id,share_code) values (%(comment_id)s,%(content)s,%(like_count)s,%(date)s,%(user_id)s,%(share_code)s)'
    sql1 = 'SELECT * FROM TB_COMMENT where COMMENT_ID=%s'
    if  cur.execute(sql1,(comment["comment_id"])):#去重
        db.commit()
        cur.close()
        print("评论已经存在")
        db.close()
    else:
        cur.execute(sql, (comment))
        db.commit()
        cur.close()
        db.close()
        print("插入评论成功")


def storeUserInf(user):#储存用户数据
    db = pymysql.connect("localhost", "root", "root", "dfcf")
    cur = db.cursor()
    sql = 'INSERT INTO TB_USER(id,fans) values (%(id)s,%(fans)s)'
    sql1='SELECT * FROM TB_USER where ID=%s'
    if  cur.execute(sql1,(user["id"])):#去重
        db.commit()
        cur.close()
        db.close()
        print("用户已经存在")
    else:
        cur.execute(sql, (user))
        db.commit()
        cur.close()
        db.close()
        print("插入用户成功")

def selectCommentOrderByDate(share_code,method):#查询评论信息
    db = pymysql.connect("localhost", "root", "root", "dfcf")
    cur = db.cursor()
    if  method==0:#按照日期升序
        sql = 'SELECT * FROM TB_COMMENT WHERE SHARE_CODE=%s ORDER BY DATE '
    else:#按照日期降序
        sql='SELECT * FROM TB_COMMENT WHERE SHARE_CODE=%s ORDER  BY DATE DESC '
    cur.execute(sql,(share_code))
    db.commit()
    cur.close()
    return  cur.fetchall()

def selectFansByUserId(userId):#查询用户粉丝数
    db = pymysql.connect("localhost", "root", "root", "dfcf")
    cur = db.cursor()
    sql = 'SELECT FANS FROM TB_USER where ID=%s'
    cur.execute(sql,userId)
    db.commit()
    cur.close()
    return cur.fetchall()