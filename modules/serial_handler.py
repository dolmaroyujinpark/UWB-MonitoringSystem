import time

import serial
import json
from threading import Thread, Event

from PySide6.QtWidgets import QMessageBox
from serial.tools import list_ports


class SerialHandler:
    def __init__(self, port, baudrate, callback, parent):
        self.serial = None
        self.port = port
        self.baudrate = baudrate
        self.callback = callback  # 데이터를 처리할 콜백 함수
        self.running = Event()
        self.port_monitoring = Event()
        self.parent = parent  # UI 접근을 위한 참조
        self.current_port = None  # 현재 연결된 포트
        self.monitor_thread = None
        self.read_thread = None  # 데이터 읽기용 스레드

    def connect(self):
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"Connected to serial port {self.port} at {self.baudrate} baud.")
            self.running.set()
            self.current_port = self.port
            self.start_reading_thread()
        except Exception as e:
            print(f"Failed to connect to serial port: {e}")
            self.serial = None

    def disconnect(self):
        self.running.clear()
        if self.serial and self.serial.is_open:
            self.serial.close()
        self.serial = None
        self.current_port = None
        print("Serial connection closed.")

    def start_reading_thread(self):
        """데이터 읽기용 스레드 시작"""
        if self.read_thread and self.read_thread.is_alive():
            print("Stopping previous reading thread.")
            self.running.clear()
            self.read_thread.join()

        self.running.set()
        self.read_thread = Thread(target=self.read_data, daemon=True)
        self.read_thread.start()

    def read_data(self):
        """
        시리얼 데이터를 읽고 콜백 함수로 전달.
        """
        while self.running.is_set():
            try:
                # 시리얼 데이터 읽기
                line = self.serial.readline().strip()
                line = line.decode("utf-8")  # 바이트 문자열을 일반 문자열로 변환
                # print(f"Raw line: {line}")

                if line:
                    # 콜백으로 데이터 전달
                    self.callback(line)
            except serial.SerialException as e:
                print(f"[ERROR] SerialException occurred: {e}")
                self.handle_serial_disconnection()
                break
            except Exception as e:
                print(f"[ERROR] Unexpected error while reading serial data: {e}")
                self.handle_serial_disconnection()
                break

    def handle_serial_disconnection(self):
        """
        시리얼 포트가 끊어진 경우 처리.
        """
        print("[INFO] Handling serial disconnection...")
        self.running.clear()
        if self.serial:
            try:
                self.serial.close()
            except Exception as e:
                print(f"[WARNING] Error while closing serial port: {e}")
        self.serial = None
        self.current_port = None
        # 연결 끊김 알림
        # QMessageBox.warning(self.parent, "Warning", "시리얼 포트 연결이 끊어졌습니다.")

        # 포트 모니터링 재개
        if not self.port_monitoring.is_set():
            self.start_port_monitoring()

    def start_port_monitoring(self):
        """포트 연결 상태 감시 스레드 시작"""
        print("Jeong: Serial handler start port monitoring")
        self.port_monitoring.set()
        self.monitor_thread = Thread(target=self.monitor_ports, daemon=True)
        self.monitor_thread.start()

    def stop_port_monitoring(self):
        """포트 연결 상태 감시 종료"""
        self.port_monitoring.clear()
        if self.monitor_thread:
            self.monitor_thread.join()

    def monitor_ports(self):
        """연결된 포트 상태를 지속적으로 감시"""
        print("monitor_ports start!")
        previous_ports = set(port.device for port in list_ports.comports())

        while self.port_monitoring.is_set():
            current_ports = set(port.device for port in list_ports.comports())
            print(f"[DEBUG] Available ports: {current_ports}")

            # 현재 포트가 끊어진 경우
            if self.current_port and self.current_port not in current_ports:
                print("[INFO] Serial port disconnected.")
                self.disconnect()
                self.current_port = None

            # 새 포트가 발견된 경우 또는 기존 포트가 다시 연결된 경우
            if not self.current_port and current_ports:
                new_port = list(current_ports)[0]  # 새 포트 중 첫 번째 포트를 선택
                self.port = new_port
                print(f"[INFO] Attempting to reconnect to port {new_port}...")

                # 재연결 시도
                try:
                    self.connect()
                    if self.serial and self.serial.is_open:
                        print(f"[INFO] Reconnected to port {new_port}.")
                        self.current_port = new_port
                    else:
                        print("[ERROR] Failed to reconnect.")
                except Exception as e:
                    print(f"[ERROR] Exception during reconnection: {e}")

            # UI 업데이트
            if hasattr(self.parent.ui, "portList"):
                self.parent.ui.portList.clear()
                self.parent.ui.portList.addItems(current_ports)

                # 첫 번째 포트를 기본값으로 선택
                if current_ports:
                    self.parent.ui.portList.setCurrentIndex(0)

            previous_ports = current_ports
            time.sleep(1)  # 1초 간격으로 감시

    def send_command(self, command):
        if self.serial and self.serial.is_open:
            self.serial.write(command.encode())
