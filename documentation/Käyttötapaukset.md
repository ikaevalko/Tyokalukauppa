## Käyttötapaukset

### 1. Tuotekategoriat

- Ylläpitäjä voi lisätä tuotekategorioita tietokantaan. Kategorialle on määriteltävä nimi lisäämisen yhteydessä.

SQL-kysely kategorian olemassaolon tarkistamiselle:
SELECT EXISTS (SELECT * FROM category WHERE category.name = ?)

SQL-kysely kategorian lisäämiselle:
INSERT INTO category (name) VALUES (?)

- Ylläpitäjä voi muokata olemassa olevien tuotekategorioiden nimiä.

SQL-kysely kategorian päivittämiselle:
UPDATE category SET name=? WHERE category.id = ?

- Asiakas tai ylläpitäjä voi hakea tuotekategorioita nimellä.
- Asiakas tai ylläpitäjä voi listata kaikki tuotekategoriat.

### 2. Tuotteet

- Ylläpitäjä voi lisätä tietokantaan tuotteita ja määritellä niille kategorioita.
- Ylläpitäjä voi muokata olemassa olevien tuotteiden tietoja ja kategorioita.
- Asiakas tai ylläpitäjä voi hakea tuotteita tietokannasta.
- Asiakas tai ylläpitäjä voi listata kaikki tuotteet.

### 3. Tilaukset

- Asiakas voi tehdä useita tilauksia. Tilaukseen sisältyy yksi tai useampi tuote.
- Asiakas voi listata tekemänsä tilaukset. Ylläpitäjä voi listata kaikki tilaukset.
