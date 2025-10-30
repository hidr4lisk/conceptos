Resumen técnico:

1. **Tipos de filtrado en cargas de archivos:**

   * **Client-Side:** Se ejecuta en el navegador del usuario. Fácil de evadir, no fiable como único control.
   * **Server-Side:** Se ejecuta en el servidor. Más difícil de evadir; requiere adaptar la carga a los filtros.

2. **Filtrado por extensión:**

   * Basado en extensiones de archivo.
   * Métodos: **Blacklisting** (prohibir extensiones) o **Whitelisting** (permitir solo extensiones específicas).
   * Vulnerable: extensiones fáciles de cambiar.

3. **Filtrado por tipo de archivo:**

   * **MIME Validation:** Basado en cabeceras de tipo de archivo. Fácil de falsificar.
   * **Magic Number Validation:** Basado en bytes iniciales del archivo. Más confiable, usado en Unix, pero no infalible.

4. **Filtrado por tamaño:**

   * Limita la longitud de los archivos para evitar sobrecarga del servidor. Puede requerir adaptar shells a tamaños permitidos.

5. **Filtrado por nombre:**

   * Evita duplicados y caracteres peligrosos. Puede renombrar archivos automáticamente, dificultando localizar la carga si se evaden filtros de contenido.

6. **Filtrado por contenido:**

   * Analiza toda la carga para verificar consistencia entre extensión, MIME y magic number. Complejo y poco común en sistemas básicos.

7. **Combinación de filtros:**

   * Generalmente se aplican múltiples filtros a la vez (extensión, tipo, tamaño, nombre) para aumentar seguridad.

8. **Exploits específicos de lenguaje:**

   * Algunos lenguajes/frameworks permiten bypasses históricos, como:

     * PHP <5: null byte en extensión.
     * PHP moderno: inyección de código en EXIF de imágenes.

Conclusión: Cada método aislado es insuficiente; la defensa efectiva combina varios filtros server-side y considera limitaciones de framework/lenguaje.
