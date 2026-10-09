-- Pedidos/init.sql
CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idUsuario INT NOT NULL,
    idProducto INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    estado VARCHAR(50) NOT NULL DEFAULT 'Pendiente',
    valortotal DECIMAL(10, 2) NOT NULL,
    fechaPedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO pedidos (idUsuario, idProducto, cantidad, estado, valortotal) VALUES
(1, 101, 2, 'Completado', 150.00),
(1, 103, 1, 'Pendiente', 45.50),
(2, 102, 3, 'Enviado', 89.97);