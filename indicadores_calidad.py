from pyzabbix import ZabbixAPI
from datetime import datetime, timedelta
from prettytable import PrettyTable
import argparse
import sys


zapi = ZabbixAPI("http://url/zabbix") # Url para hacer la conexión con la API
zapi.login("Admin", "zabbix") # Credenciales de acceso "user", "password"


print("\nIndicadores de Calidad Cesga\n")


def nombreServicio(id):
    if (id == "3"):
        nombre = "Indicador - Instituciones grandes"
        print(f"\n{nombre}")
    if (id == "9"):   
        nombre = "Indicador - Enlaces de RECETGA"
        print(f"\n{nombre}")
    if (id == "7"):
       nombre = "Indicador - Troncal Principal"
       print(f"\n{nombre}")
    if (id == "5"):
        nombre = "Indicador - Troncal extendida"
        print(f"\n{nombre}")

    
def mostrarMes(mes):
    if(mes == "01"):
        return "Enero"
    if(mes == "02"):
        return "Febrero"
    if(mes == "03"):
        return "Marzo"
    if(mes == "04"):
        return "Abril"
    if(mes == "05"):
        return "Mayo"
    if(mes == "06"):
        return "Junio"
    if(mes == "07"):
        return "Julio"
    if(mes == "08"):
        return "Agosto"
    if(mes == "09"):
        return "Septiembre"
    if(mes == "10"):
        return "Octubre"
    if(mes == "11"):
        return "Noviembre"
    if(mes == "12"):
        return "Diciembre"


def sliPorMes(result_api):
    myTable = PrettyTable(["Meses", "Disponibilidad", "Dispo.Acumulada"])

    contador_mes = 0
    disponibilidad = 0
    dispo_acumulada = 0
    cont_disponibilidad = 0
    cont_dispo_acumulada = 0
    no_hay_dato = False
    no_hay_dato_futuro = False
    for result_sli in result_api['sli']:
        fecha = result_api['periods'][contador_mes]['period_to']
        mes = datetime.utcfromtimestamp(fecha).strftime('%m')
        nombre_mes = mostrarMes(mes)
        contador_mes += 1
        for sli in result_sli:
            if (sli['sli'] == -1):
                disponibilidad += 100
                no_hay_dato = True
                no_hay_dato_futuro = True
            else:
                disponibilidad += sli['sli']
                no_hay_dato = False
                
            cont_disponibilidad += 1
        
        dispo_acumulada += disponibilidad
        cont_dispo_acumulada += cont_disponibilidad
        disponibilidad_total = disponibilidad / cont_disponibilidad
        dispo_acumulada_total = dispo_acumulada / cont_dispo_acumulada
        disponibilidad = 0
        cont_disponibilidad = 0

        if (no_hay_dato):
            myTable.add_row([nombre_mes, "N/D", "N/D"])
        else:
            if(no_hay_dato_futuro):
                myTable.add_row([nombre_mes, "{:.3f}".format(disponibilidad_total), "{:.3f}".format(dispo_acumulada_total)])
            else:
                myTable.add_row([nombre_mes, "{:.3f}".format(disponibilidad_total), "{:.3f}".format(dispo_acumulada_total)])
    
    print(myTable)
    

        


def indicadorServicio(id, fecha_unix, fecha_unix_siguiente):
    result_api = zapi.sla.getsli(slaid=id, period_from=fecha_unix, period_to=fecha_unix_siguiente)
    sliPorMes(result_api)


def comprobarAnho(anho):
    currentDateTime = datetime.now()
    date = currentDateTime.date()
    year = int(date.strftime("%Y"))
    anho_comprobar = int(anho)
    if (anho_comprobar <= year and anho_comprobar > 2000):
        return str(anho)
    else:
        return None

def buscarPorAnho(fecha):
    try:
        anho = fecha
        anho_comprobado = comprobarAnho(anho)
        if (anho_comprobado == None):
            print("Año incorrecto, vuelva a repetir\n")
            sys.exit()
    except ValueError:
        print("El parámetro debe ser un número\n")
        sys.exit()

    return anho_comprobado


parser = argparse.ArgumentParser()
parser.add_argument('-a', required=True, type=int, help='Año a buscar')
args = parser.parse_args()

anho = buscarPorAnho(args.a)
formato = "%Y"
anho_siguiente = int(anho) + 1
date = datetime.strptime(anho, formato)
date_siguiente = datetime.strptime(str(anho_siguiente), formato)
date_siguiente = date_siguiente - timedelta(days=1)
fecha_unix = int(date.timestamp())
fecha_unix_siguiente = int(date_siguiente.timestamp())


# array que contiene los id´s para hacer los indicadores
array_de_ids = ["3", "9", "7", "5"]
for i in array_de_ids:
    nombreServicio(i)
    indicadorServicio(i, fecha_unix, fecha_unix_siguiente)
        