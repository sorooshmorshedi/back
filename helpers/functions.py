def get_current_user():
    from helpers.middlewares.ModifyRequestMiddleware import ModifyRequestMiddleware

    return ModifyRequestMiddleware.user
