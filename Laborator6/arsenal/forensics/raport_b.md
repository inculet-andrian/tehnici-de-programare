### 1. Tipul real al fisierrelor
Extensia unui fisier nu spune nimic garantat despre continutul lui. Scriptul citeste primii 8 bytes si compara cu semnaturile cunoscute.

#### foto.jpg:
> Primii bytes al fisierului foto.jpg sunt FF D8 FF E0 00 10 4A 46. Asta este semnatura JPEG. Tipul fisierului image.jpg corespunde extensiei.

### 2. Metadate (exif si gps)
Scriptul citeste metadatele EXIF din foto.jpg cu getexif(). Blocul GPS contine coordonatele. 

#### Metadate generale

> - Model = iPhone 13
> - Make = Apple
> - DateTime = 2026:09:14 10:30:00

#### Coordonate GPS
> - Lat: 47.016666666666666
> - Long: 28.8575


Concluzie - fotografia pastreaza coordonatele a locului unde a fost efectuata poza. Daca ar fi publicata, oricine cu cunostintele date ar putea afla locul pozei. Platformele social media in mod normal sterg aceste metadate.

### 3. Arhiva ascunsa in ascuns.png
Am cautat in fisierul ascuns.png cu semnatura ZIP PK\x03\x04. AM gasit-o la pozitia byteului 781. Datele arhivei sunt de la aceasta pozitie pana la sfarsit.

Sirurile imprimabile din pasul 2 arata numele fisierului din arhiva si continutul sau:

> - secret.txtFLAG{ascuns_prin_carving}
> - secret.txtPK

Structura arhivei zip e alcatuit din fisierul secret.txt. La deschiderea lui vad flagul urmator:

`FLAG{ascuns_prin_carving}`