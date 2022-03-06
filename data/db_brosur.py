from firebase_admin import db
import data.model.data_db as model

import conf.conf_db as conf


def drop_table(db_name):
    ref = db.reference(db_name)
    return ref.delete()


def insert_schedule(data: model.DataBrosur):
    ref = db.reference(conf.TABEL_BROSUR)
    # print(str(time_start))
    ref.push({
        'title': data.title,
        'date_create': data.date_create,
        'file_url': data.file_url,
        'size': data.size,
        'hits': data.hits,
    })


def delete_schedule(id_brousr):
    ref = db.reference(conf.TABEL_BROSUR + "/" + id_brousr)
    return ref.delete()


def get_schedule():
    ref = db.reference(conf.TABEL_BROSUR)
    return ref.get()


def get_schedule_id(id_brousr):
    ref = db.reference(conf.TABEL_BROSUR)
    return ref.get()[id_brousr]
