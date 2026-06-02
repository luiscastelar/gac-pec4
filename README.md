# PEC2

## Lo hecho

1. Inferencia de tipo de archivo de entrada
2. Inferencia de sistema gestor
3. Utilización del sistema gestor como herramienta de obtención de metadatos más fiable que el procesado del script SQL
4. Infraestructura de contenedores para sistemas gestores (mariadb, sqlite, etc), así como motores de renderizado de salida (php, etc.)
5. Generación de la salida y conexión automática al sistema gestor de prueba. Con sustituir el fichero .env podemos conectarnos a otro servidor del mismo tipo de sistema gestor.
6. Plantillas ampliables para entradas (consultas preformadas) y salidas ("pantallas" preformadas)
7. Si se gestionan los atributos obligatorios mediante el empleo de "required"
8. Si se gestionan las actualizaciones y borrados de los tablas vinculadas mediante "ON DELETE CASCADE ON UPDATE CASCADE"

## Problemas y soluciones

### Estandarización de variables de entorno

El desarrollo planificado inicialmente ha cambiado teniendo distintas ubicaciones para las variables:

1. `.env` y `sqlite.env` en la raíz.
2. Archivos de configuración en `./config`

La solución propuesta es trasladar todas las variables de entorno a directorio `./config`, incluso las que necesitan los sevicios ofrecidos por los contenedores (_docker_).

### Readonly database

**Problema**: Si obtenemos un mensaje

``` bash
Warning: PDOStatement::execute(): SQLSTATE[HY000]: General error: 8 attempt to write a readonly database
```

Deberemos dar permisos adecuados al directororio `salida/php` ya que estamos ejecutando el servidor _nginx-php_ con el usuario _www-data_ (id:33) y habitualmente seremos otro usuario con id:1000.

**Solución**: Otorgar permisos completos para todos los usuarios en dicho directorio:

``` bash
sudo chmod 777 -R salida/php
```

Con el ello el usuario _www-data_ (id:33) podrá escribir en el directorio.

**Mejoras**: Deberíamos montar en un volumen diferente la base de datos en un directorio con permisos completos y mantener el directorio `salida/php` con permisos simples 744.

## Lo obviado

El motivo de este trabajo es la generación automática de código por lo que se han obviado los siguientes conceptos:

1. Seguridad: para su utilización real se debería establecer un mecanismo de autenticación para el acceso a la base de datos, o si estamos generando una herramienta abierta, el usuario deberá proporcionar las credenciales.
2. A prueba de fallos: existen múltiples consultas que pueden arrojar excepciones que detienen la aplicación y deberían ser adecuadamente atrapadas y procesadas.
3. No gestiono los ID. Esto es, el usuario debe indicar un ID que no existe para CREAR, o uno que existe para MODICAR o ELIMINAR
4. No gestiono los Foreign Key de las tablas. El usuario deber crear la tabla madre antes de insertar en la tabla derivada.

## Herramientas

### Exportación para obtener una definición exacta

+ DONE: mariaDB: env $(cat .env | xargs)  bash -c ' docker exec -i mariaDB mysqldump -u"$user" -p"$pass" "$db" > dump-$db.sql'
+ DONE: sqlite: script basb
