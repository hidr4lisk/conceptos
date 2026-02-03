# Crear el entorno alternativo

fede@Oficina-Portatil:~$ cd entorno_alternativo/
fede@Oficina-Portatil:~/entorno_alternativo$ python3 -m venv venv
fede@Oficina-Portatil:~/entorno_alternativo$ source venv/bin/activate

# Para salir:

 deactivate

# Instalar PIP dentro de VENV

python -m ensurepip --upgrade

# Actualizar pip 

python -m pip install --upgrade pip


# Instalar Sympy 

pip install sympy

# Verificar la instalación

python -c "import sympy; print(sympy.__version__)"

# Instalar pycrytodome

pip install pycryptodome

# Verificar la instalación

python -c "import Crypto; print(Crypto.__version__)"
