# 🍽️ StockGourmet — Sistema de Gestión de Inventario para Restaurante & Pedidos de Compra

Sistema web integral desarrollado en **Django** (Frontend y Backend integrados) diseñado para la operación rápida de cocinas, almacenes y barras en restaurantes. Permite llevar el conteo de existencias, auditar inventarios a una fecha específica, calcular automáticamente las necesidades de reposición según cantidades mínimas, consolidar conteos de múltiples áreas y generar reportes de compra listos para proveedores.

---

## 🚀 Inicio Rápido

### 1. Clonar e instalar
```bash
git clone https://github.com/Checka123/stockinve.git
cd stockinve
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Iniciar el servidor de desarrollo
```bash
python manage.py migrate
python manage.py runserver
```
Accede desde tu navegador en: **`http://127.0.0.1:8000/`**

La base de datos SQLite se crea en local con `migrate` y no se sube al repositorio.

### 3. Credenciales de Acceso
Crea el primer usuario administrador:
```bash
python manage.py createsuperuser
```
En una instalación local de ejemplo puedes usar **usuario** `admin` y **contraseña** `admin123`.

### 4. Cargar datos de ejemplo de restaurante
```bash
python manage.py seed_data
```

---

## ✨ Funcionalidades Implementadas

### 1. Catálogo de Insumos con Secuencia / Ordinal Personalizado
- **Secuencia u Ordinal (`sequence_number`):** Cada producto tiene asignado un número de orden (ej. 10, 20, 30...) para controlar exactamente el orden en que se visualiza en las hojas de conteo, reportes impresos y solicitudes de compra.
- **Datos esenciales:** El nombre y la secuencia son los datos principales del producto; se pueden asignar una o varias secciones. Los demás datos del catálogo son opcionales.
- **Moneda:** Los costos y presupuestos se muestran en quetzales guatemaltecos (Q).
- **Buscador en tiempo real:** Búsqueda instantánea por nombre, código SKU o ubicación (cámara fría, estantería, barra).
- **Cantidades mínimas e ideales:** Alerta visual de stock bajo mínimo (amarillo) y agotado (rojo).
- **Unidades de medida gastronómicas:** Kilogramos, gramos, litros, piezas, paquetes, botellas, latas, etc.

### 2. Registro de Inventario a la Fecha ("Toma de Inventario")
- **Visualización corregida de conteos:** Las casillas numéricas muestran siempre los valores contados previamente con formato estándar de punto decimal (`unlocalize`), evitando que el navegador las oculte.
- **Ubicación o Área Específica:** Cada toma permite definir su área (ej: *Bodega Central*, *Barra Principal*, *Cocina Caliente*).
- **Cálculo automático en vivo de "Cantidad a Pedir":** Al teclear lo contado, calcula automáticamente el faltante contra el stock mínimo o ideal.
- **Edición rápida:** Botones `+` / `-` y campo numérico para ajustes inmediatos.
- **Borrador y Finalización:** Guardar progreso sin alterar el stock o finalizar para actualizar el inventario real.

### 3. Bloqueo y Desbloqueo de Pedidos de Compra
- Los pedidos de compra emitidos cuentan con botón de **Bloquear / Desbloquear**.
- Un pedido **Bloqueado (🔒)** no puede ser modificado accidentalmente ni cambiar de estado hasta que un usuario autorizado lo desbloquee.
- Registro de auditoría de quién bloqueó la orden y en qué fecha/hora.

### 4. Reporte General Diario Consolidado (Multi-Área)
- **El problema en restaurantes:** Un mismo insumo existe en distintas áreas (ej: 5 botellas en Bodega, 2 en Barra Principal y 1 en Cocina).
- **La solución:**
  - En la sección **`Consolidado Diario`** puedes seleccionar varias tomas de inventario (por fecha o manual con casillas de verificación).
  - El sistema unifica las existencias por producto, muestra el desglose por ubicación y suma el total neto contado.
  - Compara el total consolidado contra la cantidad mínima para calcular el faltante real y emite un pedido consolidado único por proveedor.

### 5. Reportes de Solicitud de Compra Listos para Enviar
- **Agrupación por Proveedor:** Separa los pedidos para carnicería, verdulería, vinos/cervezas, abarrotes, etc.
- **Botón "Copiar para WhatsApp":** Genera un mensaje formateado con viñetas listo para enviar al proveedor por WhatsApp.
- **Impresión / PDF:** Hoja formal de requisición con firmas de recepción.
- **Exportación a CSV / Excel.**

### 6. Sistema de Autenticación de Usuarios
- Protección de todas las vistas con `@login_required`.
- Pantalla de inicio de sesión estilizada y responsive.
- Identificador de usuario activo en la barra de navegación y botón seguro para cerrar sesión.

---

## 🧪 Pruebas Automatizadas
Para ejecutar las pruebas:
```bash
python manage.py test
```
