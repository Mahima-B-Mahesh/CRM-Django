from django import template

register = template.Library()


@register.simple_tag
def check_user_role(request, roles):
    """
    Check if the user has any of the specified roles.

    :param user: The user object to check.
    :param roles: A variable number of role strings to check against the user's roles.
    :return: True if the user has at least one of the specified roles, otherwise False.
    """

    roles = roles.split(",")
    allow = False
    if request.user.role in roles:
        allow = True

    return allow
