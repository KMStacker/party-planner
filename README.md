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

Sen jälkeen voit tarkastaa koodin laadun komennolla:

```
$ pylint *.py
```
