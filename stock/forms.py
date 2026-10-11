from django import forms
from .models import Product, StockAudit, StockAuditItem, StockCountSession, Supplier, Category, PurchaseOrder, StockMovement


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'sku', 'sequence_number', 'group', 'presentation', 'location', 'supplier', 'unit',
            'current_stock', 'min_stock', 'ideal_stock', 'cost_price',
            'detalle_ubicacion', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Pechuga de Pollo Deshuesada'}),
            'sku': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. POL-001'}),
            'sequence_number': forms.NumberInput(attrs={'class': 'form-input', 'min': '1', 'placeholder': 'Ej. 10'}),
            'group': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Carnes, Abarrotes, Bebidas'}),
            'presentation': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Bolsa 500g, Botella 750ml'}),
            'location': forms.CheckboxSelectMultiple(attrs={
                'class': 'h-4 w-4 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500',
            }),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'current_stock': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'min_stock': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'ideal_stock': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'detalle_ubicacion': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Cámara de Congelados / Repisa 2'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def save(self, commit=True):
        product = super().save(commit=False)
        product.category = None
        if commit:
            product.save()
            self.save_m2m()
        return product


class StockCountSessionForm(forms.ModelForm):
    areas = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'h-4 w-4 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500',
        }),
        required=True,
        label="Áreas / Ubicaciones a incluir en el conteo",
        help_text="Marca todas las áreas que quieras contar (puedes dejar algunas pendientes).",
    )

    class Meta:
        model = StockCountSession
        fields = ['title', 'count_date', 'responsible', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej. Conteo General de Cierre - Viernes'
            }),
            'count_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'responsible': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej. Chef Mario / Encargado de Barra'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Comentarios, turno (mañana/noche), observaciones...'
            }),
        }


class StockAuditForm(forms.ModelForm):
    class Meta:
        model = StockAudit
        fields = ['title', 'audit_date', 'location_area', 'responsible', 'category', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej. Conteo Diario de Cocina - Viernes'
            }),
            'audit_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'location_area': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej. Bodega Central, Barra Principal, Cocina Caliente'
            }),
            'responsible': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej. Chef Mario / Encargado de Barra'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Comentarios, turno (mañana/noche), observaciones...'
            }),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_name', 'phone', 'email', 'address', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Distribuidora Avícola San Juan'}),
            'contact_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Carlos Gómez'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. +502 5555 1234 (WhatsApp)'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'pedidos@proveedor.com'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Dirección física / Mercado'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Horarios de pedido, días de entrega...'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Carnes y Proteínas'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Descripción del área'}),
            'icon': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'package, utensils, wine, etc.'}),
        }


class QuickAdjustmentForm(forms.Form):
    MOVEMENT_TYPES = [
        ('waste', 'Merma / Desperdicio / Caducidad'),
        ('entry', 'Entrada de Mercadería'),
        ('adjustment', 'Ajuste Manual'),
    ]

    movement_type = forms.ChoiceField(
        choices=MOVEMENT_TYPES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Tipo de Movimiento"
    )
    quantity = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
        label="Cantidad"
    )
    reference = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Motivo: Ej. Caducidad, Producto dañado, Donación'}),
        label="Referencia / Motivo"
    )
