#!/bin/bash

# Lee texto del portapapeles
texto=$(wl-paste | tr -d '\n')

# Aplica la plantilla
resultado="Me dirijo a Ud. en atención a la nota $texto, con relación a la referencia, la misma se acompaña asociada a la presente para su conocimiento."

# Copia el resultado al portapapeles
echo -n "$resultado" | wl-copy