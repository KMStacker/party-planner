# Party Planner (Tapahtumasovellus)

Sovelluksessa käyttäjät pystyvät suunnittelemaan yhteistä tekemistä, aktiviteetteja, tapahtumia, juhlia jne., ja kutsumaan muita käyttäjiä osallistumaan sekä ilmoittautumaan niihin. Tapahtuman tiedoista selviää mm. sen nimi, ajankohta sekä tarkempi kuvaus.

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään tapahtumia sekä muokkaamaan ja poistamaan omia tapahtumiaan.
* Käyttäjä näkee sovellukseen lisätyt tapahtumat ja niiden ajankohdat.
* Käyttäjä pystyy etsimään tapahtumia hakusanalla, tageilla ja ajankohdan perusteella.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja listan käyttäjän luomista tapahtumista.
* Käyttäjä pystyy valitsemaan tapahtumalle yhden tai useamman luokittelun (esim. Sports, Food, Party, Drink, Indoor, Outdoor, Other).
* Käyttäjä pystyy ilmoittautumaan tapahtumiin (RSVP: In, Maybe, Out). Tapahtuman sivulla näytetään lista käyttäjistä, jotka ovat ilmoittautuneet ja millä statuksella.
* Käyttäjä voi lisätä näkyville päivät, jolloin hän olisi tai ei olisi valmis osallistumaan johonkin aktiviteettiin.
* Käyttäjä voi lisätä itselleen yleisen statuksen, jossa hän ilmoittaa halustaan tehdä jotain yhdessä.

Tässä pääasiallinen tietokohde on tapahtuma ja toissijainen tietokohde on ilmoittautuminen (RSVP).

## Sovelluksen asennus

Kloonaa sovellus omalle koneellesi komennolla:

```
$ git clone git@github.com:KMStacker/party-planner.git
```

Tämän jälkeen voit siirtyä kloonaamasi sovelluksen hakemistoon komennon ```cd``` avulla, ja noudattaa seuraavia asennusohjeita:

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Käynnistä sovellus:

```
$ flask run
```

## Koodin laatu

Jos haluat tarkistaa koodin laadun Pylint-työkalulla, asenna se ensin komennolla:

```
$ pip install pylint
```

Tämän jälkeen voit tarkastaa koodin laadun komennolla:

```
$ pylint *.py
```

## Suuren tietomäärän käsittely

Sovelluksen toimintaa testattiin suurella tietomäärällä käyttäen erillistä `test_database.db`-tiedostoa, jonka sisältö generoitiin erillisellä `seed.py`-skriptillä.

### Testidata lukuina (`seed.py`)
* **Käyttäjät (Users):** 100 000 kappaletta
* **Tapahtumat (Events):** 1 000 000 kappaletta (jokaisessa 0–7 kategoriaa ja osa monipäiväisiä tapahtumia)
* **Ilmottautumiset (RSVP):** 0–50 kappaletta (per tapahtuma)

### Mittaustulokset (Etusivu - Home)
Etusivun latausaikaa mitattiin palvelimen lokista kolmessa eri vaiheessa seuraavin tuloksin:

1. **Ilman sivutusta ja indeksejä:** `19.47 s`
   * Sivu jumiutu yrittäessään näyttää jokaisen tapahtuman samalla sivulla.
2. **Sivutuksen kanssa (ei indeksejä):** `3.52 s`
   * Lataus nopeutui huomattavasti eikä sivu mennyt jumiin, viiveen ollessa kuitenkin havaittava.
3. **Sivutuksen ja indeksien kanssa:** `0.01 s`
   * Sivu latautui välittömästi ilman havaittavaa viivettä.