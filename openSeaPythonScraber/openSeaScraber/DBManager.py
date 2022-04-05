import logging
from . import DBConnection
import mysql.connector

def insert_new_instance_data( instance):
    if instance is None:
        return
    id = instance.get_id()
    insert_nft_info(id, instance.get_name(), instance.get_favourites(), instance.get_highest())
    logging.warning(len(instance.offers))
    if len(instance.offers) != 0:
        __insert_offers(id, instance.offers)
    logging.warning(len(instance.events))
    if len(instance.events) != 0:
        __insert_events(id, instance.events)


def __open_connection():
    return DBConnection.connection().get_instance()


def __close(connection, cursor):
    if connection.is_connected():
        cursor.close()
        connection.close()


def get_url_by_id(id):
    my_sql_retrieve_query = """select url.URL from url where url.ID = %s;"""
    conditions = (id,)
    return __retrieve_query(my_sql_retrieve_query,conditions)


def get_nft_info_by_id(id):
    my_sql_retrieve_query = """select * from nft where nft.ID = %s;"""
    conditions = (id,)
    return __retrieve_query(my_sql_retrieve_query, conditions)


def get_offers_by_id(id):
    my_sql_retrieve_query = """select * from offer where offer.ID = %s;"""
    conditions = (id,)
    return __retrieve_query(my_sql_retrieve_query, conditions)


def get_event_by_id(id):
    my_sql_retrieve_query = """select * from event where event.ID = %s;"""
    conditions = (id,)
    return __retrieve_query(my_sql_retrieve_query, conditions)


def delete_events_by_id(id):
    my_sql_delete_query="""DELETE from event where ID=%s"""
    condition = (id,)
    __delete_query(my_sql_delete_query, condition)


def delete_url_by_id(id):
    my_sql_delete_query="""DELETE from url where ID=%s"""
    condition = (id,)
    __delete_query(my_sql_delete_query, condition)


def delete_nft_by_id(id):
    my_sql_delete_query="""DELETE from nft where ID=%s"""
    condition = (id,)
    __delete_query(my_sql_delete_query, condition)


def delete_offer_by_id(id):
    my_sql_delete_query="""DELETE from offer where ID=%s"""
    condition = (id,)
    __delete_query(my_sql_delete_query, condition)


def __delete_query(my_sql_delete_query, conditions):
    try:
        connection = __open_connection()
        cursor = connection.cursor()
        cursor.execute(my_sql_delete_query, conditions)
        records = cursor.fetchall()
    except mysql.connector.Error as error:
        logging.warning(error)
    finally:
        __close(connection, cursor)
        return records

def __retrieve_query(my_sql_retrieve_query,conditions):
    try:
        connection = __open_connection()
        cursor = connection.cursor()
        cursor.execute(my_sql_retrieve_query, conditions)
        records = cursor.fetchall()
    except mysql.connector.Error as error:
        logging.warning(error)
    finally:
        __close(connection, cursor)
        return records


def __update_query(my_sql_update_query, conditions,new_record):
    try:
        connection = __open_connection()
        cursor = connection.cursor()
        cursor.execute(my_sql_update_query, conditions)
        connection.commit()
    except mysql.connector.Error as error:
        logging.warning(error)
    finally:
        __close(connection, cursor)


def get_url_by_version(version):
    my_sql_retrieve_query = """select * from url where url.version = %s"""
    conditions = (version,)
    return __retrieve_query(my_sql_retrieve_query, conditions)


def insert_new_urls(urls):
    mysql_insert_query = """INSERT INTO url (URL,version) values (%s,%s);"""
    urls = list(set(urls))
    records = [(url, 0) for url in urls if not __is_url_exist(url)]
    __insert_many(mysql_insert_query, records)

def __is_url_exist(url):
    my_sql_retrieve_query = """select URL from url where url.URL = %s"""
    records = __retrieve_query(my_sql_retrieve_query, (url,))
    return not len(records) == 0


def __insert_offers(id, offers):
    my_sql_insert_query = """INSERT INTO offer (ID,offer_price) values (%s,%s);"""
    records = [(id, offer) for offer in offers]
    __insert_many(my_sql_insert_query, records)


def insert_offer(id,price):
    my_sql_insert_query = """INSERT INTO offer (ID,offer_price) values (%s,%s);"""
    record = (id, price)
    insert(my_sql_insert_query, record)


def insert_nft_info(id, name, favourite, highest_bid):
    mysql_insert_query = """ INSERT INTO nft values(%s,%s,%s,%s)"""
    record = (id, name, favourite, highest_bid)
    insert(mysql_insert_query, record)


def __insert_events(id, events):
    records = [(id, event.get_event_name(), event.get_event_date(), None, None) for event in events if not event.has_price_info()]
    mysql_insert_query = """ INSERT INTO event values(%s,%s,%s,%s,%s)"""
    __insert_many(mysql_insert_query, records)
    records_with_price = [(id, event.get_event_name(), event.get_event_date(), event.get_price(), event.get_purchase_type()) for event in events if event.has_price_info()]
    if(len(records_with_price) != 0):
        __insert_many(mysql_insert_query, records_with_price)


def insert_event(id, name, date):
    record = (id, name, date)
    mysql_insert_query = """ INSERT INTO event values(%s,%s,%s)"""
    insert(mysql_insert_query, record)


def insert(my_sql_insert_query,record):
    try:
        connection = __open_connection()
        cursor = connection.cursor()
        cursor.execute(my_sql_insert_query, record)
        connection.commit()
    except mysql.connector.Error as error:
        logging.warning(error)
        logging.warning("insert one record exception")
    finally:
        __close(connection, cursor)


def __insert_many(my_sql_insert_query, records):
    try:
        connection = __open_connection()
        cursor = connection.cursor()
        cursor.executemany(my_sql_insert_query, records)
        connection.commit()
    except mysql.connector.Error as error:
        logging.warning(error)
        logging.warning("insert many exception")
    finally:
        __close(connection, cursor)