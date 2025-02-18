# ///////////////////////////////////////////////////////////////

import sys
import os
import platform

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from modules import Settings
from modules.app_functions import AppFunctions
from widgets import *
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%
from modules.utils import resource_path


# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.data = {}  # 데이터를 저장할 딕셔너리 초기화

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # SET INITIAL PAGE TO HOME
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

        # 작업현장 이동 메시지 표시
        self.show_loading_message("작업현장으로 이동합니다...")
        QTimer.singleShot(5000, self.startWorkspaceTransition)  # 3초 후 화면 전환

        # 1223 수정 중
        # AppFunctions 초기화
        self.appFunctions = AppFunctions(self)
        self.appFunctions.load_last_workspace()
        self.appFunctions.update_anchor_settings()
        # 버튼 이벤트 연결
        self.ui.pushButton.clicked.connect(self.appFunctions.open_existing_workspace)  # 버튼과 함수 연결
        self.ui.btn_exit.clicked.connect(self.appFunctions.exitApplication) # 닫기 버튼
        self.ui.pushButton_4.clicked.connect(self.appFunctions.save_as_new_workspace) # json 저장 함수
        # 앵커 설정용 SpinBox 이벤트 연결
        self.ui.g_anchorNum.valueChanged.connect(self.appFunctions.update_anchor_settings)

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "UWB - Position Monitoring System"
        description = "UWB - Position Monitoring System Interface"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    def closeEvent(self, event):
        # 창 닫기 전에 시리얼 연결 종료
        self.appFunctions.close_application()
        event.accept()




    #초기화면 로딩 관련 설정 함수  유진

    def show_loading_message(self, message="작업현장으로 이동합니다..."):
        """
        화면 중앙에 로딩 메시지를 표시
        """
        self.loading_label = QLabel(self)
        self.loading_label.setGeometry(
            self.width() // 2 - 150, self.height() // 2 - 30, 300, 60
        )  # 화면 중앙에 위치
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.8);
            color: white;
            border-radius: 10px;
            font-size: 16px;
            padding: 10px;
        """)
        self.loading_label.setText(message)
        self.loading_label.show()
        QApplication.processEvents()  # 즉시 화면 갱신

    def hide_loading_message(self):
        """
        로딩 메시지 숨기기
        """
        if hasattr(self, "loading_label") and self.loading_label:
            self.loading_label.hide()
            self.loading_label.deleteLater()
            self.loading_label = None

    def startWorkspaceTransition(self):
        """
        작업현장 화면으로 전환
        """
        self.hide_loading_message()  # 로딩 메시지 숨기기
        btnName = "btn_new"  # 버튼 이름 설정
        widgets.stackedWidget.setCurrentWidget(widgets.new_page)  # New 페이지로 전환
        UIFunctions.resetStyle(self, btnName)  # 스타일 초기화
        widgets.btn_new.setStyleSheet(UIFunctions.selectMenu(widgets.btn_new.styleSheet()))  # 버튼 스타일 적용
        print("Switched to New Page.")

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "btn_save":
            print("Save BTN clicked!")


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        """
        창 크기 변경 시 workspace QFrame 크기에 맞춰 작업 공간을 동적으로 조정
        """
        super().resizeEvent(event)

        if hasattr(self, 'appFunctions') and hasattr(self, 'workspace_settings'):
            self.appFunctions.draw_workspace_box(
                x=0, y=0,
                workspace_width=self.workspace_settings.get("workspace_width", 0),
                workspace_height=self.workspace_settings.get("workspace_height", 0),
                danger_zone_x=self.workspace_settings.get("danger_zone_x", 0),
                danger_zone_y=self.workspace_settings.get("danger_zone_y", 0),
                danger_zone_width=self.workspace_settings.get("danger_zone_width", 0),
                danger_zone_height=self.workspace_settings.get("danger_zone_height", 0),
                anchors=self.appFunctions.anchor_data
            )

        # 캘리브레이션 점 좌표 업데이트
        if hasattr(self.appFunctions, 'calibration_handler'):
            self.appFunctions.calibration_handler.update_calibration_points()

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        # self.dragPos = event.globalPos()
        self.dragPos = event.globalPosition().toPoint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
