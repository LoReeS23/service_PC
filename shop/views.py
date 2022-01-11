from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from service_app.models import *
from django.contrib.auth.models import User as Auth_user


# Create your views here.

class ShopView(LoginRequiredMixin, View):
    login_url = '/accounts/login'

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user).money_amount
        discount = Level.objects.get(user=request.user).discount * 100

        motherboards = MotherBoard.objects.filter(user=None).count()
        processors = Processor.objects.filter(user=None).count()
        graphic_cards = GraphicCard.objects.filter(user=None).count()
        power_supplies = PowerSupply.objects.filter(user=None).count()
        discs = Disc.objects.filter(user=None).count()
        memories = Memory.objects.filter(user=None).count()
        cases = Case.objects.filter(user=None).count()
        return render(request, 'shop.html', {'motherboards': motherboards,
                                             'processors': processors,
                                             'graphic_cards': graphic_cards,
                                             'power_supplies': power_supplies,
                                             'discs': discs,
                                             'memories': memories,
                                             'cases': cases,
                                             'wallet': wallet,
                                             'discount': discount})


class ShopProcessorBuyView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, id_num):
        user = request.user.username
        wallet = Wallet.objects.get(user__username=user)
        level = Level.objects.get(user=request.user)

        processor = Processor.objects.get(id=id_num)
        money = round(wallet.money_amount - processor.price, 2)
        part_discount = round(processor.price - (processor.price * level.discount), 2)
        discount = level.discount
        return render(request, 'shop_buy/processor_buy.html', {'processor': processor,
                                                               'money': money,
                                                               'part_discount': part_discount,
                                                               'discount': discount})

    def post(self, request, id_num):
        user = Auth_user.objects.get(username=request.user.username)
        wallet = Wallet.objects.get(user__username=user)
        processor = Processor.objects.get(id=id_num)
        level = Level.objects.get(user=request.user)

        if wallet.money_amount < processor.price:
            messages.error(request, 'Nie stac Cie na to!')
            return redirect(f'/game/shop/processor_buy/{id_num}')
        if level.discount != 0:
            part_discount = round(processor.price - (processor.price * level.discount), 2)
            processor.user = user
            processor.save()
            wallet.money_amount -= part_discount
            wallet.save()
            messages.info(request, 'Czesc zostala dodana do twojego magazynu!')
            return redirect('/game/shop/')

        processor.user = user
        processor.save()
        wallet.money_amount -= processor.price
        wallet.save()
        messages.info(request, 'Czesc zostala dodana do twojego magazynu!')
        return redirect('/game/shop/')


class ShopMotherboardBuyView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, id_num):
        user = request.user
        wallet = Wallet.objects.get(user=user)
        level = Level.objects.get(user=user)
        motherboard = MotherBoard.objects.get(id=id_num)
        money = round(wallet.money_amount - motherboard.price, 2)
        part_discount = round(motherboard.price - (motherboard.price * level.discount), 2)
        discount = level.discount

        return render(request, 'shop_buy/motherboard_buy.html', {'motherboard': motherboard,
                                                                 'money': money,
                                                                 'part_discount': part_discount,
                                                                 'discount': discount})

    def post(self, request, id_num):
        wallet = Wallet.objects.get(user=request.user)
        motherboard = MotherBoard.objects.get(id=id_num)
        level = Level.objects.get(user=request.user)

        if wallet.money_amount < motherboard.price:
            messages.error(request, 'Nie stac Cie na to!')
            return redirect(f'/game/shop/motherboard_buy/{id_num}')
        if level.discount != 0:
            part_discount = round(motherboard.price - (motherboard.price * level.discount), 2)
            motherboard.user = request.user
            motherboard.save()
            wallet.money_amount -= part_discount
            wallet.save()
            messages.info(request, 'Czesc zostala dodana do twojego magazynu!')
            return redirect('/game/shop/')

        motherboard.user = request.user
        motherboard.save()
        wallet.money_amount -= motherboard.price
        wallet.save()
        messages.info(request, 'Czesc zostala dodana do twojego magazynu!')
        return redirect('/game/shop/')


class ShopGraphicBuyView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, id_num):
        user = request.user.username
        wallet = Wallet.objects.get(user__username=user)
        graphic = GraphicCard.objects.get(id=id_num)
        level = Level.objects.get(user=request.user)

        money = round(wallet.money_amount - graphic.price, 2)
        part_discount = round(graphic.price - (graphic.price * level.discount), 2)
        discount = level.discount

        return render(request, 'shop_buy/graphic_card_buy.html', {'graphic': graphic,
                                                                  'money': money,
                                                                  'part_discount': part_discount,
                                                                  'discount': discount})

    def post(self, request, id_num):
        wallet = Wallet.objects.get(user=request.user)
        graphic = GraphicCard.objects.get(id=id_num)
        level = Level.objects.get(user=request.user)

        if wallet.money_amount < graphic.price:
            messages.error(request, 'Nie stac Cie na to!')
            return redirect(f'/game/shop/graphic_buy/{id_num}')
        if level.discount != 0:
            part_discount = round(graphic.price - (graphic.price * level.discount), 2)
            graphic.user = request.user
            graphic.save()
            wallet.money_amount -= part_discount
            wallet.save()
            messages.info(request, 'Czesc zostala dodana do twojego magazynu!')
            return redirect('/game/shop/')

        graphic.user = request.user
        graphic.save()
        wallet.money_amount -= graphic.price
        wallet.save()
        messages.info(request, 'Czesc zostala dodana do twojego magazynu!')
        return redirect('/game/shop/')


