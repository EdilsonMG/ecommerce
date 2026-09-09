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

* **Servicio de Usuarios:** Encargado de gestionar el registro, inicio de sesión, perfiles de clientes, direcciones de envío y la emisión/validación de tokens JWT para controlar accesos seguros a la plataforma.
* **Servicio de productos :** Administra las categorías, detalles de productos, imágenes y precios, manteniendo la actualización del stock disponible en tiempo real para evitar la sobreventa (*overselling*).
* **Servicio de Pedidos :** Procesa la creación de carritos de compra, la consolidación de la orden, la asignación de números de seguimiento y el cambio de estado del pedido (Pendiente, Pagado, Enviado).


## Comunicación entre servicios

* **Pedidos → Usuarios (Síncrona - REST API):** El servicio de Pedidos solicita a Usuarios la validación de la sesión activa y la dirección de entrega del cliente.
* **Pedidos → Productos (Síncrona - REST/gRPC):** El servicio de Pedidos solicita al Inventario verificar y reservar el stock del producto seleccionado antes de iniciar el cobro.
.

    
## Docker Compose

 home:
    image: home:4.0
    ports:
      - "3000:80"
    container_name: home

  usuarios:
    image: alpine
    container_name: usuarios

  productos:
    image: alpine
    container_name: productos

  pedidos:
    image: alpine
    container_name: pedidos

El comando docker build -t home:4.0 . le ordena a Docker construir una nueva imagen del contenedor procesando las instrucciones de nuestro archivo Dockerfile. La opción -t le asigna directamente la etiqueta con el nombre home y la versión 4.0 para identificarla en el sistema, mientras que el punto final indica que la ruta de origen y los archivos requeridos están en el directorio donde te encuentras parado.

El comando docker images sirve para ver la consulta de la base de datos de nuestro sistema para mostrar un listado completo de todas las imágenes de Docker guardadas localmente, permitiéndonos comprobar que la nueva imagen se creó correctamente junto a detalles como su ID, tamaño y fecha de creación.

El comando docker compose up -d home lee la configuración de nuestro archivo compose.yml para compilar y poner en marcha únicamente el servicio especificado llamado home, ejecutándolo de forma aislada y en segundo plano sin activar los demás servicios listados en el archivo.

El comando docker ps genera un reporte en tiempo real de todos los contenedores que permanecen activos en nuestro equipo, mostrando su ID, nombre, estado actual y los puertos mapeados para que verifiques que el proceso se inició de forma exitosa.


 
## DockerFile

FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80

CMD [ "nginx", "-g", "daemon off;" ]

La instrucción FROM nginx:alpine le indica a Docker la base sobre la cual construiremos nuestro contenedor, utilizando una versión ligera del sistema operativo Linux que ya trae el servidor web Nginx instalado de fábrica.

La instrucción COPY index.html /usr/share/nginx/html/index.html toma el archivo index.html que está en nuestra computadora y lo copia directamente a la ruta interna del contenedor donde Nginx guarda las páginas que va a mostrar.

La instrucción EXPOSE 80 informa que el contenedor estará escuchando conexiones a través del puerto 80, que es el puerto estándar que utilizan las aplicaciones web para transmitir tráfico HTTP.

La instrucción CMD  ["nginx", "-g", "daemon off;"] ejecuta el servidor Nginx al momento de arrancar el contenedor y lo fuerza a quedarse corriendo en primer plano para evitar que el contenedor se apague solo.

## Diseñado
Se definió la arquitectura del sistema distribuido basada en microservicios, identificando los dominios principales de la plataforma: Usuarios, Productos y Pedidos. Asimismo, se planificó la estructura de directorios del proyecto en Git y el esquema de empaquetamiento independiente para el servicio principal mediante contenedores Docker.

## Configurado
Se estableció el archivo de orquestación compose.yml para gestionar la ejecución conjunta de los servicios del sistema, mapeando los puertos de red y asignando los nombres fijos a cada contenedor. Se configuraron también las imágenes base livianas para los servicios auxiliares y la base del servidor Nginx para la entrega de contenido estático.

## Implementado
Se construyó e integró el servicio inicial home dentro del contenedor mediante su respectivo Dockerfile, el cual expone el puerto 80 y sirve la interfaz web de inicio. Se probó la compilación de la imagen home:4.0 y su correcto despliegue local mediante comandos de Docker y Docker Compose.

## Pendiente
Queda por desarrollar la lógica de negocio y las bases de datos de los servicios de Usuarios, Productos y Pedidos para reemplazar las imágenes genéricas temporales.

