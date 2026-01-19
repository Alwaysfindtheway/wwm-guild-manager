"""Crop calibration dialog for selecting OCR regions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from PySide6 import QtCore, QtGui, QtWidgets


@dataclass(frozen=True)
class CropRegion:
    """Represents a normalized crop region (0-1 coordinates)."""

    x: float
    y: float
    width: float
    height: float


class CropCalibrationDialog(QtWidgets.QDialog):
    """Dialog that allows users to define a crop region for screenshots."""

    def __init__(self, image_path: str, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self._image_path = image_path
        self._pixmap = QtGui.QPixmap(image_path)
        self._selection_rect = QtCore.QRect()
        self._dragging = False
        self._origin = QtCore.QPoint()
        self._displayed_pixmap_size = QtCore.QSize()

        self.setWindowTitle("Crop Calibration")
        self.resize(900, 600)

        self.image_label = QtWidgets.QLabel()
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(640, 360)
        self.image_label.setMouseTracking(True)
        self.image_label.installEventFilter(self)

        self.instructions = QtWidgets.QLabel(
            "Drag to select the profile panel area to crop.",
        )

        self.confirm_button = QtWidgets.QPushButton("Use Selection")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        self.confirm_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        action_layout = QtWidgets.QHBoxLayout()
        action_layout.addStretch(1)
        action_layout.addWidget(self.confirm_button)
        action_layout.addWidget(self.cancel_button)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.instructions)
        layout.addWidget(self.image_label, 1)
        layout.addLayout(action_layout)

        self._render_image()

    def _render_image(self) -> None:
        if self._pixmap.isNull():
            self.image_label.setText("Image not found")
            return

        scaled = self._pixmap.scaled(
            self.image_label.size(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        self._displayed_pixmap_size = scaled.size()
        overlay = QtGui.QPixmap(scaled)
        painter = QtGui.QPainter(overlay)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        if not self._selection_rect.isNull():
            pen = QtGui.QPen(QtGui.QColor(255, 165, 0), 2)
            painter.setPen(pen)
            painter.drawRect(self._selection_rect)
        painter.end()
        self.image_label.setPixmap(overlay)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self._render_image()

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if watched is not self.image_label:
            return super().eventFilter(watched, event)

        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            mouse_event = event
            if mouse_event.button() != QtCore.Qt.MouseButton.LeftButton:
                return False
            label_pos = mouse_event.position().toPoint()
            if not self._pixmap_rect().contains(label_pos):
                return False
            self._dragging = True
            self._origin = label_pos
            self._selection_rect = QtCore.QRect(self._origin, QtCore.QSize())
            self._render_image()
            return True

        if event.type() == QtCore.QEvent.Type.MouseMove:
            if not self._dragging:
                return False
            mouse_event = event
            label_pos = mouse_event.position().toPoint()
            self._selection_rect = QtCore.QRect(self._origin, label_pos).normalized()
            self._render_image()
            return True

        if event.type() == QtCore.QEvent.Type.MouseButtonRelease:
            mouse_event = event
            if mouse_event.button() != QtCore.Qt.MouseButton.LeftButton:
                return False
            if self._dragging:
                self._dragging = False
                self._render_image()
            return True

        return super().eventFilter(watched, event)

    def _pixmap_rect(self) -> QtCore.QRect:
        if not self._displayed_pixmap_size.isValid():
            return QtCore.QRect()
        label_size = self.image_label.size()
        x = int((label_size.width() - self._displayed_pixmap_size.width()) / 2)
        y = int((label_size.height() - self._displayed_pixmap_size.height()) / 2)
        return QtCore.QRect(QtCore.QPoint(x, y), self._displayed_pixmap_size)

    def selected_region(self) -> Optional[CropRegion]:
        if self._pixmap.isNull() or self._selection_rect.isNull():
            return None

        label_pixmap = self.image_label.pixmap()
        if label_pixmap is None or self._displayed_pixmap_size.isEmpty():
            return None

        offset = self._pixmap_rect().topLeft()
        selection = self._selection_rect.translated(-offset)
        selection = selection.intersected(QtCore.QRect(QtCore.QPoint(0, 0), self._displayed_pixmap_size))
        if selection.isNull():
            return None

        scale_x = self._pixmap.width() / self._displayed_pixmap_size.width()
        scale_y = self._pixmap.height() / self._displayed_pixmap_size.height()

        rect = QtCore.QRect(
            int(selection.x() * scale_x),
            int(selection.y() * scale_y),
            int(selection.width() * scale_x),
            int(selection.height() * scale_y),
        )

        return CropRegion(
            x=rect.x() / self._pixmap.width(),
            y=rect.y() / self._pixmap.height(),
            width=rect.width() / self._pixmap.width(),
            height=rect.height() / self._pixmap.height(),
        )
