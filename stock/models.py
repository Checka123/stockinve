from decimal import Decimal

from django.db import models
from django.db.models import F, IntegerField, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.utils import timezone


UNIT_CHOICES = [
    ('kg', 'Kilogramos (kg)'),
    ('g', 'Gramos (g)'),
    ('l', 'Litros (L)'),
    ('ml', 'Mililitros (ml)'),
    ('pza', 'Piezas / Unidades (pza)'),
    ('unidad', 'Unidades (unidad)'),
    ('paquete', 'Paquetes (paq)'),
    ('caja', 'Cajas (cja)'),
    ('botella', 'Botellas (bot)'),
    ('lata', 'Latas (lata)'),
    ('porcion', 'Porciones (porc)'),
]


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Área / Categoría")
    description = models.TextField(blank=True, verbose_name="Descripción")
    icon = models.CharField(max_length=50, default="package", blank=True, help_text="Nombre de icono lucide")

    class Meta:
        verbose_name = "Categoría / Área"
        verbose_name_plural = "Categorías / Áreas"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def product_count(self):
        return self.products.filter(is_active=True).count()


class Supplier(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Nombre del Proveedor / Empresa")
    contact_name = models.CharField(max_length=100, blank=True, verbose_name="Contacto")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Teléfono / WhatsApp")
    email = models.EmailField(blank=True, verbose_name="Correo Electrónico")
    address = models.CharField(max_length=250, blank=True, verbose_name="Dirección")
    notes = models.TextField(blank=True, verbose_name="Notas / Días de entrega")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=180, verbose_name="Nombre del Producto")
    sequence_number = models.PositiveIntegerField(default=10, verbose_name="Secuencia / Ordinal", help_text="Orden de aparición en listas y reportes (ej. 1, 2, 3...)")
    location = models.ManyToManyField(Category, blank=True, related_name='products', verbose_name="Ubicaciones / Áreas")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='single_products', verbose_name="Sección Principal")
    
    group = models.CharField(max_length=120, blank=True, default='', verbose_name="Grupo")
    presentation = models.CharField(max_length=120, blank=True, default='', verbose_name="Presentación")
    sku = models.CharField(max_length=60, blank=True, default='', verbose_name="Código / SKU")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="Proveedor Principal")
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='pza', blank=True, verbose_name="Unidad de Medida")
    
    current_stock = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), null=True, blank=True, verbose_name="Stock Actual")
    min_stock = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), null=True, blank=True, verbose_name="Cantidad Mínima")
    ideal_stock = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), null=True, blank=True, verbose_name="Cantidad Ideal / Objetivo")
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), null=True, blank=True, verbose_name="Precio Costo Estimado (Q)")
    
    detalle_ubicacion = models.CharField(max_length=120, blank=True, default='', verbose_name="Detalle de Ubicación (ej: Cámara 1, Repisa 3)")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['sequence_number', 'name']

    def __str__(self):
        unit_str = self.get_unit_display() if self.unit else "pza"
        return f"#{self.sequence_number} {self.name} ({unit_str})"

    @property
    def locations_display(self):
        locations = list(self.location.all())
        if self.category and self.category not in locations:
            locations.append(self.category)
        return ", ".join(location.name for location in locations) or "Sin ubicación"

    @property
    def is_out_of_stock(self):
        return self.current_stock is not None and self.current_stock <= 0

    @property
    def is_below_minimum(self):
        if self.current_stock is None or self.min_stock is None:
            return False
        return self.current_stock <= self.min_stock

    @property
    def suggested_reorder_qty(self):
        """
        Calcula la cantidad a pedir sugerida.
        Si tiene stock ideal configurado, busca llenar hasta el stock ideal.
        Si no, busca reponer hasta el stock mínimo.
        """
        if self.current_stock is None:
            return Decimal('0.00')
        c_stock = self.current_stock
        i_stock = self.ideal_stock or Decimal('0.00')
        m_stock = self.min_stock or Decimal('0.00')
        target = i_stock if i_stock > 0 else m_stock
        diff = target - c_stock
        return max(Decimal('0.00'), diff)

    @property
    def stock_status(self):
        if self.current_stock is None:
            return {'code': 'unknown', 'label': 'Sin stock definido', 'color': 'slate'}
        c_stock = self.current_stock
        if c_stock <= 0:
            return {'code': 'out', 'label': 'Agotado', 'color': 'red'}
        if self.min_stock is None:
            return {'code': 'unknown', 'label': 'Mínimo sin definir', 'color': 'slate'}
        m_stock = self.min_stock or Decimal('0.00')
        i_stock = self.ideal_stock or Decimal('0.00')
        if c_stock <= m_stock:
            return {'code': 'critical', 'label': 'Bajo Mínimo', 'color': 'amber'}
        elif i_stock > 0 and c_stock < i_stock:
            return {'code': 'regular', 'label': 'Aceptable', 'color': 'blue'}
        else:
            return {'code': 'good', 'label': 'Óptimo', 'color': 'emerald'}


