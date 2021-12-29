import config 
import logging
from random import randint
import requests
import datetime
from pprint import pprint
from aiogram import types, md
from aiogram.dispatcher.filters import BoundFilter
from aiogram.utils.exceptions import CantRestrictSelf, CantRestrictChatOwner
from aiogram.dispatcher import filters

class IsAdminFilter(BoundFilter):
	key = "is_admin"

	def __init__(self, is_admin):
		self.is_admin = is_admin

	async def check(self, message: types.Message):
		member = await bot.get_chat_member(message.chat.id, message.from_user.id)
		return member.is_chat_admin()
from aiogram import Bot, executor, Dispatcher, types
from aiogram.utils.exceptions import ChatAdminRequired
#bot = Bot(config.TOKEN)
#dp = Dispatcher(bot)
#from filters import IsAdminFilter


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

dp.filters_factory.bind(IsAdminFilter)


@dp.message_handler(commands=["start", "пинг"])
async def help_message(message:types.Message):
	text = """Я работаю! Помощь по боту: 
/ban - банит человека 

/prefix *тег* - выдает префикс 

/contact - отправляет фейк контакт

/profile - профиль человека

/info - информация о человеке

/dick - узнать длину своей *бибы*

/getdick - при ответе на сообщение, узнать длину *бибы* пользователя

/gay - узнать насколько ты *гей*

/getgay - при ответе на сообщение, узнать, насколько пользователь *гей*

/dice - бот кидает кубик

/ball - бот кидает мяч

/777 - играет в казино

/ochko - бот играет дартс

/nigga - think about maaan

/link - отправляет ссылку на чат

/start - вызвать *это сообщение*"""
	await message.answer(text, parse_mode="Markdown")




@dp.message_handler(content_types=["new_chat_members"])
async def on_user_joined(message: types.Message):
	await message.delete()

@dp.message_handler(is_admin=True, commands=["ban"], commands_prefix="!/")
async def cmd_ban(message: types.Message):
	if not message.reply_to_message:
		await message.reply("Заебал, используй эту команду ответом на сообщение!")
		return


	await message.bot.delete_message(config.GROUP_ID, message.message_id)
	try:
		await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)
		await message.reply_to_message.answer(f"{message.from_user.full_name} отсосал и был забанен.")
	except CantRestrictSelf:
		await message.answer("Ты даун чтоли?")
	except CantRestrictChatOwner:
		await message.answer("Это создатель блять.")

@dp.message_handler(commands="dice")
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")

@dp.message_handler(commands="ball")
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🏀")

@dp.message_handler(commands="777")
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎰")

@dp.message_handler(commands="ochko")
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎯")



@dp.message_handler(commands="nigga")
async def cmd_nigga(message: types.Message):
	pic = 'https://i.gifer.com/72nt.gif'
	await bot.send_document(message.chat.id, pic)

@dp.message_handler(commands=["prefix", "преф"], commands_prefix="!/")
async def pref(message: types.Message):
	if not message.reply_to_message:
		await message.reply("Сука, реплаем.")
		return
	s = message.text.split(' ')
	try:
		await bot.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_manage_chat=True)
		await bot.set_chat_administrator_custom_title(message.chat.id, message.reply_to_message.from_user.id, s[1])
		await message.reply(f"Выдали преффикс *{s[1]}* пользователю `{message.reply_to_message.from_user.id}`", parse_mode="Markdown")
	except IndexError:
		await message.reply("Укажи префикс, долбоеб")
	except ChatAdminRequired:
		await message.reply("Долбоебы, выдайте прав. Либо юзер был назначен не мной.")
@dp.message_handler(commands=["unprefix","унпреф"], commands_prefix="!/")
async def unpref(message: types.Message):
	if not message.reply_to_message:
		await message.reply("Сука, реплаем.")
		return
	try:
		await bot.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_manage_chat=False)
		await message.reply(f"Спиздили префикс у юзера `{message.reply_to_message.from_user.id}`", parse_mode="Markdown")
	except ChatAdminRequired:
		await message.reply("Долбоебы, выдайте прав. Либо юзер был назначен не мной.")
@dp.message_handler(commands=["link", "линк"], commands_prefix="!/")
async def getlink(message: types.Message):
	link = await bot.export_chat_invite_link(config.GROUP_ID)
	await message.reply(f"Ссылка для входа в чат: {link}")
@dp.message_handler(commands=["контакт","contact"], commands_prefix='/!')
async def contact(message: types.Message):
	rnum = randint(1,9)
	snek = str(rnum)*7
	await message.reply_contact(f'+9 (98) {snek}',message.from_user.first_name)
@dp.message_handler(text=["🎲"])
async def counter(message:types.Message):
	await message.answer(f"{md.escape_md(message.from_user.id)} набрал {message.dice.value} очков")

