from django.urls import path
from game.views import GamePageView, CheckStorageView, AddPartView, AddPartMotherBoardView, AddPartProcessorView, \
    AddPartGraphicCardView, AddPartDiscView, AddPartMemoryView, AddPartPowerSupplyView, AddPartCaseView, \
    CreatePCView, DeletePCView
from game.views import MotherboardPartDetailView, ProcessorDetailView, GraphicCardPartDetailView, DiscDetailView, \
    MemoryDetailView, PowerSupplyDetailView, CaseDetailView, PCDetailView
from game.views import UpdateMotherboardView, UpdateProcessorView, UpdateGraphicView, UpdateDiscView, UpdateMemoryView, \
    UpdatePowerSupplyView, UpdateCaseView
from game.views import DeleteMotherboard, DeleteProcessor, DeleteGraphics, DeleteMemory, DeleteDisc, DeletePowerSupply, \
    DeleteCase
from game.views import CheckTaskView, TaskConfirm, TaskDetail
from game.views import ChangePartMotherboard, ChangePartsProcessor, ChangePartsGraphics, ChangePartsDisc, ChangePartMemory,\
    ChangePartPowerSupply, ChangePartCase

urlpatterns = [
    #   GAME MAIN
    path('', GamePageView.as_view()),
    path('storage/', CheckStorageView.as_view()),
    #   PARTS DETAILS
    path('motherboard_details/<int:pk>', MotherboardPartDetailView.as_view()),
    path('processor_details/<int:pk>', ProcessorDetailView.as_view()),
    path('graphic_card_details/<int:pk>', GraphicCardPartDetailView.as_view()),
    path('memory_details/<int:pk>', MemoryDetailView.as_view()),
    path('disc_details/<int:pk>', DiscDetailView.as_view()),
    path('power_supply_details/<int:pk>', PowerSupplyDetailView.as_view()),
    path('case_details/<int:pk>', CaseDetailView.as_view()),
    #   ADD PARTS
    path('addpart/', AddPartView.as_view()),
    path('addpart/motherboard/', AddPartMotherBoardView.as_view()),
    path('addpart/processor/', AddPartProcessorView.as_view()),
    path('addpart/graphic_card/', AddPartGraphicCardView.as_view()),
    path('addpart/memory/', AddPartMemoryView.as_view()),
    path('addpart/disc/', AddPartDiscView.as_view()),
    path('addpart/power_supply/', AddPartPowerSupplyView.as_view()),
    path('addpart/case/', AddPartCaseView.as_view()),
    #   PC
    path('create_pc/', CreatePCView.as_view()),
    path('delete_pc/<int:pk>', DeletePCView.as_view()),
    path('pc_details/<int:pk>', PCDetailView.as_view()),
    #   UPDATE PART
    path('storage/updatepart/motherboard/<int:pk>', UpdateMotherboardView.as_view()),
    path('storage/updatepart/processor/<int:pk>', UpdateProcessorView.as_view()),
    path('storage/updatepart/graphic/<int:pk>', UpdateGraphicView.as_view()),
    path('storage/updatepart/memory/<int:pk>', UpdateMemoryView.as_view()),
    path('storage/updatepart/disc/<int:pk>', UpdateDiscView.as_view()),
    path('storage/updatepart/power_supply/<int:pk>', UpdatePowerSupplyView.as_view()),
    path('storage/updatepart/case/<int:pk>', UpdateCaseView.as_view()),
    #   SELL PARTS
    path('storage/sellpart/motherboard/<int:pk>', DeleteMotherboard.as_view()),
    path('storage/sellpart/processor/<int:pk>', DeleteProcessor.as_view()),
    path('storage/sellpart/graphics/<int:pk>', DeleteGraphics.as_view()),
    path('storage/sellpart/memory/<int:pk>', DeleteMemory.as_view()),
    path('storage/sellpart/disc/<int:pk>', DeleteDisc.as_view()),
    path('storage/sellpart/power_supply/<int:pk>', DeletePowerSupply.as_view()),
    path('storage/sellpart/case/<int:pk>', DeleteCase.as_view()),
    #   TASKS
    path('tasks/', CheckTaskView.as_view()),
    path('tasks/confirm/<int:pk>', TaskConfirm.as_view()),
    path('tasks/detail/<int:pk>', TaskDetail.as_view()),
    #   CHANGE PARTS TASK
    path('tasks/change_motherboard/<int:task_id>', ChangePartMotherboard.as_view()),
    path('tasks/change_processor/<int:task_id>', ChangePartsProcessor.as_view()),
    path('tasks/change_graphic/<int:task_id>', ChangePartsGraphics.as_view()),
    path('tasks/change_disc/<int:task_id>/<int:disc_id>', ChangePartsDisc.as_view()),
    path('tasks/change_memory/<int:task_id>/<int:memory_id>', ChangePartMemory.as_view()),
    path('tasks/change_power_supply/<int:task_id>', ChangePartPowerSupply.as_view()),
    path('tasks/change_case/<int:task_id>', ChangePartCase.as_view()),
]