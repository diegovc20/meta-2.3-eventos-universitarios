
# Nombre: Diego Valle Cuevas
# Grupo: 952
# Fecha: 11/10/2026
# Meta 2.3 Desarrollar aplicaciones con conexion a Base de Datos. Sistema de eventos universitarios que se
# conecta a la base de datos eventos_universitarios en MySQL usando mysql.connector. Permite mostrar y buscar
# eventos, consultar disponibilidad, registrar y cancelar asistentes, agregar y modificar eventos y ver los
# eventos proximos con lugares disponibles, todo desde un menu que sigue activo hasta que se elige Salir.
# Antes de correrlo hay que ejecutar el archivo eventos_universitarios.sql en MySQL e instalar la libreria con:
# pip install mysql-connector-python


import mysql.connector


# Guardamos los datos de la conexion en variables para no andarlos escribiendo en cada funcion.
# Aqui se cambia el usuario y la contraseña segun como tengas instalado MySQL en tu computadora.
HOST = "localhost"
USUARIO = "root"
PASSWORD = "200706.vC"
BASE_DATOS = "eventos_universitarios"

# Esta es la consulta base que usan varias funciones. Siempre pedimos las columnas en el mismo orden
# para que la funcion imprimir_eventos las pueda desempaquetar igual en todos los casos.
COLUMNAS = "SELECT id, nombre, fecha, hora, lugar, cupo, registrados FROM eventos"


# Paso 5. Definimos la funcion que se conecta a la base de datos
def conectar():

    # Metemos la conexion en un try porque si MySQL esta apagado, la contraseña esta mal
    # o no existe la base de datos, el connect truena, y asi mejor lo controlamos nosotros.
    try:
        conexion = mysql.connector.connect(
            host=HOST,
            user=USUARIO,
            password=PASSWORD,
            database=BASE_DATOS
        )
        return conexion

    except mysql.connector.Error as e:
        print(f"No se pudo conectar a la base de datos: {e}")
        return None


# Esta funcion es nada mas para imprimir los eventos de forma organizada, como tabla.
# La usan varias opciones del menu, asi no repetimos el mismo codigo en cada una.
def imprimir_eventos(eventos):

    # Si la consulta no regreso nada avisamos y nos salimos de la funcion
    if len(eventos) == 0:
        print("No se encontraron eventos")
        return

    # Imprimimos los encabezados. El :<4, :<55, etc. le da un ancho fijo a cada columna
    # (el < es para alinear a la izquierda) y asi todo queda alineado como tabla.
    print(f"{'ID':<4}{'NOMBRE':<55}{'FECHA':<12}{'HORA':<7}{'LUGAR':<31}{'CUPO':<6}{'REG.':<6}{'DISP.':<6}")
    print("=" * 127)

    # Cada evento viene como tupla, entonces la desempaquetamos directo en el for
    # para no andar usando evento[0], evento[1], etc.
    for id_evento, nombre, fecha, hora, lugar, cupo, registrados in eventos:

        # Lugares disponibles = cupo - registrados
        disponibles = cupo - registrados

        # La hora llega de MySQL como 10:00:00, con el [:-3] le quitamos los segundos
        hora_texto = str(hora)[:-3]

        print(f"{id_evento:<4}{nombre:<55}{str(fecha):<12}{hora_texto:<7}{lugar:<31}{cupo:<6}{registrados:<6}{disponibles:<6}")

    print("Total de eventos:", len(eventos))


# Paso 6. Definimos la funcion que consulta y muestra todos los eventos registrados
def mostrar_eventos():

    conexion = conectar()
    # Si no hubo conexion no tiene caso seguir
    if conexion is None:
        return

    try:
        # El cursor es el que ejecuta las consultas y nos regresa los resultados
        cursor = conexion.cursor()
        cursor.execute(COLUMNAS + " ORDER BY fecha, hora")

        # fetchall() nos regresa todos los renglones como una lista de tuplas
        eventos = cursor.fetchall()

        print()
        print("----- TODOS LOS EVENTOS -----")
        imprimir_eventos(eventos)

    except mysql.connector.Error as e:
        print(f"Ocurrio un error al consultar los eventos: {e}")

    # Establecemos al final, si o si la conexion se tiene que cerrar
    finally:
        conexion.close()


