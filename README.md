# encargado tecnico: Ecommerce

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
