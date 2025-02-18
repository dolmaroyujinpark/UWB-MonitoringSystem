import sqlite3

db_path = "workspaces.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='workspaces';")
result = cursor.fetchone()

if result:
    print("[INFO] 'workspaces' 테이블이 존재합니다.")
else:
    print("[INFO] 'workspaces' 테이블이 존재하지 않습니다. 새로 생성이 필요합니다.")
conn.close()
