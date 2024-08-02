from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from pydantic import BaseModel

app = FastAPI()

# CORSの設定
origins = [
    "http://localhost:3000",  # フロントエンドのURL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Stone(BaseModel):
    i: int
    j: int
    color: int

# 白 = 1
# 黒 = -1
# 空欄 = 0

board: List[List[int]] = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, -1, 0, 0, 0],
    [0, 0, 0, -1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],   
]

vectors = [
    (-1, 1), (0, 1), (1, 1),
    (-1, 0), (1, 0),
    (-1, -1), (0, -1), (1, -1)
]

# ボードを取得する
@app.get("/get_board")
def get_board():
    return board

# 位置(i, j)がボード内かチェックする
def check_range(i: int, j: int):
    if 0 <= i <= 7 and 0<= j <= 7:
        return True
    else:
        return False

# 位置(i, j)に石があるかチェックする
def check_stone(i: int, j: int):
    if not check_range(i, j):
        return False
    
    if board[i][j] == 0:
        return True
    else:
        return False

# 位置(i, j)に石を置いてボードを更新する
@app.post("/update")
def update(stone: Stone):
    # 位置が範囲内かチェックする
    if not check_range(stone.i, stone.j):
        return {"message": "範囲内に石を置いてください"}
    
    # 位置に石があるかチェックする
    if not check_stone(stone.i, stone.j):
        return {"message": "すでに石が置いてあります"}
    
    # ひっくり返した石の数
    count = 0

    # 石をひっくり返す
    for vector in vectors:
         # ひっくり返るかもしれない位置を記録
        positions = [] 
        i = stone.i + vector[0]
        j = stone.j + vector[1]
        
        # ひっくり返す石をためる
        while True:
            if not check_range(i, j):
                positions = []
                break

            if check_stone(i, j):
                positions = []
                break

            if board[i][j] * stone.color == 1:
                break
            else:
                positions.append((i, j))
                i += vector[0]
                j += vector[1]
        
        if positions:
            count += len(positions)
        for position in positions:
            board[position[0]][position[1]] *= -1

    if not count:
        return {"message": "ひっくり返せる石がありません"}
    else:
        board[stone.i][stone.j] = stone.color
        return {"message": f"石を{count}個ひっくり返しました"}
    
# 石の数をカウントするエンドポイント
@app.get("/count_stones")
def count_stones() -> Dict[str, int]:
    white_count = sum(row.count(1) for row in board)
    black_count = sum(row.count(-1) for row in board)
    return {"white": white_count, "black": black_count}
    







    






