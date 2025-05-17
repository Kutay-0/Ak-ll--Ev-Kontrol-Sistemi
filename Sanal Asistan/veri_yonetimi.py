import json
import re
from kontroller import Cihazlar, Televizyon, Lamba, Buzdolabi, Kapi

# Proje klasöründeki cihazlar.json'a doğru gidelim
DOSYA_YOLU = "cihazlar.json"

# Cihazları JSON dosyasından oku ve nesne listesine dönüştür
def json_to_nesne(dosya_yolu=DOSYA_YOLU):
    cihaz_nesneleri = []

    try:
        with open(dosya_yolu, "r", encoding="utf-8") as dosya:
            cihazlar = json.load(dosya)
    except (FileNotFoundError, json.JSONDecodeError):
        # Dosya yoksa veya boşsa sıfırdan başla
        return cihaz_nesneleri

    for tur, cihaz_listesi in cihazlar.items():
        for c in cihaz_listesi:
            if tur == "Televizyon":
                cihaz = Televizyon(c["ad"], c["marka"])
                cihaz.parlaklik = c.get("parlaklik", 50)
                cihaz.ses_duzeyi = c.get("ses_duzeyi", 50)
                cihaz.goruntu_modu = c.get("goruntu_modu", "standart")
                cihaz.kanal_no = c.get("kanal_no", 1)

            elif tur == "Lamba":
                cihaz = Lamba(c["ad"], c["marka"])
                cihaz.parlaklik = c.get("parlaklik", 50)
                cihaz.renk = c.get("renk", "beyaz")

            elif tur == "Buzdolabi":
                cihaz = Buzdolabi(c["ad"], c["marka"])
                cihaz.sicaklik = c.get("sicaklik", 4)
                cihaz.buzluk_sicaklik = c.get("buzluk_sicaklik", -18)
                cihaz.secili_mod = c.get("mod", "Normal")

            elif tur == "Kapi":
                cihaz = Kapi(c["ad"], c["marka"])
                cihaz.kilitli = c.get("kilitli", True)
                cihaz.kapi_durumu = c.get("kapi_durumu", False)

            else:
                continue  # Bilinmeyen türler atla

            cihaz.cihaz_durumu = 1 if c.get("durum", "Kapalı") == "Açık" else 0
            cihaz_nesneleri.append(cihaz)

    return cihaz_nesneleri

# Cihaz nesnelerini JSON dosyasına yaz
def nesne_to_json(cihaz_nesneleri, dosya_yolu=DOSYA_YOLU):
    cihazlar_json = {}

    for cihaz in cihaz_nesneleri:
        tur = type(cihaz).__name__
        if tur not in cihazlar_json:
            cihazlar_json[tur] = []

        cihaz_dict = {
            "ad": cihaz.name,
            "marka": cihaz.marka,
            "durum": "Açık" if cihaz.cihaz_durumu else "Kapalı",
        }

        if isinstance(cihaz, Televizyon):           # Televizyon sınıfı için
            cihaz_dict.update({                     # Televizyon nesnesinin özelliklerini ekle
                "parlaklik": cihaz.parlaklik,
                "ses_duzeyi": cihaz.ses_duzeyi,
                "goruntu_modu": cihaz.goruntu_modu,
                "kanal_no": cihaz.kanal_no,
            })

        elif isinstance(cihaz, Lamba):              # Lamba sınıfı için 
            cihaz_dict.update({                     # Lamba nesnesinin özelliklerini ekle
                "parlaklik": cihaz.parlaklik,
                "renk": cihaz.renk,
            })

        elif isinstance(cihaz, Buzdolabi):          # Buzdolabı sınıfı için
            cihaz_dict.update({                     # Buzdolabı nesnesinin özelliklerini ekle    
                "sicaklik": cihaz.sicaklik,
                "buzluk_sicaklik": cihaz.buzluk_sicaklik,
                "mod": cihaz.secili_mod,
            })

        elif isinstance(cihaz, Kapi):               # Kapi sınıfı için
            cihaz_dict.update({                     # Kapi nesnesinin özelliklerini ekle    
                "kilitli": cihaz.kilitli,
                "kapi_durumu": cihaz.kapi_durumu,
            })

        # Diğer türler için ekleme yapabilirsiniz

        cihazlar_json[tur] = cihazlar_json.get(tur, []) + [cihaz_dict]

    with open(dosya_yolu, "w", encoding="utf-8") as dosya:
        json.dump(cihazlar_json, dosya, indent=4, ensure_ascii=False)