class ShopDiscBuyView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, id_num):
        user = request.user.username
        wallet = Wallet.objects.get(user__username=user)
        disc = Disc.objects.get(id=id_num)
        money = round(wallet.money_amount - disc.price, 2)
        level = Level.objects.get(user=request.user)
        part_discount = round(disc.price - (disc.price * level.discount), 2)
        discount = level.discount

        return render(request, 'shop_buy/disc_buy.html', {'disc': disc,
                                                          'money': money,
                                                          'part_discount': part_discount,
                                                          'discount': discount})

    def post(self, request, id_num):
        user = Auth_user.objects.get(username=request.user.username)
        wallet = Wallet.objects.get(user__username=user)
        disc = Disc.objects.get(id=id_num)
        level = Level.objects.get(user=request.user)
        if wallet.money_amount < disc.price:
            messages.error(request, 'Nie stac Cie na to!')
            return redirect(f'/game/shop/disc_buy/{id_num}')
        if level.discount != 0:
            part_discount = round(disc.price - (disc.price * level.discount), 2)
            disc.user = request.user
            disc.save()
            wallet.money_amount -= part_discount
            wallet.save()
            messages.info(request, 'Czesc zostala dodana do twojego magazynu!')
            return redirect('/game/shop/')

        disc.user = user
        disc.save()
        wallet.money_amount -= disc.price
        wallet.save()
        messages.info(request, 'Czesc zostala dodana do twojego magazynu!')
        return redirect('/game/shop/')


class ShopMemoryBuyView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, id_num):
        user = request.user.username
        wallet = Wallet.objects.get(user__username=user)
        memory = Memory.objects.get(id=id_num)
        money = round(wallet.money_amount - memory.price, 2)
        level = Level.objects.get(user=request.user)
        part_discount = round(memory.price - (memory.price * level.discount), 2)
        discount = level.discount

        return render(request, 'shop_buy/memory_buy.html', {'memory': memory,
                                                            'money': money,
                                                            'part_discount': part_discount,
                                                            'discount': discount})

    def post(self, request, id_num):
        user = Auth_user.objects.get(username=request.user.username)
        wallet = Wallet.objects.get(user__username=user)
        memory = Memory.objects.get(id=id_num)
        level = Level.objects.get(user=request.user)

        if wallet.money_amount < memory.price:
            messages.error(request, 'Nie stac Cie na to!')
            return redirect(f'/game/shop/memory_buy/{id_num}')
        if level.discount != 0:
            part_discount = round(memory.price - (memory.price * level.discount), 2)
            memory.user = request.user
            memory.save()
            wallet.money_amount -= part_discount
            wallet.save()
            messages.info(request, 'Czesc zostala dodana do twojego magazynu!')
            return redirect('/game/shop/')

        memory.user = user
        memory.save()
        wallet.money_amount -= memory.price
        wallet.save()
        messages.info(request, 'Czesc zostala dodana do twojego magazynu!')
        return redirect('/game/shop/')


class ShopPowerSupplyBuyView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, id_num):
        user = request.user.username
        wallet = Wallet.objects.get(user__username=user)
        power = PowerSupply.objects.get(id=id_num)
        money = round(wallet.money_amount - power.price, 2)
        level = Level.objects.get(user=request.user)
        part_discount = round(power.price - (power.price * level.discount), 2)
        discount = level.discount
        return render(request, 'shop_buy/power_buy.html', {'power': power,
                                                           'money': money,
                                                           'part_discount': part_discount,
                                                           'discount': discount})

    def post(self, request, id_num):
        user = Auth_user.objects.get(username=request.user.username)
        wallet = Wallet.objects.get(user__username=user)
        power = PowerSupply.objects.get(id=id_num)
        level = Level.objects.get(user=request.user)

        if wallet.money_amount < power.price:
            messages.error(request, 'Nie stac Cie na to!')
            return redirect(f'/game/shop/power_buy/{id_num}')
        if level.discount != 0:
            part_discount = round(power.price - (power.price * level.discount), 2)
            power.user = request.user
            power.save()
            wallet.money_amount -= part_discount
            wallet.save()
            messages.info(request, 'Czesc zostala dodana do twojego magazynu!')
            return redirect('/game/shop/')

        power.user = user
        power.save()
        wallet.money_amount -= power.price
        wallet.save()
        messages.info(request, 'Czesc zostala dodana do twojego magazynu!')
        return redirect('/game/shop/')


