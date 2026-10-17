### 1. Ce ascunde mesajul, strat cu strat

Mesajul din probe/mesaj.txt e codat in mai multe straturi. Fiecare strat a fost identificat si desfacut.
- ghici_strat(s) e folosit pentru ghicirea stratului
- desfa(s) e folosit pentru decodarea mesajului

Etapele de decodare

| Pas | Strat recunoscut | Intrare | Ieșire |
|-----|------------------|---------|--------|
| 1 | base64 | `NTM1OTU3NTk=` | `53595759` |
| 2 | hex | `53595759` | `SYWY` |
| 3 | base64 | `SYWY` | `I\x85\x98` |

### 2, Cheie XOR
Fisierul probe/xor.bin e un texr criptat cu xor, cu o cheie de un octet. Am incercat toate cheile de la 0 pana la 255. Pentru fiecare cheie am aplicat xor pe fiecare octet si am verificat daca rezultatul e format de caractere imprimabile.

Prima cheie citibila:
> cheie:  128 ,  Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}

### Parola sparta
Fisierul probe/hashuri.txt contine hasuri. Lungimea lui arata ca e MD5. Am aplicat atac prin dictionar. Pentru fiecare cuvant din probe/wordlist.txt am calculat hashul si l-am comparat cu hashul tinta. 

Primul cuvant care se potriveste:

> Gasit:  password


