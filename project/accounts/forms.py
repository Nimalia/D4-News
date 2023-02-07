
from django.core.mail import EmailMultiAlternatives
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from newsandart.models import Author
from django.contrib.auth.models import User

#
# class CustomSignupForm(SignupForm):
#     def save(self, request):
#         user = super().save(request)
#         author_group = Group.objects.get(name="author group")
#         user.groups.add(author_group)
#         Author.objects.create(authorUser=User.objects.get(pk=user.id))
#         return user

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        author_group = Group.objects.get(name="author group")
        user.groups.add(author_group)
        Author.objects.create(authorUser=User.objects.get(pk=user.id))
        # subject = 'Добро пожаловать в наш интернет-магазин!'
        # text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        # html = (
        #     f'<b>{user.username}</b>, вы успешно зарегистрировались на '
        #     f'<a href="http://127.0.0.1:8003/news">сайте</a>!'
        # )
        # msg = EmailMultiAlternatives(
        #     subject=subject, body=text, from_email=None, to=[user.email]
        # )
        # msg.attach_alternative(html, "text/html")
        # msg.send()

        return user