import random

from service_app.models import MOTHERBOARD_SIZES, MEMORY_TYPES, GRAPHIC_CARD_MEMORY_TYPE, DISC_TYPES, DISC_FORMAT_TYPES, \
    SOCKET_CHOICES, GRAPHIC_CARD_SLOT_TYPE, CASE_FORMAT_TYPES, MotherBoard, Processor, GraphicCard, PowerSupply, Case

fake_motherboard = {
    'name': 'motherboard',
    'size': f'{MOTHERBOARD_SIZES[random.randint(0, 2)][0]}',
    'socket': f'{SOCKET_CHOICES[random.randint(0, 4)][0]}',
    'ram_slots': random.randint(2, 6),
    'memory_type': f'{MEMORY_TYPES[random.randint(0, 4)][0]}',
    'memory_frequency_lowest': random.randint(2133, 3600),
    'memory_frequency_highest': random.randint(3601, 5000),
    'm2_disc_slots': random.randint(1, 3),
    'sata_disc_slots': random.randint(1, 4),
    'usb_amount': random.randint(2, 10),
    'PCI_slots': random.randint(1, 2),
    'PCI_express_slots': random.randint(1, 3),
    'has_RGB': random.choice((True, False)),
    'price': round(random.uniform(1, 250), 2)
}

fake_processor = {
    'name': 'processor',
    'socket': f'{SOCKET_CHOICES[random.randint(0, 4)][0]}',
    'cores': random.randint(1, 16),
    'threads': random.randint(1, 64),
    'watts': random.randint(50, 120),
    'ghz': round(random.uniform(1, 4), 3),
    'price': round(random.uniform(1, 250), 2)
}

fake_graphic = {
    'name': 'graphic',
    'slot_type': f'{GRAPHIC_CARD_SLOT_TYPE[0][0]}',
    'memory': random.randint(512, 8192),
    'mhz': random.randint(100, 8000),
    'fans_number': random.randint(1, 4),
    'ram_memory_type': f'{GRAPHIC_CARD_MEMORY_TYPE[random.randint(0, 4)][0]}',
    'price': round(random.uniform(1, 250), 2)
}

fake_disc = {
    'name': 'disc',
    'type': f'{DISC_TYPES[random.randint(0, 2)][0]}',
    'memory_in_gb': random.randint(120, 2048),
    'disc_format': f'{DISC_FORMAT_TYPES[random.randint(0, 2)][0]}',
    'price': round(random.uniform(1, 250), 2)
}

fake_memory = {
    'name': 'memory',
    'memory_type': f'{MEMORY_TYPES[random.randint(0, 4)][0]}',
    'mhz': random.randint(100, 5000),
    'memory_in_gb': random.randint(1, 32),
    'delay': f"{random.choice(('CL15', 'CL16'))}",
    'price': round(random.uniform(1, 250), 2)
}

fake_power_supply = {
    'name': 'power_supply',
    'power': random.randint(100, 900),
    'format_type': f'{MOTHERBOARD_SIZES[random.randint(0, 2)][0]}',
    'price': round(random.uniform(1, 250), 2)
}

fake_case = {
    'name': 'case',
    'case_type': f'{CASE_FORMAT_TYPES[random.randint(0, 4)][0]}',
    'motherboard_standard': f'{MOTHERBOARD_SIZES[random.randint(0, 2)][0]}',
    'has_RGB': random.choice((True, False)),
    'price': round(random.uniform(1, 250), 2)
}

fake_wallet = {
    'money_amount': 1000
}

