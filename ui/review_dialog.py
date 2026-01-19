"""Dialog for reviewing OCR mismatches."""

from __future__ import annotations

from typing import Optional

from PySide6 import QtCore, QtGui, QtWidgets

from models import OCRComparisonResult


class ReviewDialog(QtWidgets.QDialog):
    """Display OCR results side-by-side for user confirmation."""

    def __init__(
        self,
        image_path: Optional[str],
        comparison: OCRComparisonResult,
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._comparison = comparison
        self._selected_text: Optional[str] = None

        self.setWindowTitle("Review OCR Result")
        self.resize(900, 600)

        layout = QtWidgets.QVBoxLayout(self)
        content = QtWidgets.QHBoxLayout()
        layout.addLayout(content)

        self.image_label = QtWidgets.QLabel()
        self.image_label.setMinimumWidth(320)
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        content.addWidget(self.image_label, 1)

        text_layout = QtWidgets.QVBoxLayout()
        content.addLayout(text_layout, 1)

        self.primary_text = self._build_text_group("Primary OCR", comparison.primary_text)
        self.secondary_text = self._build_text_group("Secondary OCR", comparison.secondary_text)
        text_layout.addWidget(self.primary_text)
        text_layout.addWidget(self.secondary_text)

        action_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(action_layout)

        self.use_primary_button = QtWidgets.QPushButton("Use Primary")
        self.use_secondary_button = QtWidgets.QPushButton("Use Secondary")
        self.manual_edit_button = QtWidgets.QPushButton("Manual Edit")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        action_layout.addWidget(self.use_primary_button)
        action_layout.addWidget(self.use_secondary_button)
        action_layout.addWidget(self.manual_edit_button)
        action_layout.addWidget(self.cancel_button)

        self.use_primary_button.clicked.connect(self._choose_primary)
        self.use_secondary_button.clicked.connect(self._choose_secondary)
        self.manual_edit_button.clicked.connect(self._open_manual_edit)
        self.cancel_button.clicked.connect(self.reject)

        self._image_path = image_path
        if image_path:
            self._load_image(image_path)

    def _build_text_group(self, title: str, text: str) -> QtWidgets.QGroupBox:
        group = QtWidgets.QGroupBox(title)
        layout = QtWidgets.QVBoxLayout(group)
        widget = QtWidgets.QPlainTextEdit(text)
        widget.setReadOnly(True)
        layout.addWidget(widget)
        return group

    def _load_image(self, image_path: str) -> None:
        pixmap = QtGui.QPixmap(image_path)
        if pixmap.isNull():
            self.image_label.setText("Image not found")
            return
        scaled = pixmap.scaled(
            self.image_label.size(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        self.image_label.setPixmap(scaled)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        if self._image_path:
            self._load_image(self._image_path)

    def _choose_primary(self) -> None:
        self._selected_text = self._comparison.primary_text
        self.accept()

    def _choose_secondary(self) -> None:
        self._selected_text = self._comparison.secondary_text
        self.accept()

    def _open_manual_edit(self) -> None:
        text, ok = QtWidgets.QInputDialog.getMultiLineText(
            self,
            "Manual Edit",
            "Edit OCR result:",
            self._comparison.primary_text,
        )
        if ok:
            self._selected_text = text
            self.accept()

    def selected_text(self) -> Optional[str]:
        return self._selected_text
