"""Main window UI for the WWM guild manager."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PySide6 import QtCore, QtWidgets

from config import AppSettings, save_settings
from core.exporter import export_records, import_records
from models import DEFAULT_FIELDS, GuildMemberRecord


class MainWindow(QtWidgets.QMainWindow):
    """Main application window with a table-based editor."""

    def __init__(self, settings: AppSettings, settings_path: Path) -> None:
        super().__init__()
        self.settings = settings
        self.settings_path = settings_path
        self.current_csv_path: Path | None = None

        self.table = QtWidgets.QTableWidget(0, len(DEFAULT_FIELDS))
        self.table.setHorizontalHeaderLabels(list(DEFAULT_FIELDS))
        self._configure_ui()

    def _configure_ui(self) -> None:
        self.setWindowTitle("WWM Guild Manager")
        self.resize(1200, 720)

        central = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(central)
        layout.addWidget(self.table)
        self.setCentralWidget(central)

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked
            | QtWidgets.QAbstractItemView.EditTrigger.SelectedClicked
        )

        self._build_menus()
        self.statusBar().showMessage("Ready")

    def _build_menus(self) -> None:
        file_menu = self.menuBar().addMenu("File")

        open_action = QtWidgets.QAction("Open CSV...", self)
        open_action.triggered.connect(self.open_csv)
        file_menu.addAction(open_action)

        new_action = QtWidgets.QAction("New CSV", self)
        new_action.triggered.connect(self.new_csv)
        file_menu.addAction(new_action)

        save_action = QtWidgets.QAction("Save", self)
        save_action.triggered.connect(self.save_csv)
        file_menu.addAction(save_action)

        save_as_action = QtWidgets.QAction("Save As...", self)
        save_as_action.triggered.connect(self.save_csv_as)
        file_menu.addAction(save_as_action)

        tools_menu = self.menuBar().addMenu("Tools")
        add_column_action = QtWidgets.QAction("Add Column...", self)
        add_column_action.triggered.connect(self.prompt_add_column)
        tools_menu.addAction(add_column_action)

    def load_records(self, records: Iterable[GuildMemberRecord], csv_path: Path | None = None) -> None:
        self.table.setRowCount(0)
        for record in records:
            self.add_record(record)
        if csv_path:
            self.current_csv_path = csv_path
            self._update_settings_from_path(csv_path)

    def clear_records(self) -> None:
        self.table.setRowCount(0)

    def add_record(self, record: GuildMemberRecord) -> None:
        row_index = self.table.rowCount()
        self.table.insertRow(row_index)
        row_data = record.to_csv_row(DEFAULT_FIELDS)

        for column, field_name in enumerate(DEFAULT_FIELDS):
            item = QtWidgets.QTableWidgetItem(str(row_data.get(field_name, "")))
            item.setData(QtCore.Qt.ItemDataRole.UserRole, field_name)
            self.table.setItem(row_index, column, item)

        for field_name in row_data:
            if field_name in DEFAULT_FIELDS:
                continue
            self._ensure_column(field_name)
            column_index = self._column_index(field_name)
            item = QtWidgets.QTableWidgetItem(str(row_data.get(field_name, "")))
            self.table.setItem(row_index, column_index, item)

    def add_custom_column(self, label: str) -> None:
        self._ensure_column(label)

    def _ensure_column(self, label: str) -> None:
        headers = self.current_csv_headers()
        if label in headers:
            return
        column_index = self.table.columnCount()
        self.table.insertColumn(column_index)
        self.table.setHorizontalHeaderItem(column_index, QtWidgets.QTableWidgetItem(label))

    def _column_index(self, label: str) -> int:
        for column in range(self.table.columnCount()):
            item = self.table.horizontalHeaderItem(column)
            if item and item.text() == label:
                return column
        raise ValueError(f"Unknown column: {label}")

    def prompt_add_column(self) -> None:
        text, ok = QtWidgets.QInputDialog.getText(self, "Add Column", "Column name:")
        if ok and text:
            self.add_custom_column(text)

    def current_csv_headers(self) -> list[str]:
        headers: list[str] = []
        for column in range(self.table.columnCount()):
            item = self.table.horizontalHeaderItem(column)
            headers.append(item.text() if item else "")
        return headers

    def open_csv(self) -> None:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if not path:
            return
        csv_path = Path(path)
        records = import_records(csv_path)
        self.load_records(records, csv_path)
        self.statusBar().showMessage(f"Loaded {csv_path}")

    def new_csv(self) -> None:
        self.clear_records()
        self.current_csv_path = None
        self.statusBar().showMessage("New CSV created")

    def save_csv(self) -> None:
        if not self.current_csv_path:
            self.save_csv_as()
            return
        self._save_to_path(self.current_csv_path)

    def save_csv_as(self) -> None:
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save CSV",
            "",
            "CSV Files (*.csv)",
        )
        if not path:
            return
        self.current_csv_path = Path(path)
        self._save_to_path(self.current_csv_path)
        self._update_settings_from_path(self.current_csv_path)

    def _save_to_path(self, path: Path) -> None:
        records = self._collect_records()
        export_records(path, records)
        self.statusBar().showMessage(f"Saved {path}")

    def _collect_records(self) -> list[GuildMemberRecord]:
        headers = self.current_csv_headers()
        records: list[GuildMemberRecord] = []
        for row in range(self.table.rowCount()):
            values = {}
            for column, header in enumerate(headers):
                item = self.table.item(row, column)
                values[header] = item.text() if item else ""

            index_text = values.get("index", str(row + 1))
            try:
                index_value = int(index_text)
            except ValueError:
                index_value = row + 1

            record = GuildMemberRecord(
                index=index_value,
                nickname=values.get("nickname", ""),
                role=values.get("role", ""),
                faction=values.get("faction", ""),
                days_since_join=values.get("days_since_join", ""),
                weekly_activity=values.get("weekly_activity", ""),
                martial_realm=values.get("martial_realm", ""),
                exploration_skill=values.get("exploration_skill", ""),
                tech_mastery=values.get("tech_mastery", ""),
                extras={
                    key: value
                    for key, value in values.items()
                    if key not in DEFAULT_FIELDS
                },
            )
            records.append(record)
        return records

    def _update_settings_from_path(self, path: Path) -> None:
        self.settings = AppSettings(
            default_csv_path=path,
            last_opened_project=path.parent,
            crop_preset=self.settings.crop_preset,
            ocr_language=self.settings.ocr_language,
        )
        save_settings(self.settings, self.settings_path)
