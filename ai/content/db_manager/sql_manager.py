from content.db import mysql_db

def insert_batch_hot_words(words):
    # data = [(1,1,'hello',10,0.32,'post_hot'),(1,1,'hello',10,0.32,'post_hot')]
    mysql = mysql_db.MYSQL()
    sql = "INSERT INTO `polygon_lens_hot_words_score` (`profileid`,`pubid`,`word`,`count`,`rank`,`type`) VALUES (%s, %s, %s, %s, %s, %s)"
    mysql.insert_batch(sql,words)
    print('insert done')


def get_comments(limit=0):
    print('read sql')
    pdb = mysql_db.PandasDB()
    sql = 'select PLP.profileid, PLP.profileidPointed,PLP.pubidPointed, PLC.description,PLC.content from ' \
          'polygon_lens_publication as PLP left join polygon_lens_content as PLC '\
          'on PLP.profileid=PLC.profileid and PLP.pubid=PLC.pubid ' \
          'where PLP.type="Comment"'
    if limit>0:
        sql+=' limit {}'.format(limit)
    a = pdb.read_sql(sql)
    pdb.close()
    return a

def get_posts(limit=0):
    print('read sql')
    pdb = mysql_db.PandasDB()
    sql = 'select PLP.profileid,PLP.pubid, PLC.description,PLC.content from ' \
          'polygon_lens_publication as PLP right join polygon_lens_content as PLC '\
          'on PLP.profileid=PLC.profileid and PLP.pubid=PLC.pubid ' \
          'where PLP.type="Post"'
    if limit>0:
        sql+=' limit {}'.format(limit)
    a = pdb.read_sql(sql)
    pdb.close()
    return a

def get_posts_try(limit=0):
    print('read sql')
    pdb = mysql_db.PandasDB()
    sql = 'select PLP.profileid,PLP.pubid, PLC.description,PLC.content from ' \
          'polygon_lens_publication as PLP right join polygon_lens_content as PLC '\
          'on PLP.profileid=PLC.profileid and PLP.pubid=PLC.pubid ' \
          'where PLP.type="Post" and PLP.profileid = 114'
    if limit>0:
        sql+=' limit {}'.format(limit)
    a = pdb.read_sql(sql)
    pdb.close()
    return a