# Paso 7. Definimos la funcion que busca eventos cuyo nombre contenga el texto que escribe el usuario
def buscar_evento(texto):

    conexion = conectar()
    if conexion is None:
        return

    try:
        cursor = conexion.cursor()

        # El %s es el parametro SQL. El texto del usuario NO se pega directo en la consulta,
        # se manda aparte en el execute y la libreria se encarga de meterlo de forma segura
        # (asi evitamos la inyeccion SQL). Los % del LIKE se los ponemos al valor y no a la
        # consulta, para que busque el texto en cualquier parte del nombre.
        consulta = COLUMNAS + " WHERE nombre LIKE %s ORDER BY fecha, hora"
        valor = "%" + texto + "%"

        # Los parametros se mandan como tupla. Como es uno solo lleva la coma al final,
        # porque si no Python lo toma como texto normal y no como tupla.
        cursor.execute(consulta, (valor,))
        eventos = cursor.fetchall()

        print()
        print("----- RESULTADOS DE LA BUSQUEDA:", texto, "-----")
        imprimir_eventos(eventos)

    except mysql.connector.Error as e:
        print(f"Ocurrio un error al buscar el evento: {e}")

    finally:
        conexion.close()


# Paso 8. Definimos la funcion que muestra los eventos que tienen lugar para cierta cantidad de asistentes
def eventos_con_disponibilidad(asistentes):

    # Validamos primero que la cantidad tenga sentido
    if asistentes <= 0:
        print("La cantidad de asistentes debe ser mayor a 0")
        return

    conexion = conectar()
    if conexion is None:
        return

    try:
        cursor = conexion.cursor()

        # Un evento esta disponible si los lugares que le quedan (cupo - registrados)
        # alcanzan para los asistentes que nos pidieron.
        # Ejemplo: cupo 100, registrados 85, quedan 15, si piden 10 si aparece.
        consulta = COLUMNAS + " WHERE cupo - registrados >= %s ORDER BY fecha, hora"
        cursor.execute(consulta, (asistentes,))
        eventos = cursor.fetchall()

        print()
        print("----- EVENTOS CON LUGAR PARA", asistentes, "ASISTENTES -----")
        imprimir_eventos(eventos)

    except mysql.connector.Error as e:
        print(f"Ocurrio un error al consultar la disponibilidad: {e}")

    finally:
        conexion.close()


# Paso 9. Definimos la funcion que registra asistentes a un evento
def registrar_asistentes(id_evento, asistentes):

    # Primera validacion: que la cantidad de asistentes sea valida
    if asistentes <= 0:
        print("La cantidad de asistentes debe ser mayor a 0")
        return

    conexion = conectar()
    if conexion is None:
        return

    try:
        cursor = conexion.cursor()

        # Buscamos el evento por su id para saber si existe y cuanto cupo le queda
        cursor.execute("SELECT nombre, cupo, registrados FROM eventos WHERE id = %s", (id_evento,))

        # fetchone() regresa un solo renglon, o None si no encontro nada
        evento = cursor.fetchone()

        # Segunda validacion: que el evento exista.
        # Aunque hagamos return adentro del try, el finally de todos modos cierra la conexion.
        if evento is None:
            print("No existe un evento con el id", id_evento)
            return

        nombre, cupo, registrados = evento
        disponibles = cupo - registrados

        # Tercera validacion: que alcance el cupo
        if asistentes > disponibles:
            print("No hay cupo suficiente en", nombre)
            print("Lugares disponibles:", disponibles, "| Asistentes que quieres registrar:", asistentes)
            return

        # Si paso las 3 validaciones ya podemos actualizar
        nuevo_total = registrados + asistentes
        cursor.execute("UPDATE eventos SET registrados = %s WHERE id = %s", (nuevo_total, id_evento))

        # El commit es el que confirma el cambio en la base de datos, si no lo ponemos no se guarda
        conexion.commit()

        print()
        print("Registro exitoso en:", nombre)
        print("Registrados actuales:", registrados)
        print("Nuevos asistentes:", asistentes)
        print("Nuevo total de registrados:", nuevo_total)

    except mysql.connector.Error as e:
        # Si algo fallo a medio camino deshacemos lo que se haya hecho con rollback
        conexion.rollback()
        print(f"Ocurrio un error al registrar los asistentes: {e}")

    finally:
        conexion.close()


