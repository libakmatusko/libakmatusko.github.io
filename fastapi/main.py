from fastapi import FastAPI
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

LEADERBOARD_FILE = "leaderboard.json"

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

leaderboard, players = load_data()

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

def get_index(name: str):
    for i, ent in enumerate(leaderboard):
        if ent.name == name:
            return i
    return -1
