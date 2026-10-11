from django.db import migrations, models


def copy_categories_to_location(apps, schema_editor):
    Product = apps.get_model('stock', 'Product')
    for product in Product.objects.all():
        product.location.set(product.categories.all())


def copy_location_to_categories(apps, schema_editor):
    Product = apps.get_model('stock', 'Product')
    for product in Product.objects.all():
        product.categories.set(product.location.all())


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_stockcountsession_stockaudit_session'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='location',
            new_name='detalle_ubicacion',
        ),
        migrations.AlterField(
            model_name='product',
            name='detalle_ubicacion',
            field=models.CharField(blank=True, default='', max_length=120, verbose_name='Detalle de Ubicación (ej: Cámara 1, Repisa 3)'),
        ),
        migrations.AddField(
            model_name='product',
            name='group',
            field=models.CharField(blank=True, default='', max_length=120, verbose_name='Grupo'),
        ),
        migrations.AddField(
            model_name='product',
            name='presentation',
            field=models.CharField(blank=True, default='', max_length=120, verbose_name='Presentación'),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.CharField(
                blank=True,
                choices=[
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
                ],
                default='pza',
                max_length=20,
                verbose_name='Unidad de Medida',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='location',
            field=models.ManyToManyField(blank=True, to='stock.category', verbose_name='Ubicaciones / Áreas'),
        ),
        migrations.RunPython(copy_categories_to_location, copy_location_to_categories),
        migrations.RemoveField(
            model_name='product',
            name='categories',
        ),
        migrations.AlterField(
            model_name='product',
            name='location',
            field=models.ManyToManyField(blank=True, related_name='products', to='stock.category', verbose_name='Ubicaciones / Áreas'),
        ),
    ]
