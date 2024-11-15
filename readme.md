# Filkrypteringsverktyg

Kryptera och dekryptera filer med hjälp av ett lösenord. Nyckeln genereras med hjälp av lösenordet och lagras i `secret.key`.

## Funktioner

- Generera en krypteringsnyckel från ett lösenord. (PBKDF2)
- Skapa och kryptera en fil med lösenord.
- Dekryptera en fil med lösenord.
- Felhantering.

## Användning

- Generera och spara en krypteringsnyckel med lösenord (t.ex. hejhej123).
```bash
python main.py generate-key --password hejhej123
```

- Skapa och kryptera en fil med lösenord. (t.ex. hemlig.txt)
```bash
python main.py encrypt --file hemlig.txt --password hejhej123
```
- Dekryptera en fil med lösenord. (t.ex. hemlig.txt.enc)
```bash
python main.py decrypt --file hemlig.txt.enc --password hejhej123
```
