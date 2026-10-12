# Meta 2.3: Desarrollar aplicaciones con conexion a Base de Datos

**Nombre:** Diego Valle Cuevas
**Grupo:** 952
**Fecha:** 11/10/2026

## Descripcion

Sistema de eventos universitarios hecho en Python que se conecta a una base de datos
MySQL (`eventos_universitarios`) usando `mysql-connector-python`. Desde un menu permite:

1. Mostrar todos los eventos
2. Buscar eventos por nombre
3. Consultar eventos con disponibilidad para cierta cantidad de asistentes
4. Registrar asistentes a un evento
5. Cancelar registros de un evento
6. Agregar un evento nuevo
7. Modificar la fecha, hora, lugar o cupo de un evento
8. Mostrar los eventos proximos que todavia tienen lugares disponibles
9. Salir

Todas las consultas que reciben datos del usuario usan parametros SQL (`%s`) y cada
operacion tiene manejo de errores con `try`, `except` y `finally`.

## Archivos

- `eventos_universitarios.sql`: crea la base de datos, la tabla `eventos` y registra 10 eventos de prueba.
- `meta 2.3.py`: programa con la conexion, las funciones de cada operacion y el menu principal.

## Como ejecutar

1. Ejecutar el script SQL en MySQL Workbench o desde la terminal:

```
mysql -u root -p < eventos_universitarios.sql
```

2. Instalar la libreria:

```
pip install mysql-connector-python
```

3. Poner el usuario y la contraseña de MySQL en las variables `USUARIO` y `PASSWORD` del archivo `meta 2.3.py`.

4. Correr el programa:

```
python "meta 2.3.py"
```
