import sys
import math
import serial
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtCore import Qt

# 시리얼 포트 설정 (아두이노 연결 포트에 맞게 수정)
SERIAL_PORT = 'COM3'
BAUD_RATE = 115200
TIMEOUT = 1

# PyQt5 설정
ANCHOR_RADIUS = 10
TAG_RADIUS = 10
SCENE_WIDTH = 800
SCENE_HEIGHT = 600
METER_TO_PIXEL = 100

# 앵커 위치 (미터 단위)
pos_a1 = (0, 0)
pos_a2 = (2.81, 0)
pos_a3 = (0.5, 1.55)

# 거리 보정값 및 무빙 어베리지
range_offset = 0.5
window_size = 5

class Calculation:
    def __init__(self):
        self.distance_history = {
            "anchor_self": [],
            "anchor_b": [],
            "anchor_c": []
        }

    def moving_average(self, new_value, history_key):
        history = self.distance_history[history_key]
        history.append(new_value)
        if len(history) > window_size:
            history.pop(0)
        return sum(history) / len(history)

    def apply_correction_and_ma(self, raw_range, anchor_key):
        corrected_range = max(raw_range - range_offset, 0)
        averaged_range = self.moving_average(corrected_range, anchor_key)
        return averaged_range

    def circle_intersections(self, c1, r1, c2, r2):
        x1, y1 = c1
        x2, y2 = c2
        d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        print(f"Circle 1 Center: {c1}, Radius: {r1}")
        print(f"Circle 2 Center: {c2}, Radius: {r2}")
        print(f"Distance between centers: {d}")

        if d > r1 + r2 or d < abs(r1 - r2) or d == 0:
            print("No intersections: Circles do not meet or are concentric.")
            return None

        a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(r1 ** 2 - a ** 2)

        x3 = x1 + a * (x2 - x1) / d
        y3 = y1 + a * (y2 - y1) / d

        offset_x = h * (y2 - y1) / d
        offset_y = h * (x2 - x1) / d

        intersection1 = (x3 + offset_x, y3 - offset_y)
        intersection2 = (x3 - offset_x, y3 + offset_y)

        print(f"Intersections: {intersection1}, {intersection2}")
        return intersection1, intersection2

    def closest_point(self, points, target):
        """
        교점 중 target에 가장 가까운 점을 선택합니다.
        """
        return min(points, key=lambda p: math.sqrt((p[0] - target[0]) ** 2 + (p[1] - target[1]) ** 2))

    def refined_trilateration(self, a1_range, a2_range, a3_range):
        points = []

        # A1 and A2
        intersections = self.circle_intersections(pos_a1, a1_range, pos_a2, a2_range)
        print(f"A1 and A2 Intersections: {intersections}")  # 디버깅 출력
        if intersections:
            points.append(self.closest_point(intersections, pos_a3))

        # A2 and A3
        intersections = self.circle_intersections(pos_a2, a2_range, pos_a3, a3_range)
        print(f"A2 and A3 Intersections: {intersections}")  # 디버깅 출력
        if intersections:
            points.append(self.closest_point(intersections, pos_a1))

        # A3 and A1
        intersections = self.circle_intersections(pos_a3, a3_range, pos_a1, a1_range)
        print(f"A3 and A1 Intersections: {intersections}")  # 디버깅 출력
        if intersections:
            points.append(self.closest_point(intersections, pos_a2))

        if len(points) == 3:
            x = sum(p[0] for p in points) / 3
            y = sum(p[1] for p in points) / 3
            return round(x, 2), round(y, 2)

        print("Not enough valid points for trilateration.")  # 디버깅 출력
        return None, None


