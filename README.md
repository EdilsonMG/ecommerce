## Arquitectura del sistema

*Microservicios*

*Justificación:* el sistema tiene múltiples dominios independientes 
(usuarios, pagos, inventario, notificaciones) que necesitan escalar por 
separado. Por ejemplo, en época de descuentos, los servicios de pedidos y 
pagos reciben mucha más carga que el de notificaciones. Además, permite que 
distintos equipos trabajen en paralelo sin bloquearse entre sí, y facilita 
agregar nuevos comercios sin afectar el resto del sistema.

- ¿Cuántos usuarios tendrá? Se espera crecimiento constante (cientos a 
  miles de comercios y compradores).
- ¿Necesita escalar? Sí, especialmente pedidos y pagos en temporadas altas.
- ¿Es un sistema pequeño o grande? Mediano, con proyección a grande.
- *Base de datos:* cada servicio tiene su propia base de datos 
  (patrón database per service), para evitar acoplamiento.

---

## Roles de usuario del sistema

| Rol | Puede hacer |
|---|---|
| Administrador | Gestiona toda la plataforma |
| Vendedor | Administra solo sus propios productos, inventario y pedidos |
| Cliente | Compra, ve su historial y da seguimiento a sus propios pedidos |
| Operador de soporte | Atiende reclamos y disputas |

---

## Revisión del equipo

- Se verificó que los servicios no se solapen en responsabilidades.
- Se confirmó que la arquitectura de microservicios es coherente con el 
  tamaño proyectado del sistema.
- Mejoras propuestas: agregar un *API Gateway* y un futuro **servicio de 
  reseñas/calificaciones**.

# Tipo de Arquitectura
- Arquitectura basada en microservicios porque permiten escalar cada servicio si uno falla, el resto del sistema sigue funcionando y que el equipo trabaja en paralelo sin bloquearse.

# Base de datos
Cada microservicio tiene su propia base de datos personal, así cuando haya un problema en alguna base de datos de algún microservicio no afecte a ninguna otra base de datos.
- Usuarios
- Productos
- Pedidos



# Posibles fallos y riesgos
- El pedido al no completarse se pierde
- No responde la base de datos
- No se envían los mensajes de confirmación

## Servicios del sistema

| Servicio | Responsabilidad | Datos administrados |
| --- | --- | --- |
| Usuarios | Gestionar clientes | Nombre, correo |
| Productos | Gestionar productos disponibles | Nombre, precio, categoría, stock |
| Pedidos | Gestionar órdenes realizadas | IdUsuario, IdProducto, estado, cantidad, valortotal, fechaPedido |

## Diseño de responsabilidades

| Servicio | Responsabilidad | Datos administrados | Comunicación con otros servicios |
| :--- | :--- | :--- | :--- |
| **Usuarios** | Gestionar clientes | Nombre, correo | **Suele ser independiente.** Responde a las consultas de validación de identidad e información del cliente solicitadas por **Pedidos**. |
| **Productos** | Gestionar productos disponibles | Nombre, precio, categoría, stock | **Recibe consultas de Pedidos** para verificar la disponibilidad de stock y confirmar el precio unitario actualizado. |
| **Pedidos** | Gestionar órdenes realizadas | IdUsuario, IdProducto, estado, cantidad, valortotal, fechaPedido | **Consulta a Usuarios** (para validar el cliente) y a **Productos** (para verificar existencia de stock y calcular el valor total). |


## Comunicación entre servicios

* **Pedidos → Usuarios (Síncrona - REST API):** El servicio de Pedidos solicita a Usuarios la validación de la sesión activa y la dirección de entrega del cliente.
* **Pedidos → Productos (Síncrona - REST/gRPC):** El servicio de Pedidos solicita al Inventario verificar y reservar el stock del producto seleccionado antes de iniciar el cobro.
.

## ENDPOINTS

### Servicio Productos

