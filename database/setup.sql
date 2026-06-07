-- ============================================================
--  Script de inicialización – Base de Datos Turismo RD
--  Ejecutar: mysql -u root -p < database/setup.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS turismo_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE turismo_db;

-- ── Tabla: ofertas ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ofertas (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    titulo              VARCHAR(200)    NOT NULL,
    descripcion         TEXT            NOT NULL,
    destino             VARCHAR(150)    NOT NULL,
    precio              DECIMAL(10,2)   NOT NULL,
    duracion_dias       INT             NOT NULL,
    imagen_url          VARCHAR(500),
    itinerario          TEXT,
    incluye             TEXT,
    cupos_disponibles   INT             DEFAULT 20,
    creado_en           DATETIME        DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_destino   (destino),
    INDEX idx_precio    (precio)
) ENGINE=InnoDB;

-- ── Tabla: reservas ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS reservas (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    oferta_id           INT             NOT NULL,
    nombre_cliente      VARCHAR(200)    NOT NULL,
    email_cliente       VARCHAR(200)    NOT NULL,
    telefono_cliente    VARCHAR(30),
    cantidad_personas   INT             DEFAULT 1,
    fecha_viaje         VARCHAR(20)     NOT NULL,
    metodo_pago         VARCHAR(50)     NOT NULL,
    estado              VARCHAR(30)     DEFAULT 'pendiente',
    notas               TEXT,
    creado_en           DATETIME        DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (oferta_id) REFERENCES ofertas(id) ON DELETE RESTRICT,
    INDEX idx_email     (email_cliente),
    INDEX idx_estado    (estado)
) ENGINE=InnoDB;

-- ── Datos de ejemplo ─────────────────────────────────────────
INSERT INTO ofertas (titulo, descripcion, destino, precio, duracion_dias, imagen_url, itinerario, incluye, cupos_disponibles)
VALUES
(
    'Playa Bávaro Todo Incluido',
    'Disfruta 5 días en el paraíso caribeño con todo incluido. Playas de arena blanca, aguas cristalinas y entretenimiento de primera.',
    'Punta Cana, República Dominicana',
    850.00, 5,
    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
    'Día 1: Llegada y check-in | Día 2: Playa y actividades acuáticas | Día 3: Excursión a Isla Saona | Día 4: Spa y relax | Día 5: Salida',
    'Vuelo, hotel 5★, comidas, bebidas, traslados, seguro de viaje',
    15
),
(
    'Aventura en Los Haitises',
    'Explora el Parque Nacional Los Haitises: manglares, cuevas taínas y fauna exótica en una expedición de 3 días inolvidable.',
    'Samaná, República Dominicana',
    320.00, 3,
    'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800',
    'Día 1: Traslado a Samaná | Día 2: Tour en bote por Los Haitises | Día 3: Avistamiento de ballenas y regreso',
    'Transporte, guía local, alojamiento, desayunos, equipo de snorkel',
    20
),
(
    'Ciudad Colonial & Gastronomía',
    'Descubre la primera ciudad europea del Nuevo Mundo. Recorrido cultural, historia viva y los mejores sabores dominicanos.',
    'Santo Domingo, República Dominicana',
    180.00, 2,
    'https://images.unsplash.com/photo-1519677100203-a0e668c92439?w=800',
    'Día 1: Zona Colonial, Catedral, Alcázar de Colón, cena típica | Día 2: Museo del Hombre Dominicano, mercado artesanal',
    'Guía certificado, entradas a museos, transporte, almuerzo típico',
    25
),
(
    'Las Terrenas Beach & Surf',
    'Semana de surf y relajación en las mejores playas de la Península de Samaná.',
    'Las Terrenas, Samaná',
    620.00, 7,
    'https://images.unsplash.com/photo-1502680390469-be75c86b636f?w=800',
    'Días 1-2: Llegada y clases básicas | Días 3-5: Práctica intensiva | Días 6-7: Surf libre y cierre',
    'Alojamiento frente al mar, clases de surf, tablas, desayunos y cenas',
    10
);

SELECT 'Base de datos turismo_db inicializada correctamente ✓' AS resultado;
