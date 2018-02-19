import csv
from database import DataLoader
from database import Database
from datetime import datetime
import pymysql


#########################exception classes#####################################################
class InvalidInputException(Exception):
    def __init__(self, field_name, value, intended=None):
        self.field_name = field_name
        self.value = value
        self.intended = intended

    def __str__(self):
        return repr("".join(["Field : ", self.field_name," Needs to be a type of ",self.intended," but found ",self.value]))

class RequiredKeyNotFound(Exception):
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return repr("".join(["This key is required but not found in constructor: ", self.key]))

class MissingRequiredFieldValue(Exception):
    def __init__(self, field_name):
        self.field_name = field_name

    def __str__(self):
        return " ".join(["Field:",str(field_name),"is a required field but left empty or not provided"])
#########################end exception class###################################################

class People():

    numeric_key_set = ['ID', 'Age']
    date_format_dict = {'Date of 3rd Grade Graduation': '%m/%d/%y'}
    profile_key = {'Age', 'Date of 3rd Grade Graduation', 'First','Last','GithubAcct'}
    required_key_set = []
    def __init__(self, profile=None, id=None, first_name=None,
                       last_name=None, age=None, github_acct=None,
                       date_3rd_gra=None):
        if profile == None:
            self.profile = {
                'ID' : id,
                'First' : first_name,
                'Last' : last_name,
                'Age' : age,
                'GithubAcct':github_acct,
                'Date of 3rd Grade Graduation' : date_3rd_gra
            }
        else:
            self.profile = profile
        self.__convert_date()


    def __str__(self):
        return ", ".join([":".join([key, str(value)]) for key, value in self.profile.items()])

    def is_data_valid(self):
        for key in People.numeric_key_set:
            if key in self.profile and self.profile[key] != None and not self.profile[key].isdigit():
                return False, "".join(["Field : ", key," Needs to be a type of int  but found ", self.profile[key]])
        for key in People.required_key_set:
            if self.profile[key] == None or self.profile[key] == "":
                return False, " ".join(["Field:",key ,"is a required field but left empty or not provided"])
        return True, ""
    def contains_all_keys(self):
        for key in People.profile_key:
            if key not in self.profile:
                return False, " ".join(["Field:",key,"is a required field but left empty or not provided"])
        return True, ""

    @staticmethod
    def __convert_empty_to_null(row_dict):
        for key, value in row_dict.items():
            if value == "":
                row_dict[key] = None

    def __convert_date(self):
        for key, value in People.date_format_dict.items():
            if self.profile[key] == "" or self.profile[key] == None:
                self.profile[key] = None
            else:
                self.profile[key] = datetime.strptime(self.profile[key], People.date_format_dict[key])

    #id conflicts disallowed
    @staticmethod
    def create_from_csv(file_path, con):

        file = open(file_path, 'r')
        file_reader = csv.DictReader(file)
        has_id = 'ID' in file_reader.fieldnames
        if has_id:
            print("Not recommanded to have id in the file, if there is a conflict, will be ignoring the record")


        for i, row in enumerate(file_reader):
            People.__convert_empty_to_null(row)
            people = People(profile=row)
            is_valid, msg = people.is_data_valid()
            if not is_valid:
                print(msg)
                continue
            has_all_req, msg = people.contains_all_keys()
            if not has_all_req:
                print(msg)
                continue

            if has_id:
                people.insert_with_id(con)
            else:
                people.insert_no_id(con)
        con.commit()

    @staticmethod
    def get_all_users(con, timestamp='1970-01-01', order_by=None, order_method='ASC'):
        """
        use to retrieve the record created after the timestamp given
        :param con: pymysql connection object
        :param timestamp: time object or time string in format of ('yyyy-mm-dd') set the start time of the query(default '1970-01-01'
        :return: list of dictionary with column defined in the query
        """
        sql = " ".join(["SELECT id as ID, firstName as First, lastName as Last, age as Age,",
                                "githubAcct as GithubAcct, date(dateThirdGradeGra) as `Date of 3rd Grade Graduation`"
                        "FROM ", "".join([Database.DB_NAME, ".", Database.TABLE_NAME]),
                        " WHERE created_at > %(timestamp)s"])
        if order_by != None:
            sql = " ".join([sql, "ORDER BY", order_by, order_method])
        return DataLoader.buffered_data_loader_dict(con, sql, {'timestamp':timestamp})

    @staticmethod
    def get_user_by_lname(con, lname=None,timestamp='1970-01-01'):
        """
        use to retrieve the record created after the timestamp with last name given
        :param con: pymysql connection object
        :param lname: string of last name to filter the query
        :param timestamp: time object or time string in format of ('yyyy-mm-dd') set the start time of the query(default '1970-01-01'
        :return: list of dictionary with column defined in the query
        """
        sql = "".join(" ".join(["SELECT id as ID",
                                "FROM ", "".join([Database.DB_NAME, ".", Database.TABLE_NAME]),
                                "WHERE lastName = %(lastName)s AND",
                                       "created_at > %(timestamp)s"]))
        return DataLoader.execute_query_res(con, sql, {'lastName':lname,'timestamp': timestamp})


    def insert_no_id(self, con):
        sql = "".join(["INSERT INTO ", Database.DB_NAME, ".", Database.TABLE_NAME,
                       "(firstName, lastName, age, gitHubAcct,dateThirdGradeGra)",
                       "VALUES (%(First)s, %(Last)s, %(Age)s, %(GithubAcct)s, %(Date of 3rd Grade Graduation)s)"])
        DataLoader.execute_query_no_res(con, sql, self.profile)



    def insert_with_id(self, con):
        sql = "".join(["INSERT INTO ", Database.DB_NAME, ".", Database.TABLE_NAME,
                       "(id, firstName, lastName, age, gitHubAcct,dateThirdGradeGra)",
                       "VALUES (%(ID)s, %(First)s, %(Last)s, %(Age)s, %(GithubAcct)s, %(Date of 3rd Grade Graduation)s)"])
        try:
            DataLoader.execute_query_no_res(con, sql, self.profile)
        except pymysql.err.IntegrityError:
            print("".join(["User: ",str(self.profile['First']), " ",str(self.profile['Last']),
                           " with ID: ", str(self.profile['ID'])," already exist, ignored"]))



if __name__ == '__main__':
    pass