# Gelen sesli komutları işleyerek cihazları kontrol etmek için kullanılır
def komut_isle(komut, cihazlar, aktif_ekran=None):
    komut = sayi_yazidan_rakama(komut)
    komut = re.sub(r"(\b\w+)\s+(\d+)\b", r"\1\2", komut)
    # Türkçe karakterleri de yakalamak için \w yerine Unicode harf ve boşluk kullanıyoruz
    deger = None

    if "cihazının" not in komut and "cihazını" not in komut:
        return "Komut formatı anlaşılamadı"
    
    if "cihazının" in komut:
        raw_ad, rest = komut.split("cihazının", 1)
    elif "cihazını" in komut:
        raw_ad, rest = komut.split("cihazını", 1)
    else:
        return "Komut formatı anlaşılamadı"
    
    ad = normalize_name(raw_ad)

    if deger is None:
        kelimeler = komut.split()
        for kelime in kelimeler:
            sayi = yazi_sayi_cevir(kelime)
            if sayi is not None:
                deger = sayi
                break

    ozellik = rest.lower()        

    m = re.search(r"-?\d+", rest) # Bu, sayıları yakalamak için kullanılır
    if m:
        deger = int(m.group())
    else:
        # Sayı bulunamazsa, mod gibi metin değeri olup olmadığını dene
        kelimeler = rest.strip().split()
        gereksizler = ["olarak", "ayarla", "değiştir", "modunu", "rengini", "modu", "parlaklığını", "sesini", "kanalını","derecesini", "sıcaklığını","soğukluğunu"]
        for i in range(len(kelimeler)):
            if kelimeler[i] not in gereksizler:
                deger = kelimeler[i]
                break

    if deger is None:
        return "Değer bulunamadı."

    print(f"Gelen renk değeri: {deger} - Türü: {type(deger)}")

    hedef = None
    for cihaz in cihazlar:
        print("cihaz adı:", cihaz.name, "-> Normalize:", normalize_name(cihaz.name))
        print("ad:", ad)
        if normalize_name(cihaz.name) == ad.lower():
            hedef = cihaz
            break

    if not hedef:
        return f"{ad} adında bir cihaz bulunamadı."

    try:
        if "aç" in komut and hasattr(hedef, "cihaz_ac"):
            ok = hedef.cihaz_ac()
            if ok:
                nesne_to_json(cihazlar)
                if aktif_ekran:
                    aktif_ekran.guncelle_bilgiler()
                return f"{ad} açıldı."
            else:
                return f"{ad} zaten açık."

        if "kapat" in komut and hasattr(hedef, "cihaz_kapat"):
            ok = hedef.cihaz_kapat()
            if ok:
                nesne_to_json(cihazlar)
                if aktif_ekran:
                    aktif_ekran.guncelle_bilgiler()
                return f"{ad} kapatıldı."
            else:
                return f"{ad} zaten kapalı."
        
        if ("renk" in ozellik or "rengini" in ozellik) and hasattr(hedef, "renk_ayarla"):
            if deger is not None:
                ok = hedef.renk_ayarla(deger)
                if ok:
                    nesne_to_json(cihazlar)
                    if aktif_ekran:
                        aktif_ekran.guncelle_bilgiler()
                    return f"{ad} rengi {deger} olarak ayarlandı."
                else:
                    return "Renk ayarlanmadı"
            else:
                return "Renk değeri belirtilmedi."

        if "parlak" in ozellik and hasattr(hedef, "parlaklik_ayarla"):
            if deger is not None:
                ok = hedef.parlaklik_ayarla(int(deger))
                if ok:
                    nesne_to_json(cihazlar)
                    if aktif_ekran:
                        aktif_ekran.guncelle_bilgiler()
                    return f"{ad} parlaklığı {deger} olarak ayarlandı."
                else:
                    return "Parlaklık ayarlanmadı"
            else:
                return "Parlaklık değeri belirtilmedi."    

        if "ses" in ozellik and hasattr(hedef, "ses_ayarla"):
            if deger is not None:
                ok = hedef.ses_ayarla(int(deger))
                if ok:
                    nesne_to_json(cihazlar)
                    if aktif_ekran:
                        aktif_ekran.guncelle_bilgiler()
                    return f"{ad} ses seviyesi {deger} olarak ayarlandı."
                else:
                    return "Ses ayarlanmadı"
            return "Ses seviyesi değeri belirtilmedi."

        if "kanal" in ozellik and hasattr(hedef, "kanal_degistir"):
            if deger is not None:
                ok = hedef.kanal_degistir(int(deger))
                if ok:
                    nesne_to_json(cihazlar)
                    if aktif_ekran:
                        aktif_ekran.guncelle_bilgiler()
                    return f"{ad} kanal numarası {deger} olarak ayarlandı."
                else:
                    return "Kanal ayarlanmadı"
            return "Kanal numarası değeri belirtilmedi."

        if ("mod" in ozellik or "modunu" in ozellik) and (hasattr(hedef, "mod_sec") or hasattr(hedef, "goruntu_ayarla")):
            if deger is not None:
                if isinstance(hedef, Televizyon):
                    ok = hedef.goruntu_ayarla(deger)
                elif isinstance(hedef, Buzdolabi):
                    ok = hedef.mod_sec(deger.lower())
                else:
                    return "Bu cihaz mod ayarını desteklemiyor."

                if ok:
                    nesne_to_json(cihazlar)
                    if aktif_ekran:
                        aktif_ekran.guncelle_bilgiler()
                    return f"{ad} mod {deger} olarak ayarlandı."
            else:
                return "Mod ayarlanmadı"
            
            return "Mod değeri belirtilmedi."
        
        if ("sıcaklığını" in ozellik or "derecesini" in ozellik) and hasattr(hedef, "sicaklik_ayari"):
            if deger is not None:
                ok = hedef.sicaklik_ayari(int(deger))
                if ok:
                    nesne_to_json(cihazlar)
                    if aktif_ekran:
                        aktif_ekran.guncelle_bilgiler()
                    return f"{ad} sıcaklığı {deger} olarak ayarlandı."
                else:
                    return "Sıcaklık ayarlanmadı"
            else:
                return "Sıcaklık değeri belirtilmedi."

        if ("buzluk sıcaklığını" in ozellik or "buzluk derecesini") and hasattr(hedef, "buzluk_sicaklik_ayarla"):
            if deger is not None:
                ok = hedef.buzluk_sicaklik_ayarla(int(deger))
                if ok:
                    nesne_to_json(cihazlar)
                    if aktif_ekran:
                        aktif_ekran.guncelle_bilgiler()
                    return f"{ad} buzluk sıcaklığı {deger} olarak ayarlandı."
                else:
                    return "Buzluk sıcaklığı ayarlanmadı"
            else:
                return "Buzluk sıcaklığı değeri belirtilmedi."


        if "kilidini" in ozellik and "aç" in komut and hasattr(hedef, "kilidi_ac"):
            ok = hedef.kilidi_ac()
            if ok:
                nesne_to_json(cihazlar)
                if aktif_ekran:
                    aktif_ekran.guncelle_bilgiler()
                return f"{ad} kilidi açıldı."
            else:
                return f"{ad} zaten açık."
            
        if "kilitle" in ozellik and hasattr(hedef, "kilitle"):
            ok = hedef.kilitle()
            if ok:
                nesne_to_json(cihazlar)
                if aktif_ekran:
                     aktif_ekran.guncelle_bilgiler()
                return f"{ad} kilitlendi."
            else:
                 return f"{ad} zaten kapalı."

        if "aç" in komut and hasattr(hedef, "kapiyi_ac"):
            ok = hedef.kapiyi_ac()
            if ok:
                nesne_to_json(cihazlar)
                if aktif_ekran:
                    aktif_ekran.guncelle_bilgiler()
                return f"{ad} kapısı açıldı."
            else:
                return f"{ad} kapısı zaten açık."
            
        if "kapat" in komut and hasattr(hedef, "kapiyi_kapat"):
            ok = hedef.kapiyi_kapat()
            if ok:
                nesne_to_json(cihazlar)
                if aktif_ekran:
                    aktif_ekran.guncelle_bilgiler()
                return f"{ad} kapısı kapatıldı."

    except Exception as e:
        return f"Hata oluştu: {e}"

    return "Komutla eşleşen bir işlem bulunamadı."

