from flask import app,Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import elasticsearch
from elasticsearch import Elasticsearch
import datetime
import concurrent.futures
import requests
import json



app = Flask(__name__)
CORS(app)
api = Api(app)

#------------------------------------------------------------------------------------------------------------
# Elasticsearch
INDEX_NAME = 'netflix_movies'
#es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

ENDPOINT = "http://localhost:9200"
es = Elasticsearch(request_timeout=600, hosts=ENDPOINT)
print(f'elasticsearch connected={es.ping()}')

#------------------------------------------------------------------------------------------------------------


"""
{
"wildcard": {
    "title": {
        "value": "{}*".format(self.query)
    }
}
}

"""


class Controller(Resource):
    def __init__(self):
       # self.query = parser.parse_args().post("query", None)
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('query', type = str, required = True,
            help = 'No task title provided', location = 'json')
        self.args = parser.parse_args()
        print("query=>",self.args['query'])
        self.baseQuery ={         
            "query": {
                "prefix": {
                    "title.keyword": {
                        "value": "{}".format(self.args['query'])
                    }
                }
            },
            "aggs": {
                "auto_complete": {
                    "terms": {
                        "field": "title.keyword",
                        "order": {
                            "_count": "desc"
                        },
                        "size": 25
                    }
                }
            }
        }

    def post(self):
        res = es.search(index=INDEX_NAME, body=self.baseQuery)
        result = {"hits": res['hits']['hits'], "aggregations": res["aggregations"]}
        print("res=>", result)
        return result


parser = reqparse.RequestParser()
parser.add_argument("query", type=str, required=True, help="query parameter is Required ")

api.add_resource(Controller, '/autocomplete')


if __name__ == '__main__':
    app.run(debug=True, port=4000)
