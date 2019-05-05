from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest, request
from django.shortcuts import redirect, resolve_url
from django.template.loader import get_template
from django.views import generic
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from pro43_game5 import settings
from .forms import LoginForm, UserCreateForm, UserUpdateForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from django.urls import reverse_lazy
from app.models import History
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect



User = get_user_model()


class Top(generic.TemplateView):
    template_name = 'authapp/top.html'


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'authapp/login.html'


# class Logout(LoginRequiredMixin, LogoutView):
#     """ログアウトページ"""
#     template_name = 'authapp/logged2_out.html'
@login_required
def logout_view(request):

    current_user = request.user
    player_account = User.objects.get(email=current_user).pk
    try:
        logout_medal1 = History.objects.filter(user = player_account, slot_number_id=1).values_list('medals', flat=True).order_by('-id')[0]
    except:
        logout_medal1 = 0
    try:
        logout_medal2 = History.objects.filter(user = player_account, slot_number_id=2).values_list('medals', flat=True).order_by('-id')[0]
    except:
        logout_medal2 = 0
    print(logout_medal1)

    if logout_medal1 == 0 and logout_medal2 == 0:
        logout(request)
        return render(request, "authapp/logged2_out.html")

    else:
        messages.info(request, 'your medal is remained in SLOT. please withdraw.')
        return redirect("/")




class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'authapp/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        #'token': dumps(user.pk),これで、分かりにくいアクティベーションurlが作れる。
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject_template = get_template('authapp/mail_template/create/subject.txt')
        subject = subject_template.render(context)

        message_template = get_template('authapp/mail_template/create/message.txt')
        message = message_template.render(context)

        user.email_user(subject, message)
        return redirect('authapp:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'authapp/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'authapp/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60 * 60 * 24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoenNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = 'authapp/user_detail.html'


class UserUpdate(OnlyYouMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'authapp/user_form.html'

    def get_success_url(self):
        # messages.success(request, 'アップデートに成功しました。')
        return resolve_url('authapp:user_detail', pk=self.kwargs['pk'])


class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('authapp:password_change_done')
    template_name = 'authapp/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'authapp/password_change_done.html'


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'authapp/mail_template/reset/subject.txt'
    email_template_name = 'authapp/mail_template/reset/message.txt'
    template_name = 'authapp/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('authapp:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'authapp/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('register:password_reset_complete')
    template_name = 'authapp/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'authapp/password_reset_complete.html'



@login_required(login_url = "/login")
def dashboard(request):
    # get user_id
    current_user = request.user
    # print(current_user)
    player_account = User.objects.get(email=current_user).pk
    print(player_account)
    # get user_id and
    my_wallet1 =  User.objects.filter(email=current_user).values_list('total_medals', flat=True)[0]
    print(my_wallet1)
    my_total_games1 = User.objects.filter(email=current_user).values_list('total_game_number', flat=True)[0]
    print(my_total_games1)
    #initial Medal in SLOT1 medal window
    # current_user = request.user
    # player_account = User.objects.get(email=current_user).pk

    try:
        game_medal1 = History.objects.filter(user=player_account, slot_number_id=1).values_list('medals', flat=True).order_by('-id')[0]
    except:
        game_medal1 = 0

    try:
        game_count1 = History.objects.filter(user=player_account, slot_number_id=1).values_list('history', flat=True).order_by('-id')[0]
    except:
        game_count1 = 0

    try:
        game_medal2 = History.objects.filter(user=player_account, slot_number_id=2).values_list('medals', flat=True).order_by('-id')[0]
    except:
        game_medal2 = 0

    try:
        game_count2 = History.objects.filter(user=player_account, slot_number_id=2).values_list('history', flat=True).order_by('-id')[0]
    except:
        game_count2 = 0

    return render(request, 'app/game.html', {'section': 'dashboard',
                                                  'dashboard_medals': my_wallet1,
                                                  'total_games': my_total_games1,
                                                  'game_medal1': game_medal1,
                                                  'count': game_count1,
                                                  'dashboard_medals2': game_medal2,
                                                  'dashboard_count2': game_count2,
                                                  })