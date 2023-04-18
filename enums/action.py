from enum import Enum

class Action(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    CHANGE_RECEIVING_LIST_STATUS = "change_receiving_list_status"
    CHANGE_PRODUCT_CATEGORY = "change_product_category"
