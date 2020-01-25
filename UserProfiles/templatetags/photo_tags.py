from django import template

register = template.Library()

@register.filter(name='split')
def split(str, key):
    return str.split(key)

@register.filter
def get_by_index(a, i):
    return a[i]


# @register.simple_tag
@register.filter
def is_user_in_contacts(user, current_user):
    # request
    # print(
    #     current_user.friends.filter(user=user),
    #     current_user.friends.all()
    # )
    return current_user.friends.first().friends.filter(user=user).exists()
    return current_user.friends.filter(user=user).exists()
    # return current_user.friends.filter(user=user).exists()