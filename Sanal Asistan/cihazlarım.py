
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox
from televizyon_ekrani import TelevizyonEkrani
from lamba_ekrani import LambaEkrani
from veri_yonetimi import json_to_nesne, cihaz_sil
import json
import os

DOSYA_YOLU = os.path.join(os.path.dirname(__file__), "cihazlar.json")
cihaz_nesneleri = json_to_nesne()

class CihazlarimEkrani(QWidget):
    def __init__(self, ana_menu, cihaz_nesneleri):
        super().__init__()
        self.ana_menu = ana_menu
        self.setWindowTitle("Cihazlarım")
        self.cihaz_nesneleri = cihaz_nesneleri
        self.setGeometry(150, 150, 400, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        cihazlar = self.cihazlari_yukle()

        if not cihazlar:
            label = QLabel("Kayıtlı cihaz bulunamadı.", self)
            layout.addWidget(label)
        else:
            for tur in sorted(cihazlar.keys()):
                cihaz_listesi = cihazlar[tur]
                baslik = QLabel(f"{tur}larım - {len(cihaz_listesi)}", self)
                baslik.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
                layout.addWidget(baslik)

                for cihaz in cihaz_listesi:
                    cihaz_layout = QHBoxLayout()
                    btn = QPushButton(f"{cihaz['ad']} ({cihaz['marka']})", self)
                    btn.clicked.connect(lambda _, t=tur, c=cihaz: self.cihaz_tiklandi(t, c))

                    sil_btn = QPushButton("Sil", self)
                    sil_btn.setStyleSheet("background-color: red; color: white;")
                    sil_btn.clicked.connect(lambda _, t=tur, c=cihaz: self.cihaz_sil(t, c)) #istenilen cihazı siler

                    cihaz_layout.addWidget(btn)
                    cihaz_layout.addWidget(sil_btn)
                    layout.addLayout(cihaz_layout)

        alt_layout = QHBoxLayout()
        self.geri_button = QPushButton("Geri", self)
        self.geri_button.clicked.connect(self.geri_don)
        alt_layout.addStretch()
        alt_layout.addWidget(self.geri_button)

        self.cikis_button = QPushButton("Çıkış Yap", self)
        self.cikis_button.clicked.connect(self.close)
        alt_layout.addWidget(self.cikis_button)

        layout.addLayout(alt_layout)
        self.setLayout(layout)

    # Cihazların en güncel durumunu yüklemek için dosyadan okuma yapar.
    def cihazlari_yukle(self):
        if not os.path.exists(DOSYA_YOLU):
            return {}

        with open(DOSYA_YOLU, "r", encoding="utf-8") as dosya:
            try:
                cihazlar = json.load(dosya)
                return cihazlar
            except json.JSONDecodeError:
                return {}

    # Cihaz silme işlemi için onay penceresi açar.
    # Eğer kullanıcı onaylarsa cihazı siler ve güncel listeyi gösterir.
    def cihaz_sil(self, tur, cihaz):
        cevap = QMessageBox.question(self, "Cihaz Sil", f"{cihaz['ad']} cihazını silmek istediğinize emin misiniz?",
                                     QMessageBox.Yes | QMessageBox.No)
        if cevap == QMessageBox.Yes:
            from veri_yonetimi import cihaz_sil, json_to_nesne
            basarili = cihaz_sil(tur, cihaz["ad"], cihaz["marka"])
            if basarili:
                QMessageBox.information(self, "Başarılı", f"{cihaz['ad']} silindi.")
                self.close()
                yeni_ekran = CihazlarimEkrani(self.ana_menu, json_to_nesne())
                yeni_ekran.show()
            else:
                QMessageBox.warning(self, "Hata", "Cihaz silinemedi.")

    # Cihaz tıklandığında hangi ekranın açılacağını belirler.
    # Cihazın türüne göre ilgili ekranı açar.
    def cihaz_tiklandi(self, tur, cihaz_sozlugu):
        cihaz_nesneleri = json_to_nesne()
        cihaz_ad = cihaz_sozlugu["ad"]
        cihaz_marka = cihaz_sozlugu["marka"]
        eslesen_cihaz = None
        for c in cihaz_nesneleri:
            if c.name == cihaz_ad and c.marka == cihaz_marka:
                eslesen_cihaz = c
                break

        if eslesen_cihaz is None:
            QMessageBox.warning(self, "Hata", "Cihaz ait nesne bulunamadı.")
            return

        self.hide()
        if tur == "Televizyon":
            from televizyon_ekrani import TelevizyonEkrani
            self.televizyon_ekrani = TelevizyonEkrani(self, eslesen_cihaz)
            self.ana_menu.aktif_ekran = self.televizyon_ekrani
            self.televizyon_ekrani.show()

        elif tur == "Lamba":
            from lamba_ekrani import LambaEkrani
            self.lamba_ekrani = LambaEkrani(self, eslesen_cihaz)
            self.ana_menu.aktif_ekran = self.lamba_ekrani
            self.lamba_ekrani.show()

        elif tur == "Buzdolabi":
            from buzdolabi_ekrani import BuzdolabiEkrani
            self.buzdolabi_ekrani = BuzdolabiEkrani(self, eslesen_cihaz)
            self.ana_menu.aktif_ekran = self.buzdolabi_ekrani
            self.buzdolabi_ekrani.show()

        elif tur == "Kapi":
            from kapi_ekrani import KapiEkrani
            self.kapi_ekrani = KapiEkrani(self, eslesen_cihaz)
            self.ana_menu.aktif_ekran = self.kapi_ekrani
            self.kapi_ekrani.show()

        else:
            QMessageBox.information(self, "Bilgi", f"{tur} için henüz arayüz yapılmadı.")
            self.show()

    def geri_don(self):
        self.close()
        self.ana_menu.show()
