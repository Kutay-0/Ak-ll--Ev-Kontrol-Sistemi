from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QInputDialog, QMessageBox
from veri_yonetimi import json_to_nesne, nesne_to_json

class TelevizyonEkrani(QWidget):
    def __init__(self, ana_pencere, cihaz_nesnesi):
        super().__init__()
        self.ana_pencere = ana_pencere
        self.cihaz = cihaz_nesnesi
        self.setWindowTitle(f"Televizyon Ayarları - {cihaz_nesnesi.name}")
        self.setGeometry(200, 200, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        baslik1 = QLabel("Cihaz Bilgileri", self)
        baslik1.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")
        layout.addWidget(baslik1)

        self.ad_label = QLabel(f"Cihaz Adı: {self.cihaz.name}", self)
        self.marka_label = QLabel(f"Marka: {self.cihaz.marka}", self)
        self.durum_label = QLabel(f"Durum: {self.cihaz.cihaz_durumu}", self)

        layout.addWidget(self.ad_label)
        layout.addWidget(self.marka_label)
        layout.addWidget(self.durum_label)

        layout.addSpacing(20)

        baslik2 = QLabel("Cihaz Özellikleri", self)
        baslik2.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")
        layout.addWidget(baslik2)

        self.parlaklik_label = QLabel(f"Parlaklık: {self.cihaz.parlaklik}", self)
        self.ses_seviyesi_label = QLabel(f"Ses Seviyesi: {self.cihaz.ses_duzeyi}", self)
        self.goruntu_modu_label = QLabel(f"Görüntü Modu: {self.cihaz.goruntu_modu}", self)
        self.kanal_label = QLabel(f"Kanal: {self.cihaz.kanal_no}", self)

        layout.addWidget(self.parlaklik_label)
        layout.addWidget(self.ses_seviyesi_label)
        layout.addWidget(self.goruntu_modu_label)
        layout.addWidget(self.kanal_label)

        alt_layout = QHBoxLayout()
        geri_btn = QPushButton("Geri", self)
        geri_btn.clicked.connect(self.geri_don)
        alt_layout.addStretch()
        alt_layout.addWidget(geri_btn)

        layout.addLayout(alt_layout)

        self.setLayout(layout)

        #--------PARLAKLIK AYARLA----------
        btn_parlaklik = QPushButton("Parlaklık Ayarla", self)
        btn_parlaklik.clicked.connect(self.parlaklik_ayarla)
        layout.addWidget(btn_parlaklik)

        #--------SES AYARLA----------
        btn_ses = QPushButton("Ses Ayarla", self)
        btn_ses.clicked.connect(self.ses_ayarla)
        layout.addWidget(btn_ses)

        #--------GÖRÜNTÜ MODU DEĞİŞTİR----------
        btn_mod = QPushButton("Görüntü Modu Değiştir", self)
        btn_mod.clicked.connect(self.goruntu_modu_degistir)
        layout.addWidget(btn_mod)

        #--------KANAL DEĞİŞTİR----------
        btn_kanal = QPushButton("Kanal Değiştir", self)
        btn_kanal.clicked.connect(self.kanal_degistir)
        layout.addWidget(btn_kanal)

        #--------CİHAZI AÇ----------
        btn_ac = QPushButton("Cihazı Aç", self)
        btn_ac.clicked.connect(self.cihaz_ac)
        layout.addWidget(btn_ac)

        #--------CİHAZI KAPAT----------
        btn_kapat = QPushButton("Cihazı Kapat", self)
        btn_kapat.clicked.connect(self.cihaz_kapat)
        layout.addWidget(btn_kapat)

        layout.addLayout(alt_layout)
        self.setLayout(layout)

    def guncelle_bilgiler(self):
        self.durum_label.setText(f"Durum: {'Açık' if self.cihaz.cihaz_durumu else 'Kapalı'}")
        self.parlaklik_label.setText(f"Parlaklık: {self.cihaz.parlaklik}")
        self.ses_seviyesi_label.setText(f"Ses Seviyesi: {self.cihaz.ses_duzeyi}")
        self.goruntu_modu_label.setText(f"Görüntü Modu: {self.cihaz.goruntu_modu}")
        self.kanal_label.setText(f"Kanal: {self.cihaz.kanal_no}")   

    def parlaklik_ayarla(self):
        num, ok = QInputDialog.getInt(self, "Parlaklık", "Parlaklık değerini girin (0-100):")
        if ok:
            self.cihaz.parlaklik_ayarla(num)
            self.guncelle_bilgiler()

    def ses_ayarla(self):
        num, ok = QInputDialog.getInt(self, "Ses Ayarı", "Ses düzeyini girin (0-100):")
        if ok:
            self.cihaz.ses_ayarla(num)
            self.guncelle_bilgiler()

    def goruntu_modu_degistir(self):
        mod, ok = QInputDialog.getItem(self, "Görüntü Modu", "Görüntü modunu seçin:", self.cihaz.goruntu_modlari, editable= False)
        if ok and mod:
            self.cihaz.goruntu_ayarla(mod)
            self.guncelle_bilgiler()

    def kanal_degistir(self):
        num, ok = QInputDialog.getInt(self, "Kanal Değiştir", "Kanal numarasını girin:")
        if ok:
            self.cihaz.kanal_degistir(num)
            self.guncelle_bilgiler()

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