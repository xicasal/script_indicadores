# script_indicadores_de_calidad
Script para calcular los indicadores de calidad de Cesga


Instalar pyzabbix para su uso en zabbix
  - Tener instalado python
    $ python3 --version
  - Instalar pip 
    $ sudo apt-get install python3-pip
  - Instalar pyzabbix usando pip
    $ pip install pyzabbix
  - Instalar prettytable usando pip
    $ pip install prettytable
    
    
 Como funciona:
  - Modificar la url, el usuario y la contraseña para poder conectarse a la API
  - Si fuera necesario cambiar las ids en el array para los indicadores
  - Clonar el archivo git
  - Ejecutar el archivo .py
    $ python3 indicadores_calidad.py -a [año_a_buscar]
