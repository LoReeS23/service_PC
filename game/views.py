import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

# Create your views here.
from django.views import View
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from game.management.commands.populatetasks import populate_tasks
from game.management.commands.populateshop import add_parts_to_shop

from service_app.forms import AddPartForm, CreatePCForm
from service_app.models import Wallet, MotherBoard, Processor, GraphicCard, PowerSupply, Disc, Memory, Case, PC, Task, \
    DayInWork, Level


class GamePageView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user).money_amount
        day = DayInWork.objects.get(user=request.user)
        level = Level.objects.get(user=request.user)
        discount = level.discount * 100
        if level.xp >= (level.lvl * 300):
            level.lvl += 1
            level.discount += 0.015
            level.save()
            messages.info(request, 'Level up!')
        return render(request, 'game.html', {'wallet': wallet,
                                             'day': day,
                                             'level': level,
                                             'discount': discount})

    def post(self, request):
        if 'next_day' in request.POST:
            tasks = Task.objects.filter(user=request.user)
            day = DayInWork.objects.get(user=request.user)
            wallet = Wallet.objects.get(user=request.user)

            for task in tasks:
                if task.deadline < day.date:
                    wallet.money_amount -= 100
                    wallet.save()
                    task.delete()
                    messages.info(request,
                                  'Nie zdazyles wykonac zlecenia! Z twojego konta zabrano 100 $ w ramach rekompensaty')
            day.day += 1
            day.date += datetime.timedelta(1)
            day.save()
            add_parts_to_shop()
            populate_tasks()
            return redirect('/game/')


class CheckStorageView(LoginRequiredMixin, View):
    login_url = 'accounts/login/'

    def get(self, request):
        user = request.user.username
        wallet = Wallet.objects.get(user=request.user).money_amount
        level = Level.objects.get(user=request.user)
        day = DayInWork.objects.get(user=request.user)
        discount = level.discount * 100

        motherboards = MotherBoard.objects.filter(user__username=user)
        processors = Processor.objects.filter(user__username=user)
        graphic_cards = GraphicCard.objects.filter(user__username=user)
        power_supplies = PowerSupply.objects.filter(user__username=user)
        discs = Disc.objects.filter(user__username=user)
        memories = Memory.objects.filter(user__username=user)
        cases = Case.objects.filter(user__username=user)
        pcs = PC.objects.filter(user__username=user)
        return render(request, 'storage.html', {'motherboards': motherboards,
                                                'processors': processors,
                                                'graphic_cards': graphic_cards,
                                                'power_supplies': power_supplies,
                                                'discs': discs,
                                                'memories': memories,
                                                'cases': cases,
                                                'pcs': pcs,
                                                'wallet': wallet,
                                                'level': level,
                                                'day': day,
                                                'discount': discount})


class AddPartView(LoginRequiredMixin, View):
    login_url = '/accounts/login'

    def get(self, request):
        form = AddPartForm()
        return render(request, 'addpart.html', {'form': form})

    def post(self, request):
        form = AddPartForm(request.POST)
        if form.is_valid():
            form_type = form.cleaned_data
            if form_type['part'] == '1':
                return redirect('/game/addpart/motherboard')
            elif form_type['part'] == '2':
                return redirect('/game/addpart/processor')
            elif form_type['part'] == '3':
                return redirect('/game/addpart/graphic_card')
            elif form_type['part'] == '4':
                return redirect('/game/addpart/disc')
            elif form_type['part'] == '5':
                return redirect('/game/addpart/memory')
            elif form_type['part'] == '6':
                return redirect('/game/addpart/power_supply')
            elif form_type['part'] == '7':
                return redirect('/game/addpart/case')
        return render(request, 'addpart.html', {"form": form})


class AddPartMotherBoardView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = '/accounts/login'
    model = MotherBoard
    template_name = 'addpart.html'
    fields = ['name', 'size', 'socket', 'ram_slots', 'memory_type', 'memory_frequency_lowest',
              'memory_frequency_highest', 'm2_disc_slots', 'sata_disc_slots', 'usb_amount', 'PCI_slots', 'has_RGB',
              'price']
    success_message = "%(name)s was created successfully"
    success_url = '/main/'


