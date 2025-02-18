# calculation.py

import math

# 거리 보정값 및 무빙 어베리지
range_offset = 0.4
window_size = 5

class KalmanFilter:
    def __init__(self, process_variance, measurement_variance):
        self.process_variance = process_variance  # 프로세스 노이즈
        self.measurement_variance = measurement_variance  # 측정 노이즈
        self.estimate = 0  # 초기 추정값
        self.error_estimate = 1  # 초기 오차 추정값

    def update(self, measurement):
        # 칼만 게인 계산
        kalman_gain = self.error_estimate / (self.error_estimate + self.measurement_variance)

        # 추정 업데이트
        self.estimate = self.estimate + kalman_gain * (measurement - self.estimate)

        # 오차 추정 업데이트
        self.error_estimate = (1 - kalman_gain) * self.error_estimate + abs(
            self.estimate - measurement) * self.process_variance

        return self.estimate

class Calculation:
    def __init__(self, anchor_count, anchor_offsets = None):
        """
        :param anchor_count: 동적으로 설정된 앵커 수
        """

        self.anchor_offsets = anchor_offsets
        self.kalman_filters = {
            f"Anchor {i}": KalmanFilter(process_variance=0.1, measurement_variance=0.1)
            for i in range(anchor_count)
        }
        print(f"Kalman Filters Initialized: {list(self.kalman_filters.keys())}")

    def moving_average(self, new_value, history_key):
        history = self.distance_history[history_key]
        history.append(new_value)
        if len(history) > window_size:  # window_size 설정
            history.pop(0)
        return sum(history) / len(history)

    '''def apply_correction_and_kf(self, raw_range, anchor_key):
            # Linear regression coefficients
            a = 0.79987778
            b = -25.89960738

            # Apply the linear regression function
            linear_corrected_range = max((a * raw_range + b) * 0.01, 0)

            # Apply the Kalman filter
            filtered_range = self.kalman_filters[anchor_key].update(linear_corrected_range)

            #print(f'필터 적용: {filtered_range}')
            return filtered_range'''

    """def apply_correction_and_kf(self, raw_range, anchor_key):
        #print(f'raw range: {raw_range}')
        '''
        # cm단위인데 잘못 if문 적용했음!!!!! 나중에 적용하면 다시 바꾸기
        if raw_range <= 0.5:
            range_offset = 0.1
        elif 0.5 < raw_range and raw_range <= 0.8:
            range_offset = 0.2
        elif 0.8 < raw_range and raw_range <= 1:
            range_offset = 0.3
        else:
            range_offset = 0.5'''
        #range_offset = 0.7

        if raw_range > 300:
            range_offset = 0.9
        else:
            range_offset = 0.45


        corrected_range = max(((raw_range)*0.01) - range_offset, 0)
        filtered_range = self.kalman_filters[anchor_key].update(corrected_range)

        #print(f'필터 적용: {filtered_range}')
        return filtered_range"""

    def apply_correction_and_kf(self, raw_range, anchor_key):
        """
        거리 보정값 및 칼만 필터 적용
        """
        if anchor_key not in self.kalman_filters:
            print(f"[ERROR] Invalid anchor_key: {anchor_key}")
            return None
        if raw_range is None:
            print("[ERROR] raw_range is None")
            return None

        # DB에서 가져온 앵커별 Offset
        db_offset = self.anchor_offsets.get(anchor_key)
        #print(f'db_offset {db_offset}')

        # 기본값 적용 로직
        if raw_range > 300:
            default_offset = 90
        else:
            default_offset = 45

        # Offset 결정: DB에서 가져온 값이 있으면 사용, 없으면 기본값  DB적용offset(주석빼기)
        #range_offset = db_offset if db_offset is not None else default_offset

        range_offset = default_offset


        # 디버깅 출력: 사용 중인 Offset 값과 앵커 정보
        #print(f"[DEBUG] Anchor: {anchor_key}, Raw Range: {raw_range}, "
        #      f"DB Offset: {db_offset}, Default Offset: {default_offset}, "
        #      f"Applied Offset: {range_offset}")

        # 거리 보정
        corrected_range = max((raw_range - range_offset)*0.01, 0)

        # 칼만 필터 적용
        filtered_range = self.kalman_filters[anchor_key].update(corrected_range)

        #print(f' kalman_filter_range: {filtered_range}')

        return filtered_range

    def circle_intersections(self, c1, r1, c2, r2, epsilon=0.2):
        """
        두 원의 교점을 계산하는 함수. 중심 거리와 반지름 합/차에 허용 오차(epsilon)를 적용.
        """
        x1, y1 = c1
        x2, y2 = c2
        d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # 두 중심 간의 거리

        # 교차하지 않음
        if d > r1 + r2 + epsilon:
            print(f"교차하지 않음 (허용 오차 {epsilon}): 중심 거리(d={d}) > 반지름 합(r1+r2={r1 + r2})")
            return None
        # 내접 상태
        elif d < abs(r1 - r2) - epsilon:
            print(f"내접 상태 (허용 오차 {epsilon}): 중심 거리(d={d}) < 반지름 차(|r1-r2|={abs(r1 - r2)})")
            return None
        # 중심이 동일
        elif d == 0:
            print("중심이 동일함: 중심 거리(d=0)이며, 두 원의 중심이 같습니다.")
            return None

        # 두 원이 교차한다고 간주
        a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(max(r1 ** 2 - a ** 2, 0))  # max로 음수 방지

        x3 = x1 + a * (x2 - x1) / d
        y3 = y1 + a * (y2 - y1) / d

        offset_x = h * (y2 - y1) / d
        offset_y = h * (x2 - x1) / d

        return (x3 + offset_x, y3 - offset_y), (x3 - offset_x, y3 + offset_y)

    def distance(self, point1, point2):
        """
        두 점 사이의 유클리드 거리를 계산합니다.

        Parameters:
            point1: 첫 번째 점 (x1, y1) 형태의 튜플
            point2: 두 번째 점 (x2, y2) 형태의 튜플

        Returns:
            두 점 사이의 거리 (float)
        """
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def closest_point(self, points, target):
        return min(points, key=lambda p: self.distance(p, target))

    def generalized_trilateration(self, num_anchors, anchor_ranges, anchor_positions):
        """
        Generalized trilateration for N anchors.

        Parameters:
            num_anchors: Number of anchors to consider (e.g., 3, 4, ...).
            anchor_ranges: List of ranges for each anchor (e.g., [a1_range, a2_range, ...]).
            anchor_positions: List of positions for each anchor (e.g., [pos_a1, pos_a2, ...]).

        Returns:
            (x, y): Refined position as the average of valid intersection points.
        """
        # print("ddddddddddddddddd", anchor_positions)
        # 입력값 검증
        if num_anchors > len(anchor_positions) or num_anchors > len(anchor_ranges):
            print(f'ancho_positions {anchor_positions}, num_acho {num_anchors}, an_rang {anchor_ranges}')
            raise ValueError("Number of anchors exceeds provided anchor data.")

        points = []

        # 선택된 앵커만큼의 원 쌍의 교점 계산
        for i in range(num_anchors):
            for j in range(i + 1, num_anchors):
                intersections = self.circle_intersections(
                    anchor_positions[i], anchor_ranges[i],
                    anchor_positions[j], anchor_ranges[j]
                )
                if intersections:
                    # 각 교점에서 다른 앵커들과의 거리 차이를 계산 (i와 j는 제외)
                    closest_intersection = min(
                        intersections,
                        key=lambda point: sum(
                            abs(self.distance(point, anchor_positions[k]) - anchor_ranges[k])
                            for k in range(num_anchors) if k != i and k != j
                        )
                    )
                    points.append(closest_intersection)
                    print(f'Chosen point: {closest_intersection} from intersections: {intersections}')

        if points:
            # 평균 좌표 계산
            x = sum(p[0] for p in points) / len(points)
            y = sum(p[1] for p in points) / len(points)
            return round(x, 2), round(y, 2)

        return None, None

    def refined_trilateration(self, a1_range, a2_range, a3_range, pos_a1, pos_a2, pos_a3, epsilon=0.2):
        points = []
        # A1 and A2
        intersections = self.circle_intersections(pos_a1, a1_range, pos_a2, a2_range, epsilon)
        # print(f'원 1,2 intersections{intersections}')
        if intersections:
            points.append(self.closest_point(intersections, pos_a3))

        # A2 and A3
        intersections = self.circle_intersections(pos_a2, a2_range, pos_a3, a3_range, epsilon)
        # print(f'원 2,3 intersections{intersections}')

        if intersections:
            points.append(self.closest_point(intersections, pos_a1))

        # A3 and A1
        intersections = self.circle_intersections(pos_a3, a3_range, pos_a1, a1_range, epsilon)
        # print(f'원 3,1 intersections{intersections}')

        if intersections:
            points.append(self.closest_point(intersections, pos_a2))

        if len(points) == 3:
            x = sum(p[0] for p in points) / 3
            y = sum(p[1] for p in points) / 3
            #print(x, y)
            return round(x, 2), round(y, 2)

        return None, None

