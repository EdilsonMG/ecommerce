# Encargado tecnico: Ecommerce

## Que servicio necesita información de otro
- el servicio de pedidos necesita del servicio de catalogo para verificar el stock disponible
- el servicio de pedidos también necesita del servicio de clientes para extraer los datos
- el servicio de pagos necesita del servicio de pedidos

## Quien solicita datos
- pedidos solicita al catalogo la cantidad de productos disponibles
- pedidos solicita validación al usuario para confirmar la compra
  
## Quien responde
- el servicio de inventario responde con la cantidad disponible de cada producto
- el servicio de pagos responde con la confirmación o cancelación del pago

## Tipo de Arquitectura
- Arquitectura basada en microservicios

## Cuantos usuarios tendrá el sistema
- Al comienzo se iniciara con pocos comercios pero se espera un crecimiento porcentual
  
## Necesita escalar
- Cada comercio espera agregar productos y gestionar pedidos con el fin de crezca y no se caiga en el intento
  
## Es un sistema pequeño o grande
- Es un sistema pequeño-intermedio pensado en que crezca con el tiempo

## Justificación
- Elegimos microservicios porque permiten escalar cada servicio si uno falla, el resto del
sistema sigue funcionando y que el equipo trabaja en paralelo sin bloquearse.

## Que información debe guardarse
Absolutamente toda la información de los microservicios debe guardarse
- Datos de usuarios
- Catalogo de productos
- Pedidos
- Pagos
- Notificaciones

## Que datos son críticos
- Pedidos y Pagos ya que requieren dinero, transacciones en tiempo real
- Catalogo de productos para no vender productos sin stock
  
## Que pasaría si se pierden
Se podrían generar pedidos duplicados, además que se las transacciones deben estar siempre registradas porque pueden hacer que el comercio pierda confiabilidad

## Todos los servicios usan la misma base de datos o cada uno tiene la suya
Cada base de datos tiene su propia base de datos personal, asi cuando haya un problema en alguna base de datos de algun microservicio no afecte a ninguna otra base de datos.

## Que pasaría si falla

## Sistema de pagos
El pedido queda en estado pendiente en vez de perderse

## Base de datos
se activa una réplica de respaldo para no dejar el sistema totalmente caido

## Servidor principal
La petición se redirige a otra instancia disponible evitando que el sistema quede sin acceso

## Soluciones
- Reintentos automáticos con limite entre servicios que fallan
- Notificaciones al usuario y al equipo tecnico cuando falla una operacion critica

# Revisión tecnica

## Por que microservicios como arquitectura 
Porque cada parte del ecommerce puede crecer y fallar de forma independiente y los microservicios permiten escalar solo lo que realmente necesita

## Por qué cada servicio tiene su propia base de datos
Para que un problema en una base no afecte a las demás y cada servicio pueda evolucionar sin dependerde los otros.