@dp.message_handler(commands=["dick"])
async def dicc(message: types.Message):
	length = randint(1,50)
	await message.reply(f"Твоя биба *{length}* см", parse_mode="MarkdownV2")
@dp.message_handler(commands=["gay"])
async def gay(message: types.Message):
	percent = randint(1,100)
	await message.reply(f"🏳️‍🌈Похоже, ты гей на *{percent}*%", parse_mode="MarkdownV2")
@dp.message_handler(is_reply=True,commands=["getdick"])
async def getdicc(message: types.Message):
	member = await bot.get_chat_member(message.chat.id,message.reply_to_message.from_user.id)
	name = md.escape_md(member.user.first_name)
	length = randint(1,50)
	await message.reply(f"Биба {name}  *{length}* см", parse_mode="MarkdownV2")
@dp.message_handler(is_reply=True,commands=["getgay"])
async def getgay(message: types.Message):
	member = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
	name = md.escape_md(member.user.first_name)
	percent = randint(1,100)
	await message.reply(f"🏳️‍🌈Похоже, {name} гей на *{percent}*%", parse_mode="MarkdownV2")
@dp.message_handler(commands=["staff"])
async def staff(message: types.Message):
	admins = await bot.get_chat_administrators(message.chat.id)
@dp.message_handler(commands=["id"])
async def get_id(message: types.Message):
	idd = md.code(message.from_user.id)
	await message.answer(f"Твой *ID*: {idd}", parse_mode="Markdown")
@dp.message_handler(is_reply=True, commands=["getid"])
@dp.message_handler(filters.IsReplyFilter(True), commands='getid')
async def getid(message: types.Message):
	user_id = md.code(message.reply_to_message.from_user.id)
	await message.answer(f"*ID* этого пользователя: {user_id}", parse_mode="Markdown")

@dp.message_handler(is_reply=True,commands=["info","инфо"])
async def info(message: types.Message):
	reply_user = message.reply_to_message.from_user
	user_id = reply_user.id
	member = await bot.get_chat_member(message.chat.id, user_id)
	status = member.status
	title = member.custom_title
	userid = md.code(member.user.id)
	if title == None:
		title = "Нет"
	if member.user.id in [837582349, 1056861593]:
		status = "Создатель бота"
	elif member.status == "creator":
		status = "Создатель"
	elif member.status == "administrator":
		status = "Администратор"
	elif member.status == "member":
		status = "Пользователь"
		title = "Пользователь"
	elif member.status == "restricted":
		status = "Ограничен"
	fullname = md.escape_md(reply_user.full_name)
	username = reply_user.username
	lang = reply_user.language_code
	mention = reply_user.get_mention()
	if username == None:
		username = "Нет"
	is_bot = reply_user.is_bot
	if is_bot == True:
		is_bot = "Да"
	elif is_bot == False:
		is_bot = "Нет"
	try:
		gpph = await bot.get_user_profile_photos(user_id, limit=1)
		gpl = gpph["photos"]
		for lol in gpl:
			pass
		msg = lol[0]
		file_id = msg["file_id"]
		text = f"""*Информация о пользователе:*
*Аватарка*: Выше
*Полное имя*: {fullname}
*ID*: {userid}
*Юзер*: @{md.escape_md(username)}
*Бот? *: {is_bot}
*Язык*: {lang}
*Статус*: {status}
*Звание*: {title}
*Пермалинк*: [клик](tg://user?id={user_id})"""
		await bot.send_photo(message.chat.id, file_id,caption=text, parse_mode="MarkdownV2")
	except UnboundLocalError:
		textnophoto=f"""*Информация о пользователе:*
*Аватарка*: Нет или недоступна
*Полное имя*: {fullname}
*ID*: {userid}
*Юзер*: @{md.escape_md(username)}
*Бот? *: {is_bot}
*Язык*: {lang}
*Статус*: {status}
*Звание*: {title}
*Пермалинк*: [клик](tg://user?id={user_id})"""
		await bot.send_message(message.chat.id, textnophoto, parse_mode="MarkdownV2")

@dp.message_handler(commands=["profile", "профиль"])
async def profile(message: types.Message):
	member = await bot.get_chat_member(message.chat.id, message.from_user.id)
	status = member.status
	title = member.custom_title
	user_id = member.user.id
	if title == None:
		title = "Нет"
	username = member.user.username
	if member.user.id in [837582349, 1056861593]:
		status = "Создатель бота"
	elif member.status == "creator":
		status = "Создатель"
	elif member.status == "administrator":
		status = "Администратор"
	elif member.status == "member":
		status = "Пользователь"
		title = "Пользователь"
	elif member.status == "restricted":
		status = "Ограничен"
	await message.reply(f"Профиль {md.escape_md(member.user.full_name)}\n\nСтатус: {status}\nЗвание: {title}\nID: {user_id}\nЮзер: @{username}")




if __name__ == '__main__':
    print("BOT was started.")
    executor.start_polling(dp, skip_updates=True)
