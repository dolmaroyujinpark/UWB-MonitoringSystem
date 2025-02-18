from PySide6.QtWidgets import QMessageBox, QApplication, QLabel
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QPainter, QPen
from collections import defaultdict
import time
import re
import json
from sklearn.linear_model import LinearRegression
import numpy as np
import math
import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 기준 디렉토리

class CalibrationHandler:
    def __init__(self, workspace, checkbox, parent, app_functions, scaled_width=0, scaled_height=0, x_offset=0,
                 y_offset=0,
                 scale_ratio=None, serial_handler=None, anchor_positions=None, workspace_name=None):

        self.workspace_name = workspace_name  # 이름 저장
        self.workspace = workspace  # workspace 저장
        self.checkbox = checkbox
        self.parent = parent
        self.scaled_width = scaled_width
        self.scaled_height = scaled_height
        self.app_functions = app_functions  # AppFunctions 참조 저장
        self.x_offset = x_offset  # 가로 오프셋
        self.y_offset = y_offset  # 세로 오프셋
        self.scale_ratio = scale_ratio
        self.calibration_active = False
        self.checkbox.stateChanged.connect(self.handle_checkbox_state)
        self.serial_handler = serial_handler  # SerialHandler 저장
        self.anchor_positions = anchor_positions
        # 기존 초기화 코드
        self.offset_values = defaultdict(dict)  # 오프셋 값을 저장할 속성 초기화




        # 캘리브레이션 데이터 저장용
        self.calibration_data = defaultdict(list)  # 앵커별 캘리브레이션 데이터


    '''def save_anchor_offsets_to_db(self, db_path, theoretical_distances):
        """
        JSON 파일 없이 동일한 계산 방식으로 평균 Offset 값을 데이터베이스에 저장.
        """
        try:
            workspace_name = self.workspace_name or "Unknown_Workspace"
            if not workspace_name:
                raise ValueError("Workspace name is not set.")

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # 테이블 확인
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='workspaces';")
            if not cursor.fetchone():
                print("[ERROR] Table 'workspaces' does not exist.")
                conn.close()
                return

            # 캘리브레이션 데이터를 사용하여 계산
            anchor_data_with_details = defaultdict(dict)

            for anchor_key, data in self.calibration_data.items():  # self.calibration_data에서 데이터 가져옴
                for point_key, point_data in data.items():
                    if anchor_key in theoretical_distances and point_key in theoretical_distances[anchor_key]:
                        theoretical_distance = np.mean(theoretical_distances[anchor_key][point_key])
                        measured_ranges = point_data.get("range", [])

                        if measured_ranges:
                            average_measured = np.mean(measured_ranges)
                            offset = average_measured - theoretical_distance

                            # 데이터를 저장
                            anchor_data_with_details[anchor_key][point_key] = {
                                "theoretical_distance": theoretical_distance,
                                "measured_ranges": measured_ranges,
                                "offset": offset,
                            }

            # 앵커별 평균 Offset 계산
            average_offsets = {}
            for anchor_key, points in anchor_data_with_details.items():
                offsets = [point_data["offset"] for point_data in points.values()]
                average_offset = np.mean(offsets) if offsets else 0
                average_offsets[anchor_key] = average_offset
                print(f"[INFO] save_anchor_position_to_db Anchor: {anchor_key}, Average Offset: {average_offset:.2f}")

            # 평균 Offset 데이터를 JSON 문자열로 변환하여 DB에 저장
            calibration_data = json.dumps(average_offsets)
            print(f"[DEBUG] Serialized calibration data for DB: {calibration_data}")

            # 기존 데이터 검색
            cursor.execute("SELECT id FROM workspaces WHERE name = ?", (workspace_name,))
            row = cursor.fetchone()

            if row:
                # 기존 데이터 업데이트
                cursor.execute("""
                    UPDATE workspaces
                    SET calibration = ?
                    WHERE name = ?
                """, (calibration_data, workspace_name))
                print(f"[INFO] Updated calibration data for workspace: {workspace_name}")
            else:
                # 새 데이터 삽입
                cursor.execute("""
                    INSERT INTO workspaces (name, data, current, calibration)
                    VALUES (?, '{}', 1, ?)
                """, (workspace_name, calibration_data))
                print(f"[INFO] Inserted new workspace with calibration data: {workspace_name}")

            conn.commit()
            conn.close()
            print("[INFO] Calibration data saved successfully.")
        except Exception as e:
            print(f"[ERROR] 평균 Offset 저장 중 오류 발생: {e}")'''




    def calculate_theoretical_distances(self, anchor_positions):
        """
        이론적 거리 값을 계산하여 반환.
        :param anchor_positions: 앵커 좌표
        :return: 딕셔너리 구조로 이론적 거리 값 반환
        """
        theoretical_distances = {}
        for anchor, anchor_pos in anchor_positions.items():
            theoretical_distances[anchor] = {}
            for idx, (actual_x, actual_y) in enumerate(self.actual_coordinates, start=1):
                point_key = f"point_{idx}"
                # 유클리드 거리 계산
                distance = ((anchor_pos["x"] - actual_x) ** 2 + (anchor_pos["y"] - actual_y) ** 2) ** 0.5
                print(f'distance {distance}')
                print(f'scale_ratio: {self.scale_ratio}')
                # scale_ratio로 나누고 센티미터로 변환

                distance_cm = (distance * 100)
                print(f"[DEBUG] Anchor: {anchor}, Point: {point_key}, Distance (cm): {distance_cm}")

                if point_key not in theoretical_distances[anchor]:
                    theoretical_distances[anchor][point_key] = []
                theoretical_distances[anchor][point_key].append(distance_cm)
        return theoretical_distances

    def show_loading_message(self, message="데이터 수집 중..."):
        """로딩 메시지를 표시"""
        self.loading_label = QLabel(self.workspace)
        self.loading_label.setGeometry(self.workspace.width() // 2 - 100, self.workspace.height() // 2 - 50, 200, 50)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.8);
            color: white;
            border-radius: 10px;
            font-size: 16px;
        """)
        self.loading_label.setText(message)
        self.loading_label.show()
        QApplication.processEvents()  # 즉시 화면에 갱신

    def hide_loading_message(self):
        """로딩 메시지를 숨김"""
        if hasattr(self, "loading_label") and self.loading_label:
            self.loading_label.hide()
            self.loading_label.deleteLater()
            del self.loading_label

    def perform_offset_calculation_and_update_json(self, input_filename, output_filename, theoretical_distances):
        """
        JSON 파일을 읽어 평균 Offset만 계산하지 않고 모든 데이터를 저장합니다.
        :param input_filename: 입력 JSON 파일 이름
        :param output_filename: 출력 JSON 파일 이름
        :param theoretical_distances: 이론적 거리 값 (딕셔너리 구조)
        """
        try:
            with open(input_filename, "r", encoding="utf-8") as json_file:
                json_data = json.load(json_file)

            anchor_data_with_details = defaultdict(dict)

            # 각 앵커와 포인트에 대해 데이터를 구성
            for anchor_key, anchor_data in json_data.items():
                for point_key, point_data in anchor_data.items():
                    if anchor_key in theoretical_distances and point_key in theoretical_distances[anchor_key]:
                        theoretical_distance = np.mean(theoretical_distances[anchor_key][point_key])
                        measured_ranges = point_data.get("range", [])

                        if measured_ranges:
                            average_measured = np.mean(measured_ranges)
                            offset = average_measured - theoretical_distance

                            # 데이터를 저장
                            anchor_data_with_details[anchor_key][point_key] = {
                                "theoretical_distance": theoretical_distance,
                                "measured_ranges": measured_ranges,
                                "offset": offset,
                            }

            # 앵커별 평균 Offset 계산
            average_offset_data = {}
            for anchor_key, points in anchor_data_with_details.items():
                offsets = [point_data["offset"] for point_data in points.values()]
                average_offset = np.mean(offsets) if offsets else 0
                average_offset_data[anchor_key] = {
                    "details": points,
                    "average_offset": average_offset,
                }
                #print(f"[INFO] Anchor: {anchor_key}, Average Offset: {average_offset:.2f}")

            # 결과를 새로운 파일로 저장
            with open(output_filename, "w", encoding="utf-8") as json_file:
                json.dump(average_offset_data, json_file, indent=4)
            print(f"[INFO] Updated JSON with detailed data saved to {output_filename}")

        except Exception as e:
            print(f"[ERROR] Failed to calculate offsets: {e}")


    #추후에 재구조화 코드 따로 빼줘서 전달하도록 하자,,,,!
    def save_calibration_data_to_json(self, filename="calibration_data.json"):
        """캘리브레이션 데이터를 JSON 파일로 저장 (앵커 기준)"""
        try:
            # 앵커 기준으로 재구조화
            anchor_data = defaultdict(lambda: defaultdict(dict))
            for point, data in self.calibration_data.items():
                for anchor, values in data.items():
                    anchor_data[anchor][point] = values

            # JSON 파일로 저장
            with open(filename, "w", encoding="utf-8") as json_file:
                json.dump(anchor_data, json_file, indent=4)
            print(f"[INFO] Calibration data saved to {filename}")
        except Exception as e:
            print(f"[ERROR] Failed to save calibration data to JSON: {e}")

    def collect_calibration_data(self, duration=5, anchor_count=3, interval=0.1):
        collected_data = {f"Anchor {i}": {"range": [], "rssi": []} for i in range(anchor_count)}

        start_time = time.time()
        while time.time() - start_time < duration:
            data = self.app_functions.latest_serial_data  # 시리얼 데이터 읽기
            if data:
                try:
                    # range와 rssi 추출
                    range_match = re.search(r"range:\(([\d.,\- ]+)\)", data)
                    rssi_match = re.search(r"rssi:\(([\d.,\- ]+)\)", data)

                    if range_match:
                        range_values = list(map(float, range_match.group(1).split(",")))
                        for i, val in enumerate(range_values[:anchor_count]):
                            collected_data[f"Anchor {i}"]["range"].append(val)

                    if rssi_match:
                        rssi_values = list(map(float, rssi_match.group(1).split(",")))
                        for i, val in enumerate(rssi_values[:anchor_count]):
                            collected_data[f"Anchor {i}"]["rssi"].append(val)

                except Exception as e:
                    print(f"[ERROR] Error processing serial data: {e}")

            # 데이터 수집 간격
            time.sleep(interval)

        print("[INFO] Calibration data collection completed.")
        print(f"[DEBUG] Collected data: {json.dumps(collected_data, indent=4)}")
        return collected_data

    def collect_and_store_data(self):
        """현재 점에서 데이터를 수집하고 저장"""
        # 5초 동안 데이터 수집
        calibration_data = self.collect_calibration_data(duration=4, anchor_count=3)

        # 수집된 데이터 저장
        self.calibration_data[f"point_{self.current_calibration_index + 1}"] = calibration_data

        # JSON 파일로 저장
        self.save_calibration_data_to_json()

        # 현재 점 색상을 파란색으로 변경
        if self.current_calibration_index < len(self.calibration_labels):
            label = self.calibration_labels[self.current_calibration_index]
            label.setStyleSheet("background-color: blue; border-radius: 10px;")
            print(f"[DEBUG] Point {self.current_calibration_index + 1} color changed to blue.")

        # 로딩 메시지 숨김
        self.hide_loading_message()

        # 다음 점으로 이동
        self.current_calibration_index += 1
        self.prompt_next_calibration_point()

    def save_offsets_to_db(self, db_path, theoretical_distances, calibration_data, workspace_name="Unknown_Workspace"):
        """
        이론적 거리 값과 캘리브레이션 데이터를 기반으로 오프셋을 계산하고 데이터베이스에 저장합니다.
        """
        try:
            print(f"[DEBUG] Starting save_offsets_to_db")
            print(f"[DEBUG] Database path: {db_path}")
            print(f"[DEBUG] Workspace name: {workspace_name}")

            # 앵커 기준으로 재구조화
            anchor_data = defaultdict(lambda: defaultdict(dict))
            for point, data in calibration_data.items():
                for anchor, values in data.items():
                    anchor_data[anchor][point] = values

            print(f"[DEBUG] Restructured calibration_data: {json.dumps(anchor_data, indent=4)}")

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("""
               CREATE TABLE IF NOT EXISTS workspaces (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT UNIQUE,
                   calibration TEXT
               )
            """)

            anchor_data_with_details = defaultdict(dict)
            for anchor_key, points in anchor_data.items():
                print(f"[DEBUG] Processing anchor: {anchor_key}")
                for point_key, point_data in points.items():
                    if anchor_key in theoretical_distances and point_key in theoretical_distances[anchor_key]:
                        theoretical_distance = np.mean(theoretical_distances[anchor_key][point_key])
                        measured_ranges = point_data.get("range", [])
                        print(f"[DEBUG] Theoretical distance: {theoretical_distance}")
                        print(f"[DEBUG] Measured ranges: {measured_ranges}")

                        if measured_ranges:
                            average_measured = np.mean(measured_ranges)
                            offset = average_measured - theoretical_distance
                            print(f"[DEBUG] Offset for anchor: {anchor_key}, point: {point_key}, offset: {offset:.2f}")

                            anchor_data_with_details[anchor_key][point_key] = {
                                "theoretical_distance": theoretical_distance,
                                "measured_ranges": measured_ranges,
                                "offset": offset,
                            }
                        else:
                            print(f"[WARNING] Measured ranges are empty for anchor: {anchor_key}, point: {point_key}")

            average_offsets = {}
            print(f"[DEBUG] Calculating average offsets per anchor.")
            for anchor_key, points in anchor_data_with_details.items():
                offsets = [point_data["offset"] for point_data in points.values()]
                average_offset = np.mean(offsets) if offsets else 0
                average_offsets[anchor_key] = average_offset
                print(f"[INFO] Anchor: {anchor_key}, Average Offset: {average_offset:.2f}")

            calibration_json = json.dumps(average_offsets)
            print(f"[DEBUG] Serialized calibration data: {calibration_json}")

            cursor.execute("SELECT id FROM workspaces WHERE name = ?", (workspace_name,))
            row = cursor.fetchone()

            if row:
                print(f"[DEBUG] Updating existing workspace: {workspace_name}")
                cursor.execute("""
                       UPDATE workspaces
                       SET calibration = ?
                       WHERE name = ?
                   """, (calibration_json, workspace_name))
            else:
                print(f"[DEBUG] Inserting new workspace: {workspace_name}")
                cursor.execute("""
                       INSERT INTO workspaces (name, calibration)
                       VALUES (?, ?)
                   """, (workspace_name, calibration_json))

            conn.commit()
            conn.close()
            print("[INFO] Calibration data saved successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to save calibration data to database: {e}")

    def end_calibration_process(self):
        """캘리브레이션 프로세스 종료 및 데이터베이스 저장"""
        self.calibration_active = False

        dialog = QMessageBox()
        dialog.setWindowTitle("캘리브레이션 완료")
        dialog.setText("모든 캘리브레이션 작업이 완료되었습니다. 데이터를 저장합니다.")
        dialog.setStandardButtons(QMessageBox.Ok)
        response = dialog.exec()

        if response == QMessageBox.Ok:
            self.remove_calibration_points()
            theoretical_distances = self.calculate_theoretical_distances(self.anchor_positions)

            input_filename = "calibration_data.json"
            output_filename = "calibration_data_with_offsets.json"
            self.perform_offset_calculation_and_update_json(input_filename, output_filename, theoretical_distances)

            db_path = os.path.join(base_dir, "workspace.db")
            self.save_offsets_to_db(
                db_path=db_path,
                theoretical_distances=theoretical_distances,
                calibration_data=self.calibration_data,
                workspace_name=self.workspace_name
            )
            # Kalman 필터를 완전히 다시 초기화
            self.app_functions.initialize_kalman_filters()

            completion_dialog = QMessageBox()
            completion_dialog.setWindowTitle("캘리브레이션 완료")
            completion_dialog.setText("캘리브레이션 데이터가 JSON 파일 및 데이터베이스에 저장되었습니다.")
            completion_dialog.setStandardButtons(QMessageBox.Ok)
            completion_dialog.exec()

    def show_calibration_labels(self):
        """캘리브레이션 점을 다시 화면에 표시"""
        for label in self.calibration_labels:
            label.show()  # QLabel을 다시 화면에 표시

    def handle_checkbox_state(self, state):
        """체크박스 상태 변경 시 호출"""
        if state == 2:  # 체크박스 ON 상태
            if not self.calibration_active:
                self.show_confirmation_dialog()

    def show_confirmation_dialog(self):
        """캘리브레이션 진행 여부 확인"""
        dialog = QMessageBox()
        dialog.setWindowTitle("Calibration")
        dialog.setText("캘리브레이션을 진행하시겠습니까?")
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.Yes)
        response = dialog.exec()

        if response == QMessageBox.Yes:
            self.start_calibration_mode()
        else:
            self.calibration_active = False
            self.checkbox.setCheckState(Qt.CheckState.Unchecked)  # 체크박스 해제
            self.checkbox.setChecked(False)

    def start_calibration_mode(self):
        """캘리브레이션 모드 시작"""

        if not self.workspace_name:  # 워크스페이스 이름 확인
            QMessageBox.critical(
                self.parent,
                "Error",
                "Workspace name is not set. Please select or create a workspace before starting calibration."
            )
            self.calibration_active = False
            self.checkbox.setCheckState(Qt.CheckState.Unchecked)  # 체크박스 해제
            return


        print("[DEBUG] Starting calibration mode")
        self.calibration_active = True

        # 4등분 기준 교차점 좌표 계산
        horizontal_step = self.scaled_width / 4
        vertical_step = self.scaled_height / 4

        calibration_points = [
            QPoint(
                int(self.x_offset + horizontal_step * i),
                int(self.y_offset + vertical_step * j)
            )
            for i in range(1, 4)
            for j in range(1, 4)
        ]

        self.show_calibration_points(calibration_points)
        self.start_calibration_process()

    def show_calibration_points(self, points):
        """캘리브레이션 점을 화면에 표시하고, 실제 좌표 계산"""
        self.remove_calibration_points()  # 기존 점 제거

        self.calibration_labels = []  # QLabel 저장
        self.actual_coordinates = []  # 실제 좌표 저장

        # 캘리브레이션 점 선택 (2, 4, 5, 6, 8번)
        selected_points = [2, 4, 5, 6, 8]
        calibration_order = list(range(1, len(points) + 1))  # 1번부터 시작하는 순서
        selected_indices = [i for i, point_num in enumerate(calibration_order) if point_num in selected_points]

        for idx in selected_indices:
            point = points[idx]
            # 화면에 동그라미 표시
            label = QLabel(self.workspace)
            label.setGeometry(point.x() - 10, point.y() - 10, 20, 20)  # 점 크기 20x20
            label.setStyleSheet("background-color: red; border-radius: 10px;")  # 동그라미 채우기
            label.show()  # QLabel 화면에 표시
            self.calibration_labels.append(label)  # QLabel 저장

            # 실제 좌표 계산
            actual_x = (point.x() - self.x_offset) / self.scale_ratio
            actual_y = (point.y() - self.y_offset) / self.scale_ratio
            self.actual_coordinates.append((actual_x, actual_y))  # 실제 좌표 저장

            print(f"[DEBUG] Label created at: {label.geometry()}")  # QLabel 위치 확인

        # 화면 강제 갱신
        QApplication.processEvents()
        print("[DEBUG] Calibration points displayed.")

    def update_current_calibration_point(self, index):
        """현재 캘리브레이션 점 업데이트"""
        for i, label in enumerate(self.calibration_labels):
            label.hide()  # 모든 점 숨김

    def remove_calibration_points(self):
        """캘리브레이션 점을 화면에서 제거"""
        if hasattr(self, "calibration_labels"):
            for label in self.calibration_labels:
                if label:
                    print(f"[DEBUG] Removing label: {label.geometry()}")
                    label.hide()  # QLabel 숨기기
                    label.deleteLater()  # QLabel 삭제 요청
            self.calibration_labels.clear()  # 목록 초기화

        QApplication.processEvents()
        print("[DEBUG] Calibration points removed.")

    def start_calibration_process(self):
        """캘리브레이션 프로세스 시작"""
        self.current_calibration_index = 0  # 초기 인덱스
        self.prompt_next_calibration_point()

    def prompt_next_calibration_point(self):
        """현재 캘리브레이션 점에 대해 사용자에게 메시지 표시"""
        if self.current_calibration_index < len(self.actual_coordinates):
            actual_x, actual_y = self.actual_coordinates[self.current_calibration_index]

            # 안내 메시지 표시
            message = f"태그를 (가로 {actual_x:.2f}m, 세로 {actual_y:.2f}m)에 두고 확인을 눌러주세요."
            dialog = QMessageBox()
            dialog.setWindowTitle("캘리브레이션 안내")
            dialog.setText(message)
            dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            response = dialog.exec()

            if response == QMessageBox.Ok:
                # 로딩 메시지 표시
                self.show_loading_message("데이터 수집 중...")

                # 데이터 수집 시작 (로딩 메시지가 보장된 후 실행)
                self.collect_and_store_data()


            elif response == QMessageBox.Cancel:

                # 캘리브레이션 상태 비활성화 및 체크박스 해제

                self.calibration_active = False

                self.checkbox.setCheckState(Qt.CheckState.Unchecked)  # 체크박스 상태 해제

                self.checkbox.setChecked(False)

                # 캘리브레이션 점 제거

                self.remove_calibration_points()

                print("[INFO] Calibration process stopped by user.")
        else:
            self.end_calibration_process()

    def move_to_next_calibration_point(self):
        """다음 캘리브레이션 점으로 이동"""
        self.current_calibration_index += 1  # 다음 점으로 이동
        self.prompt_next_calibration_point()

    def update_calibration_points(self):
        """화면 크기 변경 시 캘리브레이션 점 좌표 업데이트"""
        if not self.calibration_active:  # 캘리브레이션 진행 중이 아니면 무시
            return

        # 4등분 기준 교차점 좌표 재계산
        horizontal_step = self.scaled_width / 4
        vertical_step = self.scaled_height / 4

        updated_points = [
            QPoint(
                int(self.x_offset + horizontal_step * i),
                int(self.y_offset + vertical_step * j)
            )
            for i in range(1, 4)
            for j in range(1, 4)
        ]

        selected_points = [2, 4, 5, 6, 8]  # 선택된 캘리브레이션 점
        calibration_order = list(range(1, len(updated_points) + 1))
        selected_indices = [i for i, point_num in enumerate(calibration_order) if point_num in selected_points]

        # 점의 위치를 업데이트
        for idx, label in zip(selected_indices, self.calibration_labels):
            point = updated_points[idx]
            label.setGeometry(point.x() - 10, point.y() - 10, 20, 20)  # 새로운 위치 설정

        print("[DEBUG] Calibration points updated with new screen size.")