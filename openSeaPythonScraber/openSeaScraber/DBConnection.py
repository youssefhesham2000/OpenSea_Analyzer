import logging
import mysql.connector
from mysql.connector import Error







class connection:
    def __init__(self):
        self.__db_connection = None

    def get_instance(self):
        if self.__db_connection== None:
            self.__db_connection= self.__connect_to_db()
        elif not self.__db_connection.is_connected():
            self.__db_connection = self.__connect_to_db()
        return self.__db_connection

    def __connect_to_db(self):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='nft_opensea',
                                                 user='root',
                                                 password='FUCKYoussef0100')
            if connection.is_connected():
                db_Info = connection.get_server_info()
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                # logging.warning("You're connected to database: ", record)

        except Error as e:
            logging.WARNING("Error while connecting to MySQL" + e.__str__())
        return connection