class AddPartProcessorView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login'
    model = Processor
    template_name = 'addpart.html'
    fields = ['name', 'socket', 'cores', 'threads', 'watts', 'ghz', 'price']
    success_url = '/main/'


class AddPartGraphicCardView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login'
    model = GraphicCard
    template_name = 'addpart.html'
    fields = ['name', 'slot_type', 'memory', 'mhz', 'fans_number', 'ram_memory_type', 'price']
    success_url = '/main/'


class AddPartDiscView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login'
    model = Disc
    template_name = 'addpart.html'
    fields = ['name', 'type', 'memory_in_gb', 'disc_format', 'price']
    success_url = '/main/'


class AddPartMemoryView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login'
    model = Memory
    template_name = 'addpart.html'
    fields = ['name', 'memory_type', 'mhz', 'memory_in_gb', 'delay', 'price']
    success_url = '/main/'


class AddPartPowerSupplyView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login'
    model = PowerSupply
    template_name = 'addpart.html'
    fields = ['name', 'power', 'format_type', 'price']
    success_url = '/main/'


class AddPartCaseView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login'
    model = Case
    template_name = 'addpart.html'
    fields = ['name', 'case_type', 'motherboard_standard', 'has_RGB', 'price']
    success_url = '/main/'


#                       DETAIL PART VIEWS

class MotherboardPartDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login'
    model = MotherBoard
    template_name = 'parts_details_storage/motherboard_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(user=self.request.user)
        return context


class GraphicCardPartDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login'
    model = GraphicCard
    template_name = 'parts_details_storage/graphic_card_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(user=self.request.user)
        return context


class ProcessorDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login'
    model = Processor
    template_name = 'parts_details_storage/processor_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(user=self.request.user)
        return context


class DiscDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login'
    model = Disc
    template_name = 'parts_details_storage/disc_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(user=self.request.user)
        return context


class MemoryDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login'
    model = Memory
    template_name = 'parts_details_storage/memory_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(user=self.request.user)
        return context


class PowerSupplyDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login'
    model = PowerSupply
    template_name = 'parts_details_storage/power_supply_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(user=self.request.user)
        return context


class CaseDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login'
    model = Case
    template_name = 'parts_details_storage/case_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(user=self.request.user)
        return context


class PCDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login'
    model = PC
    template_name = 'parts_details_storage/PC_details.html'


#       CREATE PC

class CreatePCView(LoginRequiredMixin, View):
    login_url = 'accounts/login/'

    def get(self, request):
        form = CreatePCForm()
        form.fields['motherboard'].choices = MotherBoard.objects.filter(user=request.user).values_list('pk', 'name')
        form.fields['processor'].choices = Processor.objects.filter(user=request.user).values_list('pk', 'name')
        graphic_card = form.fields['graphic_card'].choices = GraphicCard.objects.filter(user=request.user).values_list(
            'pk', 'name')
        if graphic_card.all() == None:
            messages.error(request, 'Nie masz zadnych kart graficznych')
        form.fields['memory'].choices = Memory.objects.filter(user=request.user).values_list('pk', 'name')
        form.fields['disc'].choices = Disc.objects.filter(user=request.user).values_list('pk', 'name')
        form.fields['power_supply'].choices = PowerSupply.objects.filter(user=request.user).values_list('pk', 'name')
        form.fields['case'].choices = Case.objects.filter(user=request.user).values_list('pk', 'name')
        return render(request, 'create_pc.html', {'form': form})

    def post(self, request):
        form = CreatePCForm(request.POST)
        level = Level.objects.get(user=request.user)
        if form.is_valid():
            data = form.cleaned_data
            motherboard = data['motherboard']
            processor = data['processor']
            graphic = data['graphic_card']
            memory = data['memory']
            disc = data['disc']
            power_supply = data['power_supply']
            case = data['case']
            if motherboard.socket != processor.socket:
                messages.error(request, 'Socket nie pasuje')
                return redirect('/game/create_pc/')
            if case.motherboard_standard != motherboard.size:
                messages.error(request, 'Obudowa nie pasuje do plyty glownej')
                return redirect('/game/create_pc/')
            if disc.count() > (motherboard.m2_disc_slots + motherboard.sata_disc_slots):
                messages.error(request, 'Za duzo podlaczonych dyskow!')
                return redirect('/game/create_pc/')
            if memory.count() > motherboard.ram_slots:
                messages.error(request, 'Za duzo pamieci RAM')
                return redirect('/game/create_pc/')
            for a in memory:
                if a.memory_type != motherboard.memory_type:
                    messages.error(request, 'Nieodpowiednia pamiec RAM')
                    return redirect('/game/create_pc/')
            if motherboard.size != power_supply.format_type:
                messages.error(request, 'Nieodpowiedni rozmiar zasilacza')
                return redirect('/game/create_pc/')

            price = (motherboard.price + processor.price + graphic.price + power_supply.price + case.price) * 1.6

            pc = PC.objects.create(motherboard=motherboard, processor=processor, graphic_card=graphic,
                                   power_supply=power_supply,
                                   case=case, user=request.user)
            for a in disc:
                pc.disc.add(a)
                price += a.price
                a.user = None
                a.save()
            for b in memory:
                pc.memory.add(b)
                price += b.price
                b.user = None
                b.save()
            pc.price = price
            pc.save()
            motherboard.user = None
            motherboard.save()
            processor.user = None
            processor.save()
            graphic.user = None
            graphic.save()
            power_supply.user = None
            power_supply.save()
            case.user = None
            case.save()

            level.xp += 50
            level.save()
            messages.info(request, 'Stworzono poprawnie PC i dodano do magazynu!')
            messages.info(request, 'Zdobyte doswiadczenie: 50!')
            return redirect('/game/storage/')
        return render(request, 'create_pc.html', {'form': form})


