from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import View


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
     
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None;
        if (not customer.first_name):
            error_message = "Primeiro nome necessário "
        elif len(customer.first_name) < 4:
            error_message = 'Primeiro nome deve ter no minimo 1 caracteres'
        elif not customer.last_name:
            error_message = 'Sobrenome necessário'
        elif len(customer.last_name) < 4:
            error_message = 'Sobrenome deve conter 2 caracteres no minimo'
        elif not customer.phone:
            error_message = 'Numero de telefone necessario'
        elif len(customer.phone) < 10:
            error_message = 'Numero de telefone precisa de 10 numeros'
        elif len(customer.password) < 6:
            error_message = 'Senha necessita de 6 caracteres no minimo'
        elif len(customer.email) < 5:
            error_message = 'Email precisa ter 5 caracteres'
        elif customer.isExists():
            error_message = 'Email já registrado'
       

        return error_message
