import pymysql

class Database():
    DB_NAME = "Restful_Challenge"
    TABLE_NAME = "People"
    def __init__(self):
        pass


    @staticmethod
    def create_base_db_setup(con, db_name=DB_NAME, table_name=TABLE_NAME, overwrite=True):
        """
        Create database and table if not already exist
        :param con:
        :param db_name: string, name used for database
        :param table_name: string, name used for table
        :param overwrite: bool, defatul False, if True, will recreate the existing database and table
        :return: None
        """
        over_write_db = "".join(["DROP DATABASE IF EXISTS ", db_name])
        create_db = "".join(["CREATE DATABASE IF NOT EXISTS ", db_name])
        use_db = "".join(["USE ", db_name])
        create_table = "".join(["CREATE TABLE IF NOT EXISTS ", table_name, "(",
                                "id INT NOT NULL AUTO_INCREMENT,",
                                "firstName VARCHAR(255) DEFAULT NULL,",
                                "lastName VARCHAR(255) DEFAULT NULL,",
                                "age int DEFAULT NULL,",
                                "gitHubAcct VARCHAR(255) DEFAULT NULL,",
                                "dateThirdGradeGra DATETIME DEFAULT NULL,"
                                "created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),",
                                "PRIMARY KEY (id),",
                                "INDEX age_index USING BTREE (created_at, age),",
                                "INDEX last_name USING BTREE (lastName, created_at),",
                                "INDEX created_time USING BTREE(created_at))"])
        if overwrite:
            DataLoader.execute_query_no_res(con, over_write_db, {})
        DataLoader.execute_query_no_res(con, create_db, {})
        DataLoader.execute_query_no_res(con, use_db, {})
        DataLoader.execute_query_no_res(con, create_table, {})







class DataLoader():

    def __init__(self):
        pass

    @staticmethod
    def buffered_data_loader_dict(sql, con, paraList):
        """
        return a list of dictionary key as the column header, recommended for small result set passing
        :param sql: sql stmt passed in
        :param con: pymysql connection
        :param paraList: dict object, list of parameter included in query
        :return: list of dictionary
        """
        cursor = con.cursor()
        cursor.execute(sql, paraList)
        columns = cursor.description
        data_set = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        cursor.close
        return data_set


    @staticmethod
    def execute_query_no_res(con, sql, para_dict):
        """
        execute query without a result set
        :param con: pymysql connection object
        :param sql: string, sql stmt to be executed
        :param para_dict: dict, parameter included in sql stmt
        :return:
        """
        cursor = con.cursor()
        cursor.execute(sql, para_dict)
        cursor.close()

    @staticmethod
    def execute_query_res(con, sql, para_dict):
        """
        execute query without a result set
        :param con: pymysql connection object
        :param sql: string, sql stmt to be executed
        :param para_dict: dict, parameter included in sql stmt
        :return:
        """
        cursor = con.cursor()
        cursor.execute(sql, para_dict)
        result = cursor.fetchall()
        cursor.close()
        return result


if __name__ == '__main__':
    pass