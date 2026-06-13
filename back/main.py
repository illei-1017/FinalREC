from fastapi import FastAPI
from pydantic import BaseModel
import json
import random

app = FastAPI()

def read_json():
    with open("songs.json", "r", encoding="utf-8") as f:
        return json.load(f)

# 프론트 데이터
class ReqInfo(BaseModel):
    min_lv: float
    max_lv: float
    patterns: list[str]

@app.post("/recommend")
def recommend(req: ReqInfo):
    songs = read_json()
    matched = []
    
    # 필터링
    for s in songs:
        if req.min_lv <= s["level"] <= req.max_lv:
            if any(p in s["patterns"] for p in req.patterns):
                matched.append(s)
    
    # 조건 불만족
    if not matched:
        return {"status": "fail", "message": "조건에 맞는 곡이 없습니다."}
    
    # 랜덤추천
    limit = min(3, len(matched))
    selected = random.sample(matched, limit)
    
    return {"status": "success", "recommendations": selected}