from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from .models import SlotMachine, History, GraphHistory1, GraphHistory2
from authapp.models import User
from django.http import JsonResponse


class UserDeposit(LoginRequiredMixin, APIView):

    def user_depoist(self, request):
        global deposit_check

        current_user = request.user
        player_account = User.objects.get(email=current_user).pk
        #slot_number_id = int(request.POST['slot_id'])
        print(player_account)
        # Get slot_id
        slot_number_id = int(request.POST['slot_id'])
        print(slot_number_id)
        # Get total medals stored profile
        deposit_amount = User.objects.filter(
            pk=player_account).values_list('total_medals', flat=True)[0]
        print(deposit_amount)

        # Get user object
        deposit = User.objects.get(pk=player_account)

        if deposit_amount <= 0:
            message = "no"

            return JsonResponse({'dashboard_medals': deposit_amount, 'message': message})

        try:
            deposit_check = History.objects.filter(user=player_account, slot_number_id=slot_number_id).values_list(
                'deposit', flat=True).order_by('-id')[0]
            deposit_check = 1
            print("hehehe deposit check:", deposit_check)
        except:
            history_record = History()
            game_count = 0
            game_medal1 = 50
            history_record.user_id = player_account
            history_record.slot_number_id = slot_number_id
            history_record.history = game_count
            history_record.medals = game_medal1


        if deposit_amount < 50:
            hit1 = ""
            # print(deposit_amount)

            # Subtracting currently available medals from the total_medals field of Profile table (The result here is 0)
            deposit.total_medals -= deposit_amount
            # print(deposit.total_medals)
            # Save the Profile model
            deposit.save()

            # Get latest game count in history table of current user
            game_count = History.objects.filter(user=player_account, slot_number_id=slot_number_id).values_list(
                'history', flat=True).order_by('-id')[0]
            # Get latest number of medal in history table of current user
            game_medal1 = History.objects.filter(user=player_account, slot_number_id=slot_number_id).values_list(
                'medals', flat=True).order_by('-id')[0]
            # To add latest number of medal in History table(your wallet in game window) from all medals in Profile table(because deposit amount is less than 50)
            game_medal1 += deposit_amount
            # print(game_medal1)

            history_record = History()
            # Adding game count to history field(game counter) in History table
            history_record.history = game_count
            history_record.medals = game_medal1
            history_record.slot_number_id = slot_number_id
            history_record.user_id = player_account
            history_record.deposit = deposit_check
            history_record.save()

            deposit_amount = 0

            return JsonResponse({'dashboard_medals': deposit_amount, 'medals': game_medal1, 'hit1': hit1, "player_account": player_account})

        # 通常の処理
        # subtract 50 from user wallet and add 50 medal in slot
        deposit_amount -= 50
        deposit.total_medals = deposit_amount
        deposit.save()

        # playerのidと、slotのidが存在した場合の処理
        if History.objects.filter(user=player_account, slot_number_id=slot_number_id).exists():
            game_count = History.objects.filter(user=player_account, slot_number_id=slot_number_id).values_list('history',
                                                                                                                   flat=True).order_by(
                '-id')[0]
            game_medal1 = History.objects.filter(user=player_account, slot_number_id=slot_number_id).values_list('medals',
                                                                                                                    flat=True).order_by(
                '-id')[0]
            game_medal1 += 50
            history_record = History()
            history_record.history = game_count
            history_record.medals = game_medal1
            history_record.slot_number_id = slot_number_id
            history_record.user_id = player_account
            history_record.deposit = deposit_check

        # playerのidと、slotのidが存在しない場合の処理
        else:
            history_record = History()
            game_count = 0
            game_medal1 = 50
            history_record.user_id = player_account
            history_record.slot_number_id = slot_number_id
            history_record.history = game_count
            history_record.medals = game_medal1

        history_record.save()
        message = ""

        context = {'dashboard_medals': deposit_amount, 'medals': game_medal1, 'message': message, "player_account": player_account}

        return context