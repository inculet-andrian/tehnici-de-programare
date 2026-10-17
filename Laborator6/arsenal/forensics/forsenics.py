import re
from PIL import Image
from PIL.ExifTags import TAGS

print("B1:")
def tip_real(cale):
    cap = open(cale, "rb").read(8)

    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()

print(tip_real("../../probe/foto.jpg"))


print("\nB2:")

date = open("../../probe/ascuns.png", "rb").read()

for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode())

print("\nB3:")

def cord_zecimale(cord, emisfera):
    g, m, s = cord
    z = g + (m / 60.0) + (s / 3600.0)
    if (emisfera in ['W', 'S']):
        z = -z
    return z

exif = Image.open("../../probe/foto.jpg").getexif() or {}

gps_info = exif.get_ifd(34853) if hasattr(exif, "get_ifd") else {}

if gps_info:
    lat = gps_info.get(2)
    lat_ref = gps_info.get(1)
    lon = gps_info.get(4)
    lon_ref = gps_info.get(3)

if lat and lat_ref and lon and lon_ref:
    print(f'Lat: {cord_zecimale(lat, lat_ref)}')
    print(f'Long: {cord_zecimale(lon, lon_ref)}')

for id, val in exif.items():
    if (TAGS.get(id,id) != "GPSInfo"):
        print(TAGS.get(id, id), "=", val)


print("\nB4:")
date = open("../../probe/ascuns.png", "rb").read()
i = date.find(b"PK\x03\x04")

if i != -1:
    open("gasit.zip", "wb").write(date[i:])
    print("arhiva extrasa de la octetul", i)



print("\nB5:")

img = Image.open("../../probe/foto.jpg").convert("RGB")
px = list(img.getdata())
mesaj = b"FLAG{ascuns_in_pixeli}" + b"\x00"
biti = "".join(f"{x:08b}" for x in mesaj)

px_nou = []
total_biti = len(biti)
i = 0


for p in px:
    if i>= total_biti:
        px_nou.append(p)
        continue

    canale = list(p)
    for c in range(3):
        if i < total_biti:
            canale[c] = (canale[c] & ~1) | int(biti[i])
            i +=1
    px_nou.append(tuple(canale))

img_noua = Image.new("RGB", img.size)
img_noua.putdata(px_nou)
img_noua.save("stego.png")
print("S-a salvat stego.png")

print("\nB6:")
px = list(Image.open("stego.png").convert("RGB").getdata())
biti = ""
for (r, g, b) in px:
    biti += str(r & 1) + str(g & 1) + str(b & 1)

mesaj = bytearray()
for i in range(0, len(biti) - 7, 8):
    octet = int(biti[i:i+8], 2)

    if octet == 0:
        break
    mesaj.append(octet)

print(mesaj.decode("utf-8", errors="replace"))
