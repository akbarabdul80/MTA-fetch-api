from typing import List

from firebase_admin import db
import data.model.data_db as model

import conf.conf_db as conf
import ext.database_ext as db_ext


def drop_table(db_name):
    ref = db.reference(db_name)
    return ref.delete()


def insert_data(data: model.DataBrosur):
    print("insert data to db :" + data.title + " -- " + data.date_create)
    db_ext.insert_data_db(data)
    ref = db.reference(conf.TABEL_BROSUR)
    ref.push({
        'title': data.title,
        'date_create': data.date_create,
        'file_url': data.file_url,
        'size': data.size,
        'hits': data.hits,
    })


def insert_data_list(data: List[model.DataBrosur]):
    for item in data:
        insert_data(item)


def delete_schedule(id_brousr):
    ref = db.reference(conf.TABEL_BROSUR + "/" + id_brousr)
    return ref.delete()


def get_schedule():
    ref = db.reference(conf.TABEL_BROSUR)
    return ref.get()


def get_schedule_id(id_brousr):
    ref = db.reference(conf.TABEL_BROSUR)
    return ref.get()[id_brousr]