class DeletePCView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, pk):
        wallet = round(Wallet.objects.get(user=request.user).money_amount + PC.objects.get(id=pk).price, 2)
        return render(request, 'delete_form.html', {'wallet': wallet})

    def post(self, request, pk):
        pc = PC.objects.get(id=pk)
        wallet = Wallet.objects.get(user__username=request.user.username)

        wallet.money_amount += pc.price
        wallet.save()
        for memory in pc.memory.all():
            memory.delete()
        for disc in pc.disc.all():
            disc.delete()
        pc.motherboard.delete()
        pc.processor.delete()
        pc.graphic_card.delete()
        pc.power_supply.delete()
        pc.case.delete()
        return redirect('/game/storage/')


#           UPDATE PARTS VIEWS

class UpdateMotherboardView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = MotherBoard
    fields = '__all__'
    template_name = 'update_part_form.html'

    def get_success_url(self):
        model = self.object
        return f'/game/motherboard_details/{model.pk}'


class UpdateProcessorView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Processor
    fields = '__all__'
    template_name = 'update_part_form.html'

    def get_success_url(self):
        model = self.object
        return f'/game/processor_details/{model.pk}'


class UpdateGraphicView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = GraphicCard
    fields = '__all__'
    template_name = 'update_part_form.html'

    def get_success_url(self):
        model = self.object
        return f'/game/graphic_card_details/{model.pk}'


class UpdateDiscView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Disc
    fields = '__all__'
    template_name = 'update_part_form.html'

    def get_success_url(self):
        model = self.object
        return f'/game/disc_details/{model.pk}'


class UpdateMemoryView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Memory
    fields = '__all__'
    template_name = 'update_part_form.html'

    def get_success_url(self):
        model = self.object
        return f'/game/memory_details/{model.pk}'


class UpdatePowerSupplyView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = PowerSupply
    fields = '__all__'
    template_name = 'update_part_form.html'

    def get_success_url(self):
        model = self.object
        return f'/game/power_supply_details/{model.pk}'


class UpdateCaseView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Case
    fields = '__all__'
    template_name = 'update_part_form.html'

    def get_success_url(self):
        model = self.object
        return f'/game/case_details/{model.pk}'


#       DELETE PARTS

