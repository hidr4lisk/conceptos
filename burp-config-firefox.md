Flashcard técnico, minimalista y reproducible:

---

TÍTULO
Filtros Burp Suite CE – Exclusión de dominios Mozilla

ANVERSO
Regex para excluir tráfico de Mozilla/Firefox/Services en Burp (Request interception rules → Add → URL → Matches regex)

REVERSO

1. Mozilla

```
^https?://([^.]+\.)*mozilla\.com/
```

2. Firefox

```
^https?://([^.]+\.)*firefox\.com/
```

3. Services

```
^https?://([^.]+\.)*services\.mozilla\.com/
```

Configuración:

* Match type: URL
* Relationship: Matches regex
* Operator: Or

---
