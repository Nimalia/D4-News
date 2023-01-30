

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from newsandart.models import Author
from django.contrib.auth.models import User


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        author_group = Group.objects.get(name="author group")
        user.groups.add(author_group)
        Author.objects.create(authorUser=User.objects.get(pk=user.id))
        return user