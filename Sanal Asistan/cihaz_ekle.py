from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox)
from kontroller import Cihazlar, Televizyon, Kapi, Lamba, Buzdolabi
from veri_yonetimi import json_to_nesne, nesne_to_json
import json
import os
import re

DOSYA_YOLU = os.path.join(os.path.dirname(__file__), "cihazlar.json")

def normalize_name(text: str) -> str:
    text = text.lower()
    return re.sub(r"\s+", "", text) 

class CihazEkleEkrani(QWidget):
    def __init__(self, ana_menu):
        super().__init__()
        self.ana_menu = ana_menu
        self.setWindowTitle("Cihaz Ekle")
        self.setGeometry(150, 150, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.tur_label = QLabel("Cihaz Türü Seçiniz:", self)
        layout.addWidget(self.tur_label)

        self.tur_secim = QComboBox(self)
        self.tur_secim.addItems(["Buzdolabı", "Lamba", "Televizyon", "Kapı"])
        layout.addWidget(self.tur_secim)

        self.ad_label = QLabel("Cihaz Adı:", self)
        layout.addWidget(self.ad_label)

        self.ad_input = QLineEdit(self)
        layout.addWidget(self.ad_input)

        self.marka_label = QLabel("Cihaz Markası:", self)
        layout.addWidget(self.marka_label)

        self.marka_input = QLineEdit(self)
        layout.addWidget(self.marka_input)

        self.kaydet_button = QPushButton("Kaydet", self)
        self.kaydet_button.clicked.connect(self.kaydet)
        layout.addWidget(self.kaydet_button)

        alt_layout = QHBoxLayout()
        geri_btn = QPushButton("Geri", self)
        geri_btn.clicked.connect(self.geri_don)
        alt_layout.addStretch()
        alt_layout.addWidget(geri_btn)
        layout.addLayout(alt_layout)

        self.setLayout(layout)

    def kaydet(self):
        cihaz_turu = self.tur_secim.currentText().lower()
        cihaz_adi = self.ad_input.text()
        cihaz_marka = self.marka_input.text()

        if cihaz_turu == "televizyon":
            cihaz = Televizyon(cihaz_adi,cihaz_marka)
        elif cihaz_turu == "kapı":
            cihaz = Kapi(cihaz_adi, cihaz_marka)
        elif cihaz_turu == "buzdolabı":
            cihaz = Buzdolabi(cihaz_adi, cihaz_marka)
        elif cihaz_turu == "lamba":
            cihaz = Lamba(cihaz_adi, cihaz_turu)
        else:
            QMessageBox.warning(self, "Hata", "Bilinmeyen cihaz türü!")
            return
        cihazlar = json_to_nesne()
        yeni_normalize = normalize_name(cihaz_adi)

        for c in cihazlar:
            if normalize_name(c.name) == yeni_normalize:
                QMessageBox.warning(self, "Hata", f"'{cihaz_adi}' adına çok benzeyen bir cihaz zaten mevcut!")
                return   

        if not cihaz_adi or not cihaz_marka:
            QMessageBox.warning(self, "Hata", "Lütfen cihaz adı ve marka giriniz!")
            return

        cihazlar = json_to_nesne()
        cihazlar.append(cihaz)
        nesne_to_json(cihazlar)

        QMessageBox.information(self, "Başarılı", f"{cihaz_turu} eklendi!")
        self.close()
        self.ana_menu.show()   

    def geri_don(self):
        self.close()
        self.ana_menu.show()    