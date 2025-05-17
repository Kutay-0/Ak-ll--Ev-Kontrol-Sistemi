from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QMessageBox
from cihaz_ekle import CihazEkleEkrani
from cihazlarım import CihazlarimEkrani
from veri_yonetimi import json_to_nesne
import speech_recognition as sr
from veri_yonetimi import json_to_nesne, nesne_to_json, komut_isle
import sys
import json
import os

cihazlar = json_to_nesne()
for c in cihazlar:
    print(type(c), c.name , c.marka, c.cihaz_durumu)

class AnaMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ana Menü - Cihaz Kontrol Sistemi")
        self.setGeometry(100, 100, 400, 300)
        self.cihazlar = json_to_nesne()
        self.initUI()
        self.aktif_ekran = None

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Ana Menü", self)
        layout.addWidget(self.label)

        self.cihazlarim_button = QPushButton("Cihazlarım", self)
        self.cihazlarim_button.clicked.connect(self.cihazlarim_ekran)
        layout.addWidget(self.cihazlarim_button)

        self.cihaz_ekle_button = QPushButton("Cihaz Ekle", self)
        self.cihaz_ekle_button.clicked.connect(self.cihaz_ekle_ekran)
        layout.addWidget(self.cihaz_ekle_button)

        self.mikrofon_button = QPushButton("🎤 Mikrofona Konuş", self)
        self.mikrofon_button.clicked.connect(self.mikrofona_konus)
        layout.addWidget(self.mikrofon_button)

        alt_layout = QHBoxLayout()

        self.cikis_button = QPushButton("Çıkış Yap", self)
        self.cikis_button.clicked.connect(self.close)
        alt_layout.addStretch()
        alt_layout.addWidget(self.cikis_button)

        layout.addLayout(alt_layout)
        self.setLayout(layout)


    def cihazlarim_ekran(self):
        self.hide()
        self.cihazlarim_ekrani = CihazlarimEkrani(self, self.cihazlar)
        self.cihazlarim_ekrani.show()
        
    def cihaz_ekle_ekran(self):
        self.hide()
        self.cihaz_ekle_ekran = CihazEkleEkrani(self)
        self.cihaz_ekle_ekran.show()

    def mikrofona_konus(self):
        cihazlar = json_to_nesne()
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Jarvis dinliyor...")
            try:
                audio = recognizer.listen(source, timeout=5)
                komut = recognizer.recognize_google(audio, language="tr-TR")
                print("Jarvis: ",komut)

                sonuc = komut_isle(komut, self.cihazlar, self.aktif_ekran)
                print("Sonuç: ",sonuc)

                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(self, "Jarvis", str(sonuc))

            except sr.UnknownValueError:
                print("Jarvis: Anlayamadım.")
                QMessageBox.warning(self, "Jarvis", "Anlayamadım.")

            except sr.RequestError as e:
                print(f"Jarvis: Hata oluştu; {e}")
                QMessageBox.critical(self, "Jarvis", f"Hata oluştu; {e}")        

if __name__ == "__main__":

    if not os.path.exists("cihazlar.json"):
        bos_veri = {}
        with open("cihazlar.json", "w", encoding="utf-8") as dosya:
            json.dump(bos_veri, dosya, indent=4, ensure_ascii=False)
        print("cihazlar.json dosyası oluşturuldu.")
    else:
        print("cihazlar.json zaten mevcut. Sıfırlama yapılmadı.")

    app = QApplication(sys.argv)
    pencere = AnaMenu()
    pencere.show()
    bos_veri = {}    
    sys.exit(app.exec_())