| Método | Endpoint | Descripción | Entrada | Respuesta |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/productos` | Consultar productos | Ninguna | Lista de productos |
| **GET** | `/productos/{id}` | Consultar producto por id | ID producto | Producto específico |
| **POST** | `/productos` | Crear producto | JSON del Producto | Confirmación de creación |
| **PUT** | `/productos/{id}` | Actualización completa de un producto | JSON actualizado | Producto modificado |
| **PATCH** | `/productos/{id}` | Actualización parcial de un producto | JSON con los campos a modificar | Producto modificado parcialmente |
| **DELETE** | `/productos/{id}` | Eliminar producto | ID producto | Confirmación de eliminación exitosa |

### Servicio Pedidos

| Método | Endpoint | Descripción | Entrada | Respuesta |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/pedidos` | Consultar todos los pedidos | Ninguna | Lista de pedidos |
| **GET** | `/pedidos/<id>/detalle` | Consultar el detalle de un pedido por ID incluyendo datos de usuarios y productos mediante microservicios y BD | ID del pedido en la URL | Datos enriquecidos del pedido (usuario, producto, cantidad, estado, valor total y fecha) o mensaje de error |
| **POST** | `/pedidos` | Crear un nuevo pedido | JSON con datos del pedido | Confirmación y nuevo ID generado |
| **DELETE** | `/pedidos/<id>` | Eliminar un pedido | ID del pedido en la URL | Confirmación de eliminación o mensaje de error |
| **PUT** | `/pedidos/<id>` | Actualización completa de un pedido | ID en URL + JSON con todos los campos | Mensaje de actualización exitosa o error |
| **PATCH** | `/pedidos/<id>` | Actualización parcial de un pedido | ID en URL + JSON con los campos a modificar | Mensaje de actualización exitosa o error |

### Servicio Usuarios
| Método | Endpoint | Descripción | Entrada | Respuesta |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/usuarios` | Consultar todos los usuarios | Ninguna | Lista de usuarios |
| **GET** | `/usuarios/{id}` | Consultar usuario por ID | ID del usuario en la URL | Datos del usuario o mensaje de no encontrado |
| **POST** | `/usuarios` | Crear un nuevo usuario | JSON con datos del usuario (`nombre`, `email`) | Confirmación y nuevo ID generado |
| **DELETE** | `/usuarios/{id}` | Eliminar un usuario | ID del usuario en la URL | Confirmación de eliminación o mensaje de error |
| **PUT** | `/usuarios/{id}` | Actualización completa de un usuario | ID en URL + JSON con todos los campos | Mensaje de actualización exitosa o error |
| **PATCH** | `/usuarios/{id}` | Actualización parcial de un usuario | ID en URL + JSON con los campos a modificar | Mensaje de actualización exitosa o error |

### Base de datos por servicio
| Servicio | Base de datos utilizada | Tablas principales |
| :--- | :--- | :--- |
| **Usuarios** | `mysqlproductos` - `mysql:8.0` | `usuarios` (`id`, `nombre`, `email`) |
| **Productos** | `mysqlproductos` - `mysql:8.0` | `productos` (`id`, `nombre`, `categoria`, `precio`, `stock`) |
| **Pedidos** | `mysqlpedidos` - `mysql:8.0` | `pedidos` (`id`, `idUsuario`, `idProducto`, `cantidad`, `estado`, `valortotal`, `fechaPedido`) |

### Configuración mediante variables de entorno
| Variable | Uso |
| :--- | :--- |
| Variable | Uso |
| :--- | :--- |
| `USUARIOS_DB_HOST` | Host o nombre del contenedor del servidor MySQL para el servicio de Usuarios (`mysql_usuarios`) |
| `USUARIOS_DB_PORT` | Puerto de conexión a la base de datos de Usuarios (`3306`) |
| `USUARIOS_DB_USER` | Usuario para autenticarse en la base de datos de Usuarios (`root`) |
| `USUARIOS_DB_PASSWORD` | Contraseña de acceso a la base de datos de Usuarios (`root`) |
| `USUARIOS_DB_NAME` | Nombre de la base de datos del servicio de Usuarios (`usuarios_db`) |
| `PRODUCTOS_DB_HOST` | Host o nombre del contenedor del servidor MySQL para el servicio de Productos (`mysql_productos`) |
| `PRODUCTOS_DB_PORT` | Puerto de conexión a la base de datos de Productos (`3306`) |
| `PRODUCTOS_DB_USER` | Usuario para autenticarse en la base de datos de Productos (`root`) |
| `PRODUCTOS_DB_PASSWORD` | Contraseña de acceso a la base de datos de Productos (`root`) |
| `PRODUCTOS_DB_NAME` | Nombre de la base de datos del servicio de Productos (`productos_db`) |
| `PEDIDOS_DB_HOST` | Host o nombre del contenedor del servidor MySQL para el servicio de Pedidos (`mysql_pedidos`) |
| `PEDIDOS_DB_PORT` | Puerto de conexión a la base de datos de Pedidos (`3306`) |
| `PEDIDOS_DB_USER` | Usuario para autenticarse en la base de datos de Pedidos (`root`) |
| `PEDIDOS_DB_PASSWORD` | Contraseña de acceso a la base de datos de Pedidos (`root`) |
| `PEDIDOS_DB_NAME` | Nombre de la base de datos del servicio de Pedidos (`pedidos_db`) |
| `USUARIOS_URL` | URL de acceso al microservicio de Usuarios (`http://usuarios:5000`) |
| `PRODUCTOS_URL` | URL de acceso al microservicio de Productos (`http://productos:5000`) |


