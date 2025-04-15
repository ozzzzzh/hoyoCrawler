import mysql.connector
from datetime import datetime

def stConnectDatabase(pcHost, pcUser, pcPassword, pcDatabase): # localhost root ptr_null miyoushe_strategy
    conn = mysql.connector.connect(
        host=pcHost,
        user=pcUser,
        password=pcPassword,
        database=pcDatabase
    )    
    return conn

def vCloseConnection(pstCursor, pstConn):
    pstCursor.close()
    pstConn.close()

def vCreateArticlesTable(pstConn):
    pstCursor = pstConn.cursor()
    pstCursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url TEXT,
            author_name TEXT,
            author_avatar TEXT,
            content LONGTEXT,
            video_src TEXT,
            video_cover TEXT,
            can_repost INT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

def iInsertIntoArticles(pstCursor, pstConn, pcUrl, pcAuthorName, pcAuthorAvatar, pcContent, pcVideoSrc, pcVideoCover, pcCanReport)
    pstCursor.execute('''
        INSERT INTO articles (url, author_name, author_avatar, content, video_src, video_cover, can_repost, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (pcUrl, pcAuthorName, pcAuthorAvatar, pcContent, pcVideoSrc, pcVideoCover, pcCanReport, datetime.now()))
    pstConn.commit()  
    # use try and catch Exception to find out whether problem was occur but not the return value of cursor.execute 


def pcSelectFromArticles(pstCursor, iArticleId):
    pstCursor.execute("SELECT * FROM users WHERE id = %s", (iArticleId,))
    return pstCursor.fetchone()


def pcExecuteSql(pstCursor, pcSql, pcParams=None, bFetch=False):
    try:
        pstCursor.execute(pcSql, pcParams or [])
        if bFetch:
            return pstCursor.fetchall()
        else:
            return pstCursor.rowcount
    except Exception as e:
        print("SQL执行失败：", e)
        return None