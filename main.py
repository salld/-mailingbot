from vkbottle.bot import Bot, Message
import sqlite3


bot = Bot(token="")
print("Бот запущен.")

db = sqlite3.connect('base.db')
sql = db.cursor()


sql.execute("""CREATE TABLE IF NOT EXISTS users (
    userid INT,
    status TEXT,
    ron INT
)""")

# Чтобы в дальнейшем не ебаться с получением данных из бд и не засорять лишними строками код.
async def get(message, arg):
	sql.execute(f"SELECT {arg} FROM users WHERE userid = '{message.from_id}'")
	# Получаем результат в переменную
	result = sql.fetchone()[0]
	# Возвращаем переменную
	return result

@bot.on.message(text="рассылка")
async def ras(message: Message):
	status = await get(message, "status")
	if status == "Администратор":
		await message.reply("Введите текст для рассылки:")
		# Нужно для того, чтобы полный текст админа обрабатывался
		sql.execute(f'UPDATE users SET ron = ? WHERE userid = ?', (1, message.from_id))
		db.commit()
	else:
		await message.answer("Вы не администратор.")


@bot.on.message()
async def reg(message: Message):
	sql.execute(f"SELECT userid FROM users WHERE userid = '{message.from_id}'")
	if sql.fetchone() is None:
		sql.execute(f"INSERT INTO users VALUES (?, ?, ?)", (message.from_id, 'Обычный', 0))
		db.commit()
		await message.reply("✅")
	r = await get(message, "ron")
	if r == 1:
	# Проверяем, включал ли админ рассылку, если да то:
		sql.execute(f'UPDATE users SET ron = ? WHERE userid = ?', (0, message.from_id))
		db.commit()
		await message.answer(f"Ваше сообщение для рассылки: {message.text}")
		# Получаем все ID-шники из бд
		sql.execute(f"SELECT userid FROM users")
		# Записываем все ID-шники в переменную
		result = sql.fetchall()

		n = -1
		for i in result:
			# И обрабатываем каждого нашего юзера.
			n += 1
			await bot.api.messages.send(peer_id=result[n], message=message.text, random_id=0)
		await message.reply("Рассылка закончена.")




bot.run_forever()
