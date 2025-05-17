from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from veri_yonetimi import json_to_nesne, nesne_to_json

class KapiEkrani(QWidget):
    def __init__(self, ana_pencere, cihaz):
        super().__init__()
        self.ana_pencere = ana_pencere
        self.cihaz = cihaz
        self.setWindowTitle(f"Kapı Ayarları - {cihaz.name}")
        self.setGeometry(200, 200, 400, 300)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Cihaz bilgileri
        baslik1 = QLabel("Cihaz Bilgileri", self)
        baslik1.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.layout.addWidget(baslik1)

        self.ad_label = QLabel(self)
        self.marka_label = QLabel(self)
        self.durum_label = QLabel(self)

        self.layout.addWidget(self.ad_label)
        self.layout.addWidget(self.marka_label)
        self.layout.addWidget(self.durum_label)

        self.layout.addSpacing(15)

        # Kapı özellikleri
        baslik2 = QLabel("Kapı Özellikleri", self)
        baslik2.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.layout.addWidget(baslik2)

        self.kilit_label = QLabel(self)
        self.layout.addWidget(self.kilit_label)

        self.layout.addSpacing(10)

        # --- Butonlar ---
        btn_kilitle = QPushButton("Kilitle", self)
        btn_kilitle.clicked.connect(self.kilitle)
        self.layout.addWidget(btn_kilitle)

        btn_kilit_ac = QPushButton("Kilidi Aç", self)
        btn_kilit_ac.clicked.connect(self.kilidi_ac)
        self.layout.addWidget(btn_kilit_ac)

        btn_ac = QPushButton("Kapıyı Aç", self)
        btn_ac.clicked.connect(self.kapiyi_ac)
        self.layout.addWidget(btn_ac)

        btn_kapat = QPushButton("Kapıyı Kapat", self)
        btn_kapat.clicked.connect(self.kapiyi_kapat)
        self.layout.addWidget(btn_kapat)

        # Geri butonu
        alt_layout = QHBoxLayout()
        btn_geri = QPushButton("Geri", self)
        btn_geri.clicked.connect(self.geri_don)
        alt_layout.addStretch()
        alt_layout.addWidget(btn_geri)
        self.layout.addLayout(alt_layout)

        self.setLayout(self.layout)
        self.guncelle_bilgiler()

    # --- Etiketleri güncelle ---
    def guncelle_bilgiler(self):
        self.ad_label.setText(f"Cihaz Adı: {self.cihaz.name}")
        self.marka_label.setText(f"Marka: {self.cihaz.marka}")
        self.durum_label.setText(f"Durum: {'Açık' if self.cihaz.cihaz_durumu else 'Kapalı'}")
        self.kilit_label.setText(f"Kilitli mi: {'Evet' if self.cihaz.kilitli else 'Hayır'}")

    # --- Komutlar ---
    def kilitle(self):
        self.cihaz.kilitle()
        self.guncelle_bilgiler()

    def kilidi_ac(self):
        self.cihaz.kilidi_ac()
        self.guncelle_bilgiler()

    def kapiyi_ac(self):
        self.cihaz.kapiyi_ac()
        nesne_to_json(json_to_nesne())
        self.guncelle_bilgiler()

    def kapiyi_kapat(self):
        self.cihaz.kapiyi_kapat()
        nesne_to_json(json_to_nesne())
        self.guncelle_bilgiler()

    def geri_don(self):
        self.close()
        self.ana_pencere.show()
