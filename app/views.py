from django.shortcuts import render
from .models import History, GraphHistory1, GraphHistory2
from authapp.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from app.withdraw import UserWithdraw
from app.deposit import UserDeposit
from app.slotmachine import UserSlotMachine
from django.views import generic
from rest_framework.views import APIView
from app.display_item import Display


@login_required
def deposit(request):

    # deposit function is that move to "game medals" in game window from "your wallet"
    if request.method == 'POST':
        # Get user_id
        current_user = request.user
        player_account = User.objects.get(email=current_user).pk
        #slot_number_id = int(request.POST['slot_id'])

        slot_user_deposit = UserDeposit()
        deposit_medal = slot_user_deposit.user_depoist(request)
        print(deposit_medal)


        return JsonResponse(deposit_medal)

    return render(request, 'app/game.html')


@login_required
def withdraw(request):
    if request.method == 'POST':
        # """ Get current user's id """
        # current_user = request.user
        # player_account = Profile.objects.get(user_id=current_user).pk
        """class分けの実験中"""
        slot_user_withdraw = UserWithdraw()
        withdraw_medal = slot_user_withdraw.user_withdraw(request)
        print(withdraw_medal)

        return JsonResponse(withdraw_medal)

    return render(request, 'app/game.html')


# class SlotMachine(LoginRequiredMixin, generic.TemplateView, APIView):
#         template_name = 'app/game.html'
#         print("aaa")
#         display_medals_games = Display()
#         print(display_medals_games)
#
#         def display(self):
#             display_initial = display_medals_games.display_initital(request)

            # return display_initial

        # def display(self, request):
        #     print("bbb")

@login_required
def slotmachine(request):
    if request.method == 'POST':
        slot_user_slotmachine = UserSlotMachine()
        slotmachine_game = slot_user_slotmachine.user_slotmachine(request)
        print(slotmachine_game)

        return JsonResponse(slotmachine_game)

     # game_counts = {'count': game_count1, 'medals': game_medal1, 'count2': game_count2, 'medals2': game_medal2,}
    return render(request, 'app/game.html')

# @login_required
# def slotmachine(request):
#
#     if request.method == 'POST':
#
#         slot_user_slotmachine = UserSlotMachine()
#         slotmachine_game = slot_user_slotmachine.user_slotmachine(request)
#         print(slotmachine_game)
#
#         return JsonResponse(slotmachine_game)

    # game_counts = {'count': game_count1, 'medals': game_medal1, 'count2': game_count2, 'medals2': game_medal2,}
    # return render(request, 'app/game.html')




class ChartData(LoginRequiredMixin, APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    print(authentication_classes)
    permission_classes = (IsAuthenticated,)
    print(permission_classes)


    def get(self, request, format=None):
        player_account = User.objects.get(email=request.user).pk
        game_history_label = GraphHistory1.objects.filter(user=player_account).order_by('-id')[:101].values_list('game', flat=True)

        game_history = GraphHistory1.objects.filter(user=player_account).order_by('-id')[:101].values_list('medal', flat=True)
        print("game_history:",game_history)
        game_history_label2 = GraphHistory2.objects.filter(user=player_account).order_by('-id')[:101].values_list('game', flat=True)
        game_history2 = GraphHistory2.objects.filter(user=player_account).order_by('-id')[:101].values_list('medal', flat=True)

        #qs_count = Player.objects.all().count()
        labels = []
        labels2 = []

        for it in game_history_label:
            labels.insert(0, it)

        for it in game_history_label2:
            labels2.insert(0, it)

        default_items = []
        default_items2 = []

        for it in game_history:
            default_items.insert(0, it)

        for it in game_history2:
            default_items2.insert(0, it)

        data = {
            "labels": labels,
            "defaults": default_items,
            "labels2": labels2,
            "defaults2": default_items2,
        }

        return JsonResponse(data)


class Aboutview(generic.TemplateView):
    template_name = 'app/yamadaslot.html'