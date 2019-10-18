## Käyttötapaukset

### 1. Käyttäjät

- Uuden asiakaskäyttäjän rekisteröinti.<br>
```INSERT INTO account (name, username, password, is_admin) VALUES (?, ?, ?, ?);```

- Sisäänkirjautuminen (käyttäjän hakeminen käyttäjänimen perusteella).<br>
  ```
  SELECT account.id AS account_id, 
  account.name AS account_name, 
  account.username AS account_username, 
  account.password AS account_password, 
  account.is_admin AS account_is_admin FROM account 
  WHERE account.username = ? 
  LIMIT ? OFFSET ?;
  ```

### 2. Tuotekategoriat

- Ylläpitäjä voi lisätä tuotekategorioita tietokantaan. Kategorialle on määriteltävä nimi lisäämisen yhteydessä.<br>
```INSERT INTO category (name) VALUES (?);```

- Ylläpitäjä voi muokata olemassa olevien tuotekategorioiden nimiä.<br>
```UPDATE category SET name=? WHERE category.id = ?;```

- Ylläpitäjä voi poistaa olemassa olevia tuotekategorioita.<br>
```DELETE FROM category WHERE category.id = ?;```

- Asiakas tai ylläpitäjä voi listata kaikki tuotekategoriat.<br>
```SELECT category.id AS category_id, category.name AS category_name FROM category;```

SQL-kyselyt kategorian olemassaolon tarkistamiselle (käytetään muiden kyselyiden yhteydessä):<br>
```SELECT EXISTS (SELECT * FROM category WHERE category.name = ?);```<br>
```SELECT EXISTS (SELECT * FROM category WHERE category.id = ?);```

### 3. Tuotteet

- Ylläpitäjä voi lisätä tietokantaan tuotteita ja määritellä niille kategorioita.<br>
```INSERT INTO product (name, description, price, quantity, category_id) VALUES (?, ?, ?, ?, ?);```

- Ylläpitäjä voi muokata olemassa olevien tuotteiden tietoja ja kategorioita.<br>
```UPDATE product SET name=?, description=?, price=?, quantity=?, category_id=? WHERE product.id = ?;```

- Ylläpitäjä voi poistaa olemassa olevia tuotteita.<br>
```DELETE FROM product WHERE product.id = ?;```

- Asiakas tai ylläpitäjä voi listata kaikki tuotteet.<br>
  ```
  SELECT product.id AS product_id, 
  product.name AS product_name, 
  product.description AS product_description, 
  product.price AS product_price, 
  product.quantity AS product_quantity, 
  product.category_id AS product_category_id FROM product;
  ```

- Asiakas tai ylläpitäjä voi listata kategorian tuotteet.<br>
  ```
  SELECT product.id AS product_id, 
  product.name AS product_name, 
  product.description AS product_description, 
  product.price AS product_price, 
  product.quantity AS product_quantity, 
  product.category_id AS product_category_id FROM product 
  WHERE product.category_id = ?;
  ```

- Asiakas tai ylläpitäjä voi järjestää tuotteiden listausta hinnan perusteella.<br>
  ```
  SELECT product.id AS product_id, 
  product.name AS product_name, 
  product.description AS product_description, 
  product.price AS product_price, 
  product.quantity AS product_quantity, 
  product.category_id AS product_category_id FROM product 
  ORDER BY product.price ASC;
  ```
  ```
  SELECT product.id AS product_id, 
  product.name AS product_name, 
  product.description AS product_description, 
  product.price AS product_price, 
  product.quantity AS product_quantity, 
  product.category_id AS product_category_id FROM product 
  ORDER BY product.price DESC;
  ```

- Asiakas tai ylläpitäjä voi hakea tuotteita.<br>
  ```
  SELECT product.id AS product_id, 
  product.name AS product_name, 
  product.description AS product_description, 
  product.price AS product_price, 
  product.quantity AS product_quantity, 
  product.category_id AS product_category_id FROM product 
  WHERE product.name LIKE ?;
  ```

SQL-kysely tuotteen olemassaolon tarkistamiselle (käytetään muiden kyselyiden yhteydessä):<br>
```SELECT EXISTS (SELECT * FROM product WHERE product.id = ?);```

### 4. Tilaukset

- Asiakas voi tehdä useita tilauksia. Tilaukseen sisältyy yksi tai useampi tuote.<br>
```INSERT INTO orders (date, address, postal_code, city, completed, account_id) VALUES (CURRENT_DATE, ?, ?, ?, ?, ?);```<br>
```INSERT INTO order_product (order_id, product_id, amount) VALUES (?, ?, ?);```

- Asiakas voi listata tekemänsä tilaukset.<br>
  ```
  SELECT orders.id AS orders_id, 
  orders.date AS orders_date, 
  orders.address AS orders_address, 
  orders.postal_code AS orders_postal_code, 
  orders.city AS orders_city, 
  orders.completed AS orders_completed, 
  orders.account_id AS orders_account_id FROM orders 
  WHERE orders.account_id = ?;
  ```
  
- Ylläpitäjä voi listata kaikki tilaukset.<br>
  ```
  SELECT orders.id AS orders_id, 
  orders.date AS orders_date, 
  orders.address AS orders_address, 
  orders.postal_code AS orders_postal_code, 
  orders.city AS orders_city, 
  orders.completed AS orders_completed, 
  orders.account_id AS orders_account_id FROM orders;
  ```

- Asiakas tai ylläpitäjä voi listata tilauksen tuotteet (asiakas vain omien tilaustensa).<br>
  ```
  SELECT product.id AS product_id, 
  product.name AS product_name, 
  product.description AS product_description, 
  product.price AS product_price, 
  product.quantity AS product_quantity, 
  product.category_id AS product_category_id FROM product, order_product 
  WHERE ? = order_product.order_id AND product.id = order_product.product_id;
  ```

- Ylläpitäjä voi merkitä tilauksia suoritetuksi.<br>
```UPDATE orders SET completed=? WHERE orders.id = ?;```

### 5. Tilastot

- Ylläpitäjä voi listata erilaisia tilastoja tietokannasta.<br>

  Myydyimmät tuotteet (rivien määrä rajoitetaan kymmeneen ennen listausta):
  
  ```
  SELECT product.name, product.price, COUNT(orders.id) AS amount_sold FROM product 
  JOIN order_product ON product.id = order_product.product_id 
  JOIN orders on order_product.order_id = orders.id 
  GROUP BY product.name, product.price 
  ORDER BY amount_sold DESC;
  ```
  
  Vähiten myydyt tuotteet (rivien määrä rajoitetaan kymmeneen ennen listausta):
  
  ```
  SELECT product.name, product.price, COUNT(orders.id) AS amount_sold FROM product 
  JOIN order_product ON product.id = order_product.product_id 
  JOIN orders on order_product.order_id = orders.id 
  GROUP BY product.name, product.price 
  ORDER BY amount_sold ASC;
  ```
  
  Hintojen keskiarvot kategorioittain:
  ```
  SELECT category.name, ROUND(AVG(product.price), 2) FROM category 
  JOIN product ON category.id = product.category_id 
  GROUP BY category.name;
  ```