# Paso 10. Definimos la funcion que cancela registros de un evento
def cancelar_registros(id_evento, cantidad):

    if cantidad <= 0:
        print("La cantidad a cancelar debe ser mayor a 0")
        return

    conexion = conectar()
    if conexion is None:
        return

    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, registrados FROM eventos WHERE id = %s", (id_evento,))
        evento = cursor.fetchone()

        if evento is None:
            print("No existe un evento con el id", id_evento)
            return

        nombre, registrados = evento

        # Verificamos que no se quieran cancelar mas personas de las que estan registradas
        if cantidad > registrados:
            print("No se pueden cancelar", cantidad, "registros porque", nombre, "solo tiene", registrados, "registrados")
            return

        nuevo_total = registrados - cantidad
        cursor.execute("UPDATE eventos SET registrados = %s WHERE id = %s", (nuevo_total, id_evento))
        conexion.commit()

        print()
        print("Cancelacion exitosa en:", nombre)
        print("Registrados antes:", registrados)
        print("Registros cancelados:", cantidad)
        print("Nuevo total de registrados:", nuevo_total)

    except mysql.connector.Error as e:
        conexion.rollback()
        print(f"Ocurrio un error al cancelar los registros: {e}")

    finally:
        conexion.close()


# Paso 11. Definimos la funcion que agrega un evento nuevo
def agregar_evento(nombre, fecha, hora, lugar, cupo):

    # Validamos que no venga vacio el nombre ni el lugar y que el cupo sea mayor a 0
    if nombre == "" or lugar == "":
        print("El nombre y el lugar no pueden ir vacios")
        return

    if cupo <= 0:
        print("El cupo debe ser mayor a 0")
        return

    conexion = conectar()
    if conexion is None:
        return

    try:
        cursor = conexion.cursor()

        # Hacemos el INSERT con parametros. Los registrados van en 0 porque el evento es nuevo
        # y todavia no hay nadie inscrito. El id no lo mandamos porque es AUTO_INCREMENT.
        consulta = "INSERT INTO eventos (nombre, fecha, hora, lugar, cupo, registrados) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(consulta, (nombre, fecha, hora, lugar, cupo, 0))
        conexion.commit()

        # lastrowid nos dice que id le puso MySQL al evento nuevo
        print("Evento agregado correctamente con el id", cursor.lastrowid)

    except mysql.connector.Error as e:
        conexion.rollback()
        print(f"Ocurrio un error al agregar el evento: {e}")
        print("Revisa que la fecha tenga el formato AAAA-MM-DD y la hora HH:MM")

    finally:
        conexion.close()


# Paso 12. Definimos la funcion que modifica la fecha, hora, lugar y/o cupo de un evento que ya existe.
# Si alguno de los datos llega vacio ("") o el cupo llega como None, se queda el valor que ya tenia.
def modificar_evento(id_evento, fecha, hora, lugar, cupo):

    conexion = conectar()
    if conexion is None:
        return

    try:
        cursor = conexion.cursor()

        # Primero traemos los datos actuales del evento para saber si existe
        # y para poder dejar igual lo que el usuario no quiso cambiar
        cursor.execute("SELECT nombre, fecha, hora, lugar, cupo, registrados FROM eventos WHERE id = %s", (id_evento,))
        evento = cursor.fetchone()

        if evento is None:
            print("No existe un evento con el id", id_evento)
            return

        nombre, fecha_actual, hora_actual, lugar_actual, cupo_actual, registrados = evento

        # Si el usuario no escribio nada en algun campo, usamos el valor que ya tenia
        if fecha == "":
            fecha = fecha_actual
        if hora == "":
            hora = hora_actual
        if lugar == "":
            lugar = lugar_actual
        if cupo is None:
            cupo = cupo_actual

        # El cupo nuevo no puede ser menor a la gente que ya esta registrada
        if cupo <= 0 or cupo < registrados:
            print("El cupo debe ser mayor a 0 y no puede ser menor a los", registrados, "ya registrados")
            return

        # Hacemos el UPDATE con los 4 datos (los que cambiaron y los que se quedaron igual)
        consulta = "UPDATE eventos SET fecha = %s, hora = %s, lugar = %s, cupo = %s WHERE id = %s"
        cursor.execute(consulta, (fecha, hora, lugar, cupo, id_evento))
        conexion.commit()

        print("Evento", nombre, "modificado correctamente")

    except mysql.connector.Error as e:
        conexion.rollback()
        print(f"Ocurrio un error al modificar el evento: {e}")
        print("Revisa que la fecha tenga el formato AAAA-MM-DD y la hora HH:MM")

    finally:
        conexion.close()


