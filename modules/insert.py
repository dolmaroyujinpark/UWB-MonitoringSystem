import os
import os

base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 기준 디렉토리
db_path = os.path.join(base_dir, "workspace.db")


print(f"[DEBUG] base_dir: {base_dir}")
print(f"[DEBUG] db_path: {db_path}")
