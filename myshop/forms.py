from django import forms  # импортируем модуль forms из фреймворка Django


class UserRegisterForm(forms.Form):  # определяем класс UserRegisterForm, который наследуется от forms.Form.
    # Этот класс будет представлять HTML-форму для регистрации пользователя
    username = forms.CharField(max_length=30, label="Введите логин")
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label="Введите пароль")  # для ввода пароля
    # использ. виджет PasswordInput, он скрывает вводимые символы, мин длина 8 симв.
    repeat_password = forms.CharField(widget=forms.PasswordInput, min_length=8, label="Повторите пароль")
    age = forms.IntegerField(min_value=0, max_value=100, label="Введите свой возраст")  # ставим ограничение га возраст
    # 100 лет