# Yazı şeklindeki sayıları işleme tabi tutulabilen rakamlara çevirir
def yazi_sayi_cevir(kelime):
    sayilar = {
        "sıfır": 0, "bir": 1, "iki": 2, "üç": 3, "dört": 4, "beş": 5,
        "altı": 6, "yedi": 7, "sekiz": 8, "dokuz": 9,
        "on": 10, "yirmi": 20, "otuz": 30, "kırk": 40, "elli": 50,
        "altmış": 60, "yetmiş": 70, "seksen": 80, "doksan": 90,
        "yüz": 100
    }

    kelime = kelime.lower().strip()

    negatif = False
    if kelime.startswith("eksi"):
        negatif = True
        kelime = kelime.replace("eksi","").strip()

    deger = sayilar.get(kelime, None)
    if deger is not None:
        return -deger if negatif else deger
       
    return sayilar.get(kelime.strip(), None)

# Bu fonksiyon, metindeki sayıları yazıdan rakama çevirir
def sayi_yazidan_rakama(metin):
    sayi_map = {
        "bir": "1", "iki": "2", "üç": "3", "dört": "4", "beş": "5",
        "altı": "6", "yedi": "7", "sekiz": "8", "dokuz": "9",
        "on": "10", "sıfır": "0"
    }

    kelimeler = metin.split()
    yeni_kelimeler = []

    for i in range(len(kelimeler)-1):
        ilk = kelimeler[i]
        ikinci = kelimeler[i+1]

        if ilk in sayi_map and ikinci == "cihazının":
            yeni_kelimeler.append(sayi_map[ilk] + "cihazının")
            yeni_kelimeler += kelimeler[i+2:]
            return " ".join(yeni_kelimeler)
        
        elif ilk not in sayi_map:
            yeni_kelimeler.append(ilk)

    return metin

