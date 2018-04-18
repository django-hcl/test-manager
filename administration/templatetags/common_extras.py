from django import template
from administration.models import Customuser, Test, Testsection


register = template.Library()

@register.filter()
def is_admin(username):
    user_lists = Customuser.objects.filter(custom_userid=username).values('custom_roleid')
    if user_lists and user_lists[0]['custom_roleid'] == 1:
        return True
    else:
        return False



