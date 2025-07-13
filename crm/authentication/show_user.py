def show_user_name(request):
    """
    Function to display the username of the logged-in user.
    """
    user_name = request.user.username

    name = user_name.split("@")[0]

    return {"name_of_user": name}
