class Cihazlar:
    def __init__(self, nam, brnd):
        self.name = nam             #Cihazın adı
        self.marka = brnd           #Cihazın markası
        self.cihaz_durumu = 0       #Cihazın açık-kapalı durumu (0 ise kapalı, 1 ise açık)

    #Cihazın bilgilerini gösteren metot
    def bilgiler(self):
        print(f"Cihazın adı: {self.name}")
        print(f"Cihazın markası: {self.marka}")
        print(f"Cihazın açık-kapalı durumu: {self.cihaz_durumu}")

    #Cihazı açmak için kullanılan metot
    def cihaz_ac(self):
        if self.cihaz_durumu == 1:
            print("Cihazınız zaten açık durumda")
            return 0
        else:
            self.cihaz_durumu = 1
            print("Cihazınız başarıyla açıldı !")
            return 1

    #Cihazı kapatmak için kullanılan metot
    def cihaz_kapat(self):
        if self.cihaz_durumu == 0:
            print("Cihazının zaten kapalı durumda")
            return 0
        else:
            self.cihaz_durumu = 0
            print("Cihazınız başarıyla kapatıldı !")
            return 1

class Televizyon(Cihazlar):
    def __init__(self, nam, brnd):
        super().__init__(nam, brnd)
        self.parlaklik = 50
        self.ses_duzeyi = 50
        self.goruntu_modlari = ["canlı", "standart", "film", "oyun"]
        self.goruntu_modu = "standart"
        self.kanal_no = 1

    #Televizyonun parlaklığını ayarlayan metot
    def parlaklik_ayarla(self, num):
        if num < 0 or num > 100:
            print("Lütfen 0-100 arasında bir değer giriniz")
            return 0
        else:
            self.parlaklik = num
            print(f"Parlaklık ayarlandı: {self.parlaklik}")
            return 1
        
    #Televizyonun ses düzeyini ayarlayan metot
    def ses_ayarla(self, num):
        if num < 0 or num > 100:
            print("Lütfen 0-100 arasında bir değer giriniz")
            return 0
        else:
            self.ses_duzeyi = num
            print(f"Ses düzeyi ayarlandı: {self.ses_duzeyi}")
            return 1

    #Televizyonun görüntü modunu değiştiren metot
    def goruntu_ayarla(self,mod):
        if mod not in self.goruntu_modlari:
            print("Lütfen geçerli bir mod seçiniz")
            return 0
        else:
            self.goruntu_modu = mod
            print(f"Görüntü modu değiştirildi: {self.goruntu_modu}")
            return 1

    #Televizyonun kanalını değiştiren metot
    def kanal_degistir(self,num):
        if num < 1:
            print("Lütfen 0'dan büyük bir değer giriniz")
            return 0
        else:
            self.kanal_no = num
            print(f"Kanal değiştirildi: {self.kanal_no}")
            return 1

class Lamba(Cihazlar):
    def __init__(self, nam, brnd):
        super().__init__(nam, brnd)
        self.parlaklik = 50
        self.renk = "beyaz"

    #Lambanın parlaklığını değiştiren metot
    def parlaklik_ayarla(self, num):
        if num < 0 or num > 100:
            print(f"Lütfen 0-100 arasında bir değer giriniz")
            return 0
        else:
            self.parlaklik = num
            print(f"Parlaklık ayarlandı: {self.parlaklik}")
            return 1

    #Lambanın rengini değiştiren metot
    def renk_ayarla(self, color):
        color = color.lower()
        if color in ["kırmızı", "yeşil", "mavi"]:
            self.renk = color
            print(f"Renk değiştirildi: {self.renk}")
            return 1
        else:
            print("Lütfen geçerli bir renk giriniz(kırmızı,yeşil,mavi)")
            return 0

class Buzdolabi(Cihazlar):
    def __init__(self, nam, brnd):
        super().__init__(nam, brnd)
        self.sicaklik = 4
        self.buzluk_sicaklik = -18
        self.modlar = ["normal", "ekonomik", "hızlı soğutma"]
        self.secili_mod = "Normal"

    def sicaklik_ayari(self, derece):
        if derece < 1 or derece > 10:
            print("Lütfen 1-10 arasında bir değer giriniz")
            return 0
        else:
            self.sicaklik = derece
            print(f"Sıcaklık ayarlandı: {self.sicaklik}°C")
            return 1

    def buzluk_sicaklik_ayarla(self, derece):
        if derece < -25 or derece > -10:
            print("Lütfen -25 ile -10 arasında bir değer giriniz")
            return 0
        else:
            self.buzluk_sicaklik = derece
            print(f"Buzluk sıcaklığı ayarlandı: {self.buzluk_sicaklik}°C")
            return 1

    def mod_sec(self, mod):
        if mod not in self.modlar:
            print("Lütfen geçerli bir mod seçiniz")
            return 0
        else:
            self.secili_mod = mod
            print(f"Mod değiştirildi: {self.secili_mod}")
            return 1   

class Kapi(Cihazlar):
    def __init__(self, nam, brnd):
        super().__init__(nam, brnd)
        self.kilitli = True #Kapı başlangıçta kilitli

    def kilitle(self):
        if self.kilitli:
            print("Kapı zaten kilitli")
            return 0
        else:
            if self.kapi_durumu:
                print("Kapı açık, kilitlenemez")
                return 0
            
            self.kilitli = True
            print("Kapı kilitlendi")
            return 1
            
    def kilidi_ac(self):
        if not self.kilitli:
            print("Kapı zaten kilitli değil")
            return 0
        else:
            self.kilitli = False
            print("Kapı kilidi açıldı")
            return 1

    def kapiyi_ac(self):
        if self.kilitli:
            print("Kapı kilitli, açılamıyor")
            return 0
        else:
            self.cihaz_durumu = 1
            print("Kapı açıldı")
            return 1

    def kapiyi_kapat(self):
        if not self.kapi_durumu:
            print("Kapı zaten kapalı")
            return 0
        else:
            self.cihaz_durumu = 0
            print("Kapı kapatıldı")
            return 1       