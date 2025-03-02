from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
from bisect import bisect_right
from fastapi.middleware.cors import CORSMiddleware

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

leaderboard:list[ScoreEntry] = []
players = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to the leaderboard API"}

@app.post("/new_run")
def new_run(entry: ScoreEntry):
    if entry.name in players:
        if players[entry.name].score >= entry.score:
            return {"message": "Score not improved", "position": get_index(entry.name)+1}
        
        leaderboard.pop(bisect_right(leaderboard, -players[entry.name].score, key=lambda x: -x.score)-1)
        index = bisect_right(leaderboard, -entry.score, key=lambda x: -x.score)
        leaderboard.insert(index, entry)
        players[entry.name] = entry

        return {"message": "Score impoved", "position": index+1}

    else:
        index = bisect_right(leaderboard, entry.score, key=lambda x: -x.score)
        leaderboard.insert(index, entry)
        players[entry.name] = entry  

        return {"message": "Score added", "position": index+1}

def get_index(name: str):
    for i, ent in enumerate(leaderboard):
        if ent.name == name:
            return i
