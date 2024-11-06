from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import UserRegisterForm
from .models import Buyer
from .models import Medicine


# Главная страница
def home(request):
    return render(request, 'myshop/platform.html')


# Магазин
def shop_medicines(request):
    # Получение всех игр из базы данных
    products = Medicine.objects.all()  # Получаем все записи из модели Game

    # Передача словаря через параметр context
    return render(request, 'myshop/medicines.html', {'products': products})


# Корзина
def cart(request):
    # информация о корзине
    cart_info = "Ваша корзина пока пуста. Добавьте товары для продолжения."
    return render(request, 'myshop/cart.html', {'cart_info': cart_info})


# функция, которая будет обрабатывать запросы на регистрацию пользователя с использованием формы Django
def sign(request):
    info = {}  # создаем словарь хранения инфы для передачи в шаблон
    if request.method == 'POST':  # если метод запроса - POST, т.е. отправка формы
        form = UserRegisterForm(request.POST)  # создаем экземпляр нашей формы с переданными данными (request.POST)
        if form.is_valid():  # если форма валидна, то извлекаем данные из полей формы словаря cleaned_data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            # Обработка ошибок
            if Buyer.objects.filter(name=username).exists():  # проверяем, существует ли пользователь с таким именем
                info['error'] = 'Пользователь уже существует'
            elif password != repeat_password:
                info['error'] = 'Пароли не совпадают'
            elif age < 18:
                info['error'] = 'Вы должны быть старше 18 лет'
            else:
                # Успешная регистрация
                Buyer.objects.create(name=username, balance=0.00, age=age)  # создаем нового покупателя
                info['success'] = f'Приветствуем, {username}!'  # добавляем в словарь сообщение об успешной регистрации
        else:  # если форма невалидна, в словарь info добавляется сообщение об ошибке
            info['error'] = 'Некорректно заполнена форма'
    else:  # если метод запроса GET, создается пустой экземпляр формы UserRegisterForm
        form = UserRegisterForm()

    info['form'] = form
    return render(request, 'myshop/registration_page.html', info)
