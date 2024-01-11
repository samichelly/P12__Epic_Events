from models import User_role


def has_permission(context, allowed_roles):
    # print("context")
    # print(context.user.role.name)
    if context.user.role.name in allowed_roles:
        return True
    else:
        print("Permission denied. You don't have the required role.")
        return False


def read_permission(context):
    return has_permission(context, ["sales", "support", "management"])


def create_customer_permission(context):
    return has_permission(context, ["sales"])


def create_event_permission(context):
    return has_permission(context, ["sales"])


def create_contract_permission(context):
    return has_permission(context, ["management"])


def create_contract_permission(context):
    return has_permission(context, ["management"])


def update_event_permission(context):
    return has_permission(context, ["management"])
