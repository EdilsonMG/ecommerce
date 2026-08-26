## Servicios del sistema
* **Servicio de Usuarios y Autenticación:** Encargado de gestionar el registro, inicio de sesión, perfiles de clientes, direcciones de envío y la emisión/validación de tokens JWT para controlar accesos seguros a la plataforma.
* **Servicio de Catálogo e Inventario:** Administra las categorías, detalles de productos, imágenes y precios, manteniendo la actualización del stock disponible en tiempo real para evitar la sobreventa.
* **Servicio de Pedidos:** Procesa la creación de carritos de compra, la consolidación de la orden, la asignación de números de seguimiento y el cambio de estado del pedido (Pendiente, Pagado, Enviado).
* **Servicio de Pagos:** Procesa la transacción monetaria integrándose con pasarelas externas (Stripe, PayPal, MercadoPago) y maneja las respuestas de confirmación o rechazo de pago.
* **Servicio de Notificaciones:** Genera y envía automáticamente comprobantes de compra por correo electrónico, mensajes SMS de estado de envío y alertas operativas.