## Docker Compose
docker compose up --build

### Comunicación entre servicios

| Elemento | Descripción |
| :--- | :--- |
| **Servicio que solicita** | Pedidos |
| **Servicio que responde** | Usuarios |
| **Endpoint utilizado** | `GET /pedidos/{id}/detalle` |
| **Información enviada** | ID del usuario obtenido del registro del pedido (`idUsuario`) |
| **Información recibida** | Datos completos del usuario (nombre, correo) para enriquecer el detalle |

| Elemento | Descripción |
| :--- | :--- |
| **Servicio que solicita** | Pedidos |
| **Servicio que responde** | Productos |
| **Endpoint utilizado** | `GET /pedidos/{id}/detalle` |
| **Información enviada** | ID del producto obtenido del registro del pedido (`idProducto`) |
| **Información recibida** | Datos completos del producto (nombre, categoría, precio) para enriquecer el detalle |


## Arquitectura del sistema

*Microservicios*

*Justificación:* el sistema tiene múltiples dominios independientes 
(usuarios, pagos, inventario, notificaciones) que necesitan escalar por 
separado. Por ejemplo, en época de descuentos, los servicios de pedidos y 
pagos reciben mucha más carga que el de notificaciones. Además, permite que 
distintos equipos trabajen en paralelo sin bloquearse entre sí, y facilita 
agregar nuevos comercios sin afectar el resto del sistema.

- ¿Cuántos usuarios tendrá? Se espera crecimiento constante (cientos a 
  miles de comercios y compradores).
- ¿Necesita escalar? Sí, especialmente pedidos y pagos en temporadas altas.
- ¿Es un sistema pequeño o grande? Mediano, con proyección a grande.
- *Base de datos:* cada servicio tiene su propia base de datos 
  (patrón database per service), para evitar acoplamiento.

---

