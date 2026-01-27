Flash cards técnicas — **hashcat (GPU)**. Formato directo para guardar.

---

### 📌 Básico

**Ver dispositivos**

```bash
hashcat -I
```

**Benchmark GPU**

```bash
hashcat -b -D 2
```

**Forzar solo GPU**

```bash
-D 2
```

---

### 🔐 Hashes comunes

**MD5**

```bash
hashcat -m 0 -a 0 hashes.txt wordlist.txt -D 2
```

**SHA1**

```bash
hashcat -m 100 -a 0 hashes.txt wordlist.txt -D 2
```

**SHA256**

```bash
hashcat -m 1400 -a 0 hashes.txt wordlist.txt -D 2
```

**bcrypt**

```bash
hashcat -m 3200 -a 0 hashes.txt wordlist.txt -D 2
```

---

### 🌐 WiFi

**WPA/WPA2 (hc22000)**

```bash
hashcat -m 22000 -a 0 capture.hc22000 wordlist.txt -D 2
```

**WPA con reglas**

```bash
hashcat -m 22000 -a 0 capture.hc22000 wordlist.txt -r rules/best64.rule -D 2
```

---

### 🎯 Ataques

**Dictionary**

```bash
-a 0
```

**Combinator**

```bash
hashcat -a 1 left.txt right.txt -m 0 -D 2
```

**Mask (bruteforce dirigido)**

```bash
hashcat -a 3 -m 0 hashes.txt ?l?l?l?l?d?d -D 2
```

**Hybrid wordlist + mask**

```bash
hashcat -a 6 -m 0 hashes.txt wordlist.txt ?d?d -D 2
```

---

### 🧠 Reglas

**Aplicar reglas**

```bash
-r rules/best64.rule
```

**Varias reglas**

```bash
-r rules/rockyou-30000.rule
```

---

### ⚙️ Rendimiento / Control

**Workload alto**

```bash
-w 4
```

**Estado cada 10s**

```bash
--status --status-timer=10
```

**Abortar por temperatura**

```bash
--hwmon-temp-abort=85
```

**Optimizar kernels**

```bash
-O
```

---

### 📂 Sesiones

**Guardar sesión**

```bash
--session lab1
```

**Restaurar**

```bash
hashcat --restore --session lab1
```

---

### 📤 Output

**Guardar cracks**

```bash
-o cracked.txt --outfile-format=2
```

**Mostrar cracks**

```bash
hashcat -m 0 --show hashes.txt
```

---

### 🧪 Debug

**Ver progreso detallado**

```bash
--status --status-timer=5
```

**Logs**

```bash
--logfile-disable
```

---

### 📎 Nota clave

* GPU activa: `-D 2`
* OpenCL NVIDIA OK
* CUDA toolkit **opcional**
* No mezclar drivers/toolkits


