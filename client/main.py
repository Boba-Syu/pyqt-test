import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox, QInputDialog
)

from client.http_client import HttpClient


class TableApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.httpClient = HttpClient("127.0.0.1:8080")

        self.setWindowTitle("PyQt6表格示例")
        self.setGeometry(300, 300, 600, 400)

        # 创建主控件和布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout()
        main_widget.setLayout(self.layout)

        # 初始化表格
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["用户ID", "用户名", "用户密码", "创建时间", "修改时间"])
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 200)

        # 添加初始数据
        self.load_initial_data()

        self.bth_setting()

    def bth_setting(self):
        # 创建按钮
        btn_add = QPushButton("添加行")
        btn_add.clicked.connect(self.add_row)
        btn_delete = QPushButton("删除选中行")
        btn_delete.clicked.connect(self.delete_row)

        # 按钮布局
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_delete)

        # 组合布局
        self.layout.addLayout(btn_layout)
        self.layout.addWidget(self.table)

        # 启用双击编辑
        self.table.cellDoubleClicked.connect(self.edit_cell)

    def load_initial_data(self):
        try:
            response = self.httpClient.get("/user/all")
            if response['code'] != 200:
                QMessageBox.critical(self, "错误", f"数据加载失败: {response['reason']}")
                return

            data = response['data']
            self.table.setRowCount(len(data))

            for row, item in enumerate(data):
                fields = [
                    str(item.get('id', '')),
                    item.get('username', ''),
                    item.get('password', ''),
                    item.get('create_time', ''),
                    item.get('update_time', '')
                ]

                for col, value in enumerate(fields):
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(row, col, item)

        except Exception as e:
            QMessageBox.critical(self, "错误", f"连接错误: {str(e)}")

    def add_row(self):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setItem(row_count, 0, QTableWidgetItem("用户ID"))
        self.table.setItem(row_count, 1, QTableWidgetItem("用户名"))
        self.table.setItem(row_count, 2, QTableWidgetItem("用户密码"))
        self.table.setItem(row_count, 3, QTableWidgetItem("创建时间"))
        self.table.setItem(row_count, 4, QTableWidgetItem("修改时间"))

    def delete_row(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "警告", "请先选择要删除的行！")
            return
        self.table.removeRow(current_row)

    def edit_cell(self, row, col):
        item = self.table.item(row, col)
        old_value = item.text()
        new_value, ok = QInputDialog.getText(
            self, "编辑单元格",
            f"编辑内容 ({self.table.horizontalHeaderItem(col).text()}):",
            text=old_value
        )
        if ok and new_value:
            item.setText(new_value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableApp()
    window.show()
    sys.exit(app.exec())
