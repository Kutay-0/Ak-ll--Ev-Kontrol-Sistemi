from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QInputDialog, QMessageBox
from veri_yonetimi import json_to_nesne, nesne_to_json

class LambaEkrani(QWidget):
    def __init__(self, ana_pencere, cihaz):
        super().__init__()
        self.ana_pencere = ana_pencere
        self.cihaz = cihaz
        self.setWindowTitle(f"Lamba Ayarları - {cihaz.name}")
        self.setGeometry(200, 200, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Cihaz bilgisi gösteriyoruz:
        baslik1 = QLabel("Cihaz Bilgileri", self)
        baslik1.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")
        layout.addWidget(baslik1)

        ad_label = QLabel(f"Cihaz Adı: {self.cihaz.name}", self)
        marka_label = QLabel(f"Marka: {self.cihaz.marka}", self)
        self.durum_label = QLabel(f"Durum: {'Açık' if self.cihaz.cihaz_durumu else 'Kapalı'}", self)
        layout.addWidget(self.durum_label)

        layout.addWidget(ad_label)
        layout.addWidget(marka_label)

        layout.addSpacing(20)

        baslik2 = QLabel("Cihaz Özellikleri", self)
        baslik2.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")
        layout.addWidget(baslik2)

        self.parlaklik_label = QLabel(f"Parlaklık: {self.cihaz.parlaklik}", self)
        self.renk_label = QLabel(f"Renk: {self.cihaz.renk}", self)

        layout.addWidget(self.parlaklik_label)
        layout.addWidget(self.renk_label)
        # Buraya ayar butonları gelecek (parlaklık, renk vb.)

        #---------PARLAKLIK AYARLA----------
        btn_parlaklik = QPushButton("Parlaklık Ayarla", self)
        btn_parlaklik.clicked.connect(self.parlaklik_ayarla)
        layout.addWidget(btn_parlaklik)

        #---------RENK AYARLA----------
        btn_renk = QPushButton("Rengini Değiştir", self)
        btn_renk.clicked.connect(self.rengini_degistir)
        layout.addWidget(btn_renk)

        #---------CİHAZI AC----------
        btn_ac = QPushButton("Cihazı Aç", self)
        btn_ac.clicked.connect(self.cihaz_ac)
        layout.addWidget(btn_ac)

        #---------CİHAZI KAPAT----------
        btn_kapat = QPushButton("Cihazı Kapat", self)
        btn_kapat.clicked.connect(self.cihaz_kapat)
        layout.addWidget(btn_kapat)

        # Geri dönmek için buton
        alt_layout = QHBoxLayout()
        geri_btn = QPushButton("Geri", self)
        geri_btn.clicked.connect(self.geri_don)
        alt_layout.addStretch()
        alt_layout.addWidget(geri_btn)

        layout.addLayout(alt_layout)
        self.setLayout(layout)

    def guncelle_bilgiler(self):
        print("Güncelleniyor...")
        self.parlaklik_label.setText(f"Parlaklık: {self.cihaz.parlaklik}")
        self.renk_label.setText(f"Renk: {self.cihaz.renk}")
        self.durum_label.setText(f"Durum: {'Açık' if self.cihaz.cihaz_durumu else 'Kapalı'}")   

    def parlaklik_ayarla(self):
        num, ok = QInputDialog.getInt(self, "Parlaklık Ayarla", "Parlaklık (0-100):")
        if ok:
            self.cihaz.parlaklik_ayarla(num)
            self.guncelle_bilgiler()

    def rengini_degistir(self):
        renk, ok = QInputDialog.getItem(self, "Renk Değiştir", "Bir Renk Seçin:",["Kırmızı", "Mavi", "Yeşil"], editable=False)
        if ok:
            self.cihaz.renk_ayarla(renk)
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