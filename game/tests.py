from django.contrib.auth.models import User

from service_app.models import MOTHERBOARD_SIZES, SOCKET_CHOICES, MEMORY_TYPES, MotherBoard, Processor, \
    GraphicCard, Disc, Memory, PowerSupply, Case, PC, Wallet, Task, DayInWork
from django.test import Client
import pytest
import random


#                   GET PAGE

@pytest.mark.django_db
def test_get_main_page():
    client = Client()
    response = client.get('/main/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_about_page():
    client = Client()
    response = client.get('/about/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_login_page():
    client = Client()
    response = client.get('/accounts/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_register_page():
    client = Client()
    response = client.get('/accounts/register/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_game_page(user):
    client = Client()
    client.force_login(user)
    response = client.get('/game/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_storage_page(user):
    client = Client()
    client.force_login(user)
    response = client.get('/game/storage/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_create_pc_page(user):
    client = Client()
    client.force_login(user)
    response = client.get('/game/create_pc/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_shop_page(user):
    client = Client()
    client.force_login(user)
    response = client.get('/game/shop/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_delete_pc_page(user, pc):
    client = Client()
    client.force_login(user)
    response = client.get(f'/game/delete_pc/{pc.pk}')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_tasks_page(user):
    client = Client()
    client.force_login(user)
    response = client.get('/game/tasks/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_task_detail_page(user, pc):
    client = Client()
    client.force_login(user)
    task = {
        'description': 'test',
        'pc': pc
    }
    new_task = Task.objects.create(**task)
    assert client.get(f'/game/tasks/detail/{new_task.id}')
    new_task.user = user
    new_task.save()
    assert new_task.user.username == 'maciek'


#                   PART DETAIL GET PAGES

@pytest.mark.django_db
def test_get_motherboard_details_page(user, motherboard):
    client = Client()
    client.force_login(user)
    created_motherboard = MotherBoard.objects.create(**motherboard)
    response = client.get('/game/motherboard_details/1')
    assert response.status_code == 200
    random_num = random.randint(1, 4)
    disc_slots_created_motherboard = created_motherboard.sata_disc_slots
    while disc_slots_created_motherboard == random_num:
        random_num += 1
        created_motherboard.sata_disc_slots = random_num
    created_motherboard.save()


@pytest.mark.django_db
def test_get_processor_details_page(user, processor):
    client = Client()
    client.force_login(user)
    processor_created = Processor.objects.create(**processor)
    response = client.get('/game/processor_details/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_graphics_details_page(user, graphic):
    client = Client()
    client.force_login(user)
    GraphicCard.objects.create(**graphic)
    response = client.get('/game/graphic_card_details/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_memory_details_page(user, memory):
    client = Client()
    client.force_login(user)
    Memory.objects.create(**memory)
    response = client.get('/game/memory_details/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_disc_details_page(user, disc):
    client = Client()
    client.force_login(user)
    Disc.objects.create(**disc)
    response = client.get('/game/disc_details/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_power_supply_details_page(user, power_supply):
    client = Client()
    client.force_login(user)
    PowerSupply.objects.create(**power_supply)
    response = client.get('/game/power_supply_details/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_case_details_page(user, case):
    client = Client()
    client.force_login(user)
    Case.objects.create(**case)
    response = client.get('/game/case_details/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_pc_details_page(user, pc):
    client = Client()
    client.force_login(user)
    response = client.get('/game/pc_details/1')
    assert response.status_code == 200


#                   LOGIN/REGISTER

@pytest.mark.django_db
def test_login(user):
    client = Client()
    client.force_login(user)
    assert user.is_authenticated
    assert user.is_active
    assert Wallet.objects.get(user=user).money_amount == 1000


@pytest.mark.django_db
def test_register():
    client = Client()
    client.get('/accounts/register/')
    new_user = {
        'username': 'maciek',
        'password': '123',
        'password_repeat': '123'
    }
    response = client.post('/accounts/register/', data=new_user)
    assert response.status_code == 302
    day = DayInWork.objects.get(user__username='maciek')
    assert day.day == 1
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_logout(user):
    client = Client()
    client.force_login(user)
    client.get("accounts/logout/")
    assert user.is_authenticated


#           ADD PART

@pytest.mark.django_db
def test_add_motherboard_part(superuser, motherboard):
    client = Client()
    client.force_login(superuser)
    response = client.post('/game/addpart/motherboard/', motherboard)
    assert MotherBoard.objects.count() == 1
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_processor_part(superuser, processor):
    client = Client()
    client.force_login(superuser)

    response = client.post('/game/addpart/processor/', processor)
    assert response.status_code == 302
    assert Processor.objects.count() == 1


@pytest.mark.django_db
def test_add_graphic_part(superuser, graphic):
    client = Client()
    client.force_login(superuser)

    response = client.post('/game/addpart/graphic_card/', graphic)
    assert response.status_code == 302
    assert GraphicCard.objects.count() == 1


@pytest.mark.django_db
def test_add_disc_part(superuser, disc):
    client = Client()
    client.force_login(superuser)

    response = client.post('/game/addpart/disc/', disc)
    assert response.status_code == 302
    assert Disc.objects.count() == 1


@pytest.mark.django_db
def test_add_memory_part(superuser, memory):
    client = Client()
    client.force_login(superuser)

    response = client.post('/game/addpart/memory/', memory)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_power_supply_part(superuser, power_supply):
    client = Client()
    client.force_login(superuser)

    response = client.post('/game/addpart/power_supply/', power_supply)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_case_part(superuser, case):
    client = Client()
    client.force_login(superuser)
    Case.objects.create(**case)

    response = client.post('/game/addpart/case/', case)
    assert response.status_code == 302


#               PC

@pytest.mark.django_db
def test_create_pc(user, pc):
    client = Client()
    assert PC.objects.count() == 1
    response = client.get('/game/pc_details/1')
    assert response.status_code == 302
    assert pc.motherboard.name == 'motherboard'
    assert pc.price > 1
    assert pc.disc is not None
    assert pc.memory is not None
    pc.user = user
    pc.save()
    assert pc.user == user


@pytest.mark.django_db
def test_sell_pc(user, pc):
    wallet = Wallet.objects.get(user=user)
    wallet.money_amount += pc.price
    pc.delete()
    assert pc not in PC.objects.all()
    assert wallet.money_amount > 1000
    assert pc.user is None


#           TASKS

@pytest.mark.django_db
def test_change_part(user, pc, motherboard):
    client = Client()
    client.force_login(user)
    pc = PC.objects.first()
    other_motherboard = MotherBoard.objects.create(**motherboard)
    pc.motherboard = other_motherboard
    pc.save()
    assert pc.motherboard != other_motherboard or pc.motherboard == other_motherboard