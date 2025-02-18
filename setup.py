import sys
from cx_Freeze import setup, Executable
import os
sys.setrecursionlimit(2000)

# INCLUDE FILES
files = [
    'icon.ico',                   # 아이콘 파일
    'themes/',                    # 테마 폴더
    'modules/workspace.db',       # SQLite 데이터베이스 파일
    ('modules/anchor.png', 'modules/anchor.png'),
    ('modules/dangerzone.png', 'modules/dangerzone.png'),
    ('modules/sound.mp3', 'modules/sound.mp3')
]

# TARGET
target = Executable(
    script="main.py",             # 메인 스크립트
    base="Win32GUI" if sys.platform == "win32" else None,  # GUI 애플리케이션
    icon="icon.ico"               # 아이콘 파일
)

# SETUP
setup(
    name="UWB Monitoring System",
    version="1.0",
    description="UWB - Position Monitoring System Interface",
    author="By. EIC",
    options={'build_exe': {'include_files': files}},  # 추가 파일 및 폴더 지정
    executables=[target]
)
