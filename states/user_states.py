from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    client = State()
    phone = State()
    cost = State()
    tariff = State()
    tariff_limit = State()
    count_of_branches = State()
    billing_cycle = State()
    verify = State()


    order = State()
    order_location = State()
    complaint = State()
    complaint_location = State()
    client = State()
    client_location = State()
