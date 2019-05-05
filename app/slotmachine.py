from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from .models import History, GraphHistory1, GraphHistory2
from django.http import JsonResponse
from authapp.models import User
from app.display_item import RandomItem, MakeRandom
import random
from app.deposit import UserDeposit


class UserSlotMachine(LoginRequiredMixin, APIView):


    def user_slotmachine(self, request):
        global deposit_check
        global graph_deposit_check

        num3 = random.randint(0, 9999)
        num4 = random.randint(0, 9999)

        slot_id = int(request._post['slot_id'])
        history_record = History()
        print(slot_id)
        # get user_id
        current_user = request.user
        #current_id = Profile.objects.filter(user_id=current_user)
        player_account = User.objects.get(email=current_user).pk

        game_count1 = History.objects.filter(user_id=player_account, slot_number_id=slot_id).values_list('history',
                                                                                                         flat=True).order_by(
            '-id')[0]

        game_medal1 = History.objects.filter(user_id=player_account, slot_number_id=slot_id).values_list('medals',
                                                                                                         flat=True).order_by(
            '-id')[0]

        hit1 = False

        """get game mode and if medal empty(game mode connect to generate random)"""
        get_mode_value = int(request.POST['game_mode'])
        message = None

        """Check turbo mode"""
        check_turbo1 = User.objects.get(email=current_user).turbo_slot1
        check_turbo2 = User.objects.get(email=current_user).turbo_slot2
        print(check_turbo1)
        print(check_turbo2)

        """check deposit"""
        deposit_check = History.objects.filter(user_id=player_account, slot_number_id=slot_id).values_list(
            'deposit', flat=True).order_by('-id')[0]
        if deposit_check == 1:
            graph_deposit_check = 1
            deposit_check = 0
            print("graph_deposit_check:",graph_deposit_check)
        else:
            graph_deposit_check = 0

        if check_turbo1:
            get_mode_value = 4

        if check_turbo2:
            get_mode_value = 5


        if game_medal1 < 3:
            message = "Empty!"
            hit1 = "Empty"

            context = {'count': game_count1, 'medals': game_medal1, 'message': message, "hit1": hit1, "graph_deposit_check":graph_deposit_check}

            return context

        print("now:",get_mode_value)
        if get_mode_value == 1:
            make_random = MakeRandom()
            game_random = make_random.make_random95(1)

        if get_mode_value == 2:
            make_random = MakeRandom()
            game_random = make_random.make_random95(2)

        if get_mode_value == 3:
            make_random = MakeRandom()
            game_random = make_random.make_random95(3)

        if get_mode_value == 4:
            make_random = MakeRandom()
            game_random = make_random.make_random95(4)

        if get_mode_value == 5:
            make_random = MakeRandom()
            #user_info_turbo = make_random.get_user_info(request)
            game_random = make_random.get_user_info(request)

        num_seven = game_random["num_seven"]
        num_bar = game_random["num_bar"]
        num_bell = game_random["num_bell"]

        for num in num_seven:

            if num3 == num:
                game_medal1 += 300
                hit1 = "Seven"

        for num in num_bar:

            if num3 == num:
                game_medal1 += 150
                hit1 = "Bar"

        for num in num_bell:

            if num3 == num:
                game_medal1 += 30
                hit1 = "Bell"


        """ Here we are creating a character of an outlier."""
        miss_item = RandomItem()
        miss_item_list = miss_item.random_item()
        # print(miss_item_list)
        first_item = miss_item_list[0]
        second_item = miss_item_list[1]
        third_item = miss_item_list[2]


        if slot_id == 1:

            """ Making new instance(record) from model GraphHistory"""
            graphistory = GraphHistory1()
            """ Get user_id for graph of slot_id 1 """
            #graphistory.user_id = player_account

            game_count1 += 1
            history_record.history = game_count1
            graphistory.game = game_count1
            game_medal1 -= 3

            # Save the graph within the game display.

            graphistory.medal = game_medal1
            graphistory.slot = slot_id
            graphistory.user_id = player_account
            graphistory.save()


        if slot_id == 2:

            graphistory2 = GraphHistory2()
            game_count1 += 1
            history_record.history = game_count1
            graphistory2.game = game_count1
            game_medal1 -= 3

            # Process related to the graph within the game display.
            graphistory2.medal = game_medal1
            graphistory2.slot = slot_id
            graphistory2.user_id = player_account
            graphistory2.save()

        # ゲーム履歴に関わる処理　save game medal
        history_record.slot_number_id = slot_id
        # print(history_record.slot_number_id)
        history_record.medals = game_medal1
        history_record.user_id = player_account
        # print(history_record.user_id)
        history_record.turbo2 = game_random["turbo"]
        history_record.save()


        context = {'count': game_count1, 'medals': game_medal1, 'hit1': hit1, "message": message,
                             "first_item": first_item, "second_item": second_item, "third_item": third_item,
                   "graph_deposit_check": graph_deposit_check}

        return context




