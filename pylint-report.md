# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksen lopullisesta versiosta:
```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:26:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:31:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:35:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:45:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:53:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:65:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:106:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:110:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:142:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:161:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:173:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:179:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:234:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:255:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:272:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:332:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:345:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:363:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:382:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:390:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:433:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:444:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:11:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module events
events.py:1:0: C0114: Missing module docstring (missing-module-docstring)
events.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:23:0: R0913: Too many arguments (6/5) (too-many-arguments)
events.py:23:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
events.py:42:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:52:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:59:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:69:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:74:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:82:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:82:0: R0913: Too many arguments (6/5) (too-many-arguments)
events.py:82:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
events.py:100:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:108:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:108:0: R0913: Too many arguments (6/5) (too-many-arguments)
events.py:108:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
events.py:137:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module seed
seed.py:1:0: C0114: Missing module docstring (missing-module-docstring)
seed.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
seed.py:10:0: R0914: Too many local variables (38/15) (too-many-locals)
seed.py:10:0: R0915: Too many statements (53/50) (too-many-statements)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:9:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:24:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:33:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:42:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:51:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:60:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:67:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:71:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.67/10 (previous run: 8.63/10, +0.04)
```

Seuraavaksi perustellaan, miksi edellä raportissa mainittuja kohtia ei ole korjattu.

## Docstring-ilmoitukset

Valtaosa raportin ilmoituksista on seuraavanlaisia docstring-ilmoituksia:

```
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
```

Sovelluksen kehityksessä on päätetty, ettei siinä käytetä docstringejä, joten sen takia ne puuttuvat myös moduuleista ja funktioista.

## Liian monta argumenttia funktioissa

Tiedostossa `events.py` esiintyy seuraavanlaisia ilmoituksia:

```
events.py:108:0: R0913: Too many arguments (6/5) (too-many-arguments)
events.py:108:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
```

Nämä huomautukset liittyvät funktioihin, jotka vastaavat tapahtumien etsimisestä. Kurssivaatimukset huomioon ottaen, on paras tapa jättää kaikki argumentit koodiin eikä alkaa kehittelemään jotain vaihtoehtoista tapaa suorittaa asioita.

## Liian monta paikallista muuttujaa ja komentoa

Tiedostossa `seed.py` esiintyy seuraavanlaiset ilmoitukset:

```
seed.py:10:0: R0914: Too many local variables (38/15) (too-many-locals)
seed.py:10:0: R0915: Too many statements (53/50) (too-many-statements)
```

Nämä varoitukset kohdistuvat `seed_database`-funktioon, jonka tarkoituksena on syöttää testidataa järjestelmään ohjelman suorituskyvyn mittaamista varten. Koska testidata tulee syöttää tietyssä järjestyksessä, ja koska kyseessä on ainoastaan testidatan syöttämisestä vastaava tiedosto, kannattaa nykyinen muotoilu säilyttää tiedostossa eikä alkaa monimutkaistamaan kyseistä skriptiä esimerkiksi paloittelemalla sitä useampaan funktioon.