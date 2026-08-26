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



