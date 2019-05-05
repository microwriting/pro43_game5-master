import random
#from .views import slotmachine
from .models import History
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from authapp.models import User


class RandomItem:

    def random_item(self):

        rand_number = []
        display_item = []
        a = [1,1,1]
        b = [2,2,2]
        c = [3,3,3]

        for i in range(3):
            rand_number.append(random.randrange(1, 4))
            print(rand_number)

        if rand_number == a or rand_number == b or rand_number == c:
            rand_number = random.sample(range(1,4),3)
            print(rand_number)

        if rand_number[0] == 1:
            display_item.append("app/images/seven_single")
        elif rand_number[0] == 2:
            display_item.append("app/images/bar_single")
        elif rand_number[0] == 3:
            display_item.append("app/images/bell_single")

        if rand_number[1] == 1:
            display_item.append("app/images/seven_single")
        elif rand_number[1] == 2:
            display_item.append("app/images/bar_single")
        elif rand_number[1] == 3:
            display_item.append("app/images/bell_single")

        if rand_number[2] == 1:
            display_item.append("app/images/seven_single")
        elif rand_number[2] == 2:
            display_item.append("app/images/bar_single")
        elif rand_number[2] == 3:
            display_item.append("app/images/bell_single")

        return display_item


class MakeRandom(LoginRequiredMixin, APIView):


    def get_user_info(self, request):
        global turbo2_count
        slot_id = int(request._post['slot_id'])
        current_user = request.user
        player_account = User.objects.get(user_id=current_user).pk

        try:
            turbo2_count = History.objects.filter(user_id=player_account, slot_number_id=slot_id).values_list('turbo2',
                                                                                                         flat=True).order_by(
            '-id')[0]
            #print('turbo2', turbo2_count)
        except:
            new_record = History()
            new_record.history = 0
            new_record.slot_number_id = slot_id
            new_record.medals = 100
            new_record.turbo2 = 0
            new_record.user = player_account
            new_record.save()

        turbo_mode2 = self.make_random95(5)
        turbo_number = turbo_mode2

        return turbo_number

    # a = 0

    # def __init__(self):
    #     self.a = 0
    #
    # def counter(self ,a):
    #     self.a += 1
    #     b = self.a
    #
    #     return b


    def make_random95(self, payout):

        global turbo2_count
        num_seven = []
        num_bar = []
        num_bell = []
        num_game = []

        num_game = random.sample(range(10000), k=10000)

        if payout == 1:

            num_seven = num_game[0:47]
            num_bar = num_game[48:95]
            num_bell = num_game[96:335]
            turbo2_count = 0


        if payout == 2:

            num_seven = num_game[0:49]
            num_bar = num_game[50:99]
            num_bell = num_game[100:349]
            turbo2_count = 0


        if payout == 3:

            num_seven = num_game[0:52]
            num_bar = num_game[53:105]
            num_bell = num_game[106:369]
            turbo2_count = 0


        if payout == 4:

            num_seven = num_game[0:12]
            num_bar = num_game[13:62]
            num_bell = num_game[63:1062]
            turbo2_count = 0


        if payout == 5:

            print('hehehehe:', turbo2_count)
            turbo2_count += 9
            num_seven = num_game[0: 52]
            num_bar = num_game[53:105]
            print('hehehehe part2:',len(num_bar))
            num_bell = num_game[106:106 + turbo2_count]

            if turbo2_count > 900:
                turbo2_count = 0

        context = {"num_seven": num_seven, "num_bar": num_bar, "num_bell": num_bell, "turbo": turbo2_count}
        return context


# class TurboMode1(MakeRandom):
#
#     num_seven = []
#     num_bar = []
#     num_bell = []
#     num_game = []
#
#     def make_random95(self, payout):
#
#         num_game = random.sample(range(10000), k=10000)
#
#         num_seven = num_game[0:12]
#         num_bar = num_game[13:62]
#         num_bell = num_game[63:687]
#
#         context = {"num_seven":num_seven, "num_bar":num_bar, "num_bell":num_bell}
#
#         return context

class Display(LoginRequiredMixin, APIView):

    def display_initital(self,request):
        current_user = request.user
        print(current_user)
        player_account = User.objects.get(user_id=current_user).pk
        print(player_account)
        your_wallet = User.objects.get(user_id=player_account).total_medals
        print(your_wallet)
        context = {"dashboard_medals": your_wallet}

        return context