class ProductAreaSequence(models.Model):
    """Orden del producto dentro de un área. No pisa el orden de las demás áreas."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='area_sequences')
    area = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_sequences')
    sequence_number = models.PositiveIntegerField(default=10, verbose_name="Orden en el área")

    class Meta:
        verbose_name = "Orden por área"
        verbose_name_plural = "Órdenes por área"
        unique_together = ('product', 'area')
        ordering = ['sequence_number', 'product__name']

    def __str__(self):
        return f"{self.area.name}: #{self.sequence_number} {self.product.name}"


def order_queryset_by_area(qs, area, product_id_field='product_id', name_field='product__name'):
    """Ordena por la secuencia del área y, si no hay, por la secuencia general del producto."""
    if area is None:
        fallback_name = 'sequence_number' if product_id_field == 'pk' else 'product__sequence_number'
        return qs.order_by(fallback_name, name_field)
    area_seq = ProductAreaSequence.objects.filter(
        product_id=OuterRef(product_id_field),
        area_id=area.pk,
    ).values('sequence_number')[:1]
    fallback = F('sequence_number') if product_id_field == 'pk' else F('product__sequence_number')
    return qs.annotate(
        area_sequence=Coalesce(
            Subquery(area_seq, output_field=IntegerField()),
            fallback,
            output_field=IntegerField(),
        )
    ).order_by('area_sequence', name_field)


def sequences_for_area(area, product_ids):
    if area is None or not product_ids:
        return {}
    return dict(
        ProductAreaSequence.objects.filter(area=area, product_id__in=product_ids)
        .values_list('product_id', 'sequence_number')
    )


class StockCountSession(models.Model):
    """
    Registro de conteo de stock de una fecha determinada.
    Agrupa varios conteos por área/ubicación (Categoría) para poder contarlos
    uno por uno, dejar áreas pendientes y al finalizar generar un consolidado
    general o reportes independientes por área.
    """
    STATUS_CHOICES = [
        ('draft', 'En Proceso (Borrador)'),
        ('completed', 'Consolidado y Aplicado'),
    ]

    count_date = models.DateField(default=timezone.now, verbose_name="Fecha del Conteo")
    title = models.CharField(max_length=200, verbose_name="Título / Descripción del Conteo", help_text="Ej: Conteo de Cierre de Semana, Inventario General")
    responsible = models.CharField(max_length=120, blank=True, verbose_name="Responsable del Conteo", help_text="Chef, Barman o Administrador")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Estado")
    notes = models.TextField(blank=True, verbose_name="Observaciones Generales")
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Finalización")

    class Meta:
        verbose_name = "Registro de Conteo de Stock"
        verbose_name_plural = "Registros de Conteo de Stock"
        ordering = ['-count_date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.count_date.strftime('%d/%m/%Y')} ({self.get_status_display()})"

    @property
    def total_areas(self):
        return self.audits.count()

    @property
    def completed_areas(self):
        return self.audits.filter(status='completed').count()

    @property
    def pending_areas(self):
        return self.audits.filter(status='draft').count()

    @property
    def progress_percent(self):
        total = self.total_areas
        if not total:
            return 0
        return int((self.completed_areas / total) * 100)

    @property
    def total_counted_products(self):
        return StockAuditItem.objects.filter(audit__session=self, counted_stock__isnull=False).count()

    @property
    def audit_ids_csv(self):
        cached = getattr(self, '_prefetched_objects_cache', {}).get('audits')
        if cached is not None:
            return ",".join(str(audit.id) for audit in cached)
        return ",".join(str(audit_id) for audit_id in self.audits.values_list('id', flat=True))

    def apply_consolidated_to_inventory(self):
        """
        Consolida los conteos de todas las áreas (sumando cantidades del mismo
        producto contadas en distintas ubicaciones), aplica el stock resultante
        al inventario real y genera los movimientos de auditoría.
        """
        if self.status == 'completed':
            return False

        totals = {}
        counted_items = StockAuditItem.objects.filter(
            audit__session=self,
            counted_stock__isnull=False
        ).select_related('product')
        for item in counted_items:
            totals.setdefault(item.product_id, Decimal('0.00'))
            totals[item.product_id] += item.counted_stock

        for product_id, new_stock in totals.items():
            product = Product.objects.get(pk=product_id)
            prev_stock = product.current_stock or Decimal('0.00')
            product.current_stock = new_stock
            product.save(update_fields=['current_stock', 'updated_at'])
            StockMovement.objects.create(
                product=product,
                movement_type='audit',
                quantity=new_stock - prev_stock,
                previous_stock=prev_stock,
                new_stock=new_stock,
                reference=f"Conteo de Stock: {self.title} ({self.count_date}) - Consolidado"
            )

        now = timezone.now()
        counted_audit_ids = counted_items.values_list('audit_id', flat=True).distinct()
        self.audits.filter(id__in=list(counted_audit_ids)).update(status='completed', completed_at=now)

        self.status = 'completed'
        self.completed_at = now
        self.save()
        return True


class StockAudit(models.Model):
    STATUS_CHOICES = [
        ('draft', 'En Proceso (Borrador)'),
        ('completed', 'Completado y Actualizado'),
    ]

    session = models.ForeignKey('StockCountSession', on_delete=models.CASCADE, null=True, blank=True, related_name='audits', verbose_name="Registro de Conteo (Sesión)")
    audit_date = models.DateField(default=timezone.now, verbose_name="Fecha del Conteo")
    title = models.CharField(max_length=200, verbose_name="Título / Descripción de la Toma", help_text="Ej: Conteo de Cierre de Semana, Auditoría de Barra")
    location_area = models.CharField(max_length=120, blank=True, verbose_name="Ubicación / Área de Conteo", help_text="Ej: Bodega Central, Barra Principal, Cocina Caliente")
    responsible = models.CharField(max_length=120, blank=True, verbose_name="Responsable del Conteo", help_text="Chef, Barman o Administrador")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Filtrar por Área / Categoría (Opcional)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Estado")
    notes = models.TextField(blank=True, verbose_name="Observaciones Generales")
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Finalización")

    class Meta:
        verbose_name = "Registro de Inventario a la Fecha"
        verbose_name_plural = "Registros de Inventario a la Fecha"
        ordering = ['-audit_date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.audit_date.strftime('%d/%m/%Y')} ({self.get_status_display()})"

    @property
    def total_products_in_audit(self):
        return self.items.count()

    @property
    def total_counted_products(self):
        return self.items.filter(counted_stock__isnull=False).count()

    @property
    def items_to_order_count(self):
        return self.items.filter(final_order__gt=0).count()

    @property
    def estimated_order_total(self):
        total = Decimal('0.00')
        for item in self.items.filter(final_order__gt=0).select_related('product'):
            total += item.final_order * (item.product.cost_price or Decimal('0.00'))
        return total

    def apply_counts_to_inventory(self):
        """
        Aplica los conteos registrados al inventario real de productos
        y genera los registros de movimiento correspondientes.
        """
        if self.status == 'completed':
            return False

        for item in self.items.all():
            if item.counted_stock is not None:
                product = item.product
                prev_stock = product.current_stock or Decimal('0.00')
                new_stock = item.counted_stock
                diff = new_stock - prev_stock

                # Actualizar stock del producto
                product.current_stock = new_stock
                product.save(update_fields=['current_stock', 'updated_at'])

                # Registrar movimiento de auditoría
                StockMovement.objects.create(
                    product=product,
                    movement_type='audit',
                    quantity=diff,
                    previous_stock=prev_stock,
                    new_stock=new_stock,
                    reference=f"Toma de Inventario: {self.title} ({self.audit_date})"
                )

        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
        return True

    def mark_area_complete(self):
        """Cierra el conteo de un área de la sesión sin aplicar stock todavía."""
        if self.status != 'completed':
            self.status = 'completed'
            self.completed_at = timezone.now()
            self.save(update_fields=['status', 'completed_at'])

    def reopen_area(self):
        """Reabre un área ya finalizada para seguir contando (solo si la sesión sigue en proceso)."""
        if self.status != 'draft':
            self.status = 'draft'
            self.completed_at = None
            self.save(update_fields=['status', 'completed_at'])


class StockAuditItem(models.Model):
    audit = models.ForeignKey(StockAudit, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='audit_items')
    
    # Snapshot histórico de los valores al momento del conteo
    previous_stock = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name="Stock Registrado en Sistema")
    min_stock = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name="Stock Mínimo")
    ideal_stock = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name="Stock Ideal")
    
    # Conteo real y sugerencia
    counted_stock = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Cantidad Contada a la Fecha")
    suggested_order = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name="Cantidad a Pedir (Sugerida)")
    final_order = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name="Cantidad a Pedir (Final)")
    
    notes = models.CharField(max_length=255, blank=True, verbose_name="Notas del Producto")

    class Meta:
        verbose_name = "Detalle de Conteo"
        verbose_name_plural = "Detalles de Conteo"
        unique_together = ('audit', 'product')
        ordering = ['product__sequence_number', 'product__name']

    def __str__(self):
        return f"{self.product.name} en {self.audit.title}"

    @property
    def difference(self):
        if self.counted_stock is not None:
            return self.counted_stock - self.previous_stock
        return Decimal('0.00')

    @property
    def is_below_min_after_count(self):
        if self.counted_stock is not None:
            return self.counted_stock <= self.min_stock
        return False

    @property
    def subtotal_cost(self):
        return self.final_order * (self.product.cost_price or Decimal('0.00'))


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente de Envío'),
        ('sent', 'Enviado a Proveedor'),
        ('received', 'Recibido en Cocina'),
        ('cancelled', 'Cancelado'),
    ]

    code = models.CharField(max_length=50, unique=True, verbose_name="Número de Solicitud / Pedido")
    audit = models.ForeignKey(StockAudit, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_orders', verbose_name="Toma de Inventario de Origen")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_orders', verbose_name="Proveedor")
    date = models.DateField(default=timezone.now, verbose_name="Fecha del Pedido")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Estado")
    responsible = models.CharField(max_length=120, blank=True, verbose_name="Solicitado Por")
    notes = models.TextField(blank=True, verbose_name="Instrucciones para el Proveedor / Notas")
    
    is_locked = models.BooleanField(default=False, verbose_name="Bloqueado contra modificaciones")
    locked_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Bloqueo")
    locked_by = models.CharField(max_length=120, blank=True, verbose_name="Bloqueado Por")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Solicitud / Pedido de Compra"
        verbose_name_plural = "Solicitudes / Pedidos de Compra"
        ordering = ['-date', '-created_at']

    def __str__(self):
        supp_name = self.supplier.name if self.supplier else "Varios Proveedores"
        return f"{self.code} - {supp_name} ({self.date.strftime('%d/%m/%Y')})"

    @property
    def total_cost(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        return self.items.count()


class PurchaseOrderItem(models.Model):
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Cantidad Solicitada")
    unit = models.CharField(max_length=20, verbose_name="Unidad")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name="Precio Estimado")
    notes = models.CharField(max_length=255, blank=True, verbose_name="Nota específica")

    class Meta:
        verbose_name = "Ítem de Solicitud"
        verbose_name_plural = "Ítems de Solicitud"

    def __str__(self):
        return f"{self.quantity} {self.unit} de {self.product.name}"

    @property
    def subtotal(self):
        return self.quantity * self.unit_price


class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('audit', 'Ajuste por Conteo de Inventario'),
        ('entry', 'Entrada de Mercadería / Compra'),
        ('waste', 'Merma / Desperdicio / Caducidad'),
        ('manual', 'Ajuste Manual'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES, verbose_name="Tipo de Movimiento")
    quantity = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Cantidad (Diferencia)")
    previous_stock = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Stock Previo")
    new_stock = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Nuevo Stock")
    reference = models.CharField(max_length=200, blank=True, verbose_name="Referencia / Motivo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")

    class Meta:
        verbose_name = "Movimiento de Stock"
        verbose_name_plural = "Movimientos de Stock"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity:+})"


class AppSettings(models.Model):
    """Una sola fila con las opciones generales de la aplicación."""
    hide_previous_field = models.BooleanField(
        default=False,
        verbose_name="Ocultar el campo Previo",
    )
    hide_minimum_field = models.BooleanField(
        default=False,
        verbose_name="Ocultar el campo Mínimo",
    )

    class Meta:
        verbose_name = "Configuración general"
        verbose_name_plural = "Configuración general"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return

    @classmethod
    def load(cls):
        settings_row, _created = cls.objects.get_or_create(pk=1)
        return settings_row

    def __str__(self):
        return "Configuración general"
