from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from .models import History, GraphHistory1, GraphHistory2
from authapp.models import User
from django.http import JsonResponse


class UserWithdraw(LoginRequiredMixin, APIView):
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)

    def user_withdraw(self, request):
        current_user = request.user
        player_account = User.objects.get(email=current_user).pk
        print("player_account:", player_account)

        """ Get current slot id """
        slot_number_id = int(request.POST['slot_id'])
        """ Get latest object for current user（It is important!）"""
        history_record = History.objects.filter(user=player_account, slot_number_id=slot_number_id).last()
        """ Making new instance(record) when do save() by setting None """
        history_record.id = None

        """ Get Profile object for save """
        deposit = User.objects.get(pk=player_account)
        """ Get total_medals in Profile object """
        deposit_amount = User.objects.filter(pk=player_account).values_list('total_medals', flat=True)[0]
        """ Get total_game_numbers in Profile object """
        deposit_total_games = User.objects.filter(pk=player_account).values_list('total_game_number', flat=True)[0]

        """ History の今アクセスしているユーザーの最新の値のリストを全て取得（こうしないと、インスタンスに保存するときにおかしくなる）"""
        history_reset = History.objects.filter(
            user=player_account, slot_number_id=slot_number_id).values_list(flat=True).order_by('-id')[0]

        """ アクセスしているユーザーのHistory内の最新のメダル情報を取得 """
        game_medal1 = History.objects.filter(user=player_account, slot_number_id=slot_number_id).values_list(
            'medals', flat=True).order_by('-id')[0]

        """ アクセスしているユーザーのHistory内の最新のゲーム数を取得 """
        game_history1 = History.objects.filter(user=player_account, slot_number_id=slot_number_id).values_list(
            'history', flat=True).order_by('-id')[0]

        """ Game count のreset用 """
        game_count1 = History.objects.filter(user=player_account, slot_number_id=slot_number_id).values_list(
            'history', flat=True).order_by('-id')[0]
        """ Profileオブジェクトのtotal medalsに、今のslotのmedalを合算（historyから取得）"""
        deposit_amount += game_medal1

        """ Plofileオブジェクトのtotal medalsに、上で合算した数値を収納 """
        deposit.total_medals = deposit_amount

        """ Profileオブジェクトのtotal_game_numberに、２つのゲームの合算を取得 """
        deposit_total_games += game_history1
        deposit.total_game_number = deposit_total_games
        deposit.save()

        """ reset用の数値 """
        game_medal1 = 0
        game_history1 = 0

        """ 最新のhistory objectのmedalsに、上でresetした数値"0"を代入 """
        history_record.medals = game_medal1
        """ 最新のhistory objectのhisoryに、上でresetした数値"0"を代入 """
        history_record.history = game_history1
        history_record.save()

        if slot_number_id == 1:
            GraphHistory1.objects.filter(user=player_account).delete()

        if slot_number_id == 2:
            # GraphHistory2.objects.all().delete()
            GraphHistory2.objects.filter(user=player_account).delete()

        context = {'dashboard_medals': deposit_amount, 'medals': game_medal1, 'count': game_history1, 'total_games': deposit_total_games}

        return context