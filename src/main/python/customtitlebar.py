import platform
from fbs_runtime import PUBLIC_SETTINGS, platform
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QToolButton,
    QWidget,
)

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initial_pos = None
        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(1, 1, 1, 1)
        title_bar_layout.setSpacing(2)
        self.title = QLabel(f'{PUBLIC_SETTINGS["app_name"]} - Version: {PUBLIC_SETTINGS["version"]}', self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # self.title.setStyleSheet(
        #     """
        # QLabel { text-transform: uppercase; font-size: 10pt; margin-left: 48px; }
        # """
        # )
        self.title.setStyleSheet(
            """
        QLabel {font-size: 12pt; margin-left: 8px; }
        """
        )

        if title := parent.windowTitle():
            self.title.setText(title)
        # title_bar_layout.addWidget(self.title)
        # Min button
        self.min_button = QToolButton(self)
        min_icon = QIcon()
        min_icon.addFile("min.svg")
        self.min_button.setIcon(min_icon)
        self.min_button.clicked.connect(self.window().hide)

        # Max button
        self.max_button = QToolButton(self)
        max_icon = QIcon()
        max_icon.addFile("max.svg")
        self.max_button.setIcon(max_icon)
        self.max_button.clicked.connect(self.window().showMaximized)

        # Close button
        self.close_button = QToolButton(self)
        close_icon = QIcon()
        close_icon.addFile("close.svg")  # Close has only a single state.
        self.close_button.setIcon(close_icon)
        self.close_button.clicked.connect(self.window().close)

        # Normal button
        self.normal_button = QToolButton(self)
        normal_icon = QIcon()
        normal_icon.addFile("normal.svg")
        self.normal_button.setIcon(normal_icon)
        self.normal_button.clicked.connect(self.window().showNormal)
        self.normal_button.setVisible(False)
        # Add buttons
        buttons = [
            self.close_button,
            self.max_button,
            self.normal_button,
            self.min_button
        ]
        for button in buttons:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setFixedSize(QSize(16, 16))
            button.setStyleSheet(
                """QToolButton {
                    border: none;
                    padding: 2px;
                }
                """
            )
            # title_bar_layout.addWidget(button)
        
        if platform.name() == 'Mac' or 'Linux':
            for button in buttons:
                title_bar_layout.addWidget(button)
            title_bar_layout.addWidget(self.title)
        elif platform.name() == 'Windows':
            title_bar_layout.addWidget(self.title)
            for button in buttons[::-1]:
                title_bar_layout.addWidget(button)

    def window_state_changed(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)