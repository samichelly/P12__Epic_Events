from models import User_role


def has_permission(context, allowed_roles):
    if context.user.role.name in allowed_roles:
        return True
    else:
        print("Permission denied. You don't have the required role.")
        return False


def read_permission(context):
    return has_permission(context, ["sales", "support", "management"])


def sales_permission(context):
    return has_permission(context, ["sales"])


# def create_event_permission(context):
#     return has_permission(context, ["sales"])


def management_permission(context):
    return has_permission(context, ["management"])


# def management_permission(context):
#     return has_permission(context, ["management"])


# def management_permission(context):
#     return has_permission(context, ["management"])
