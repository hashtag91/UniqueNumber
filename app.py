from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLabel
from PyQt5.QtCore import Qt
from ui import CustomWidget
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ANONYMAT")
        self.stacked = QStackedWidget()
        self.expired = QLabel()
        self.expired.setText("SESSION EXPIREE !")
        self.expired.setAlignment(Qt.AlignCenter)
        self.expired.setStyleSheet("""
            background:qlineargradient(
                x1:0, y1:0,
                x2:1, y2:1,
                stop:0 #020024,
                stop:1 #090979
            );
            color: red;
            font-size: 18px;
        """)

        ui = CustomWidget()
        self.stacked.addWidget(ui)
        self.stacked.addWidget(self.expired)

        self.licence_funtcion()

        self.setCentralWidget(self.stacked)
        self.setFixedSize(600, 280)
        self.show()

    def est_date_atterieure_ou_egale(self, date_cible):
        aujourd_hui = datetime.now().date()
        return aujourd_hui >= date_cible
    
    def licence_funtcion(self):
        date_cible = datetime(2026, 8, 31).date()

        if self.est_date_atterieure_ou_egale(date_cible):
            self.stacked.setCurrentIndex(1)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())