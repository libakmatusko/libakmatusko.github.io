from flask import Flask, jsonify, request
import json
from flask_cors import CORS
from datetime import datetime, timedelta


app = Flask(__name__)
CORS(app)
# Path to the users.json file
FILE_PATH = '/home/MatusLibak/mysite/users.json'
ANSWERS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Helper function to load the JSON file
def load_users():
    with open(FILE_PATH, 'r') as file:
        return json.load(file)
            

# Helper function to write to the JSON file
def write_users(users):
    with open(FILE_PATH, 'w') as file:
        json.dump(users, file, indent=4)

def sort_user(user):
    return -(user["score"]*10**7 - user["wrong_answers"]*10**4 - user["time"]*10**0)

def day(): #vracia sutazny den
    start_date = datetime(2024, 10, 12, 6, 0, 0) #tu sa nastavuje zaciatok
    current_date = datetime.now()
    time_difference = current_date - start_date
    current_day = time_difference.days + 1
    return current_day if current_day > 0 else 0  # If it's before the start date, return 0

def time_since_last_6am():
    now = datetime.now()
    today_6am = datetime(now.year, now.month, now.day, 6, 0, 0)
    if now >= today_6am:
        last_6am = today_6am
    else:
        last_6am = today_6am - timedelta(days=1)
    time_difference = now - last_6am
    return time_difference.total_seconds()

# Route to get all users
@app.route('/all_users', methods=['GET'])
def get_users():
    users = load_users()
    return jsonify(users)

# Route to add a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    new_user = request.json
    users = load_users()
    for u in users:
        if u['name'] == new_user['name']:
            break
    else:
        users.append(new_user)
        write_users(users)
        return {
            "status": "fail",
            "message": "username already exists"
        } 
    return {
        "status": "succes",
        "message": "user added"
    } 

@app.route('/dashboard', methods=['GET'])
def dashboard():
    users = load_users()
    for user in users:
        for key in ("password", "members"):
            user.pop(key)
        user['score'] = sum(user.pop('scores'))
    users.sort(key=sort_user)
    return jsonify(users)

@app.route('/login_user', methods=['POST'])
def login_user():
    logging_user = request.json
    for user in load_users():
        if user['name'] == logging_user['name'] and user['password'] == logging_user['password']:
            logging_user = user
            logging_user.pop("password")
            return {
                "status": "success",
                "message": "User logged in successfully.",
                "user": logging_user
            }

    return {
        "status": "error",
        "message": "Invalid username or password."
    }

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    submit = request.json
    users = load_users()
    for u in users:
        if u['name'] == submit['name']:
            if submit['answer'] == str(ANSWERS[day()-1]): #dorobit
                if u['scores'][day()-1] != 5:
                    u['scores'][day()-1] = 5
                    u['time'] += time_since_last_6am()
                    write_users(users)
                return {
                    "status": "success",
                    "isCorrect": True,
                    "message": "Correct answer!"
                }
            else:
                u['wrong_answers'] += 1
                write_users(users)
                return {
                    "status": "success",
                    "isCorrect": False,
                    "message": "Wrong answer."
                }
    return {
        "status": "fail",
        "isCorrect": False,
        "message": "Unknown user."
    }   

@app.route('/late_answer', methods=['POST'])
def late_answer():
    submit = request.json
    users = load_users()
    for u in users:
        if u['name'] == submit['name']:
            if submit['answer'] == str(ANSWERS[int(submit['day'])-1]): #dorobit
                if u['scores'][int(submit['day'])-1] == 0:
                    u['scores'][int(submit['day'])-1] = 3
                    u['time'] += time_since_last_6am()
                    write_users(users)
                return {
                    "status": "success",
                    "isCorrect": True,
                    "message": "Correct answer!"
                }
            else:
                u['wrong_answers'] += 1
                write_users(users)
                return {
                    "status": "success",
                    "isCorrect": False,
                    "message": "Wrong answer."
                }
    return {
        "status": "fail",
        "isCorrect": False,
        "message": "Unknown user."
    } 

if __name__ == '__main__':
    app.run(debug=True)