# Normalizasyon işlemi için Türkçe karakterleri ve sayıları düzelt
def normalize_name(text: str) -> str:
    text = text.lower()

    turkce_map = str.maketrans(
        "şğüçöı", "sgucoi"  # Türkçe karakterleri İngilizce karşılıklarına çevir
    )

    text = text.translate(turkce_map)

    word2digit = {
        "sıfır": "0", "bir": "1", "iki": "2", "üç": "3", "dört": "4",
        "beş": "5", "altı": "6", "yedi": "7", "sekiz": "8", "dokuz": "9", "on": "10"
    }
    for word , digit in word2digit.items():
        text = re.sub(rf"\b{word}\b", digit, text) # kelimeyi rakama çevir

    text = re.sub(r"\s+", "", text) # boşlukları kaldır

    return text

# Kayıtlı cihazları silmek için kullanılır
def cihaz_sil(tur, ad, marka, dosya_yolu=DOSYA_YOLU):
    cihazlar = {}
    with open(dosya_yolu, "r", encoding="utf-8") as dosya:
        cihazlar = json.load(dosya)

    if tur in cihazlar:
        cihazlar[tur] = [
            c for c in cihazlar[tur]
            if not (normalize_name(c["ad"]) == normalize_name(ad) and c["marka"] == marka)
        ]
        with open(dosya_yolu, "w", encoding="utf-8") as dosya:
            json.dump(cihazlar, dosya, indent=4, ensure_ascii=False)
        return True
    return False
