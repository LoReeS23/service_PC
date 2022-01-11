import datetime

from django.db import models
from django.contrib.auth.models import User as User_auth

# Create your models here.

SOCKET_CHOICES = [
    ('LGA_775', 'LGA 775'),
    ('LGA_1151', 'LGA 1151'),
    ('LGA_1155', 'LGA 1155'),
    ('AM3', 'AM3'),
    ('AM4', 'AM4')
]
MOTHERBOARD_SIZES = [
    ('miniATX', 'miniITX'),
    ('microATX', 'microATX'),
    ('ATX', 'ATX')
]
DISC_TYPES = [
    ('HDD', 'HDD'),
    ('SSD', 'SSD'),
    ('M.2', 'M.2')
]
MEMORY_TYPES = [
    ('DDR', 'DDR'),
    ('DDR2', 'DDR2'),
    ('DDR3', 'DDR3'),
    ('DDR4', 'DDR4'),
    ('DDR5', 'DDR5')
]
GRAPHIC_CARD_SLOT_TYPE = [
    ('PCI_E_3.0', 'PCI Express 3.0 x16')
]
GRAPHIC_CARD_MEMORY_TYPE = [
    ('GDDR3', 'GDDR3'),
    ('GDDR4', 'GDDR4'),
    ('GDDR5', 'GDDR5'),
    ('GDDR6', 'GDDR6'),
    ('GDDR6X', 'GDDR6X')
]
DISC_FORMAT_TYPES = [
    ('m.2', 'M.2'),
    ('2.5', '2.5'),
    ('3.5', '3.5')
]
CASE_FORMAT_TYPES = [
    ('Mini_tower', 'Mini Tower'),
    ('Midi_tower', 'Midi Tower'),
    ('Big_tower', 'Big Tower'),
    ('Micro_tower', 'Micro Tower'),
    ('Media_center', 'Media Center'),
    ('ITX', 'ITX')
]


class MotherBoard(models.Model):
    name = models.CharField(max_length=64)
    size = models.CharField(max_length=15, choices=MOTHERBOARD_SIZES)
    socket = models.CharField(max_length=15, choices=SOCKET_CHOICES)
    ram_slots = models.PositiveSmallIntegerField(default=2)
    memory_type = models.CharField(max_length=5, choices=MEMORY_TYPES)
    memory_frequency_lowest = models.PositiveSmallIntegerField()
    memory_frequency_highest = models.PositiveSmallIntegerField()
    m2_disc_slots = models.PositiveSmallIntegerField(default=1)
    sata_disc_slots = models.PositiveSmallIntegerField(default=1)
    usb_amount = models.PositiveSmallIntegerField(default=4)
    PCI_slots = models.PositiveSmallIntegerField(default=1)
    PCI_express_slots = models.PositiveSmallIntegerField(default=1)
    has_RGB = models.BooleanField(default=False)
    user = models.ForeignKey(User_auth, on_delete=models.CASCADE, null=True)
    price = models.FloatField(default=0)

    def get_absolute_url(self):
        return '/game/storage/motherboard_details/%d/' % self.pk


class GraphicCard(models.Model):
    name = models.CharField(max_length=64)
    slot_type = models.CharField(max_length=20, choices=GRAPHIC_CARD_SLOT_TYPE)
    memory = models.IntegerField()
    mhz = models.IntegerField()
    fans_number = models.PositiveSmallIntegerField(default=1)
    ram_memory_type = models.CharField(max_length=10, choices=GRAPHIC_CARD_MEMORY_TYPE)
    user = models.ForeignKey(User_auth, on_delete=models.CASCADE, null=True)
    price = models.FloatField(default=0)


class Processor(models.Model):
    name = models.CharField(max_length=64)
    socket = models.CharField(max_length=10, choices=SOCKET_CHOICES)
    cores = models.PositiveSmallIntegerField()
    threads = models.PositiveSmallIntegerField()
    watts = models.PositiveSmallIntegerField()
    ghz = models.FloatField(default=1.0)
    user = models.ForeignKey(User_auth, on_delete=models.CASCADE, null=True)
    price = models.FloatField(default=0)


class Disc(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=5, choices=DISC_TYPES)
    memory_in_gb = models.PositiveIntegerField()
    disc_format = models.CharField(max_length=5, choices=DISC_FORMAT_TYPES)
    user = models.ForeignKey(User_auth, on_delete=models.CASCADE, null=True)
    price = models.FloatField(default=0)


class Memory(models.Model):
    name = models.CharField(max_length=64)
    memory_type = models.CharField(max_length=10, choices=MEMORY_TYPES)
    mhz = models.PositiveSmallIntegerField()
    memory_in_gb = models.PositiveIntegerField()
    delay = models.CharField(max_length=5)
    user = models.ForeignKey(User_auth, on_delete=models.CASCADE, null=True)
    price = models.FloatField(default=0)


class PowerSupply(models.Model):
    name = models.CharField(max_length=64)
    power = models.PositiveSmallIntegerField()
    format_type = models.CharField(max_length=10, choices=MOTHERBOARD_SIZES)
    user = models.ForeignKey(User_auth, on_delete=models.CASCADE, null=True)
    price = models.FloatField(default=0)


class Case(models.Model):
    name = models.CharField(max_length=64)
    case_type = models.CharField(max_length=20, choices=CASE_FORMAT_TYPES)
    motherboard_standard = models.CharField(max_length=10, choices=MOTHERBOARD_SIZES)
    has_RGB = models.BooleanField()
    user = models.ForeignKey(User_auth, on_delete=models.CASCADE, null=True)
    price = models.FloatField(default=0)


class PC(models.Model):
    motherboard = models.ForeignKey(MotherBoard, on_delete=models.CASCADE)
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)
    graphic_card = models.ForeignKey(GraphicCard, on_delete=models.CASCADE)
    power_supply = models.ForeignKey(PowerSupply, on_delete=models.CASCADE)
    memory = models.ManyToManyField(Memory)
    disc = models.ManyToManyField(Disc)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    user = models.ForeignKey(User_auth, on_delete=models.CASCADE, null=True)
    price = models.FloatField(default=0)


class Wallet(models.Model):
    money_amount = models.IntegerField(default=1000)
    user = models.OneToOneField(User_auth, on_delete=models.CASCADE)


class Shop(models.Model):
    motherboard = models.ForeignKey(MotherBoard, on_delete=models.CASCADE, related_name='motherboard_shop')
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE, related_name='processor_shop')
    graphic = models.ForeignKey(GraphicCard, on_delete=models.CASCADE, related_name='graphic_shop')
    disc = models.ForeignKey(Disc, on_delete=models.CASCADE, related_name='disc_shop')
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE, related_name='memory_shop')
    power_supply = models.ForeignKey(PowerSupply, on_delete=models.CASCADE, related_name='power_supply_shop')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='case_shop')
    user = models.ForeignKey(User_auth, on_delete=models.CASCADE, related_name='user_shop')


class Task(models.Model):
    user = models.ForeignKey(User_auth, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    pc = models.OneToOneField(PC, on_delete=models.CASCADE, default=None)
    deadline = models.DateField(default=datetime.date.today())


class DayInWork(models.Model):
    day = models.IntegerField()
    date = models.DateField()
    user = models.ForeignKey(User_auth, on_delete=models.CASCADE)


class Level(models.Model):
    xp = models.IntegerField(default=0)
    discount = models.FloatField()
    lvl = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User_auth, on_delete=models.CASCADE)
