## Käyttötapaukset

### 1. Tuotekategoriat

- Ylläpitäjä voi lisätä tuotekategorioita tietokantaan. Kategorialle on määriteltävä nimi lisäämisen yhteydessä.
	* SQL-kysely kategorian lisäämiselle: <br> INSERT INTO category (name) VALUES (?)

- Ylläpitäjä voi muokata olemassa olevien tuotekategorioiden nimiä.
	* SQL-kysely kategorian päivittämiselle: <br> UPDATE category SET name=? WHERE <span>category</span>.id = ?

- Ylläpitäjä voi poistaa olemassa olevia tuotekategorioita.
	* SQL-kysely kategorian poistamiselle: <br> DELETE FROM category WHERE <span>category</span>.id = ?

- Asiakas tai ylläpitäjä voi listata kaikki tuotekategoriat.
	* SQL-kysely kategorioiden listaamiselle: <br> SELECT <span>category</span>.id AS category_id, <span>category</span>.name AS category_name FROM category

SQL-kysely kategorian olemassaolon tarkistamiselle (käytetään muiden kyselyiden yhteydessä): <br> SELECT EXISTS (SELECT * FROM category WHERE <span>category</span>.name = ?)

### 2. Tuotteet

- Ylläpitäjä voi lisätä tietokantaan tuotteita ja määritellä niille kategorioita.
	* SQL-kysely tuotteen lisäämiselle: <br> INSERT INTO product (name, "desc", price, quantity, category_id) VALUES (?, ?, ?, ?, ?)

- Ylläpitäjä voi muokata olemassa olevien tuotteiden tietoja ja kategorioita.
	* SQL-kysely tuotteen päivittämiselle: <br> UPDATE product SET name=?, desc=?, price=?, quantity=? WHERE <span>product</span>.id = ?

- Ylläpitäjä voi poistaa olemassa olevia tuotteita.
	* SQL-kysely tuotteen poistamiselle: <br> DELETE FROM product WHERE <span>product</span>.id = ?

- Asiakas tai ylläpitäjä voi hakea tuotteita tietokannasta. **Ei vielä toteutettu.**

- Asiakas tai ylläpitäjä voi listata kaikki tuotteet.
	* SQL-kysely tuotteiden listaamiselle: <br> SELECT <span>product</span>.id AS product_id, <span>product</span>.name AS product_name, product."desc" AS product_desc, product.price AS product_price, product.quantity AS product_quantity, product.category_id AS product_category_id FROM product LIMIT ? OFFSET ?

SQL-kysely tuotteen olemassaolon tarkistamiselle (käytetään muiden kyselyiden yhteydessä): <br> SELECT EXISTS (SELECT * FROM product WHERE <span>product</span>.name = ?)

### 3. Tilaukset (ei vielä toteutettu)

- Asiakas voi tehdä useita tilauksia. Tilaukseen sisältyy yksi tai useampi tuote.
- Asiakas voi listata tekemänsä tilaukset. Ylläpitäjä voi listata kaikki tilaukset.
