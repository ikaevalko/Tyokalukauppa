## Asennusohje

Sovelluksen käyttöönottoon tarvitset:
- Python 3.5 tai uudempi
- Pythonin venv-kirjasto virtuaaliympäristön luomiseen
- Pythonin pip kirjastojen lataamiseen
- SQLite-tietokannanhallintajärjestelmän
- Git-versionhallinta

#### Asennus paikallisesti
1. Lataa tai kloonaa sovellus osoitteesta <https://github.com/ikaevalko/Tyokalukauppa>

2. Luo sovelluksen juureen Python-virtuaaliympäristö ja ota se käyttöön.<br>
```python3 -m venv venv```<br>
```source venv/bin/activate```

3. Lataa virtuaaliympäristössä sovelluksen riippuvuudet käyttämällä pip-työkalua. Riippuvuudet löytyvät requirements-tiedostosta.<br>
```pip install -r requirements.txt```

4. Käynnistä sovellus paikallisesti suorittamalla Pythonilla tiedosto ```run.py```<br>
```python3 run.py```

5. Sovellus on näkyvissä selaimella osoitteessa ```localhost:5000```

#### Admin-käyttäjän luominen
1. Rekisteröi sovelluksessa tietokantaan uusi käyttäjä.

2. Avaa tietokanta tietokannanhallintajärjestelmällä.

3. Muuta luomasi käyttäjä ylläpitäjäksi päivityskyselyllä.<br>

    ```UPDATE account SET is_admin="1" WHERE username="?";```<br>

    Kysymysmerkin paikalle tulee rekisteröimäsi käyttäjän käyttäjänimi. Huom. sarakkeen "is_admin" arvo on boolean-tyyppinen, jonka tässä esitetty muoto on SQLite-spesifi.
    
#### Asennus Herokuun
1. Suorita ensin asennus paikallisesti.

2. Luo tili Heroku-pilvipalveluun, jos sinulla ei valmiiksi jo ole tiliä. <https://signup.heroku.com>

3. Asenna työvälineet Herokun käyttöön. <https://devcenter.heroku.com/articles/heroku-cli>

4. Luo Herokuun uusi paikka sovelluksellesi. Vaihda komennosta _sovellus_ haluamaksesi nimeksi.<br>
```heroku create sovellus```

5. Lisää sovellukselle tieto Herokun käytöstä.<br>
```heroku config:set HEROKU=1```

6. Lisää Herokuun tietokanta.<br>
```heroku addons:add heroku-postgresql:hobby-dev```

7. Lisää sovellus versionhallintaan. Vaihda komennosta _sovellus_ valitsemaksesi nimeksi. <br>
```git remote add heroku https://git.heroku.com/sovellus.git```

8. Luo uusi commit Gitillä. Voit kirjoittaa commit-viestiksi mitä haluat.<br>
```git add .```<br>
```git commit -m "Deploy to Heroku"```

9. Puske sovellus Herokuun.<br>
```git push heroku master```

10. Sovellus on näkyvissä osoitteessa ```https://sovellus.herokuapp.com``` (kohtaan _sovellus_ tulee valitsemasi nimi)