## Compose.YML
services:

  home:
    build: ./home
    image: home:4.0
    ports:
      - "3000:80"
    container_name: home

  usuarios:
    build: ./usuarios
    container_name: usuarios
    ports:
      - "5001:5000"  
    env_file:
      - .env
    depends_on:
      - mysqlusuarios

  productos:
    build: ./productos
    container_name: productos
    ports:
      - "5002:5000"  
    env_file:
      - .env
    depends_on:
      - mysqlproductos

  pedidos:
    build: ./pedidos
    container_name: pedidos
    ports:
      - "5003:5000"  
    env_file:
      - .env
    depends_on:
      - mysqlpedidos

  mysqlpedidos:
    image: mysql:8.0
    container_name: mysqlpedidos
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: pedidos_db
    ports:
      - "3309:3306"
    volumes:
      - pedidos_data:/var/lib/mysql

  mysqlproductos:
    image: mysql:8.0
    container_name: mysqlproductos
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: productos_db
    ports:
      - "3307:3306"
    volumes:
      - productos_data:/var/lib/mysql

  mysqlusuarios:
    image: mysql:8.0
    container_name: mysqlusuarios
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: usuarios_db
    ports:
      - "3308:3306"
    volumes:
      - usuarios_data:/var/lib/mysql

volumes:
  pedidos_data:
  productos_data:
  usuarios_data:

El comando docker build -t home:4.0 . le ordena a Docker construir una nueva imagen del contenedor procesando las instrucciones de nuestro archivo Dockerfile. La opción -t le asigna directamente la etiqueta con el nombre home y la versión 4.0 para identificarla en el sistema, mientras que el punto final indica que la ruta de origen y los archivos requeridos están en el directorio donde te encuentras parado.

El comando docker images sirve para ver la consulta de la base de datos de nuestro sistema para mostrar un listado completo de todas las imágenes de Docker guardadas localmente, permitiéndonos comprobar que la nueva imagen se creó correctamente junto a detalles como su ID, tamaño y fecha de creación.

El comando docker compose up -d home lee la configuración de nuestro archivo compose.yml para compilar y poner en marcha únicamente el servicio especificado llamado home, ejecutándolo de forma aislada y en segundo plano sin activar los demás servicios listados en el archivo.

El comando docker ps genera un reporte en tiempo real de todos los contenedores que permanecen activos en nuestro equipo, mostrando su ID, nombre, estado actual y los puertos mapeados para que verifiques que el proceso se inició de forma exitosa.


 
## DockerFile

FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80
main

CMD [ "nginx", "-g", "daemon off;" ]

La instrucción FROM nginx:alpine le indica a Docker la base sobre la cual construiremos nuestro contenedor, utilizando una versión ligera del sistema operativo Linux que ya trae el servidor web Nginx instalado de fábrica.

La instrucción COPY index.html /usr/share/nginx/html/index.html toma el archivo index.html que está en nuestra computadora y lo copia directamente a la ruta interna del contenedor donde Nginx guarda las páginas que va a mostrar.

La instrucción EXPOSE 80 informa que el contenedor estará escuchando conexiones a través del puerto 80, que es el puerto estándar que utilizan las aplicaciones web para transmitir tráfico HTTP.

La instrucción CMD  ["nginx", "-g", "daemon off;"] ejecuta el servidor Nginx al momento de arrancar el contenedor y lo fuerza a quedarse corriendo en primer plano para evitar que el contenedor se apague solo.

## Configurado
Se estableció el archivo de orquestación `compose.yml` para gestionar la ejecución conjunta de los servicios del sistema, mapeando los puertos de red y asignando nombres fijos a cada contenedor. Se configuraron las bases de datos MySQL para cada microservicio con persistencia mediante volúmenes dedicados, junto con la integración de los archivos de entorno y la base del servidor Nginx para la entrega de contenido estático del servicio inicial.

## Implementado
Se construyeron e integraron por completo los microservicios de **Usuarios**, **Productos** y **Pedidos** a través de sus respectivos `Dockerfile` y lógica de negocio en Flask, reemplazando las imágenes genéricas temporales. Cada microservicio cuenta ahora con su propia base de datos MySQL dedicada (`usuarios_db`, `productos_db` y `pedidos_db`), comunicación interna configurada mediante variables de entorno, endpoints de gestión completos (incluyendo el enriquecimiento de datos en el detalle de pedidos) y despliegue local exitoso mediante Docker Compose.

## Pendiente
Se ha completado el desarrollo principal de la arquitectura de microservicios, bases de datos y orquestación local del sistema.


