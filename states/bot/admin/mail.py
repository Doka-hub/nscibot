from typing import Union

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext


class MailState(StatesGroup):
    material_format_id = State()

    image_id = State()
    video_id = State()

    title = State()
    text = State()

    button1 = State()
    button2 = State()
    button3 = State()
    button4 = State()

    time_to_mail = State()

    message_template__name = State()

    @classmethod
    async def set_button_state_by_number(cls, number: Union[int, str]):
        number = int(number)
        (
            await cls.button1.set() if number == 1 else
            await cls.button2.set() if number == 2 else
            await cls.button3.set() if number == 3 else
            await cls.button4.set()
        )

    @classmethod
    async def update_button_data_by_state(cls, state: FSMContext, button: str):
        number = int((await state.get_state()).replace('MailState:button', ''))
        (
            await state.update_data(button1=button) if number == 1 else
            await state.update_data(button2=button) if number == 2 else
            await state.update_data(button3=button) if number == 3 else
            await state.update_data(button4=button)
        )
