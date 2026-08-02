from PyQt5.QtWidgets import (QWidget, QFrame, QLineEdit, QVBoxLayout, QLabel, QToolButton, QHBoxLayout, 
                             QGraphicsDropShadowEffect, QProgressBar, QSizePolicy, QComboBox,
                             QMessageBox)
from PyQt5.QtGui import QColor, QIcon, QCursor
from PyQt5.QtCore import Qt, QSize, QThread
from logic import select_file, ExcelWorker
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 120))

        background_frame = QFrame()
        background_frame.setObjectName("background_frame")

        self.setStyleSheet("""
            QFrame#background_frame{

                background:qlineargradient(
                    x1:0, y1:0,
                    x2:1, y2:1,
                    stop:0 #020024,
                    stop:1 #090979
                );

                border:1px solid white;
            }
            """)
        layout.addWidget(background_frame)

        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(20, 20, 20, 20)
        background_frame.setLayout(frame_layout)

        title = QLabel("ANONYMAT")
        title.setAlignment(Qt.AlignCenter) # type: ignore
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        frame_layout.addWidget(title)

        file_uploader = QFrame()
        file_uploader.setObjectName("file_uploader")
        file_uploader.setStyleSheet("""
            QFrame#file_uploader{
                background:qlineargradient(
                    x1:0, y1:0,
                    x2:1, y2:1,

                    stop:0 rgba(255,255,255,70),
                    stop:1 rgba(255,255,255,35)
                );

                border:1px solid rgba(255,255,255,100);

                border-radius:5px;
            }
        """)
        file_uploader.setGraphicsEffect(shadow)
        file_uploader.setFixedHeight(45)
        file_uploader_layout = QHBoxLayout()
        file_uploader_layout.setContentsMargins(15, 10, 15, 10)
        file_uploader.setLayout(file_uploader_layout)
        frame_layout.addWidget(file_uploader)

        self.file_line = QLineEdit()
        self.file_line.setReadOnly(True)
        self.file_line.setPlaceholderText("Selectionnez votre fichier excel...")
        self.file_line.setStyleSheet("background: transparent; border: none; font-size: 16px; color: white")
        file_uploader_layout.addWidget(self.file_line)

        file_button = QToolButton()
        file_button.setText("Browse")
        file_button.setStyleSheet("background: transparent; border: none;")
        file_button.setIcon(QIcon(resource_path("images/folder.svg")))
        file_button.setIconSize(QSize(20,20))
        file_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        file_uploader_layout.addWidget(file_button)

        columns_layout = QHBoxLayout()
        frame_layout.addLayout(columns_layout)

        self.first_column = QComboBox()
        self.first_column.setVisible(False)
        self.first_column.setStyleSheet(f"""
            QComboBox {{
                background: qlineargradient(
                    x1:0, y1:0,
                    x2:1, y2:1,
                    stop:0 rgba(255,255,255,60),
                    stop:1 rgba(255,255,255,40)
                );

                border: 1px solid rgba(255,255,255,100);
                border-radius: 5px;

                padding: 8px 35px 8px 12px;

                color: white;
                font-size: 14px;
                font-weight: 500;
            }}


            QComboBox:hover {{
                background: qlineargradient(
                    x1:0, y1:0,
                    x2:1, y2:1,
                    stop:0 rgba(255,255,255,80),
                    stop:1 rgba(255,255,255,60)
                );

                border: 1px solid rgba(255,255,255,100);
            }}


            QComboBox:focus {{
                border: 1px solid rgba(255,255,255,220);
            }}


            /* Flèche */
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}


            QComboBox::down-arrow {{
                image: url({{resource_path("images/arrow-down.svg")}});
                width: 20px;
                height: 20px;
            }}


            /* Liste déroulante */
            QComboBox QAbstractItemView {{

                background-color: rgba(30,30,40,220);

                border: 1px solid rgba(255,255,255,80);
                border-radius: 12px;

                color: white;

                selection-background-color: rgba(255,255,255,80);
                selection-color: white;

                outline: none;
            }}


            QComboBox QAbstractItemView::item {{
                padding: 8px;
            }}


            QComboBox QAbstractItemView::item:hover {{
                background-color: rgba(255,255,255,50);
            }}
            """)
        self.first_column.setGraphicsEffect(shadow)
        columns_layout.addWidget(self.first_column)
        self.new_column = QLineEdit()
        self.new_column.setVisible(False)
        self.new_column.setStyleSheet(f"""
            QLineEdit {{

                background: qlineargradient(
                    x1:0, y1:0,
                    x2:1, y2:1,
                    stop:0 rgba(255,255,255,60),
                    stop:1 rgba(255,255,255,40)
                );

                border: 1px solid rgba(255,255,255,100);
                border-radius: 5px;

                padding: 10px 15px;

                color: white;
                font-size: 15px;

                selection-background-color: rgba(255,255,255,80);
            }}


            /* Texte indicatif */
            QLineEdit::placeholder {{
                color: rgba(255,255,255,150);
            }}


            /* Survol */
            QLineEdit:hover {{

                background: qlineargradient(
                    x1:0, y1:0,
                    x2:1, y2:1,
                    stop:0 rgba(255,255,255,70),
                    stop:1 rgba(255,255,255,50)
                );

                border: 1px solid rgba(255,255,255,100);
            }}


            /* Quand le champ est actif */
            QLineEdit:focus {{

                border: 1px solid rgba(255,255,255,220);

                background: qlineargradient(
                    x1:0, y1:0,
                    x2:1, y2:1,
                    stop:0 rgba(255,255,255,80),
                    stop:1 rgba(255,255,255,70)
                );
            }}
            """)
        self.new_column.setPlaceholderText("Nom de la nouvelle colonne...")
        columns_layout.addWidget(self.new_column)

        self.generator = QToolButton()
        self.generator.setText("Générer")
        self.generator.setDisabled(True)
        self.generator.setStyleSheet("""
            QToolButton{
                background:qlineargradient(
                    x1:0,y1:0,
                    x2:1,y2:1,
                    stop:0 rgba(255,255,255,90),
                    stop:1 rgba(255,255,255,35)
                );

                border:1px solid rgba(255,255,255,90);
                border-radius:5px;

                color:white;
                font-size:14px;
                font-weight:bold;

                padding:8px;
            }

            QToolButton:hover{
                background:qlineargradient(
                    x1:0,y1:0,
                    x2:1,y2:1,
                    stop:0 rgba(255,255,255,120),
                    stop:1 rgba(255,255,255,60)
                );

                border:1px solid rgba(255,255,255,180);
            }

            QToolButton:pressed{
                background:rgba(255,255,255,150);
            }
        """)
        self.generator.setFixedSize(QSize(150,35))
        self.generator.setGraphicsEffect(shadow)
        self.generator.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        file_button.clicked.connect(lambda: select_file(self, self.file_line, self.first_column, 
                                                        self.generator, self.new_column))
        self.generator.clicked.connect(self.start_process)

        generator_layout = QHBoxLayout()
        generator_layout.setAlignment(Qt.AlignCenter) # type: ignore
        generator_layout.addWidget(self.generator)
        frame_layout.addLayout(generator_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMinimumHeight(14)
        self.progress_bar.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        self.progress_bar.setStyleSheet("""

            QProgressBar{
                background:rgba(255,255,255,40);
                border:1px solid rgba(255,255,255,80);
                border-radius:10px;
                height:18px;
                color:white;
            }


            QProgressBar::chunk{

                border-radius:10px;

                background:qlineargradient(
                    x1:0,y1:0,
                    x2:1,y2:0,
                    stop:0 #4facfe,
                    stop:1 #00f2fe
                );
            }
        """)
        self.progress_bar.setVisible(False)

        frame_layout.addWidget(self.progress_bar)

        frame_layout.setSpacing(20)
        frame_layout.addStretch(1)


    def start_process(self):

        self.progress_bar.setValue(0)

        self.mon_thread = QThread()

        self.worker = ExcelWorker(
            self.file_line.text(),
            self.first_column.currentText(),
            self.new_column.text()
        )

        self.worker.moveToThread(
            self.mon_thread
        )

        self.mon_thread.started.connect(
            self.worker.run
        )

        self.worker.progress.connect(
            self.progress_bar.setValue
        )

        self.worker.finished.connect(
            self.mon_thread.quit
        )

        self.worker.finished.connect(
            self.operation_finished
        )

        self.worker.error.connect(
            self.operation_failed
        )

        self.mon_thread.start()

    def operation_finished(self):
        QMessageBox.information(self, "Succès","Opération effectuée avec succès !")

        self.progress_bar.setVisible(False)

        self.worker.deleteLater() # type: ignore
        self.mon_thread.deleteLater() # type: ignore

        self.worker = None
        self.mon_thread = None

    def operation_failed(self,e:str):
        message = f"L'erreur suivante est survenue: {e}\nVeuillez contacter le developpeur"
        if "permission denied" in e.lower():
            message = "Veuillez d'abord fermer le fichier excel"
        QMessageBox.critical(self, "Erreur", message)

        # arrêter le thread
        if self.mon_thread and self.mon_thread.isRunning():
            self.mon_thread.quit()
            self.mon_thread.wait()

        # nettoyage
        self.worker.deleteLater() # type: ignore
        self.mon_thread.deleteLater() # type: ignore

        self.worker = None
        self.mon_thread = None