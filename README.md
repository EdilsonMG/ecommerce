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

## Fallas y riesgos

| Si falla... | Consecuencia | Solución propuesta |
|---|---|---|
| Servicio de pagos | Pedidos quedan sin confirmar | Reintentos automáticos + cola de mensajes |
| Base de datos | Pérdida/inconsistencia de datos | Respaldos periódicos + réplicas |
| Servidor principal | Plataforma caída | Balanceador de carga + servidores redundantes |

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
