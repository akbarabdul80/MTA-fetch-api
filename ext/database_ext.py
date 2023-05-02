import data.model.data_db as model

import conf.conf_db as conf
import sqlite3


def insert_data_db(data: model.DataBrosur):
    conn = sqlite3.connect('database/' + conf.DB_NAME)

    query = 'INSERT INTO BROSUR (TITLE,DATE_CREATE,FILE_URL,SIZE,HITS) \
      VALUES ("' + data.title + '", "' + data.date_create + '", "' + data.file_url + '", "' + data.size + '", "' + data.hits + '")'

    print(query)
    conn.execute(query)
    conn.commit()
    conn.close()


def get_data_db():
    conn = sqlite3.connect('database/' + conf.DB_NAME)

    query = 'SELECT * FROM BROSUR'
    cursor = conn.execute(query)
    data = []
    for row in cursor:
        data.append(model.DataBrosur(row[0], row[1], row[2], row[3], row[4]))
    conn.close()
    return data


def get_last_brosur_by_date():
    conn = sqlite3.connect('database/' + conf.DB_NAME)

    query = 'SELECT * FROM BROSUR ORDER BY DATE_CREATE DESC LIMIT 1'
    cursor = conn.execute(query)
    data = []
    for row in cursor:
        data.append(model.DataBrosur(row[0], row[1], row[2], row[3], row[4]))
    conn.close()
    if len(data) == 0:
        return None
    return data[0]