class UWBVisualization(QMainWindow):
    def __init__(self):
        super().__init__()
        self.anchor_labels = {}  # 초기화를 가장 먼저 수행
        self.initUI()
        self.serial = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
        self.calculation = Calculation()

    def initUI(self):
        self.setWindowTitle('UWB Visualization')
        self.setGeometry(100, 100, SCENE_WIDTH, SCENE_HEIGHT)

        # 그래픽 장면 및 뷰 설정
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        # 앵커 그리기
        self.draw_anchor(pos_a1, "A1")
        self.draw_anchor(pos_a2, "A2")
        self.draw_anchor(pos_a3, "A3")

        # 태그 아이템 초기화
        self.tag_item = QGraphicsEllipseItem()
        self.tag_item.setRect(-TAG_RADIUS, -TAG_RADIUS, TAG_RADIUS * 2, TAG_RADIUS * 2)
        self.tag_item.setBrush(Qt.blue)
        self.scene.addItem(self.tag_item)

        self.tag_label = QGraphicsTextItem()
        self.scene.addItem(self.tag_label)

    def draw_anchor(self, pos, label):
        x, y = pos
        x_px = x * METER_TO_PIXEL
        y_px = y * METER_TO_PIXEL  # PyQt 좌표계에서는 아래로 증가하므로 그대로 사용

        anchor = QGraphicsEllipseItem()
        anchor.setRect(x_px - ANCHOR_RADIUS, y_px - ANCHOR_RADIUS, ANCHOR_RADIUS * 2, ANCHOR_RADIUS * 2)
        anchor.setBrush(Qt.green)
        self.scene.addItem(anchor)

        text = QGraphicsTextItem(label)
        text.setPos(x_px, y_px - 20)  # 텍스트를 약간 위에 배치
        self.scene.addItem(text)

        # 거리 정보 텍스트 추가
        distance_label = QGraphicsTextItem()
        distance_label.setPos(x_px + 20, y_px)
        self.scene.addItem(distance_label)
        self.anchor_labels[label] = distance_label

    def update_anchor_distance(self, label, distance):
        if label in self.anchor_labels:
            self.anchor_labels[label].setPlainText(f"{distance:.2f} m")

    def update_tag_position(self, x, y):
        x_px = x * METER_TO_PIXEL
        y_px = y * METER_TO_PIXEL  # PyQt 좌표계 그대로 사용

        self.tag_item.setPos(x_px - TAG_RADIUS, y_px - TAG_RADIUS)  # 원 중심 위치 보정
        self.tag_label.setPlainText(f"Tag: ({x:.2f}, {y:.2f})")
        self.tag_label.setPos(x_px + 10, y_px - 10)
        print(f"Tag Position Updated: ({x}, {y})")  # 콘솔 출력

    def process_serial_data(self):
        try:
            line = self.serial.readline().decode('utf-8').strip()
            if line:
                data = json.loads(line)

                # 원본 거리값을 읽음
                a1_raw = data["anchor_self"]
                a2_raw = data["anchor_b"]
                a3_raw = data["anchor_c"]

                # 거리 보정값 및 무빙 어베리지 적용
                a1_range = self.calculation.apply_correction_and_ma(a1_raw, "anchor_self")
                a2_range = self.calculation.apply_correction_and_ma(a2_raw, "anchor_b")
                a3_range = self.calculation.apply_correction_and_ma(a3_raw, "anchor_c")

                # 콘솔 출력 (무빙 어베리지가 적용된 거리값)
                print(f"Anchor A1 (0,0): {a1_range:.2f} m")
                print(f"Anchor A2 (1.2,0): {a2_range:.2f} m")
                print(f"Anchor A3 (1.5,1.35): {a3_range:.2f} m")

                # 화면 업데이트 (무빙 어베리지가 적용된 거리값)
                self.update_anchor_distance("A1", a1_range)
                self.update_anchor_distance("A2", a2_range)
                self.update_anchor_distance("A3", a3_range)

                # 개선된 삼변측량법을 통해 태그의 위치 계산
                x, y = self.calculation.refined_trilateration(a1_range, a2_range, a3_range)
                if x is not None and y is not None:
                    print(f"Calculated Tag Position: x={x}, y={y}")  # 콘솔 출력
                    self.update_tag_position(x, y)

        except json.JSONDecodeError:
            print("Invalid JSON received.")
        except Exception as e:
            print(f"Error: {e}")

    def start(self):
        while True:
            self.process_serial_data()
            QApplication.processEvents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UWBVisualization()
    window.show()
    window.start()
