from django.core.management.base import BaseCommand, CommandError

from stock.importer import import_products_from_workbook


class Command(BaseCommand):
    help = 'Importa o actualiza productos desde un archivo Excel (.xlsx).'

    def add_arguments(self, parser):
        parser.add_argument('path', help='Ruta al archivo .xlsx a importar.')
        parser.add_argument(
            '--no-update',
            action='store_true',
            help='No modifica productos existentes; solo crea los nuevos.',
        )

    def handle(self, *args, **options):
        path = options['path']
        try:
            with open(path, 'rb') as handle:
                summary = import_products_from_workbook(
                    handle, update_existing=not options['no_update']
                )
        except FileNotFoundError:
            raise CommandError(f'No se encontró el archivo: {path}')
        except Exception as exc:  # noqa: BLE001
            raise CommandError(f'No se pudo procesar el archivo: {exc}')

        self.stdout.write(self.style.SUCCESS(
            f"Filas procesadas: {summary['total']} | "
            f"Creados: {summary['created']} | "
            f"Actualizados: {summary['updated']} | "
            f"Omitidos: {summary['skipped']} | "
            f"Áreas nuevas: {summary['areas_created']}"
        ))
        for error in summary['errors']:
            self.stdout.write(self.style.WARNING(error))
