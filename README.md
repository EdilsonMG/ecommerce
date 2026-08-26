 Tipo de Arquitectura
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


=======
## Arquitectura del sistema

**Microservicios**

**Justificación:** el sistema tiene múltiples dominios independientes 
(usuarios, pagos, inventario, notificaciones) que necesitan escalar por 
separado. Por ejemplo, en época de descuentos, los servicios de pedidos y 
pagos reciben mucha más carga que el de notificaciones. Además, permite 
que distintos equipos trabajen en paralelo sin bloquearse entre sí, y 
facilita agregar nuevos comercios sin afectar el resto del sistema.

- ¿Cuántos usuarios tendrá? Se espera crecimiento constante (cientos a 
  miles de comercios y compradores).
- ¿Necesita escalar? Sí, especialmente pedidos y pagos en temporadas altas.
- ¿Es un sistema pequeño o grande? Mediano, con proyección a grande.
- **Base de datos:** cada servicio tiene su propia base de datos 


## Problema que resuelve

Muchos negocios pequeños (tiendas de barrio, papelerías, boutiques) no tienen 
presencia digital ni forma de vender en línea. Los que lo intentan usan hojas 
de cálculo o WhatsApp para gestionar pedidos, lo que genera errores de 
inventario, demoras en pagos y mala experiencia del cliente.

**MarketExpress** resuelve esto ofreciendo una plataforma donde estos 
comercios pueden publicar productos, recibir pedidos, procesar pagos y 
gestionar inventario de forma centralizada y automatizada.

- **¿Quién lo usará?** Dueños de tiendas pequeñas (vendedores), compradores 
  finales y administradores de la plataforma.
- **¿Qué pasaría si no existiera?** Los comercios seguirían dependiendo de 
  procesos manuales propensos a errores, perderían ventas frente a 
  competidores con presencia digital, y los clientes tendrían una mala 
  experiencia de compra.


## Usuarios del sistema

| Rol | Puede hacer |
|---|---|
| Administrador | Gestiona toda la plataforma |
| Vendedor | Administra solo sus propios productos, inventario y pedidos |
| Cliente | Compra, ve su historial y da seguimiento a sus propios pedidos |
| Operador de soporte | Atiende reclamos y disputas |

