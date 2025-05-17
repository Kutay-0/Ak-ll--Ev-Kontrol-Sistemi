from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QInputDialog, QHBoxLayout
from veri_yonetimi import json_to_nesne, nesne_to_json

class BuzdolabiEkrani(QWidget):
    def __init__(self, ana_pencere, cihaz):
        super().__init__()
        self.ana_pencere = ana_pencere
        self.cihaz = cihaz
        self.setWindowTitle(f"Buzdolabı Ayarları - {cihaz.name}")
        self.setGeometry(200, 200, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Cihaz bilgileri başlığı
        baslik1 = QLabel("Cihaz Bilgileri", self)
        baslik1.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(baslik1)

        layout.addWidget(QLabel(f"Cihaz Adı: {self.cihaz.name}", self))
        layout.addWidget(QLabel(f"Marka: {self.cihaz.marka}", self))
        
        self.durum_label = QLabel(f"Durum: {'Açık' if self.cihaz.cihaz_durumu else 'Kapalı'}", self)
        layout.addWidget(self.durum_label)

        layout.addSpacing(15)

        # Cihaz özellikleri başlığı
        baslik2 = QLabel("Cihaz Özellikleri", self)
        baslik2.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(baslik2)

        self.sicaklik_label = QLabel(f"Sıcaklık: {self.cihaz.sicaklik}°C", self)
        layout.addWidget(self.sicaklik_label)

        self.buzluk_sicaklik_label = QLabel(f"Buzluk Sıcaklığı: {self.cihaz.buzluk_sicaklik}°C", self)
        layout.addWidget(self.buzluk_sicaklik_label)

        self.mod_label = QLabel(f"Mod: {self.cihaz.secili_mod}", self)
        layout.addWidget(self.mod_label)

        layout.addSpacing(10)

        # --- Butonlar ---
        btn_sicaklik = QPushButton("Sıcaklık Ayarla", self)
        btn_sicaklik.clicked.connect(self.sicaklik_ayarla)
        layout.addWidget(btn_sicaklik)

        btn_buzluk = QPushButton("Buzluk Sıcaklığını Ayarla", self)
        btn_buzluk.clicked.connect(self.buzluk_ayarla)
        layout.addWidget(btn_buzluk)

        btn_mod = QPushButton("Mod Seç", self)
        btn_mod.clicked.connect(self.mod_degistir)
        layout.addWidget(btn_mod)

        btn_ac = QPushButton("Cihazı Aç", self)
        btn_ac.clicked.connect(self.cihaz_ac)
        layout.addWidget(btn_ac)

        btn_kapat = QPushButton("Cihazı Kapat", self)
        btn_kapat.clicked.connect(self.cihaz_kapat)
        layout.addWidget(btn_kapat)

        # Geri butonu
        alt_layout = QHBoxLayout()
        btn_geri = QPushButton("Geri", self)
        btn_geri.clicked.connect(self.geri_don)
        alt_layout.addStretch()
        alt_layout.addWidget(btn_geri)

        layout.addLayout(alt_layout)
        self.setLayout(layout)

    # --- Metotlar ---
    def sicaklik_ayarla(self):
        derece, ok = QInputDialog.getInt(self, "Sıcaklık Ayarı", "1-10 °C arasında bir değer giriniz:")
        if ok:
            self.cihaz.sicaklik_ayari(derece)
            self.guncelle_bilgiler()

    def buzluk_ayarla(self):
        derece, ok = QInputDialog.getInt(self, "Buzluk Ayarı", "-25 ile -10 °C arasında bir değer giriniz:")
        if ok:
            self.cihaz.buzluk_sicaklik_ayarla(derece)
            self.guncelle_bilgiler()

    def mod_degistir(self):
        secim, ok = QInputDialog.getItem(
            self, "Mod Seç", "Bir mod seçiniz:",
            self.cihaz.modlar,
            editable=False
        )
        if ok:
            self.cihaz.mod_sec(secim)
            self.guncelle_bilgiler()
    
    def guncelle_bilgiler(self):
        self.sicaklik_label.setText(f"Sıcaklık: {self.cihaz.sicaklik}°C")
        self.buzluk_sicaklik_label.setText(f"Buzluk Sıcaklığı: {self.cihaz.buzluk_sicaklik}°C")
        self.mod_label.setText(f"Mod: {self.cihaz.secili_mod}")
        self.durum_label.setText(f"Durum: {'Açık' if self.cihaz.cihaz_durumu else 'Kapalı'}")


    def cihaz_ac(self):
        self.cihaz.cihaz_ac()
        nesne_to_json(json_to_nesne())
        self.guncelle_bilgiler()

    def cihaz_kapat(self):
        self.cihaz.cihaz_kapat()
        nesne_to_json(json_to_nesne())
        self.guncelle_bilgiler()

    def geri_don(self):
        self.close()
        self.ana_pencere.show()
