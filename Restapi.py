from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
from datetime import *

app = Flask(__name__)
api = Api(app)


def valid_time_check(delivery_time, start_time='10:00AM', end_time='7:00PM'):
    start_time = datetime.strptime(start_time, "%I:%M%p")
    end_time = datetime.strptime(end_time, "%I:%M%p")
    try:
        delivery_time = datetime.strptime(delivery_time, "%I:%M%p")
    except:
        return False
    return start_time <= delivery_time <= end_time


def valid_date_check(date):
    dates_avaliable = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Saturday', 'Sunday']
    for day in dates_avaliable:
        if date.lower() == day.lower():
            return True
    else:
        return False


class Users(Resource):
    data = {"userName": "hSimpson23", "userFName": "Homer", "userLName": "Simpson", "email": "chunkylover53@aol.com",
            "phone": "(939)-555-0113", "deliveryAddress": "742 Evergreen Terrace, Springfield, OR", "groceryList": "{}",
            "deliveryDay": "", "deliveryTime": ""}

    def get(self):
        data_list = json.dumps(self.data)
        self.data = json.loads(data_list)
        return self.data, 200

    def put(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userName', required=True)  # add args
        parser.add_argument('deliveryTime', required=True)
        parser.add_argument('groceryList', required=True)
        parser.add_argument('deliveryDay', required=True)
        args = parser.parse_args()  # parse arguments to dictionary
        if args['userName'] == self.data['userName']:  # Check if it's correct user
            if valid_time_check(delivery_time=args['deliveryTime']):# Check if it is valid time
                if valid_date_check(date=args['deliveryDay']):  # Check if it is valid day
                    self.data['deliveryTime'] = args['deliveryTime']
                    self.data['groceryList'] = args['groceryList']
                    self.data['deliveryDay'] = args['deliveryDay']
                else:
                    return {'message': f"{args['deliveryDay']} is not a valid day"}, 400 #return bad day
            else:
                return {'message': f"{args['deliveryTime']} is not between 10:00AM and 7:00P"}, 400 #return bad time
            return self.data, 200 #Post request was successful
        else:
            # otherwise the userId does not exist
            return {'message': f"'{args['userName']}' user not found."}, 404


api.add_resource(Users, '/users')  # '/users' is our entry point for Users

if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app
