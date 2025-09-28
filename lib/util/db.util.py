#@File   : .py
#@Time   : 2025/9/23 13:57
#@Author : 
#@Software: PyCharm
import pymysql

import os

from lib.util.config_loader import load_yaml


class DBUtils:
    def __init__(self, db_alias="default"):
        # 读取配置文件
        config_path = os.path.join(os.path.dirname(__file__), "..", "conf", "db_config.yaml")

        conf = load_yaml(config_path)[db_alias]

        self.conn = pymysql.connect(
            host=conf["host"],
            port=conf["port"],
            user=conf["user"],
            password=conf["password"],
            database=conf["database"],
            charset="utf8mb4"
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def query_one(self, sql):
        """查询单条"""
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def query_all(self, sql):
        """查询多条"""
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def execute(self, sql):
        """增删改"""
        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
