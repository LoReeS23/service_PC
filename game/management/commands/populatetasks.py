import datetime

from service_app.models import MotherBoard, Processor, GraphicCard, Memory, Disc, PowerSupply, Case, PC, Task
from django.core.management.base import BaseCommand
import random


def populate_tasks():
    for new_task in range(random.randint(1, 3)):
        new_pc = {
            'motherboard': random.choice(MotherBoard.objects.all()),
            'processor': random.choice(Processor.objects.all()),
            'graphic_card': random.choice(GraphicCard.objects.all()),
            'power_supply': random.choice(PowerSupply.objects.all()),
            'case': random.choice(Case.objects.all())
        }
        created_pc = PC.objects.create(**new_pc)

        for x in range(random.randint(1, created_pc.motherboard.sata_disc_slots)):
            disc_sata = random.choice(
                (random.choice(Disc.objects.filter(type='SSD')), random.choice(Disc.objects.filter(type='HDD'))))
            created_pc.disc.add(disc_sata)
        for y in range(random.randint(0, created_pc.motherboard.m2_disc_slots)):
            disc_m2 = random.choice(Disc.objects.filter(type='M.2'))
            created_pc.disc.add(disc_m2)
        for z in range(random.randint(1, created_pc.motherboard.ram_slots)):
            memory = random.choice(Memory.objects.filter(memory_type=created_pc.motherboard.memory_type))
            created_pc.memory.add(memory)
        created_pc.save()

        deadline = datetime.date.today() + datetime.timedelta(5)

        new_task = {
            'description': 'Cos mi nie dziala w komputerze.. Sprawdzisz to dla mnie?',
            'pc': created_pc,
            'deadline': deadline
        }
        Task.objects.create(**new_task)


class Command(BaseCommand):
    help = 'Adds new tasks'

    def handle(self, *args, **options):
        populate_tasks()
        self.stdout.write(self.style.SUCCESS("Successfully added new tasks"))
