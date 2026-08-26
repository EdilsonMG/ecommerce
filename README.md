# MarketExpress

## Problemática

Muchos negocios pequeños (tiendas de barrio, papelerías, boutiques) no tienen 
presencia digital ni forma de vender en línea. Los que lo intentan usan hojas 
de cálculo o WhatsApp para gestionar pedidos, lo que genera errores de 
inventario, demoras en pagos y mala experiencia del cliente.

**MarketExpress** resuelve esto ofreciendo una plataforma donde estos comercios 
pueden publicar productos, recibir pedidos, procesar pagos y gestionar 
inventario de forma centralizada y automatizada.

- **¿Quién lo usará?** Dueños de tiendas pequeñas (vendedores), compradores 
  finales y administradores de la plataforma.
- **¿Qué pasaría si no existiera?** Los comercios seguirían dependiendo de 
  procesos manuales propensos a errores, perderían ventas frente a 
  competidores con presencia digital, y los clientes tendrían una mala 
  experiencia de compra.

## Roles del equipo

| Rol | Responsabilidades |
|---|---|
| Líder del proyecto | Coordina el avance, toma decisiones finales, revisa y aprueba los Pull Requests |
| Encargado de documentación | Redacta el README, escribe commits y descripciones de PR |
| Encargado técnico | Define arquitectura, base de datos, comunicación entre servicios y manejo de fallas |
| Encargado de presentación | Prepara la exposición y el diagrama final del proyecto |


##  Servicios identificados

| Servicio | Función principal |
|---|---|
| Usuarios | Registro y login de compradores y vendedores |
| Catálogo / Productos | Publicación y gestión de productos |
| Pedidos | Creación y seguimiento de órdenes de compra |
| Pagos | Procesamiento de transacciones (tarjetas, PSE, etc.) |
| Notificaciones | Envío de emails/push sobre estado de pedidos |
| Inventario | Control de stock en tiempo real |

## Comunicación entre servicios

```
Pedidos      → solicita →  Inventario       (¿hay stock?)
Pedidos      → solicita →  Pagos            (procesar cobro)
Pagos        → confirma →  Pedidos          (pago exitoso, cambia estado)
Pedidos      → notifica →  Notificaciones   (avisa a comprador y vendedor)
Inventario   → actualiza → Catálogo         (refleja nuevo stock)
```

## Arquitectura elegida

**Microservicios**

**Justificación:** el sistema tiene múltiples dominios independientes 
(usuarios, pagos, inventario, notificaciones) que necesitan escalar por 
separado. Por ejemplo, en época de descuentos, pedidos y pagos reciben mucha 
más carga que notificaciones. Además, permite que distintos equipos trabajen 
en paralelo sin bloquearse, y facilita agregar nuevos comercios sin afectar 
el resto del sistema.

- **Base de datos:** cada servicio tiene su propia base de datos


## Roles de usuario del sistema

| Rol | Puede hacer |
|---|---|
| Administrador | Gestiona toda la plataforma |
| Vendedor | Administra solo sus propios productos, inventario y pedidos |
| Cliente | Compra, ve su historial y da seguimiento a sus propios pedidos |
| Operador de soporte | Atiende reclamos y disputas |

---

## Fallas y riesgos

| Si falla... | Consecuencia | Solución propuesta |
|---|---|---|
| Servicio de pagos | Pedidos quedan sin confirmar | Reintentos automáticos + cola de mensajes |
| Base de datos | Pérdida/inconsistencia de datos | Respaldos periódicos + réplicas |
| Servidor principal | Plataforma caída | Balanceador de carga + servidores redundantes |


