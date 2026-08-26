# ecommerce encargado de la presentación

## Problema que resuelve
Permite la compra y venta de productos en línea de manera ininterrumpida, gestionando picos de tráfico durante eventos de alta demanda como Black Friday sin que la plataforma se caiga o procese cobros duplicados.
* **Usuarios:** Clientes finales, administradores de tienda y operadores de logística.
* **Impacto sin el sistema:** Pérdidas financieras por ventas no procesadas, saturación de servidores e inconsistencia en los inventarios.

## Servicios del sistema
* **Servicio de Usuarios y Autenticación:** Gestiona registros, perfiles y tokens de sesión.
* **Servicio de Catálogo e Inventario:** Controla los productos disponibles y la actualización de stock en tiempo real.
* **Servicio de Pedidos:** Procesa la creación de carritos y la orden de compra.
* **Servicio de Pagos:** Procesa las transacciones de tarjeta/transferencia mediante pasarelas externas.
* **Servicio de Notificaciones:** Envía correos y alertas de confirmación de compra y envío.

## Comunicación entre servicios
* **Pedidos → Inventario:** El servicio de Pedidos solicita la reserva de stock al servicio de Inventario.
* **Pedidos → Pagos:** El servicio de Pedidos solicita procesar la transacción financiera.
* **Pagos → Pedidos:** Pagos confirma si la transacción fue exitosa para cambiar el estado de la orden.
* **Pedidos → Notificaciones:** Pedidos emite un evento para enviar la confirmación por correo al cliente.

## Tipo de arquitectura
**Microservicios orientada a eventos (Híbrida)**
* **Justificación:** Elegimos esta arquitectura porque los picos de tráfico en e-commerce afectan principalmente al catálogo y pagos, por lo que cada servicio debe escalar de forma independiente sin detener la totalidad de la tienda.

## Base de datos
* **Enfoque:** Database per Service (Cada microservicio maneja su propia base de datos).
* **Datos críticos:** Transacciones de pago, historial de pedidos y stock.
* **Riesgo por pérdida:** Pérdida de dinero, duplicidad de pedidos y reclamos legales de clientes.

## Usuarios del sistema
* **Cliente:** Puede navegar, agregar al carrito, pagar y rastrear su pedido.
* **Administrador:** Modifica catálogo, ajusta precios y analiza reportes.
* **Operador de Logística:** Actualiza estados de envío de las compras.

## Riesgos y fallas posibles
* **Falla en Pasarela de Pagos:** Implementación de reintentos automáticos y guardado de estado transitorio.
* **Caída de la Base de Datos:** Réplicas de lectura e historial de transacciones en cola de mensajes para procesamiento diferido.
* **Saturación del Servidor:** Balanceadores de carga y escalado horizontal de contenedores.

## Base de datos
* **Enfoque:** Database per Service, cada microservicio maneja su propia base de datos.
* **Datos críticos:** Transacciones de pago, historial de pedidos y stock.
* **Riesgo por pérdida:** Pérdida de dinero, duplicidad de pedidos y reclamos legales de clientes.

```mermaid
graph TD
    Cliente -->|1. Pide Producto| Pedidos
    Pedidos -->|2. Consulta Stock| Inventario
    Pedidos -->|3. Solicita Cobro| Pagos
    Pagos -->|4. Confirma Pago| Pedidos
    Pedidos -->|5. Activa Alerta| Notificaciones
