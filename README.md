# PEC4

## Lo hecho

1. Inferencia de la base de datos

## Problemas y soluciones

### Estandarización de variables de entorno

El desarrollo planificado inicialmente ha cambiado teniendo distintas ubicaciones para las variables:

1. `.env` y `sqlite.env` en la raíz.
2. Archivos de configuración en `./config`

La solución propuesta es trasladar todas las variables de entorno a directorio `./config`, incluso las que necesitan los sevicios ofrecidos por los contenedores (_docker_).

## Lo obviado

El motivo de este trabajo es la generación automática de código por lo que se han obviado los siguientes conceptos:

1. Seguridad: para su utilización real se debería establecer un mecanismo de autenticación para el acceso a la base de datos, o si estamos generando una herramienta abierta, el usuario deberá proporcionar las credenciales.
2. A prueba de fallos: existen múltiples consultas que pueden arrojar excepciones que detienen la aplicación y deberían ser adecuadamente atrapadas y procesadas.
3. No gestiono los ID. Esto es, el usuario debe indicar un ID que no existe para CREAR, o uno que existe para MODICAR o ELIMINAR
4. No gestiono los Foreign Key de las tablas. El usuario deber crear la tabla madre antes de insertar en la tabla derivada.

## Herramientas
