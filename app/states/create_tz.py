from aiogram.fsm.state import State, StatesGroup


class CreateTZ(StatesGroup):
    waiting_description = State()
    answering_questions = State()
    generating = State()