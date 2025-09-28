from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
# States
from .admin_states import Xabar_yuborish
# Database funk
from database_funk.users_funk import get_all_user_ids

router = Router()

@router.message(F.text == "✉️ Xabar yuborish")
async def xabar_yuborish_handler(message: Message, state: FSMContext):
    await message.answer("Xabar yuborish uchun xabarni kiriting!")
    await state.set_state(Xabar_yuborish.xabar)

@router.message(Xabar_yuborish.xabar)
async def xabar_handler(message: Message, state: FSMContext):
    xabar = message.text
    user_ids = get_all_user_ids()
    await message.answer(f"Xabar yuborilmoqda... {len(user_ids)} ta foydalanuvchiga")
    for user_id in user_ids:
        try:
            await message.bot.send_message(user_id, xabar)
        except Exception as e:
            print(f"Xabar yuborishda xatolik: {e}")
    await message.answer("Xabar yuborildi!")
    await state.clear()