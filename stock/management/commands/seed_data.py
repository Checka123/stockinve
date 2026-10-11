from decimal import Decimal
from django.core.management.base import BaseCommand
from stock.models import Category, Supplier, Product, StockMovement


class Command(BaseCommand):
    help = 'Puebla la base de datos con insumos, proveedores y áreas reales para un restaurante'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Inicializando datos de prueba para restaurante...'))

        # 1. Crear Categorías / Áreas
        categories_data = [
            {'name': 'Carnes & Aves', 'description': 'Cortes de res, cerdo, aves y derivados cárnicos', 'icon': 'beef'},
            {'name': 'Frutas & Verduras', 'description': 'Vegetales frescos de diario, tubérculos y hierbas', 'icon': 'carrot'},
            {'name': 'Lácteos & Huevos', 'description': 'Quesos, crema, mantequilla, leche y huevo fresco', 'icon': 'egg'},
            {'name': 'Abarrotes & Secos', 'description': 'Aceites, harinas, pastas, enlatados, arroces y condimentos', 'icon': 'package'},
            {'name': 'Bar & Bebidas', 'description': 'Licores, vinos, cervezas, refrescos, jarabes e insumos de coctelería', 'icon': 'wine'},
            {'name': 'Limpieza & Desechables', 'description': 'Servilletas, papel aluminio, químicos desinfectantes y bolsas', 'icon': 'sparkles'},
        ]

        cats = {}
        for cdata in categories_data:
            cat, _ = Category.objects.get_or_create(name=cdata['name'], defaults=cdata)
            cats[cdata['name']] = cat

        # 2. Crear Proveedores
        suppliers_data = [
            {
                'name': 'Carnes Selectas San José',
                'contact_name': 'Mario Hernández',
                'phone': '+502 5555 1234',
                'email': 'pedidos@carnesanjose.com',
                'address': 'Mercado de Abastos Local 42',
                'notes': 'Pedidos antes de las 18:00 hrs para entrega al día siguiente temprano.'
            },
            {
                'name': 'Distribuidora Agrícola La Huerta',
                'contact_name': 'Elena Morales',
                'phone': '+502 5555 2345',
                'email': 'ventas@lahuerta.com',
                'address': 'Bodega 14, Nave de Frutas',
                'notes': 'Entrega lunes, miércoles y viernes a las 7:00 AM.'
            },
            {
                'name': 'Quesos & Lácteos El Ranchito',
                'contact_name': 'Roberto Dávila',
                'phone': '+502 5555 3456',
                'email': 'contacto@elranchito.com',
                'address': 'Av. Industrial 500',
                'notes': 'Mozzarella y quesos madurados de calidad gourmet.'
            },
            {
                'name': 'Abarrotes & Especias La Colonial',
                'contact_name': 'Sara Fuentes',
                'phone': '+502 5555 4567',
                'email': 'pedidos@lacolonial.com',
                'address': 'Calle Comercio 88',
                'notes': 'Aceites en bidón, harinas 25kg, salsas y secos.'
            },
            {
                'name': 'Cava Real Licores & Vinos',
                'contact_name': 'David Soto',
                'phone': '+502 5555 5678',
                'email': 'distribucion@cavareal.com',
                'address': 'Zona Comercial Norte 12',
                'notes': 'Cervezas artesanales, destilados y vinos por caja.'
            },
        ]

        supps = {}
        for sdata in suppliers_data:
            supp, _ = Supplier.objects.get_or_create(name=sdata['name'], defaults=sdata)
            supps[sdata['name']] = supp

        # 3. Insumos típicos de Restaurante con cantidades mínimas
        products_data = [
            # Carnes
            {
                'name': 'Filete de Res Calidad Angus',
                'sku': 'CAR-001',
                'category': cats['Carnes & Aves'],
                'supplier': supps['Carnes Selectas San José'],
                'unit': 'kg',
                'current_stock': Decimal('4.50'),
                'min_stock': Decimal('10.00'), # BAJO MINIMO
                'ideal_stock': Decimal('18.00'),
                'cost_price': Decimal('320.00'),
                'detalle_ubicacion': 'Cámara Fría 1 (Carnes)',
            },
            {
                'name': 'Pechuga de Pollo Deshuesada',
                'sku': 'CAR-002',
                'category': cats['Carnes & Aves'],
                'supplier': supps['Carnes Selectas San José'],
                'unit': 'kg',
                'current_stock': Decimal('3.00'),
                'min_stock': Decimal('15.00'), # BAJO MINIMO CRITICO
                'ideal_stock': Decimal('25.00'),
                'cost_price': Decimal('115.00'),
                'detalle_ubicacion': 'Cámara Fría 1 (Carnes)',
            },
            {
                'name': 'Ribeye Corte 12oz',
                'sku': 'CAR-003',
                'category': cats['Carnes & Aves'],
                'supplier': supps['Carnes Selectas San José'],
                'unit': 'pza',
                'current_stock': Decimal('18.00'),
                'min_stock': Decimal('12.00'),
                'ideal_stock': Decimal('24.00'),
                'cost_price': Decimal('195.00'),
                'detalle_ubicacion': 'Cámara Fría 1',
            },
            # Frutas & Verduras
            {
                'name': 'Tomate Saladette Rojo',
                'sku': 'VER-001',
                'category': cats['Frutas & Verduras'],
                'supplier': supps['Distribuidora Agrícola La Huerta'],
                'unit': 'kg',
                'current_stock': Decimal('6.00'),
                'min_stock': Decimal('15.00'), # BAJO MINIMO
                'ideal_stock': Decimal('30.00'),
                'cost_price': Decimal('28.50'),
                'detalle_ubicacion': 'Cámara 2 (Vegetales)',
            },
            {
                'name': 'Cebolla Blanca',
                'sku': 'VER-002',
                'category': cats['Frutas & Verduras'],
                'supplier': supps['Distribuidora Agrícola La Huerta'],
                'unit': 'kg',
                'current_stock': Decimal('12.00'),
                'min_stock': Decimal('10.00'),
                'ideal_stock': Decimal('25.00'),
                'cost_price': Decimal('22.00'),
                'detalle_ubicacion': 'Estantería Verduras',
            },
            {
                'name': 'Limón Persa sin Semilla',
                'sku': 'VER-003',
                'category': cats['Frutas & Verduras'],
                'supplier': supps['Distribuidora Agrícola La Huerta'],
                'unit': 'kg',
                'current_stock': Decimal('2.00'),
                'min_stock': Decimal('12.00'), # CRITICO
                'ideal_stock': Decimal('20.00'),
                'cost_price': Decimal('35.00'),
                'detalle_ubicacion': 'Cámara 2 / Barra',
            },
            {
                'name': 'Aguacate Hass de Primera',
                'sku': 'VER-004',
                'category': cats['Frutas & Verduras'],
                'supplier': supps['Distribuidora Agrícola La Huerta'],
                'unit': 'kg',
                'current_stock': Decimal('8.00'),
                'min_stock': Decimal('8.00'), # AL LIMITE
                'ideal_stock': Decimal('16.00'),
                'cost_price': Decimal('65.00'),
                'detalle_ubicacion': 'Cámara 2',
            },
            # Lácteos
            {
                'name': 'Queso Mozzarella Rayado',
                'sku': 'LAC-001',
                'category': cats['Lácteos & Huevos'],
                'supplier': supps['Quesos & Lácteos El Ranchito'],
                'unit': 'kg',
                'current_stock': Decimal('4.00'),
                'min_stock': Decimal('12.00'), # BAJO MINIMO
                'ideal_stock': Decimal('20.00'),
                'cost_price': Decimal('145.00'),
                'detalle_ubicacion': 'Cámara 1 (Lácteos)',
            },
            {
                'name': 'Huevo Fresco Limpio (Cono 30 pzas)',
                'sku': 'LAC-002',
                'category': cats['Lácteos & Huevos'],
                'supplier': supps['Quesos & Lácteos El Ranchito'],
                'unit': 'paquete',
                'current_stock': Decimal('5.00'),
                'min_stock': Decimal('4.00'),
                'ideal_stock': Decimal('10.00'),
                'cost_price': Decimal('92.00'),
                'detalle_ubicacion': 'Almacén Seco Cocina',
            },
            {
                'name': 'Mantequilla sin Sal Gourmet',
                'sku': 'LAC-003',
                'category': cats['Lácteos & Huevos'],
                'supplier': supps['Quesos & Lácteos El Ranchito'],
                'unit': 'kg',
                'current_stock': Decimal('3.50'),
                'min_stock': Decimal('5.00'),
                'ideal_stock': Decimal('8.00'),
                'cost_price': Decimal('180.00'),
                'detalle_ubicacion': 'Cámara 1',
            },
            # Abarrotes & Secos
            {
                'name': 'Aceite de Oliva Extra Virgen (Bidón 5L)',
                'sku': 'ABA-001',
                'category': cats['Abarrotes & Secos'],
                'supplier': supps['Abarrotes & Especias La Colonial'],
                'unit': 'l',
                'current_stock': Decimal('4.00'),
                'min_stock': Decimal('10.00'), # BAJO MINIMO
                'ideal_stock': Decimal('20.00'),
                'cost_price': Decimal('210.00'),
                'detalle_ubicacion': 'Bodega de Secos Estante 1',
            },
            {
                'name': 'Harina de Trigo Extra Fina',
                'sku': 'ABA-002',
                'category': cats['Abarrotes & Secos'],
                'supplier': supps['Abarrotes & Especias La Colonial'],
                'unit': 'kg',
                'current_stock': Decimal('35.00'),
                'min_stock': Decimal('20.00'),
                'ideal_stock': Decimal('50.00'),
                'cost_price': Decimal('24.00'),
                'detalle_ubicacion': 'Tarima Secos',
            },
            {
                'name': 'Pasta Italiana Penne Rigate',
                'sku': 'ABA-003',
                'category': cats['Abarrotes & Secos'],
                'supplier': supps['Abarrotes & Especias La Colonial'],
                'unit': 'kg',
                'current_stock': Decimal('15.00'),
                'min_stock': Decimal('10.00'),
                'ideal_stock': Decimal('25.00'),
                'cost_price': Decimal('48.00'),
                'detalle_ubicacion': 'Bodega de Secos Estante 2',
            },
            # Bar & Bebidas
            {
                'name': 'Tequila Don Julio Reposado 750ml',
                'sku': 'BEB-001',
                'category': cats['Bar & Bebidas'],
                'supplier': supps['Cava Real Licores & Vinos'],
                'unit': 'botella',
                'current_stock': Decimal('2.00'),
                'min_stock': Decimal('6.00'), # BAJO MINIMO
                'ideal_stock': Decimal('12.00'),
                'cost_price': Decimal('890.00'),
                'detalle_ubicacion': 'Barra Principal / Almacén Licores',
            },
            {
                'name': 'Cerveza Modelo Especial 355ml',
                'sku': 'BEB-002',
                'category': cats['Bar & Bebidas'],
                'supplier': supps['Cava Real Licores & Vinos'],
                'unit': 'botella',
                'current_stock': Decimal('48.00'),
                'min_stock': Decimal('72.00'), # BAJO MINIMO
                'ideal_stock': Decimal('144.00'),
                'cost_price': Decimal('21.50'),
                'detalle_ubicacion': 'Cámara de Cervezas Barra',
            },
            {
                'name': 'Vino Tinto Malbec Reserva 750ml',
                'sku': 'BEB-003',
                'category': cats['Bar & Bebidas'],
                'supplier': supps['Cava Real Licores & Vinos'],
                'unit': 'botella',
                'current_stock': Decimal('8.00'),
                'min_stock': Decimal('6.00'),
                'ideal_stock': Decimal('18.00'),
                'cost_price': Decimal('240.00'),
                'detalle_ubicacion': 'Cava de Vinos',
            },
            {
                'name': 'Agua Mineral Topo Chico 600ml',
                'sku': 'BEB-004',
                'category': cats['Bar & Bebidas'],
                'supplier': supps['Cava Real Licores & Vinos'],
                'unit': 'botella',
                'current_stock': Decimal('10.00'),
                'min_stock': Decimal('24.00'), # BAJO MINIMO
                'ideal_stock': Decimal('48.00'),
                'cost_price': Decimal('16.00'),
                'detalle_ubicacion': 'Cámara Barra',
            },
        ]

        created_prods = 0
        seq = 10
        for pdata in products_data:
            section = pdata.pop('category')
            pdata['sequence_number'] = seq
            seq += 10
            p, created = Product.objects.get_or_create(
                sku=pdata['sku'],
                defaults={**pdata, 'category': section},
            )
            p.location.add(section)
            if not created and p.sequence_number == 100:
                p.sequence_number = pdata['sequence_number']
                p.save(update_fields=['sequence_number'])
            elif created:
                created_prods += 1
                StockMovement.objects.create(
                    product=p,
                    movement_type='entry',
                    quantity=p.current_stock,
                    previous_stock=Decimal('0.00'),
                    new_stock=p.current_stock,
                    reference='Carga inicial de inventario'
                )

        self.stdout.write(self.style.SUCCESS(
            f'¡Carga completada exitosamente! {len(categories_data)} Áreas, {len(suppliers_data)} Proveedores, {created_prods} Productos creados.'
        ))