class DeleteMotherboard(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login'
    model = MotherBoard
    template_name = 'delete_form.html'
    success_url = '/game/storage/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_price = self.object.price
        wallet = Wallet.objects.get(user=self.request.user)
        context['wallet'] = wallet.money_amount + object_price
        return context


class DeleteProcessor(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login'
    model = Processor
    template_name = 'delete_form.html'
    success_url = '/game/storage/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_price = self.object.price
        wallet = Wallet.objects.get(user=self.request.user)
        context['wallet'] = wallet.money_amount + object_price
        return context


class DeleteGraphics(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login'
    model = GraphicCard
    template_name = 'delete_form.html'
    success_url = '/game/storage/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_price = self.object.price
        wallet = Wallet.objects.get(user=self.request.user)
        context['wallet'] = wallet.money_amount + object_price
        return context


class DeleteMemory(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login'
    model = Memory
    success_url = '/game/storage/'
    template_name = 'delete_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_price = self.object.price
        wallet = Wallet.objects.get(user=self.request.user)
        context['wallet'] = wallet.money_amount + object_price
        return context


class DeleteDisc(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login'
    model = Disc
    success_url = '/game/storage/'
    template_name = 'delete_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_price = self.object.price
        wallet = Wallet.objects.get(user=self.request.user)
        context['wallet'] = wallet.money_amount + object_price
        return context


class DeletePowerSupply(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login'
    model = PowerSupply
    success_url = '/game/storage/'
    template_name = 'delete_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_price = self.object.price
        wallet = Wallet.objects.get(user=self.request.user)
        context['wallet'] = wallet.money_amount + object_price
        return context


class DeleteCase(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login'
    model = Case
    success_url = '/game/storage/'
    template_name = 'delete_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_price = self.object.price
        wallet = Wallet.objects.get(user=self.request.user)
        context['wallet'] = wallet.money_amount + object_price
        return context


#           TASKS

class CheckTaskView(LoginRequiredMixin, View):
    def get(self, request):
        wallet = Wallet.objects.get(user=request.user).money_amount
        level = Level.objects.get(user=request.user)
        all_tasks = Task.objects.all()
        all_not_taken_tasks = Task.objects.filter(user=None)
        my_tasks = Task.objects.filter(user__username=request.user.username)

        if level.xp >= (level.lvl * 300):
            level.lvl += 1
            level.discount += 0.015
            level.save()
            messages.info(request, 'Level up!')
        return render(request, 'showtasks.html', {'tasks': all_tasks,
                                                  'all_not_taken_tasks': all_not_taken_tasks,
                                                  'my_tasks': my_tasks,
                                                  'wallet': wallet,
                                                  'level': level})


class TaskConfirm(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        return render(request, 'task_confirm.html', {'task': task})

    def post(self, request, pk):
        if 'confirm' in request.POST:
            task = Task.objects.get(id=pk)
            task.user = request.user
            task.save()
            return redirect('/game/tasks/')
        if 'reject' in request.POST:
            task = Task.objects.get(id=pk)
            level = Level.objects.get(user=request.user)

            task.delete()
            level.xp -= 20
            level.save()
            messages.info(request, 'Odrzuciles zlecenie :/ Odjeto Tobie 20 doswiadczenia')
            return redirect('/game/tasks/')


class TaskDetail(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        wallet = Wallet.objects.get(user=request.user)
        return render(request, 'task_detail.html', {'task': task,
                                                    'wallet': wallet})

    def post(self, request, pk):
        task = Task.objects.get(id=pk)
        wallet = Wallet.objects.get(user=request.user)
        level = Level.objects.get(user=request.user)

        if 'check' in request.POST:
            if task.pc.processor.socket != task.pc.motherboard.socket:
                messages.error(request, 'Socket nie pasuje')
                return redirect(f'/game/tasks/detail/{task.id}')
            if task.pc.motherboard.size != task.pc.power_supply.format_type:
                messages.error(request, 'Rozmiar zasilacza nie pasuje do plyty glownej')
                return redirect(f'/game/tasks/detail/{task.id}')
            if (task.pc.motherboard.sata_disc_slots + task.pc.motherboard.m2_disc_slots) < task.pc.disc.count():
                messages.error(request, 'Za duzo podlaczonych dyskow')
                return redirect(f'/game/tasks/detail/{task.id}')
            if task.pc.motherboard.ram_slots < task.pc.memory.count():
                messages.error(request, 'Za duzo podlaczonych kosci RAM')
                return redirect(f'/game/tasks/detail/{task.id}')
            if task.pc.motherboard.m2_disc_slots < task.pc.disc.filter(disc_format='m.2').count():
                messages.error(request, 'Za duzo podlaczonych dyskow typu M.2')
                return redirect(f'/game/tasks/detail/{task.id}')
            for memory in task.pc.memory.all():
                if memory.memory_type != task.pc.motherboard.memory_type:
                    messages.error(request, 'Niewlasciwy typ pamieci RAM')
                    return redirect(f'/game/tasks/detail/{task.id}')
            if task.pc.motherboard.sata_disc_slots < (
                    task.pc.disc.filter(disc_format='SSD').count() + task.pc.disc.filter(disc_format='HDD').count()):
                messages.error(request, 'Za duzo podpietych dyskow SATA')
                return redirect(f'/game/tasks/detail/{task.id}')
            messages.info(request, 'Wszystko jest okej. Mozna zakonczyc zlecenie!')
            return redirect(f'/game/tasks/detail/{task.id}')

        if 'give_back' in request.POST:
            if task.pc.processor.socket != task.pc.motherboard.socket \
                    or task.pc.motherboard.size != task.pc.power_supply.format_type \
                    or (task.pc.motherboard.sata_disc_slots + task.pc.motherboard.m2_disc_slots) < task.pc.disc.count() \
                    or task.pc.motherboard.ram_slots < task.pc.memory.count() \
                    or task.pc.motherboard.m2_disc_slots < task.pc.disc.filter(disc_format='m.2').count() \
                    or task.pc.motherboard.sata_disc_slots < (
                    task.pc.disc.filter(disc_format='SSD').count() + task.pc.disc.filter(disc_format='HDD').count()) \
                    or [memory for memory in task.pc.memory.all() if memory.memory_type == task.pc.motherboard.memory_type] == []:
                        level.xp -= 100
                        messages.error(request, 'Widocznie nie sprawdziles czy wszystko jest okej i klient nie byl zadowolony z uslugi :/')
                        return redirect(f'/game/tasks/')
            else:
                task_prize = 300
                wallet.money_amount += task_prize
                level.xp += 150
                level.save()
                wallet.save()
                task.delete()
                messages.info(request, f'Wykonano zadanie! Na twoje konto wplynelo: {task_prize}')
                return redirect('/game/tasks/')

        if 'fail' in request.POST:
            wallet.money_amount -= 100
            wallet.save()
            level.xp -= 50
            task.delete()
            messages.info(request, 'Odrzuciles zlecenie :/ Z twojego konta jako rekompensate zabrano 100 $ oraz 50 XP')
            return redirect('/game/tasks/')


#           CHANGE PARTS IN TASK

class ChangePartMotherboard(View):
    def get(self, request, task_id):
        motherboards = MotherBoard.objects.filter(user=request.user)
        return render(request, 'change_task_parts/change_motherboard.html', {'motherboards': motherboards})

    def post(self, request, task_id):
        motherboard_form = request.POST.get('motherboards')
        motherboard_to_install = MotherBoard.objects.get(name=motherboard_form, user=request.user)
        task_pc = Task.objects.get(id=task_id)
        part_to_storage = MotherBoard.objects.get(id=task_pc.pc.motherboard.pk)

        part_to_storage.user = request.user
        part_to_storage.save()
        motherboard_to_install.user = None
        motherboard_to_install.save()
        task_pc.pc.motherboard = motherboard_to_install
        task_pc.pc.save()
        return redirect(f'/game/tasks/detail/{task_id}')


class ChangePartsProcessor(View):
    def get(self, request, task_id):
        processors = Processor.objects.filter(user=request.user)
        return render(request, 'change_task_parts/change_processor.html', {'processors': processors})

    def post(self, request, task_id):
        processor_form = request.POST.get('processors')
        processor_to_install = Processor.objects.get(name=processor_form, user=request.user)
        task_pc = Task.objects.get(id=task_id)
        part_to_storage = Processor.objects.get(id=task_pc.pc.processor.pk)

        processor_to_install.user = None
        processor_to_install.save()
        part_to_storage.user = request.user
        part_to_storage.save()
        task_pc.pc.processor = processor_to_install
        task_pc.pc.save()
        return redirect(f'/game/tasks/detail/{task_id}')


class ChangePartsGraphics(View):
    def get(self, request, task_id):
        graphics = GraphicCard.objects.filter(user=request.user)
        return render(request, 'change_task_parts/change_graphic.html', {'graphics': graphics})

    def post(self, request, task_id):
        graphic_form = request.POST.get('graphics')
        graphic_to_install = GraphicCard.objects.get(name=graphic_form, user=request.user)
        task_pc = Task.objects.get(id=task_id)

        part_to_storage = GraphicCard.objects.get(id=task_pc.pc.graphic_card.pk)
        part_to_storage.user = request.user
        part_to_storage.save()
        graphic_to_install.user = None
        graphic_to_install.save()
        task_pc.pc.graphic_card = graphic_to_install
        task_pc.pc.save()
        return redirect(f'/game/tasks/detail/{task_id}')


class ChangePartsDisc(View):
    def get(self, request, task_id, disc_id):
        discs = Disc.objects.filter(user=request.user)
        return render(request, 'change_task_parts/change_disc.html', {'discs': discs})

    def post(self, request, task_id, disc_id):
        disc_form = request.POST.get('discs')
        disc_to_install = Disc.objects.get(name=disc_form, user=request.user)
        task_pc = Task.objects.get(id=task_id)
        disc_task = task_pc.pc.disc.get(id=disc_id)

        disc_to_install.user = None
        disc_to_install.save()
        disc_task.user = request.user
        disc_task.save()
        task_pc.pc.disc.remove(disc_task)
        task_pc.pc.disc.add(disc_to_install)
        task_pc.pc.save()
        return redirect(f'/game/tasks/detail/{task_id}')


class ChangePartMemory(View):
    def get(self, request, task_id, memory_id):
        memories = Memory.objects.filter(user=request.user)
        return render(request, 'change_task_parts/change_memory.html', {'memories': memories})

    def post(self, request, task_id, memory_id):
        memory_form = request.POST.get('memories')
        memory_to_install = Memory.objects.get(name=memory_form, user=request.user)
        task_pc = Task.objects.get(id=task_id)
        memory_task = task_pc.pc.memory.get(id=memory_id)

        memory_to_install.user = None
        memory_to_install.save()
        memory_task.user = request.user
        memory_task.save()
        task_pc.pc.memory.remove(memory_task)
        task_pc.pc.memory.add(memory_to_install)
        task_pc.pc.save()
        return redirect(f'/game/tasks/detail/{task_id}')


class ChangePartPowerSupply(View):
    def get(self, request, task_id):
        power_supplies = PowerSupply.objects.filter(user=request.user)
        return render(request, 'change_task_parts/change_power_supply.html', {'power_supplies': power_supplies})

    def post(self, request, task_id):
        power_supply_form = request.POST.get('power_supplies')
        power_supply_to_install = PowerSupply.objects.get(name=power_supply_form, user=request.user)
        task_pc = Task.objects.get(id=task_id)
        part_to_storage = PowerSupply.objects.get(id=task_pc.pc.power_supply.pk)

        power_supply_to_install.user = None
        power_supply_to_install.save()
        part_to_storage.user = request.user
        part_to_storage.save()
        task_pc.pc.power_supply = power_supply_to_install
        task_pc.pc.save()
        return redirect(f'/game/tasks/detail/{task_id}')


class ChangePartCase(View):
    def get(self, request, task_id):
        cases = Case.objects.filter(user=request.user)
        return render(request, 'change_task_parts/change_case.html', {'cases': cases})

    def post(self, request, task_id):
        case_form = request.POST.get('cases')
        case_to_install = Case.objects.get(name=case_form)
        task_pc = Task.objects.get(id=task_id)
        part_to_storage = Case.objects.get(id=task_pc.pc.case.pk)

        case_to_install.user = None
        case_to_install.save()
        part_to_storage.user = request.user
        part_to_storage.save()
        task_pc.pc.case = case_to_install
        task_pc.pc.save()
        return redirect(f'/game/tasks/detail/{task_id}')
