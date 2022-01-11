import datetime

import pytest
from django.contrib.auth.models import User
from service_app.models import MotherBoard, Processor, GraphicCard, Disc, Memory, PowerSupply, Case, PC, Wallet, \
    DayInWork, Level
from game.utils import fake_motherboard, fake_processor, fake_graphic, fake_memory, fake_disc, fake_power_supply, \
    fake_case, fake_wallet
import random


@pytest.fixture
def user():
    new_user = User.objects.create_user(username='maciek')
    Level.objects.create(xp=0, lvl=1, discount=0, user=new_user)
    DayInWork.objects.create(day=1, date=datetime.date.today(), user=new_user)
    Wallet.objects.create(money_amount=1000, user=new_user)
    return new_user


@pytest.fixture
def superuser():
    new_superuser = User.objects.create_superuser(username='Andrzej', email='sample@sample.pl', password='1')
    return new_superuser


@pytest.fixture
def motherboard():
    return fake_motherboard


@pytest.fixture
def processor():
    return fake_processor


@pytest.fixture
def graphic():
    return fake_graphic


@pytest.fixture
def disc():
    return fake_disc


@pytest.fixture
def memory():
    return fake_memory


@pytest.fixture
def power_supply():
    return fake_power_supply


@pytest.fixture
def case():
    return fake_case


@pytest.fixture
def pc():
    motherboard_pc = MotherBoard.objects.create(**fake_motherboard)
    processor_pc = Processor.objects.create(**fake_processor)
    graphic_pc = GraphicCard.objects.create(**fake_graphic)
    memory_pc = Memory.objects.create(**fake_memory)
    disc_pc = Disc.objects.create(**fake_disc)
    power_supply_pc = PowerSupply.objects.create(**fake_power_supply)
    case_pc = Case.objects.create(**fake_case)
    price = (
                    motherboard_pc.price + processor_pc.price + graphic_pc.price + memory_pc.price + disc_pc.price + power_supply_pc.price + case_pc.price) * 3

    pc = PC.objects.create(motherboard=motherboard_pc, processor=processor_pc, graphic_card=graphic_pc,
                           power_supply=power_supply_pc, case=case_pc, price=price)
    pc.memory.add(memory_pc)
    pc.disc.add(disc_pc)
    return pc


@pytest.fixture
def wallet():
    return fake_wallet


@pytest.fixture
def task():
    created_pc = PC.objects.create(**fake_pc)
    fake_task = {
        'description': 'test',
        'pc': created_pc
    }
    return fake_task
