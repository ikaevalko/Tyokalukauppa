## Tietokantarakenne

Tietokanta ei ole täysin normalisoitu. Order-taulun attribuutit address, postal_code ja city aiheuttavat tiedon toisteisuutta. Päätin olla luomatta näille käsitteille erillisiä tauluja pitääkseni tietokannan kohtuullisen yksinkertaisena. Normalisoinnin täydentäminen on suunnitelmissa jatkokehitykselle.

Tietokantataulujen pää- ja viiteavaimille lisätään automaattisesti indeksit.

![](Tietokantakaavio.png)

#### Account
```
CREATE TABLE account (
	id INTEGER NOT NULL, 
    name VARCHAR(32) NOT NULL, 
    username VARCHAR(32) NOT NULL, 
    password VARCHAR(64) NOT NULL, 
    is_admin BOOLEAN NOT NULL, 
    PRIMARY KEY (id), 
    CHECK (is_admin IN (0, 1))
);
```

#### Category
```
CREATE TABLE category (
	id INTEGER NOT NULL, 
	name VARCHAR(24) NOT NULL, 
	PRIMARY KEY (id)
);
```

#### Product
```
CREATE TABLE product (
	id INTEGER NOT NULL, 
    name VARCHAR(64) NOT NULL, 
    "desc" TEXT NOT NULL, 
    price NUMERIC(6, 2) NOT NULL, 
    quantity INTEGER NOT NULL, 
    category_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(category_id) REFERENCES category (id)
);
```

#### Order
Huom. SQLAlchemy luo Order-taulun nimen lainausmerkkien kanssa. Syytä tähän en saanut selville.

```
CREATE TABLE IF NOT EXISTS "order" (
	id INTEGER NOT NULL, 
    date DATE, 
    address VARCHAR(32) NOT NULL, 
    postal_code INTEGER NOT NULL, 
    city VARCHAR(32) NOT NULL, 
    completed BOOLEAN NOT NULL, 
    account_id INTEGER, 
    PRIMARY KEY (id), 
    CHECK (completed IN (0, 1)), 
    FOREIGN KEY(account_id) REFERENCES account (id)
);
```

#### OrderProduct (liitostaulu)
```
CREATE TABLE order_product (
	order_id INTEGER NOT NULL, 
    product_id INTEGER NOT NULL, 
    amount INTEGER NOT NULL, 
    PRIMARY KEY (order_id, product_id), 
    FOREIGN KEY(order_id) REFERENCES "order" (id), 
    FOREIGN KEY(product_id) REFERENCES product (id)
);
```
