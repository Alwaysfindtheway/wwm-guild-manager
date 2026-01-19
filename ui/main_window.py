"""Main window UI for the WWM guild manager."""

from __future__ import annotations

from typing import Iterable

from PySide6 import QtCore, QtWidgets

from config import AppSettings
from models import DEFAULT_FIELDS, GuildMemberRecord


class MainWindow(QtWidgets.QMainWindow):
    """Main application window with a table-based editor."""

    def __init__(self, settings: AppSettings) -> None:
        super().__init__()
        self.settings = settings
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

    def load_records(self, records: Iterable[GuildMemberRecord]) -> None:
        self.table.setRowCount(0)
        for record in records:
            self.add_record(record)

    def add_record(self, record: GuildMemberRecord) -> None:
        row_index = self.table.rowCount()
        self.table.insertRow(row_index)
        row_data = record.to_csv_row(DEFAULT_FIELDS)

        for column, field_name in enumerate(DEFAULT_FIELDS):
            item = QtWidgets.QTableWidgetItem(str(row_data.get(field_name, "")))
            item.setData(QtCore.Qt.ItemDataRole.UserRole, field_name)
            self.table.setItem(row_index, column, item)

    def add_custom_column(self, label: str) -> None:
        column_index = self.table.columnCount()
        self.table.insertColumn(column_index)
        self.table.setHorizontalHeaderItem(column_index, QtWidgets.QTableWidgetItem(label))

    def current_csv_headers(self) -> list[str]:
        headers: list[str] = []
        for column in range(self.table.columnCount()):
            item = self.table.horizontalHeaderItem(column)
            headers.append(item.text() if item else "")
        return headers
