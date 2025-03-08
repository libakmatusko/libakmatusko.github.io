from fastapi import FastAPI, Request
from pydantic import BaseModel, constr
from bisect import bisect_right
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains for security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class ScoreEntry(BaseModel):
    score: int
    name: constr(strip_whitespace=True, min_length=1)  # Ensures name is not empty or just whitespace

class SingInData(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    email: str
    password: str

class LogInData(BaseModel):
    loggin: str
    password: str

LEADERBOARD_FILE = "leaderboard.json"
USERS_FILE = 'users.json'

def load_data():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            try:
                data = json.load(f)
                return [ScoreEntry(**entry) for entry in data.get("leaderboard", [])], data.get("players", {})
            except json.JSONDecodeError:
                return [], {}
    return [], {}

def save_data():
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump({"leaderboard": [entry.dict() for entry in leaderboard], "players": players}, f, indent=4)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            try:
                data = json.load(f)
                return data, {v['email']:k for k, v in data.items()}
            except json.JSONDecodeError:
                return {}, {}
    return {}, {}

def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

leaderboard, players = load_data()
users, email_to_user = load_users()

@app.get("/")
def read_root():
    return {"message": "Welcome to the leaderboard API"}

@app.get('/leaderboard')
def leaderboard_view():
    return [entry.dict() for entry in leaderboard]

@app.post("/new_run")
def new_run(entry: ScoreEntry):
    if entry.name in players:
        if players[entry.name]["score"] >= entry.score:
            return {"message": "Score not improved", "position": get_index(entry.name) + 1, 'max':leaderboard[0].score}
        
        leaderboard.pop(bisect_right(leaderboard, -players[entry.name]["score"], key=lambda x: -x.score) - 1)
        
        index = bisect_right(leaderboard, -entry.score, key=lambda x: -x.score)
        leaderboard.insert(index, entry)
        players[entry.name] = entry.dict()
    else:
        index = bisect_right(leaderboard, -entry.score, key=lambda x: -x.score)
        leaderboard.insert(index, entry)
        players[entry.name] = entry.dict()
    
    save_data()
    return {"message": "Score added", "position": index + 1, 'max':leaderboard[0].score}

@app.post("/sing_in")
def sing_in(data: SingInData):
    if (data.email not in email_to_user) and (data.name not in users):
        users[data.name] = {
            'email': data.email,
            'password': data.password,
            'inventory':{'coin':0, 'Player':[[0, 0, 255]]}
        }
        email_to_user[data.email] = data.name
        save_users()
        return {'message':'New user created'}
    return {'message':'Username or email not valid or already in use'}

@app.post("/log_in")
def log_in(data: LogInData):
    name = email_to_user.get(data.loggin, False)
    if name == False:
        name = data.loggin
    user = users.get(name, False)
    if user:
        if user['password'] == data.password:
            return {'message':'User logged in', 'name':name, 'inventory':user['inventory']}
        return {'message':'Wrong password'}
    return {'message':'Invalid username'}

@app.post('/update/{user}')
async def update_user(user: str, request: Request):
    data = await request.json()
    if user in users:
        users[user]['inventory'] = data
        save_users()
        return {'message':'Inventory updated'}
    return {'message':'Invalid username'}

def get_index(name: str):
    for i, ent in enumerate(leaderboard):
        if ent.name == name:
            return i
    return -1
