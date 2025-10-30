Flashcard: **Instalar fuente TTF en Ubuntu para usar en LibreOffice**

---

**Pregunta:**
¿Cómo instalo un archivo `.ttf` para usarlo en LibreOffice en Ubuntu?

**Respuesta (usuario actual):**

```bash
mkdir -p ~/.fonts
cp ~/Downloads/mr-robot/MR\ ROBOT.ttf ~/.fonts/
fc-cache -fv
```

---

**Pregunta:**
¿Cómo lo instalo para todos los usuarios del sistema?

**Respuesta (sistema completo):**

```bash
sudo mkdir -p /usr/local/share/fonts/truetype/custom
sudo cp ~/Downloads/mr-robot/MR\ ROBOT.ttf /usr/local/share/fonts/truetype/custom/
sudo fc-cache -fv
```

---

**Pregunta:**
¿Cómo verifico que la fuente se instaló?

**Respuesta:**

```bash
fc-list | grep "MR ROBOT"
```

---
