## 1. Qué significa una **clave fuerte** en cryptography

Una clave es fuerte **no por “ser complicada”**, sino por tres propiedades técnicas:

### Longitud

* El espacio de búsqueda crece exponencialmente.
* 128 bits ⇒ (2^{128}) combinaciones.
* No es “difícil”, es **computacionalmente inviable**.

### Entropía

* La clave debe venir de un **CSPRNG**.(Cryptographically Secure Pseudo-Random Number Generator)
* Si se deriva de timestamps, PID, MAC, username, etc., **pierde entropía real**.
* Mucho material de ataques RSA explota exactamente esto.

### Unicidad

* Reutilizar claves o partes de claves rompe supuestos matemáticos.
* En RSA: reutilizar **p o q** = key compromise inmediato vía GCD.

---

## 2. Matemática mínima de RSA (lo esencial)

RSA no “cifra”, **eleva a potencias módulo n**.

### Clave pública

* ( n = p \times q )
* ( e ) (normalmente 65537)

### Clave privada

* ( \varphi(n) = (p-1)(q-1) )
* ( d = e^{-1} \mod \varphi(n) )

Condición clave:
[
e \cdot d \equiv 1 \pmod{\varphi(n)}
]

### Seguridad real

No depende de que RSA sea “secreto”, depende de:

* que **factorizar n sea impracticable**
* que **p y q sean aleatorios, grandes y únicos**

Si p o q son débiles ⇒ RSA cae completo.

---

## 3. Sobre el ejemplo de “factorisation time”

El script **no demuestra crecimiento exponencial real**.
Factorizar números pequeños con `sympy` **no representa** el problema real.

Factorizar:

* 32 bits: trivial
* 64 bits: trivial
* 1024 bits: **inviable**
* 2048 bits: **no existe ataque práctico**

El crecimiento **no es exponencial simple**, es sub-exponencial (GNFS), pero igual impracticable a escala real.

Conclusión: el ejemplo es **didáctico**, no una prueba criptográfica seria.

---

## 4. Qué es *“P’s and Q’s”* y por qué es crítico

El paper demuestra que **RSA falla en la práctica**, no en la teoría, por errores de implementación.

### Ataques reales documentados:

#### 1. Primos predecibles

* RNG mal inicializado
* Entropía baja en embedded / IoT / early boot
* El atacante reconstruye p y q

#### 2. Primos compartidos

Si:

* ( n_1 = p \times q_1 )
* ( n_2 = p \times q_2 )

Entonces:
[
\gcd(n_1, n_2) = p
]

Tiempo: **polinomial**
Impacto: **key recovery instantáneo**

#### 3. Primos cercanos

* Si ( |p - q| ) es pequeño
* Fermat factorisation funciona rápido

Resultado: RSA roto sin brute force.

---

## 5. Qué te pide exactamente el ejercicio

Te dan:

* ( n )
* ( e )
* ( c )

Y asumen:

* ( n ) fue generado con primes débiles

Objetivo:

1. Factorizar ( n )
2. Calcular ( \varphi(n) )
3. Obtener ( d )
4. Descifrar ( c )

---

## 6. Flujo técnico completo (sin magia)

### 1. Factorizar n

```python
from sympy import factorint

n = 43941819371451617899582143885098799360907134939870946637129466519309346255747
factors = factorint(n)
p, q = factors.keys()
```

En un entorno real:

* `sympy` no escala
* se usaría YAFU / msieve / FactorDB

---

### 2. Calcular φ(n)

```python
phi_n = (p - 1) * (q - 1)
```

---

### 3. Calcular d

```python
from Crypto.Util.number import inverse

e = 65537
d = inverse(e, phi_n)
```

Esto solo funciona porque:

* gcd(e, φ(n)) = 1

---

### 4. Descifrar

```python
from Crypto.Util.number import long_to_bytes

c = 9002431156311360251224219512084136121048022631163334079215596223698721862766
m = pow(c, d, n)
plaintext = long_to_bytes(m)
print(plaintext.decode())
```

Matemáticamente:
[
m = c^d \mod n
]

---

## 7. Broadcast RSA (aclaración final)

Esto **es otro ataque**, distinto al factoring.

Condiciones:

* mismo plaintext
* mismo e pequeño (ej: 3)
* múltiples n distintos
* sin padding

Se rompe usando CRT.

Por eso:

* e = 65537
* OAEP obligatorio
* plaintext único por destinatario

---

## 8. Idea clave que tenés que llevarte

RSA **no se rompe por matemática avanzada**, se rompe por:

* RNG pobre
* reutilización
* malas prácticas
* falta de padding

El ejercicio está diseñado para que **n sea débil**, no para que fuerces RSA real.

Eso es exactamente lo que se explota en escenarios reales de pentesting y research.
