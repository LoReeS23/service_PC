from service_app.models import MotherBoard, Processor, GraphicCard, Memory, Disc, PowerSupply, Case, PC, \
    MOTHERBOARD_SIZES, MEMORY_TYPES, SOCKET_CHOICES, GRAPHIC_CARD_SLOT_TYPE, GRAPHIC_CARD_MEMORY_TYPE, DISC_TYPES, \
    DISC_FORMAT_TYPES, CASE_FORMAT_TYPES
from game.utils import fake_motherboard
from django.core.management.base import BaseCommand
import random


def add_parts_to_shop():
    for new_motherboard in range(random.randint(0, 2)):
        motherboard = {
            'name': f'motherboard {new_motherboard}',
            'size': f'{MOTHERBOARD_SIZES[random.randint(0, 2)][0]}',
            'socket': f'{SOCKET_CHOICES[random.randint(0, 4)][0]}',
            'ram_slots': random.randint(2, 6),
            'memory_type': f'{MEMORY_TYPES[random.randint(0, 4)][0]}',
            'memory_frequency_lowest': random.randint(2133, 3600),
            'memory_frequency_highest': random.randint(3601, 5000),
            'm2_disc_slots': random.randint(1, 3),
            'sata_disc_slots': random.randint(1, 4),
            'usb_amount': random.randint(2, 8),
            'PCI_slots': random.randint(1, 2),
            'PCI_express_slots': random.randint(1, 3),
            'has_RGB': random.choice((True, False)),
            'price': round(random.uniform(1, 250), 2)
        }
        MotherBoard.objects.create(**motherboard)
    for new_processor in range(random.randint(0, 2)):
        processor = {
            'name': f'processor {new_processor}',
            'socket': f'{SOCKET_CHOICES[random.randint(0, 4)][0]}',
            'cores': random.randint(1, 16),
            'threads': random.randint(1, 64),
            'watts': random.randint(50, 120),
            'ghz': round(random.uniform(1, 4), 2),
            'price': round(random.uniform(1, 250), 2)
        }
        Processor.objects.create(**processor)
    for new_graphic in range(random.randint(0, 2)):
        graphic = {
            'name': f'graphic {new_graphic}',
            'slot_type': f'{GRAPHIC_CARD_SLOT_TYPE[0][0]}',
            'memory': random.randint(512, 8192),
            'mhz': random.randint(100, 8000),
            'fans_number': random.randint(1, 4),
            'ram_memory_type': f'{GRAPHIC_CARD_MEMORY_TYPE[random.randint(0, 4)][0]}',
            'price': round(random.uniform(1, 250), 2)
        }
        GraphicCard.objects.create(**graphic)
    for new_disc in range(random.randint(0, 2)):
        disc = {
            'name': f'disc {new_disc}',
            'type': f'{DISC_TYPES[random.randint(0, 2)][0]}',
            'memory_in_gb': random.randint(120, 2048),
            'disc_format': f'{DISC_FORMAT_TYPES[random.randint(0, 2)][0]}',
            'price': round(random.uniform(1, 250), 2)
        }
        Disc.objects.create(**disc)
    for new_memory in range(random.randint(0, 2)):
        memory = {
            'name': f'memory {new_memory}',
            'memory_type': f'{MEMORY_TYPES[random.randint(0, 4)][0]}',
            'mhz': random.randint(100, 5000),
            'memory_in_gb': random.randint(1, 32),
            'delay': f"{random.choice(('CL15', 'CL16'))}",
            'price': round(random.uniform(1, 250), 2)
        }
        Memory.objects.create(**memory)
    for new_power_supply in range(random.randint(0, 2)):
        power_supply = {
            'name': f'power_supply {new_power_supply}',
            'power': random.randint(100, 900),
            'format_type': f'{MOTHERBOARD_SIZES[random.randint(0, 2)][0]}',
            'price': round(random.uniform(1, 250), 2)
        }
        PowerSupply.objects.create(**power_supply)
    for new_case in range(random.randint(0, 2)):
        case = {
            'name': f'case {new_case}',
            'case_type': f'{CASE_FORMAT_TYPES[random.randint(0, 4)][0]}',
            'motherboard_standard': f'{MOTHERBOARD_SIZES[random.randint(0, 2)][0]}',
            'has_RGB': random.choice((True, False)),
            'price': round(random.uniform(1, 250), 2)
        }
        Case.objects.create(**case)


class Command(BaseCommand):
    help = 'Adds parts to shop'

    def handle(self, *args, **options):
        add_parts_to_shop()
        self.stdout.write(self.style.SUCCESS("Successfully populated shop with new parts"))
