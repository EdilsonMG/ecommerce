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
- Catalogo de productos
- Pedidos
- Pagos
- Notificaciones

# Posibles fallos y riesgos
- El pedido al no completarse se pierde
- No responde la base de datos
- No se envían los mensajes de confirmación

## Servicios del sistema

* **Servicio de Usuarios y Autenticación (Auth Service):** Encargado de gestionar el registro, inicio de sesión, perfiles de clientes, direcciones de envío y la emisión/validación de tokens JWT para controlar accesos seguros a la plataforma.
* **Servicio de Catálogo e Inventario (Catalog & Inventory Service):** Administra las categorías, detalles de productos, imágenes y precios, manteniendo la actualización del stock disponible en tiempo real para evitar la sobreventa (*overselling*).
* **Servicio de Pedidos (Orders Service):** Procesa la creación de carritos de compra, la consolidación de la orden, la asignación de números de seguimiento y el cambio de estado del pedido (Pendiente, Pagado, Enviado).
* **Servicio de Pagos (Payment Gateway Service):** Procesa la transacción monetaria integrándose con pasarelas externas (Stripe, PayPal, MercadoPago) y maneja las respuestas de confirmación o rechazo de pago.
* **Servicio de Notificaciones (Notification Service):** Genera y envía automáticamente comprobantes de compra por correo electrónico, mensajes SMS de estado de envío y alertas operativas.

## Comunicación entre servicios

* **Pedidos → Usuarios (Síncrona - REST API):** El servicio de Pedidos solicita a Usuarios la validación de la sesión activa y la dirección de entrega del cliente.
* **Pedidos → Inventario (Síncrona - REST/gRPC):** El servicio de Pedidos solicita al Inventario verificar y reservar el stock del producto seleccionado antes de iniciar el cobro.
* **Pedidos → Pagos (Asíncrona - Event/HTTP):** Pedidos solicita al servicio de Pagos la transacción. Pagos confirma el resultado del cobro para que Pedidos actualice el estado a "Aprobado".
* **Pagos → Inventario (Asíncrona - Event-Driven):** Tras la confirmación del pago exitoso, el servicio de Pagos emite un evento para descontar definitivamente el stock del Inventario.
* **Pedidos → Notificaciones (Asíncrona - Message Broker):** Pedidos emite un evento de "Orden Creada" a la cola de mensajes para que Notificaciones prepare y envíe la confirmación por correo al cliente sin ralentizar la compra.



```mermaid
graph TD
    Cliente -->|1. Autenticación / Registro| Auth[Servicio de Usuarios]
    Cliente -->|2. Crear Pedido| Orders[Servicio de Pedidos]
    Orders -->|3. Validar / Reservar Stock| Catalog[Servicio de Inventario]
    Orders -->|4. Procesar Cobro| Payments[Servicio de Pagos]
    Payments -->|5. Confirma Pago Exitoso| Orders
    Payments -->|6. Evento: Descontar Stock| Catalog
    Orders -->|7. Evento: Notificar Cliente| Notifications[Servicio de Notificaciones]
