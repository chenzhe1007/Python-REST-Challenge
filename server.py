from flask import Flask, request, jsonify
from flask_cache import Cache
from functools import wraps
from people import People
from database import Database
import argparse
import sys
import time

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE':'simple'})


def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            request.json
        except BadRequest as e:
            msg = "post request must be sending a valid json doc"
            return jsonify({'error':msg}),400
        return f(*args, **kw)
    return wrapper


@app.route('/ping',methods=['GET'])
def pingServer():
    '''
    Ping request to make sure server is alive, return 'pong'
    '''
    # TODO
    return "pong"


@app.route('/people',methods=['GET'])
@cache.cached(timeout=3, key_prefix='id')
def getPeople():
    '''
    Return a standard JSON block of people in any order of format. Must be valid JSON
    '''
    # TODO
    con_cur = Database.get_connection()
    result = jsonify(People.get_all_users(con_cur))
    con_cur.close()
    return result

@app.route('/people/age',methods=['GET'])
@cache.cached(timeout=3, key_prefix='id_age')
def sortPeopleByAge():
    '''
    Returns Json block containing a list of people sorted by age youngest to oldest
    '''
    # TODO
    con_cur = Database.get_connection()
    result = jsonify(People.get_all_users(con_cur, order_by='age'))
    con_cur.close()
    return result

@app.route('/ids/lastname/<lastname>',methods=['GET'])
@cache.memoize(timeout=3)
def getIdsByLastName(lastname):
    '''
    Returns Json block of ids found for the given last name
    Using path params
    '''
    # TODO
    con_cur = Database.get_connection()
    result = jsonify(People.get_user_by_lname(con_cur, lastname))
    con_cur.close()
    return result



# TODO Create an endpoint POST that accepts a 'person' and appends it to our people. Returns the newley update JSON block of all people.
# New endpoint goes here.

@app.route('/', methods=['GET'])
def index():
    return jsonify("Restful_challenge")

@app.route('/people/add', methods=['POST'])
@validate_json
def create_people():
    """
    sample request body:{
                            "First":"Zhe",
                            "Last":"Chen",
                            "Age":"31",
                            "GithubAcct":"zchen1007",
                            "Date of 3rd Grade Graduation":"3/04/98"
                        }
    not recommending using id as one of the key in the json
    :return: json object response
    """
    input = request.json
    people = People(profile=input)
    is_valid, msg = people.is_data_valid()
    if not is_valid:
        return jsonify({"err": msg}), 400
    has_all_req, msg = people.contains_all_keys()
    if not has_all_req:
        return jsonify({"err": msg}), 400
    con_cur = Database.get_connection()
    if 'ID' in people.profile:
        app.logger.warning("manually input ID has the risk of conflicting with existing, if conflicts records will be ignored")
        people.insert_with_id(con_cur)
    else:
        people.insert_no_id(con_cur)
    con_cur.commit()
    con_cur.close()
    return getPeople()








if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Optional Debug Mode for stack traces", action="store_true")
    parser.add_argument("-r", "--remove", help="Optional whether to remove data in relevant table before restart server", action="store_false")

    # TODO: pass in a port from the command line and run on that port i.e. 'python3 server.py 9000 test.csv'

    parser.add_argument("port", help="Port this app will listen to")
    parser.add_argument("file", help="File to import data from")

    # TODO: Initialize any pre-application start code here if needed
    time.sleep(25) #when compose mysql server is slower than flask cause the app to exit
    args = parser.parse_args()
    con = Database.get_connection()
    app.logger.info("database connection successful")
    Database.create_base_db_setup(con, overwrite=args.remove)
    app.logger.info("base schema, table and column setup done")
    # TODO: Read in people from people.csv into an appropraite data structure so that the endpoints can return data based
    #       on the data in the csv.
    People.create_from_csv(args.file, con)
    con.close()
    del con
    app.logger.info("initial user loadded")
    
    app.debug = args.debug
    app.run(host='0.0.0.0',port=int(args.port))
