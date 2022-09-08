from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, View

from wega_auth.forms import LoginUserForm, RegisterUserForm
from project.utils import DataMixin

from django.contrib.auth import authenticate, login, logout
from django.conf import settings



class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'wega_auth/register.html'
    success_url = '/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))
    def post(self, request, *args, **kwargs):
        r = super(RegisterUser, self).post(request, *args, **kwargs)
        if self.object:
            login(request, self.object)
            return redirect(reverse_lazy('profile_index'))
        return r
            

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
class LoginUser(DataMixin, View):
    form_class = LoginUserForm
    template_name = 'wega_auth/register.html'
    success_url = reverse_lazy('profile_index')
    http_method_names = ['get', 'post']
    queryset = User.objects.all()
    
    def get(self, request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            if settings.WEGA_DEFAULT_USER and settings.WEGA_DEFAULT_PASSWORD:
                user = authenticate(request, username=settings.WEGA_DEFAULT_USER, password=settings.WEGA_DEFAULT_PASSWORD)
                if user:
                    login(request, user)
                    return redirect(self.success_url)
            
        context = self.get_user_context(title="Авторизация", btn_name='Войти')
        context['form'] = self.form_class
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if not user:
            print(f'error login user {user}  ip {get_client_ip(request)} ')
            context = self.get_user_context(title="Авторизация", btn_name='Войти')
            context['form'] = self.form_class(request.POST)
            context['form'].is_valid()
            from django.forms.utils import ErrorList
            errors = context['form']._errors.setdefault("email", ErrorList())
            errors.append('Имя или пароль невалидны')
            return render(request, template_name=self.template_name, context=context)
        
        else:
            print(f'login user {user}  ip {get_client_ip(request)} ')
            login(request, user)
            return redirect(self.success_url)


class LogoutUser(DataMixin, View):
    template_name = 'wega_auth/register.html'
    success_url = reverse_lazy('profile_index')
    http_method_names = ['get', 'post']
    queryset = User.objects.all()
    
    def get(self, request, *args, **kwargs):
        context = self.get_user_context(title="Выход", btn_name='Выход')
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
        
        
        

