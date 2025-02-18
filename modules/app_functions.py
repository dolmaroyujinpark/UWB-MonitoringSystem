# ///////////////////////////////////////////////////////////////
import csv

from PySide6.QtGui import QColor, QPainter, Qt
from PySide6.QtWidgets import QMessageBox, QDialog, QListWidget, QPushButton, QVBoxLayout
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, QTimer
# MAIN FILE
from main import *
from modules import Settings
from PySide6.QtWidgets import QLabel, QFileDialog, QMessageBox
import json
import serial
from serial.tools import list_ports
from modules.utils import resource_path
from modules.uwb_functions import Calculation
from modules.serial_handler import SerialHandler
from modules.calibration_handler import CalibrationHandler
from datetime import datetime
import re

import sqlite3
import os

# 데이터베이스 파일 경로 설정
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace.db")


# ///////////////////////////////////////////////////////////////
class AppFunctions:
    def __init__(self, parent):

        # 현재 워크스페이스 이름 초기화
        self.current_workspace_name = None

        # QMediaPlayer 설정
        self.media_player = QMediaPlayer()  # MP3 파일 재생을 위한 미디어 플레이어
        self.audio_output = QAudioOutput()  # 오디오 출력 설정
        self.media_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.8)  # 볼륨 설정 (0.0 ~ 1.0)

        # MP3 파일 경로 설정
        mp3_path = resource_path("modules/sound.mp3")
        self.media_player.setSource(QUrl.fromLocalFile(mp3_path))

        # 디버깅용 출력
        # print(f"MP3 파일 경로: {mp3_path}")
        if not self.media_player.source():
            print("[ERROR] MP3 파일을 찾을 수 없습니다.")

        # pos 리스트
        self.anchor_positions = []
        self.anchor_labels = {}

        self.parent = parent
        # 유진

        self.danger_image_label = None  # 위험 구역 이미지를 위한 QLabel 참조 저장

        # 데이터베이스 파일 경로 설정
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace.db")
        self.data_cache = {"anchor_self": None, "anchor_b": None, "anchor_c": None}  # 데이터 캐시 초기화
        self.serial_handler = None
        self.scale_ratio = None
        self.serial = None  # 시리얼 포트 객체
        self.tag_item = None  # 태그 아이템
        self.tag_label = None  # 태그 텍스트 라벨
        self.tag_position = None
        self.workspace_loaded = False  # 워크스페이스 로드 상태
        self.danger_color = QColor(255, 0, 0)  # 기본 빨간색 반투명
        self.workspace_color = QColor(130, 163, 196, 50)  # 기본 작업 공간 색상
        self.tag_status_list = []

        # 태그 관련 초기화
        self.tag_names = {}  # 태그 이름 저장소
        self.parent.ui.h_tagNum.valueChanged.connect(self.update_tag_list)
        self.parent.ui.i2_tagSelect.currentIndexChanged.connect(self.update_tag_name)
        self.parent.ui.tagName.editingFinished.connect(self.save_tag_name)

        # 초기화
        # self.update_tag_list()
        self.active_tag_index = None

        self.initialize_tag_status()
        self.parent.ui.h_tagNum.valueChanged.connect(self.initialize_tag_status)

        self.calibration_handler = CalibrationHandler(
            workspace=self.parent.ui.workspace,  # workspace 전달
            checkbox=self.parent.ui.calibrationCheckBox,
            parent=parent,
            serial_handler=self.serial_handler,  # SerialHandler 전달
            app_functions=self
        )

        # 앵커 데이터 초기화
        self.anchor_data = {}
        self.calculation = None  # Calculation 클래스 초기화 지연
        self.initialize_kalman_filters()  # 초기화

        # g_anchorNum 변경 시 Kalman Filters 재초기화
        self.parent.ui.g_anchorNum.valueChanged.connect(self.update_anchor_count)

        # self.initialize_serial()
        # QComboBox에 연결된 포트 추가
        self.populate_serial_ports()

        # 연결된 포트 저장
        self.connected_ports = []

        # QTimer 초기화
        self.port_timer = QTimer()
        self.port_timer.timeout.connect(self.update_serial_ports)
        self.port_timer.start(1000)  # 1초마다 실행

        # 기존 포트 목록 초기화
        self.populate_serial_ports()

        self.parent.ui.workspace.paintEvent = self.paint_workspace
        self.parent.ui.wsLog.paintEvent = self.paint_ws_log

        # Save as New Workspace 버튼 연결
        self.parent.ui.pushButton_4.pressed.connect(self.save_as_new_workspace)

        # Edit Workspace 버튼 연결
        self.parent.ui.pushButton_3.pressed.connect(self.edit_workspace)

        # 열린 워크스페이스 파일 경로 저장 변수
        self.current_workspace_file = None

        # 데이터베이스 초기화
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace.db")
        self.initialize_database()
        # self.update_anchor_settings()

        # QFrame에 그려질 박스 초기화
        self.workspace = {"x": 0, "y": 0, "width": 0, "height": 0}

        # 콤보박스 이벤트 연결
        self.parent.ui.i_anchorSelect.currentIndexChanged.connect(self.update_anchor_position)

        # 스핀박스 이벤트 연결
        self.parent.ui.j_anchorX.valueChanged.connect(self.save_anchor_position)
        self.parent.ui.k_anchorY.valueChanged.connect(self.save_anchor_position)

        # 앵커 그리기
        self.initialize_anchor_labels()
        self.parent.ui.g_anchorNum.valueChanged.connect(self.update_visible_anchors)

        # JSON 파일 열기 버튼 이벤트 연결
        self.parent.ui.pushButton.pressed.connect(self.open_existing_workspace)

        # inactive, active Button 관련
        self.tag_in_danger_zone = False
        self.initialize_buttons()

    # ///////////////////////////////////////////////////////////////
    # 시리얼, 태그 관련 설정
    # ///////////////////////////////////////////////////////////////

    def populate_serial_ports(self):
        """QComboBox에 연결된 시리얼 포트를 추가"""
        self.parent.ui.portList.clear()  # 기존 항목 제거
        ports = list_ports.comports()  # 연결된 포트 탐색
        port_names = [port.device for port in ports]

        if not port_names:
            #QMessageBox.warning(self.parent, "Warning", "연결된 시리얼 포트가 없습니다.")
            return

        # 포트를 콤보박스에 추가
        self.parent.ui.portList.addItems(port_names)

        # 연결된 포트가 하나인 경우 자동 연결
        if len(port_names) == 1:
            self.parent.ui.portList.setCurrentIndex(0)  # 포트를 선택
            selected_port = port_names[0]
            self.start_serial_connection()  # 자동으로 시리얼 연결 시작
            #QMessageBox.information(self.parent, "Info", f"{selected_port} 포트가 자동으로 선택되고 연결되었습니다.")

    def update_serial_ports(self):
        """연결된 포트를 주기적으로 업데이트"""
        current_ports = [port.device for port in list_ports.comports()]

        if current_ports != self.connected_ports:  # 기존 포트 목록과 비교
            print(f"[DEBUG] Serial ports updated: {current_ports}")
            self.connected_ports = current_ports

            # QComboBox 업데이트
            self.parent.ui.portList.clear()
            self.parent.ui.portList.addItems(self.connected_ports)

            # 선택 항목 초기화
            if self.connected_ports:
                self.parent.ui.portList.setCurrentIndex(0)

    def start_serial_connection(self):
        """사용자가 선택한 포트로 시리얼 연결"""
        selected_port = self.parent.ui.portList.currentText()  # QComboBox에서 선택된 포트 가져오기
        if not selected_port:
            #QMessageBox.warning(self.parent, "Warning", "포트를 선택하세요.")
            return

        # 이미 연결된 포트인지 확인
        if self.serial_handler and self.serial_handler.port == selected_port and self.serial_handler.serial.is_open:
            #QMessageBox.information(self.parent, "Info", f"{selected_port} 포트는 이미 연결되어 있습니다.")
            return

        # 기존 연결 종료
        if self.serial_handler:
            # self.serial_handler.stop_port_monitoring()  # 포트 모니터링 중지
            self.serial_handler.disconnect()

        # 새 포트로 연결
        self.serial_handler = SerialHandler(
            port=selected_port,
            baudrate=115200,
            callback=self.process_serial_data,
            parent=self
        )
        self.serial_handler.connect()

        if self.serial_handler.serial and self.serial_handler.serial.is_open:
            #QMessageBox.information(self.parent, "Info", f"{selected_port} 포트와 연결되었습니다.")
            self.serial_handler.start_port_monitoring()  # 데이터 모니터링 시작
        else:
            QMessageBox.critical(self.parent, "Error", f"{selected_port} 포트와 연결할 수 없습니다.")

    # 앵커별 offset불러오기
    def get_anchor_offsets(self):
        """
        workspaces 테이블의 calibration 컬럼에서 앵커별 Offset 값을 불러옵니다.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        anchor_offsets = {}

        try:
            # workspaces 테이블에서 calibration 데이터 가져오기
            cursor.execute("SELECT calibration FROM workspaces WHERE name = ?", (self.current_workspace_name,))
            row = cursor.fetchone()

            if row and row[0]:  # calibration 데이터가 있을 경우
                calibration_data = json.loads(row[0])  # JSON 데이터 파싱
                print(f"[DEBUG] Calibration data loaded: {calibration_data}")

                # Offset 추출
                anchor_offsets = calibration_data
                print(f"[DEBUG] Extracted anchor_offsets: {anchor_offsets}")
            else:
                print(f"[WARNING] No calibration data found for workspace: {self.current_workspace_name}")

        except sqlite3.Error as e:
            print(f"[ERROR] Failed to fetch calibration data: {e}")
        except json.JSONDecodeError as e:
            print(f"[ERROR] Failed to parse calibration JSON data: {e}")
        finally:
            conn.close()

        return anchor_offsets

    def process_serial_data(self, data):
        """
        시리얼 데이터를 처리하는 메서드. 유효하지 않은 앵커를 제외하고 칼만 필터를 적용한 후 위치 계산.
        """
        try:
            # print(f'raw data: {data}')
            # 앵커 수 읽어오기
            anchor_count = self.parent.ui.g_anchorNum.value()

            # 태그 ID 추출
            tag_match = re.search(r"tid:\s*(\d+)", data)
            if tag_match:
                tag_id = int(tag_match.group(1))  # 태그 ID
            else:
                print("[ERROR] 태그 ID가 없습니다!")
                self.update_tag_status(0, "inactive")
                return

            # range 값 추출
            range_match = re.search(r"range:\(([\d,\. ]+)\)", data)
            if range_match:
                range_values = list(map(float, range_match.group(1).split(",")))
                range_values = range_values[:anchor_count]
            else:
                range_values = [0.0] * anchor_count

            # rssi 값 추출
            rssi_match = re.search(r"rssi:\(([-\d\., ]+)\)", data)
            if rssi_match:
                rssi_values = list(map(float, rssi_match.group(1).split(",")))
                rssi_values = rssi_values[:anchor_count]
            else:
                rssi_values = [None] * anchor_count

            # 유효하지 않은 값 확인
            for i in range(anchor_count):
                range_val = range_values[i]
                rssi_val = rssi_values[i] if i < len(rssi_values) else None
                if range_val <= 0:
                    print(f"[INFO] 유효하지 않은 range 값: 앵커 {i}, range={range_val}")
                elif rssi_val is not None and rssi_val <= -90:
                    print(f"[INFO] 유효하지 않은 RSSI 값: 앵커 {i}, RSSI={rssi_val}")

            # 유효한 앵커 필터링 및 칼만 필터 적용
            valid_anchors = []
            for i in range(anchor_count):
                range_val = range_values[i]
                rssi_val = rssi_values[i] if i < len(rssi_values) else None

                # 조건: range가 0보다 크고 RSSI가 -90 이상인 경우만 유효
                if range_val > 0 and (rssi_val is None or rssi_val > -90):
                    # 칼만 필터 적용
                    corrected_range = self.calculation.apply_correction_and_kf(range_val, f"Anchor {i}")
                    if corrected_range > 0:  # 보정된 값도 유효한 경우에만 추가
                        valid_anchors.append({
                            "index": i,
                            "range": corrected_range,
                            "position": self.anchor_positions[i]
                        })

            # print(f"Valid Anchors (after Kalman): {valid_anchors}")

            # 유효한 앵커가 2개 미만일 경우 처리
            if len(valid_anchors) < 3:
                print("[CRITICAL] 유효한 앵커가 3개 미만입니다. 위치 계산을 중단합니다!")
                self.update_tag_status(0, "inactive")
                return

            # 필터링된 데이터로 위치 계산 준비
            filtered_ranges = [anchor["range"] for anchor in valid_anchors]
            filtered_positions = [anchor["position"] for anchor in valid_anchors]

            # 위치 계산
            x, y = self.calculation.generalized_trilateration(
                num_anchors=len(filtered_ranges),
                anchor_ranges=filtered_ranges,
                anchor_positions=filtered_positions
            )

            print(f"Using generalized_trilateration with {filtered_ranges} anchors.")
            print(f"Using generalized_trilateration with {filtered_positions} anchors.")

            if x is not None and y is not None:
                self.update_tag_position(x, y)

            # 데이터를 저장
            self.latest_serial_data = data
            # print(f"[INFO] Latest Serial Data Stored: {self.latest_serial_data}")

        except (KeyError, ValueError, IndexError) as e:
            self.update_tag_status(0, "inactive")
            print(f"[ERROR] 데이터 처리 중 오류 발생: {e}")

    def update_tag_position(self, x, y, tag_index=0):
        """
        태그의 위치를 업데이트하고 화면에 그립니다.
        """
        painter = QPainter(self.parent.ui.workspace)
        painter.setRenderHint(QPainter.Antialiasing)

        # 태그 원본 좌표 저장        self.tag_position = (x, y)

        # 작업 공간 박스의 오프셋 및 크기 가져오기
        x_offset = self.workspace_box.x()
        y_offset = self.workspace_box.y()

        # 태그 좌표 변환
        x_scaled = x * self.scale_ratio + x_offset
        y_scaled = y * self.scale_ratio + y_offset

        # 태그 위치 및 크기 설정
        self.tag_position = (x_scaled, y_scaled)
        # print(f'tag position: {self.tag_position}')


        # 태그가 위험 구역에 있는지 확인
        if hasattr(self, "danger_box") and self.danger_box.contains(x_scaled, y_scaled):
            # print("[경고] 태그가 위험 구역에 있습니다!")
            # self.danger_color = QColor(255, 0, 0)
            self.update_tag_status(tag_index, "danger")
            self.tag_in_danger_zone = True
            self.handle_inactive_button()

            # 사운드 재생
            if self.media_player.playbackState() != QMediaPlayer.PlayingState:  # 중복 재생 방지
                self.media_player.play()
        else:
            # self.danger_color = QColor(255, 255, 0, 127)  # 기본 노란색으로 복원
            self.update_tag_status(tag_index, "active")
            self.tag_in_danger_zone = False

            # 사운드 중지
            if self.media_player.playbackState() == QMediaPlayer.PlayingState:  # 현재 재생 중인 경우
                self.media_player.stop()

        # QFrame 갱신 (태그만 다시 그리기)
        self.parent.ui.workspace.update()

    def update_tag_status(self, tag_index, status):
        """
        태그의 상태를 업데이트하고 wsLog에 출력합니다.
        """
        if tag_index >= len(self.tag_status_list):
            # print(f"[ERROR] Invalid tag index: {tag_index}")
            return

        # 상태 업데이트
        self.tag_status_list[tag_index] = status
        self.parent.ui.wsLog.update()  # wsLog 다시 그리기

    def initialize_tag_status(self):
        """
        태그 상태 리스트를 초기화합니다.
        """
        num_tags = self.parent.ui.h_tagNum.value()  # 현재 설정된 태그 수
        self.tag_status_list = ["inactive"] * num_tags  # 모든 태그를 inactive 상태로 초기화
        self.parent.ui.wsLog.update()  # wsLog 다시 그리기

    def update_tag_list(self):
        """
        QSpinBox(h_tagNum)의 값에 따라 QComboBox(i2_tagSelect)에 태그 목록을 동적으로 업데이트.
        """
        tag_count = self.parent.ui.h_tagNum.value()  # 태그 수 읽어오기
        current_count = self.parent.ui.i2_tagSelect.count()

        # 태그 추가
        if tag_count > current_count:
            for i in range(current_count, tag_count):
                tag_name = f"Tag {i}"
                self.parent.ui.i2_tagSelect.addItem(tag_name)
                self.tag_names[tag_name] = "None"  # 기본값으로 초기화

        # 태그 제거
        elif tag_count < current_count:
            for i in range(current_count - 1, tag_count - 1, -1):
                tag_name = self.parent.ui.i2_tagSelect.itemText(i)
                self.parent.ui.i2_tagSelect.removeItem(i)
                self.tag_names.pop(tag_name, None)  # 해당 태그 삭제

        # 콤보박스 초기화 후 첫 번째 태그 선택
        if self.parent.ui.i2_tagSelect.count() > 0:
            self.parent.ui.i2_tagSelect.setCurrentIndex(0)
            self.update_tag_name()

    def update_tag_name(self):
        """
        QComboBox에서 선택된 태그의 이름을 QLineEdit(tagName)에 표시.
        """
        selected_tag = self.parent.ui.i2_tagSelect.currentText()  # 선택된 태그 가져오기

        if selected_tag in self.tag_names:
            # 저장된 이름 가져와 QLineEdit에 표시
            self.parent.ui.tagName.setText(self.tag_names[selected_tag])
        else:
            # 기본값으로 None 표시
            self.parent.ui.tagName.setText("None")

    def save_tag_name(self):
        """
        QLineEdit(tagName)에서 입력된 이름을 저장.
        """
        selected_tag = self.parent.ui.i2_tagSelect.currentText()  # 선택된 태그 가져오기
        tag_name = self.parent.ui.tagName.text().strip()  # 입력된 텍스트 가져오기

        if not selected_tag:
            return

        # 저장된 값이 없거나 빈 문자열인 경우 기본값 "None" 사용
        if not tag_name:
            tag_name = "None"

        # 태그 이름 저장
        self.tag_names[selected_tag] = tag_name
        print(f"태그 이름 저장: {selected_tag} -> {tag_name}")

    def close_application(self):
        if self.serial_handler:
            self.serial_handler.disconnect()

    # ///////////////////////////////////////////////////////////////
    # 워크스페이스 관련 설정
    # ///////////////////////////////////////////////////////////////
    def start_processing(self):
        """
        데이터 처리를 시작 (워크스페이스가 로드된 경우만 실행)
        """
        if not self.workspace_loaded:
            print("Workspace not loaded. Cannot start processing.")
            return

        while True:
            self.process_serial_data()
            QApplication.processEvents()

    def draw_workspace_box(self, x, y, workspace_width, workspace_height, danger_zone_x, danger_zone_y,
                           danger_zone_width, danger_zone_height, anchors):

        # print(f"[DEBUG] draw_workspace_box called with anchors: {anchors}")

        # QFrame의 크기 가져오기
        frame_width = self.parent.ui.workspace.width()
        frame_height = self.parent.ui.workspace.height()
        # print(f"[DEBUG] frame size: {frame_width, frame_height}")

        # 작업 공간 크기가 0인 경우 처리 방지
        if frame_width == 0 or frame_height == 0:
            return

        # 단일 스케일 비율 계산 (가로, 세로 중 작은 비율 선택)
        self.scale_ratio = min(frame_width / workspace_width, frame_height / workspace_height) * 0.9

        # 작업 공간 크기를 비율에 맞게 조정
        scaled_width = workspace_width * self.scale_ratio
        scaled_height = workspace_height * self.scale_ratio
        # print(f"[DEBUG] scaled width: {scaled_width}, scaled height: {scaled_height}")

        # 중앙 배치용 offset 계산
        x_offset = (frame_width - scaled_width) / 2
        y_offset = (frame_height - scaled_height) / 2
        # print(f"[DEBUG] offset: x={x_offset}, y={y_offset}")

        # CalibrationHandler에 업데이트된 값 전달
        if hasattr(self, "calibration_handler"):
            self.calibration_handler.scaled_width = scaled_width
            self.calibration_handler.scaled_height = scaled_height
            self.calibration_handler.x_offset = x_offset
            self.calibration_handler.y_offset = y_offset
            self.calibration_handler.scale_ratio = self.scale_ratio
            self.calibration_handler.anchor_positions = self.anchor_data

        # 작업 공간 박스 설정
        self.workspace_box = QRectF(x_offset, y_offset, scaled_width, scaled_height)

        '''# 위험 구역 박스 크기와 위치를 작업 공간 비율에 맞게 조정
        scaled_danger_x = danger_zone_x * self.scale_ratio
        scaled_danger_y = danger_zone_y * self.scale_ratio
        scaled_danger_width = danger_zone_width * self.scale_ratio
        scaled_danger_height = danger_zone_height * self.scale_ratio

        self.danger_box = QRectF(
            scaled_danger_x + x_offset,
            scaled_danger_y + y_offset,
            scaled_danger_width,
            scaled_danger_height
        )'''

        # 위험 구역 박스 크기와 위치를 작업 공간 비율에 맞게 조정
        scaled_danger_x = (danger_zone_x / workspace_width) * scaled_width + x_offset
        scaled_danger_y = (danger_zone_y / workspace_height) * scaled_height + y_offset
        scaled_danger_width = (danger_zone_width / workspace_width) * scaled_width
        scaled_danger_height = (danger_zone_height / workspace_height) * scaled_height
        self.danger_box = QRectF(
            scaled_danger_x,
            scaled_danger_y,
            scaled_danger_width,
            scaled_danger_height
        )
        # 기존 danger_image_label 제거
        if self.danger_image_label:
            self.danger_image_label.deleteLater()  # QLabel 삭제
            self.danger_image_label = None  # 참조 해제

        # 앵커 위치 스케일링
        for anchor_name, coordinates in anchors.items():
            # print(f"[DEBUG] Processing anchor: {anchor_name}, coords: {coordinates}")
            # 워크스페이스 내부 좌표계 기준 스케일링
            anchor_x_scaled = (coordinates["x"] / workspace_width) * scaled_width + x_offset - 15
            anchor_y_scaled = (coordinates["y"] / workspace_height) * scaled_height + y_offset - 15
            # print(f"[DEBUG] Original Anchor: x={coordinates['x']}, y={coordinates['y']}")
            # print(f"[DEBUG] Scaled Anchor: x={anchor_x_scaled}, y={anchor_y_scaled}")

            # 디버깅 출력
            # print(f"[DEBUG] Anchor {anchor_name}: Final (x={anchor_x_scaled}, y={anchor_y_scaled})")

            # 앵커 라벨 표시
            label = self.anchor_labels.get(anchor_name)
            if label:
                label.move(int(anchor_x_scaled), int(anchor_y_scaled))
                label.show()

        # 위험 구역 이미지 추가
        '''image_path = "modules/dangerzone.png"
        pixmap = QPixmap(image_path)

        if not pixmap.isNull():
            resized_pixmap = pixmap.scaled(scaled_danger_width, scaled_danger_height)

            # 새로운 QLabel 생성 및 설정
            self.danger_image_label = QLabel(self.parent.ui.workspace)
            self.danger_image_label.setPixmap(resized_pixmap)
            self.danger_image_label.setGeometry(
                int(scaled_danger_x),
                int(scaled_danger_y),
                int(scaled_danger_width),
                int(scaled_danger_height)
            )
            self.danger_image_label.lower()  # QLabel을 뒤로 보내기
            self.danger_image_label.show()'''
        # QFrame 다시 그리기
        self.parent.ui.workspace.update()

    # 작업 공간, 위험 구역, 태그 그리기
    def paint_workspace(self, event):
        painter = QPainter(self.parent.ui.workspace)
        painter.setRenderHint(QPainter.Antialiasing)

        # 작업 공간 박스 그리기
        if hasattr(self, "workspace_box") and self.workspace_box:
            painter.setBrush(self.workspace_color)  # 작업 공간 색상
            painter.drawRect(self.workspace_box)

        # 위험 구역 박스 그리기
        if hasattr(self, "danger_box") and self.danger_box:
            # 테두리 선 설정
            pen = painter.pen()
            # self.danger_color = QColor(255, 0, 0)
            pen.setColor(self.danger_color)  # self.danger_color
            pen.setWidth(7)  # 테두리 두께 (픽셀 단위)
            painter.setPen(pen)
            #painter.setBrush(Qt.NoBrush)  # 투명한 내부 색상
            painter.drawRect(self.danger_box)  # 테두리 그리기

        # 태그 그리기
        if hasattr(self, "tag_position") and self.tag_position:
            x, y = self.tag_position
            painter.setPen(Qt.NoPen)  # 테두리 없음
            painter.setBrush(QColor(0, 255, 0))
            painter.drawEllipse(x - 5, y - 5, 15, 15)

    def paint_ws_log(self, event):
        painter = QPainter(self.parent.ui.wsLog)
        painter.setRenderHint(QPainter.Antialiasing)

        # 텍스트 출력 설정
        margin_x, margin_y = 10, 30
        line_spacing = 20  # 각 줄 간격

        for index, status in enumerate(self.tag_status_list):
            y = margin_y + index * line_spacing  # 각 태그의 Y 위치
            circle = "⚪"  # 기본 상태 (회색 동그라미)
            tag_name = self.tag_names.get(f"Tag {index}", "None")  # 저장된 태그 이름 가져오기
            text = f"Tag {index} : {tag_name} (inactive)"  # 기본 상태 텍스트

            if status == "active":
                circle = "🟢"  # 활성 상태 (녹색 동그라미)
                text = f"Tag {index} : {tag_name} (active)"
            elif status == "danger":
                circle = "🔴"  # 위험 상태 (빨간색 동그라미)
                text = f"Tag {index} : {tag_name} (danger)"

            # 흰색 텍스트 출력
            painter.setPen(QColor(255, 255, 255))  # 흰색 글자색
            painter.setFont(QFont("Arial", 10))
            painter.drawText(margin_x, y, f"{circle} {text}")

    # ///////////////////////////////////////////////////////////////
    # workspace 파일 관련 설정
    # ///////////////////////////////////////////////////////////////

    # 파일 열기 및 내용 표시
    def open_existing_workspace(self):
        """
        보조 창에서 데이터베이스에 저장된 워크스페이스를 선택하여 로드
        """
        workspace_list = self.get_workspace_list()

        # 보조 창 생성
        dialog = QDialog(self.parent)
        dialog.setWindowTitle("Select Workspace")
        dialog.setFixedSize(400, 300)

        # 리스트 위젯
        list_widget = QListWidget(dialog)
        list_widget.addItems(workspace_list)

        # 확인 버튼
        select_button = QPushButton("Load Selected Workspace", dialog)
        select_button.pressed.connect(lambda: self.load_selected_workspace(dialog, list_widget))

        # 레이아웃 설정
        layout = QVBoxLayout(dialog)
        layout.addWidget(list_widget)
        layout.addWidget(select_button)
        dialog.setLayout(layout)

        # 창 띄우기
        dialog.exec()

    def load_selected_workspace(self, dialog, list_widget):
        """
        보조 창에서 선택된 워크스페이스를 데이터베이스에서 로드
        """
        selected_item = list_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(self.parent, "Warning", "Please select a workspace!")
            return

        workspace_name = selected_item.text()
        data = self.load_workspace_from_db(workspace_name)

        if data:
            self.current_workspace_name = workspace_name
            self.calibration_handler.workspace_name = workspace_name  # 핸들러에 전달
            self.apply_workspace_data(data)

            QMessageBox.information(self.parent, "Success", f"Workspace '{workspace_name}' loaded successfully!")
            self.update_current_workspace(workspace_name)
            dialog.accept()  # 보조 창 닫기
        else:
            QMessageBox.critical(self.parent, "Error", f"Failed to load workspace '{workspace_name}'.")
            self.current_workspace_name = None  # 초기화

    # 창 닫기 함수
    def exitApplication(self):
        self.parent.close()  # 창 닫기

    # 새 workspace 저장
    def save_as_new_workspace(self):
        """
        현재 워크스페이스 데이터를 데이터베이스에 저장
        """
        workspace_name, ok = QInputDialog.getText(self.parent, "Save Workspace", "Enter workspace name:")
        if not ok or not workspace_name.strip():
            QMessageBox.warning(self.parent, "Warning", "Workspace name cannot be empty.")
            return

        # 워크스페이스 데이터 생성
        workspace_data = {
            "workspace_settings": {
                "workspace_width": self.parent.ui.a_workspace_width.value(),
                "workspace_height": self.parent.ui.b_workspace_height.value(),
                "danger_zone_width": self.parent.ui.c_danger_width.value(),
                "danger_zone_height": self.parent.ui.d_danger_height.value(),
                "danger_zone_x": self.parent.ui.e_danger_zone_x.value(),
                "danger_zone_y": self.parent.ui.f_danger_zone_y.value(),
            },
            "anchors": self.anchor_data,
            "anchor_count": self.parent.ui.g_anchorNum.value(),
            "tag_count": self.parent.ui.h_tagNum.value(),
            "tags": {f"Tag {i}": self.tag_names.get(f"Tag {i}", "None") for i in range(self.parent.ui.h_tagNum.value())}
        }

        # 데이터베이스에 저장
        self.save_workspace_to_db(workspace_name, workspace_data)

        # 현재 워크스페이스 이름 업데이트
        self.current_workspace_name = workspace_name
        self.calibration_handler.workspace_name = workspace_name  # 핸들러에 반영

        self.update_current_workspace(workspace_name)

    def apply_workspace_data(self, data):
        """
        UI에 워크스페이스 데이터를 적용하고 QFrame에 그림을 그림
        """
        workspace_settings = data.get("workspace_settings", {})
        self.parent.workspace_settings = workspace_settings

        self.parent.ui.a_workspace_width.setValue(workspace_settings.get("workspace_width", 0))
        self.parent.ui.b_workspace_height.setValue(workspace_settings.get("workspace_height", 0))
        self.parent.ui.c_danger_width.setValue(workspace_settings.get("danger_zone_width", 0))
        self.parent.ui.d_danger_height.setValue(workspace_settings.get("danger_zone_height", 0))
        self.parent.ui.e_danger_zone_x.setValue(workspace_settings.get("danger_zone_x", 0))
        self.parent.ui.f_danger_zone_y.setValue(workspace_settings.get("danger_zone_y", 0))
        self.parent.ui.g_anchorNum.setValue(data.get("anchor_count", 0))
        self.parent.ui.h_tagNum.setValue(data.get("tag_count", 0))

        # 태그 이름 업데이트
        self.tag_names = data.get("tags", {})
        self.update_tag_list()

        # 앵커 데이터 업데이트
        self.anchor_data = data.get("anchors", {})
        self.update_visible_anchors()

        # 앵커 위치 리스트 업데이트
        self.update_anchor_positions()

        # 첫 번째 앵커를 선택하고 X, Y 좌표 업데이트
        if self.anchor_data:
            first_anchor = list(self.anchor_data.keys())[0]
            self.parent.ui.i_anchorSelect.setCurrentText(first_anchor)
            self.update_anchor_position()  # SpinBox 값 갱신

        # 작업 공간 로드 상태 설정
        self.workspace_loaded = True

        # QFrame에 그림을 그리기 위해 draw_workspace_box 호출
        self.draw_workspace_box(
            x=0, y=0,
            workspace_width=workspace_settings.get("workspace_width", 0),
            workspace_height=workspace_settings.get("workspace_height", 0),
            danger_zone_x=workspace_settings.get("danger_zone_x", 0),
            danger_zone_y=workspace_settings.get("danger_zone_y", 0),
            danger_zone_width=workspace_settings.get("danger_zone_width", 0),
            danger_zone_height=workspace_settings.get("danger_zone_height", 0),
            anchors=self.anchor_data
        )
        self.parent.ui.workspace.update()  # 테두리 포함 다시 그리기


    def edit_workspace(self):
        if not hasattr(self, "current_workspace_name") or not self.current_workspace_name:
            QMessageBox.warning(self.parent, "Warning", "현재 열려 있는 워크스페이스가 없습니다.")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # 기존 데이터 조회
            cursor.execute("SELECT calibration, current FROM workspaces WHERE name = ?", (self.current_workspace_name,))
            row = cursor.fetchone()

            if row:
                calibration = row[0]
                current = row[1]
            else:
                calibration = None
                current = 0

            # 수정된 워크스페이스 데이터 생성
            workspace_data = {
                "workspace_settings": {
                    "workspace_width": self.parent.ui.a_workspace_width.value(),
                    "workspace_height": self.parent.ui.b_workspace_height.value(),
                    "danger_zone_width": self.parent.ui.c_danger_width.value(),
                    "danger_zone_height": self.parent.ui.d_danger_height.value(),
                    "danger_zone_x": self.parent.ui.e_danger_zone_x.value(),
                    "danger_zone_y": self.parent.ui.f_danger_zone_y.value(),
                },
                "anchors": self.anchor_data,
                "anchor_count": self.parent.ui.g_anchorNum.value(),
                "tag_count": self.parent.ui.h_tagNum.value(),
                "tags": {f"Tag {i}": self.tag_names.get(f"Tag {i}", "None") for i in
                         range(self.parent.ui.h_tagNum.value())}
            }

            # 데이터베이스 업데이트
            cursor.execute("""
                  UPDATE workspaces
                  SET data = ?, calibration = ?, current = ?
                  WHERE name = ?
              """, (json.dumps(workspace_data), calibration, current, self.current_workspace_name))

            conn.commit()

            # Update the workspace drawings
            self.apply_workspace_data(workspace_data)  # Apply changes to UI
            QMessageBox.information(self.parent, "Success",
                                    f"Workspace '{self.current_workspace_name}' updated successfully!")
        except sqlite3.Error as e:
            print(f"[ERROR] 워크스페이스 수정 실패: {e}")
        finally:
            conn.close()

    def update_anchor_position(self):
        """
        콤보박스에서 선택된 앵커의 X, Y 좌표를 SpinBox에 업데이트합니다.
        """
        # 콤보박스에서 선택된 앵커 이름 가져오기
        selected_anchor = self.parent.ui.i_anchorSelect.currentText()

        # 빈 문자열 제외
        if not selected_anchor.strip():
            return

        # 선택된 앵커가 anchor_data에 없으면 초기화 (값 0, 0으로 설정)
        if selected_anchor not in self.anchor_data:
            self.anchor_data[selected_anchor] = {"x": 0.0, "y": 0.0}

        # 선택된 앵커의 좌표 가져오기
        x = self.anchor_data[selected_anchor]["x"]
        y = self.anchor_data[selected_anchor]["y"]

        # SpinBox에 값 설정 (신호 차단으로 이벤트 중복 방지)
        self.parent.ui.j_anchorX.blockSignals(True)
        self.parent.ui.k_anchorY.blockSignals(True)
        self.parent.ui.j_anchorX.setValue(x)
        self.parent.ui.k_anchorY.setValue(y)
        self.parent.ui.j_anchorX.blockSignals(False)
        self.parent.ui.k_anchorY.blockSignals(False)

        # self.anchor_positions에도 업데이트
        try:
            # selected_anchor의 인덱스를 추출
            anchor_index = list(self.anchor_data.keys()).index(selected_anchor)

            # anchor_positions 크기를 동기화
            if len(self.anchor_positions) <= anchor_index:
                self.anchor_positions.extend([(0.0, 0.0)] * (anchor_index + 1 - len(self.anchor_positions)))

            # 현재 선택된 앵커의 좌표를 업데이트
            self.anchor_positions[anchor_index] = (x, y)
            # print(f"[DEBUG] Updated self.anchor_positions[{anchor_index}] to: {self.anchor_positions[anchor_index]}")
        except ValueError:
            print(f"[WARNING] Selected anchor '{selected_anchor}' not found in anchor_data.")

    def save_anchor_position(self):
        """
        SpinBox에서 입력된 X, Y 좌표를 현재 선택된 앵커에 저장합니다.
        """
        selected_anchor = self.parent.ui.i_anchorSelect.currentText()

        if selected_anchor in self.anchor_data:
            # SpinBox 값을 가져와서 저장
            x = self.parent.ui.j_anchorX.value()
            y = self.parent.ui.k_anchorY.value()
            self.anchor_data[selected_anchor]["x"] = x
            self.anchor_data[selected_anchor]["y"] = y

            # 앵커 위치 업데이트
            self.update_anchor_positions()

    # 앵커 표시 업데이트
    def update_visible_anchors(self):
        # print(f"[DEBUG] Updating visible anchors: {self.anchor_data.keys()}")  # 앵커 키 확인
        anchor_count = self.parent.ui.g_anchorNum.value()  # 표시할 앵커 수
        current_count = len(self.anchor_labels)

        # 앵커 추가
        if anchor_count > current_count:
            for i in range(current_count, anchor_count):
                anchor_name = f"Anchor {i}"
                # anchor_data에 기본값 추가
                self.anchor_data[anchor_name] = {"x": 0.0, "y": 0.0}

                # QLabel과 레이아웃 생성
                anchor_widget = QWidget(self.parent.ui.workspace)  # 하나의 위젯에 이미지와 텍스트 포함
                anchor_widget.setStyleSheet("background-color: transparent;")
                layout = QVBoxLayout(anchor_widget)
                layout.setContentsMargins(0, 0, 0, 0)  # 여백 제거
                layout.setSpacing(5)  # 이미지와 텍스트 사이 간격

                # 이미지 QLabel 생성
                image_label = QLabel(anchor_widget)
                pixmap = QPixmap(resource_path("modules/anchor.png"))
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(30, 30)  # 이미지 크기 조정
                    image_label.setPixmap(scaled_pixmap)
                    image_label.setAlignment(Qt.AlignCenter)

                    # QLabel 크기 확인
                    width = scaled_pixmap.width()
                    height = scaled_pixmap.height()
                    # print(f"Image QLabel size: width={width}, height={height}")

                # 텍스트 QLabel 생성
                text_label = QLabel(anchor_name, anchor_widget)
                text_label.setStyleSheet("font-size: 10px; color: white; font-weight: bold;")
                text_label.setAlignment(Qt.AlignCenter)

                # 레이아웃에 추가
                layout.addWidget(image_label)
                layout.addWidget(text_label)
                anchor_widget.setLayout(layout)

                # anchor_labels에 추가
                self.anchor_labels[anchor_name] = anchor_widget

                # UI에 표시
                anchor_widget.show()

        # 앵커 좌표 스케일링 및 QLabel 이동
        for anchor_name, coords in self.anchor_data.items():
            if anchor_name in self.anchor_labels:
                anchor_widget = self.anchor_labels[anchor_name]

                # 스케일링 적용
                if hasattr(self, "scale_ratio") and hasattr(self, "workspace_box"):
                    x_scaled = coords["x"] * self.scale_ratio + self.workspace_box.x()
                    y_scaled = coords["y"] * self.scale_ratio + self.workspace_box.y()
                    # QLabel 이동
                    anchor_widget.move(int(x_scaled), int(y_scaled))

        # 디버깅 출력
        # print(f"Anchor labels updated: {list(self.anchor_labels.keys())}")

    def initialize_anchor_labels(self):
        """
        화면 상에 앵커를 표시하기 위해 QLabel을 초기화합니다.
        """
        # 기존 레이블 삭제
        if hasattr(self, "anchor_labels"):
            for label in self.anchor_labels.values():
                label.deleteLater()  # 기존 QLabel 삭제
        self.anchor_labels = {}  # 새 레이블 초기화

        # 앵커 데이터 초기화
        self.anchor_data = {}

        # 앵커 개수 읽기
        anchor_count = self.parent.ui.g_anchorNum.value()

        # 앵커 위치 리스트 초기화
        self.anchor_positions = [(0.0, 0.0) for _ in range(anchor_count)]

        # 초기 업데이트 호출
        self.update_visible_anchors()

        # 앵커 데이터 기반 위치 업데이트
        self.update_anchor_positions()

    def update_anchor_settings(self):
        # 앵커 개수를 가져옴
        anchor_count = self.parent.ui.g_anchorNum.value()

        self.parent.anchor_data = {
            f"Anchor {i}": {"x": 0.0, "y": 0.0} for i in range(anchor_count)
        }

        # print("JEong", self.parent.anchor_data)

        self.parent.ui.i_anchorSelect.clear()

        # 앵커 개수에 따라 항목 추가
        for i in range(anchor_count):
            self.parent.ui.i_anchorSelect.addItem(f"Anchor {i}")

    def initialize_kalman_filters(self):
        """
        g_anchorNum 값에 따라 Kalman Filters를 초기화.
        """
        try:
            anchor_count = self.parent.ui.g_anchorNum.value()
            anchor_offsets = self.get_anchor_offsets()  # 앵커별 Offset 가져오기
            print(f"[DEBUG] Initializing Calculation with offsets: {anchor_offsets}")
            self.calculation = Calculation(anchor_count, anchor_offsets)  # Offsets 전달
        except Exception as e:
            print(f"Error initializing Kalman Filters: {e}")

    def update_anchor_positions(self):
        """
        `self.anchor_data`를 기반으로 `self.anchor_positions` 업데이트.
        """
        try:
            self.anchor_positions = []  # 앵커 위치 리스트 초기화
            for anchor_name, coords in self.anchor_data.items():
                if "x" in coords and "y" in coords:
                    self.anchor_positions.append((coords["x"], coords["y"]))
            # print(f"[DEBUG] Updated anchor positions: {self.anchor_positions}")  # 디버깅 출력
        except Exception as e:
            print(f"[ERROR] Failed to update anchor positions: {e}")

    '''
    def update_anchor_positions(self):
        """
        `self.anchor_data`를 기반으로 `self.anchor_positions`를 업데이트합니다.
        """
        try:
            # anchor_data의 길이 확인
            anchor_count = len(self.anchor_data)
            print(f"[DEBUG] Number of anchors in anchor_data: {anchor_count}")

            # anchor_positions 크기 조정
            if len(self.anchor_positions) != anchor_count:
                self.anchor_positions = [(0.0, 0.0) for _ in range(anchor_count)]
                print(f"[DEBUG] Resized anchor_positions to: {len(self.anchor_positions)}")

            print("[DEBUG] anchor_data 상태 확인:")
            for anchor_name, coords in self.anchor_data.items():
                print(f"  {anchor_name}: {coords}")

            # anchor_data를 기반으로 anchor_positions 업데이트
            for i, (anchor_name, coords) in enumerate(self.anchor_data.items()):
                if i < len(self.anchor_positions):
                    # x, y 값 유효성 확인
                    if "x" in coords and "y" in coords:
                        self.anchor_positions[i] = (coords["x"], coords["y"])
                        print(f"[DEBUG] Updated {anchor_name} to position: {self.anchor_positions[i]}")
                    else:
                        print(f"[WARNING] Missing 'x' or 'y' in coords for {anchor_name}: {coords}")
                else:
                    print(f"[WARNING] Skipping anchor {anchor_name} as it exceeds position array size.")

        except Exception as e:
            print(f"[ERROR] Failed to update anchor positions: {e}")'''

    def update_anchor_count(self):
        """
        g_anchorNum 값 변경 시 호출. 앵커 데이터를 업데이트.
        """
        try:
            # 앵커 라벨 및 데이터 초기화
            self.initialize_anchor_labels()

            # Kalman Filters 초기화
            self.initialize_kalman_filters()

            self.update_anchor_positions()

        except Exception as e:
            print(f"Error updating anchor count: {e}")

    # ///////////////////////////////////////////////////////////////
    # 데이터베이스 초기화
    # ///////////////////////////////////////////////////////////////
    def initialize_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 데이터베이스에 테이블 생성
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS workspaces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            data TEXT
            current INTEGER DEFAULT 0
        )
        """)

        try:
            cursor.execute("ALTER TABLE workspaces ADD COLUMN current INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            # print("[INFO] 'current' column already exists in the database.")
            pass

        conn.commit()
        conn.close()
        print("[INFO] Database initialized!")

    # 데이터베이스에 워크스페이스 저장
    def save_workspace_to_db(self, name, data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # 기존 워크스페이스 데이터 조회
            cursor.execute("SELECT calibration, current FROM workspaces WHERE name = ?", (name,))
            row = cursor.fetchone()

            # 기존 값 유지
            if row:
                calibration = row[0]
                current = row[1]
            else:
                calibration = None  # 초기값
                current = 0  # 기본값

            # INSERT 또는 UPDATE 시 기존 값 유지
            cursor.execute("""
                INSERT INTO workspaces (name, data, calibration, current)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    data = excluded.data,
                    calibration = COALESCE(excluded.calibration, workspaces.calibration),
                    current = COALESCE(excluded.current, workspaces.current)
            """, (name, json.dumps(data), calibration, current))

            conn.commit()
            print(f"[INFO] Workspace '{name}' saved to database.")
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to save workspace: {e}")
        finally:
            conn.close()

    # 데이터베이스에서 워크스페이스 가져오기
    def load_workspace_from_db(self, name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT data FROM workspaces WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                data = json.loads(row[0])  # JSON 데이터를 파싱
                print(f"[DEBUG] Loaded workspace data: {data}")  # 디버깅 출력
                return data
            else:
                print(f"[WARNING] Workspace '{name}' not found in database.")
                return None
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to load workspace: {e}")
            return None
        finally:
            conn.close()

    def get_workspace_list(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT name FROM workspaces")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to fetch workspace list: {e}")
            return []
        finally:
            conn.close()

    def load_last_workspace(self):
        """
        데이터베이스에서 마지막 작업장을 로드
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT name FROM workspaces WHERE current = 1")
            row = cursor.fetchone()
            if row:
                last_workspace_name = row[0]
                data = self.load_workspace_from_db(last_workspace_name)
                if data:
                    self.current_workspace_name = last_workspace_name
                    self.calibration_handler.workspace_name = last_workspace_name  # CalibrationHandler에 이름 전달
                    self.apply_workspace_data(data)
                    print(f"[INFO] Automatically loaded last workspace: {last_workspace_name}")
                else:
                    print("[WARNING] Failed to load workspace data.")
                    self.current_workspace_name = None
            else:
                print("[INFO] No recent workspace found.")
                self.current_workspace_name = None
        finally:
            conn.close()

    def update_current_workspace(self, workspace_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            # 모든 워크스페이스의 current 값을 0으로 초기화
            cursor.execute("UPDATE workspaces SET current = 0")
            # 선택한 워크스페이스의 current 값을 1로 설정
            cursor.execute("UPDATE workspaces SET current = 1 WHERE name = ?", (workspace_name,))
            conn.commit()
            print(f"[INFO] Updated current workspace to: {workspace_name}")
        finally:
            conn.close()

    # ///////////////////////////////////////////////////////////////
    # active, inactive Button 관련 설정
    # ///////////////////////////////////////////////////////////////

    def initialize_buttons(self):
        """
        activeButton과 inactiveButton을 초기화하고 기본 설정을 적용합니다.
        """
        active_button = self.parent.ui.activeButton
        inactive_button = self.parent.ui.inactiveButton

        # inactiveButton 초기 배경색 설정
        self.set_button_background(inactive_button, "#de1d1d")
        self.set_button_background(active_button, None)

        # 버튼 클릭 이벤트 연결
        self.parent.ui.activeButton.pressed.connect(self.handle_active_button)
        self.parent.ui.inactiveButton.pressed.connect(self.handle_inactive_button)

    def set_button_background(self, button, background_color, text_color="white"):
        """
        버튼의 배경색과 텍스트 색상을 설정합니다.
        """
        if background_color:
            button.setStyleSheet(
                f"""
                    background-color: {background_color};
                    color: {text_color};
                    font-weight: bold;
                    """
            )
        else:
            button.setStyleSheet("")

    def handle_active_button(self):
        """
        Active 버튼 클릭 시 동작 정의.

        if self.tag_in_danger_zone:
            QMessageBox.warning(self.parent, "Warning", "태그가 위험 구역 안에 있습니다. Active 버튼을 누를 수 없습니다.")
            return
        """

        # Active 버튼 배경색 초록색으로 설정
        self.set_button_background(self.parent.ui.activeButton, "#4fd746", "black")
        # Inactive 버튼 배경색 제거
        self.set_button_background(self.parent.ui.inactiveButton, None)

        # Danger zone 테두리를 초록색으로 변경
        self.danger_color = QColor(0, 255, 0)  # 초록색
        self.parent.ui.workspace.update()  # 화면 갱신

    def handle_inactive_button(self):
        """
        Inactive 버튼 클릭 시 동작 정의.
        """
        # Inactive 버튼 배경색 빨간색으로 설정
        self.set_button_background(self.parent.ui.inactiveButton, "#de1d1d", "white")
        # Active 버튼 배경색 제거
        self.set_button_background(self.parent.ui.activeButton, None)

        # Danger zone 테두리를 빨간색으로 변경
        self.danger_color = QColor(255, 0, 0)  # 빨간색
        self.parent.ui.workspace.update()  # 화면 갱신