# Paso 13. Definimos la funcion que muestra los eventos proximos que todavia tienen lugares disponibles
def eventos_proximos():

    conexion = conectar()
    if conexion is None:
        return

    try:
        cursor = conexion.cursor()

        # CURDATE() es la fecha de hoy en MySQL, entonces fecha >= CURDATE() son los que no han pasado.
        # Con registrados < cupo nos quedamos nada mas con los que todavia tienen lugar.
        # Los ordenamos por fecha y hora para que salga primero el mas cercano.
        consulta = COLUMNAS + " WHERE fecha >= CURDATE() AND registrados < cupo ORDER BY fecha, hora"
        cursor.execute(consulta)
        eventos = cursor.fetchall()

        print()
        print("----- EVENTOS PROXIMOS CON LUGARES DISPONIBLES -----")
        # La columna DISP. de la tabla es la de lugares disponibles = cupo - registrados
        imprimir_eventos(eventos)

    except mysql.connector.Error as e:
        print(f"Ocurrio un error al consultar los eventos proximos: {e}")

    finally:
        conexion.close()


# Paso 14. Esta funcion nada mas imprime las opciones del menu
def mostrar_menu():
    print()
    print("===== SISTEMA DE EVENTOS UNIVERSITARIOS =====")
    print()
    print("1. Mostrar eventos")
    print("2. Buscar evento")
    print("3. Consultar eventos con disponibilidad")
    print("4. Registrar asistentes")
    print("5. Cancelar registros")
    print("6. Agregar evento")
    print("7. Modificar evento")
    print("8. Mostrar eventos próximos")
    print("9. Salir")


# Definimos el menu principal. Con el while True el menu se sigue repitiendo
# hasta que el usuario elige la opcion 9 y hacemos break.
def menu():

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        # Metemos todo en un try porque en varias opciones convertimos lo que escribe el usuario
        # a numero con int(), y si escribe letras eso truena con un ValueError.
        try:
            if opcion == "1":
                mostrar_eventos()

            elif opcion == "2":
                texto = input("Escribe el nombre o parte del nombre del evento: ")
                buscar_evento(texto)

            elif opcion == "3":
                asistentes = int(input("¿Cuántos asistentes quieres registrar? "))
                eventos_con_disponibilidad(asistentes)

            elif opcion == "4":
                id_evento = int(input("Id del evento: "))
                asistentes = int(input("¿Cuántos asistentes quieres registrar? "))
                registrar_asistentes(id_evento, asistentes)

            elif opcion == "5":
                id_evento = int(input("Id del evento: "))
                cantidad = int(input("¿Cuántos registros quieres cancelar? "))
                cancelar_registros(id_evento, cantidad)

            elif opcion == "6":
                nombre = input("Nombre del evento: ")
                fecha = input("Fecha (AAAA-MM-DD): ")
                hora = input("Hora (HH:MM): ")
                lugar = input("Lugar: ")
                cupo = int(input("Cupo máximo: "))
                agregar_evento(nombre, fecha, hora, lugar, cupo)

            elif opcion == "7":
                id_evento = int(input("Id del evento a modificar: "))
                print("Escribe el dato nuevo o deja vacío (Enter) para no cambiarlo")
                fecha = input("Nueva fecha (AAAA-MM-DD): ")
                hora = input("Nueva hora (HH:MM): ")
                lugar = input("Nuevo lugar: ")
                cupo_texto = input("Nuevo cupo: ")

                # Si dejo el cupo vacio mandamos None para que se quede igual,
                # y si escribio algo lo convertimos a numero
                if cupo_texto == "":
                    cupo = None
                else:
                    cupo = int(cupo_texto)

                modificar_evento(id_evento, fecha, hora, lugar, cupo)

            elif opcion == "8":
                eventos_proximos()

            elif opcion == "9":
                print("Saliendo del sistema... ¡Hasta luego!")
                break

            else:
                print("Opción no válida, escribe un número del 1 al 9")

        except ValueError:
            print("Debes escribir un número entero, intenta de nuevo")


# Prueba del programa
if __name__ == "__main__":
    menu()
