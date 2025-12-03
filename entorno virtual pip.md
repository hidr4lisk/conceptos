**Flashcard – Entorno virtual Python (Ubuntu 24.04)**

---

**Instalar soporte para entornos virtuales**

```bash
sudo apt install python3-venv -y
```

---

**Crear entorno**

```bash
python3 -m venv ~/.venvs/laboratorio
```

---

**Activar entorno**

```bash
source ~/.venvs/laboratorio/bin/activate
```

---

**(Opcional) Alias para activar rápido**
Editar `~/.bashrc` y agregar:

```bash
alias laboratorio='source ~/.venvs/laboratorio/bin/activate'
```

Actualizar sesión:

```bash
source ~/.bashrc
```

---

**Instalar paquetes dentro del entorno**

```bash
pip install kaggle google-adk
```

---

**Desactivar entorno**

```bash
deactivate
```

---

**Nota clave:**
Todo lo instalado con `pip` dentro del entorno **solo existe ahí**.
Debés activarlo antes de usar esos paquetes.