class ShopCaseBuyView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, id_num):
        user = request.user.username
        wallet = Wallet.objects.get(user__username=user)
        case = Case.objects.get(id=id_num)
        money = round(wallet.money_amount - case.price, 2)
        level = Level.objects.get(user=request.user)
        part_discount = round(case.price - (case.price * level.discount), 2)
        discount = level.discount

        return render(request, 'shop_buy/case_buy.html', {'case': case,
                                                          'money': money,
                                                          'part_discount': part_discount,
                                                          'discount': discount})

    def post(self, request, id_num):
        user = Auth_user.objects.get(username=request.user.username)
        wallet = Wallet.objects.get(user__username=user)
        case = Case.objects.get(id=id_num)
        level = Level.objects.get(user=request.user)

        if wallet.money_amount < case.price:
            messages.error(request, 'Nie stac Cie na to!')
            return redirect(f'/game/shop/case_buy/{id_num}')
        if level.discount != 0:
            part_discount = round(case.price - (case.price * level.discount), 2)
            case.user = request.user
            case.save()
            wallet.money_amount -= part_discount
            wallet.save()
            messages.info(request, 'Czesc zostala dodana do twojego magazynu!')
            return redirect('/game/shop/')

        case.user = user
        case.save()
        wallet.money_amount -= case.price
        wallet.save()
        messages.info(request, 'Czesc zostala dodana do twojego magazynu!')
        return redirect('/game/shop/')


class MotherBoardList(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        motherboards = MotherBoard.objects.filter(user=None)
        wallet = Wallet.objects.get(user=request.user).money_amount
        level = Level.objects.get(user=request.user).discount * 100
        return render(request, 'shop_lists/shop_motherboards_list.html', {'motherboards': motherboards,
                                                                          'wallet': wallet,
                                                                          'discount': level})

    def post(self, request):
        rgb = request.POST.get('rgb')
        size = request.POST.get('size')
        socket = request.POST.get('socket')
        memory_type = request.POST.get('memory_type')
        m2_discs = request.POST.get('m2_discs')
        sata_discs = request.POST.get('sata_discs')
        queryset = MotherBoard.objects.filter(user=None)
        wallet = Wallet.objects.get(user=request.user).money_amount
        level = Level.objects.get(user=request.user).discount * 100

        if 'reset_filters' in request.POST:
            return render(request, 'shop_lists/shop_motherboards_list.html', {"motherboards": queryset})
        if 'filter' in request.POST:
            if rgb == 'on':
                queryset = queryset.filter(has_RGB=True)
            if m2_discs is not "":
                queryset = queryset.filter(m2_disc_slots=m2_discs)
            if sata_discs is not "":
                queryset = queryset.filter(sata_disc_slots=sata_discs)
            if size is not None:
                queryset = queryset.filter(size=size)
            if socket is not None:
                queryset = queryset.filter(socket=socket)
            if memory_type is not None:
                queryset = queryset.filter(memory_type=memory_type)

            return render(request, 'shop_lists/shop_motherboards_list.html', {'motherboards': queryset,
                                                                              'wallet': wallet,
                                                                              'discount': level})


class ProcessorsList(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        processors = Processor.objects.filter(user=None)
        wallet = Wallet.objects.get(user=request.user).money_amount
        level = Level.objects.get(user=request.user).discount * 100
        return render(request, 'shop_lists/shop_processors_list.html', {'processors': processors,
                                                                        'wallet': wallet,
                                                                        'discount': level})

    def post(self, request):
        wallet = Wallet.objects.get(user=request.user).money_amount
        level = Level.objects.get(user=request.user).discount * 100
        socket = request.POST.get('socket')
        min_cores = request.POST.get('min_cores')
        max_cores = request.POST.get('max_cores')
        min_threads = request.POST.get('min_threads')
        max_threads = request.POST.get('max_threads')
        min_ghz = request.POST.get('min_ghz')
        max_ghz = request.POST.get('max_ghz')
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        queryset = Processor.objects.filter(user=None)
        if 'reset_filters' in request.POST:
            return render(request, 'shop_lists/shop_processors_list.html', {'processors': queryset,
                                                                            'wallet': wallet,
                                                                            'discount': level})
        if 'filter' in request.POST:
            if socket is not None:
                queryset = queryset.filter(socket=socket)
            if min_cores is not "":
                queryset = queryset.filter(cores__gte=min_cores)
            if max_cores is not "":
                queryset = queryset.filter(cores__lte=max_cores)
            if min_threads is not "":
                queryset = queryset.filter(threads__gte=min_threads)
            if max_threads is not "":
                queryset = queryset.filter(threads__lte=max_threads)
            if min_ghz is not "":
                queryset = queryset.filter(ghz__gte=min_ghz)
            if max_ghz is not "":
                queryset = queryset.filter(ghz__lte=max_ghz)
            if min_price is not "":
                queryset = queryset.filter(price__gte=min_price)
            if max_price is not "":
                queryset = queryset.filter(price__lte=max_price)

            return render(request, 'shop_lists/shop_processors_list.html', {'processors': queryset,
                                                                            'wallet': wallet,
                                                                            'discount': level})
