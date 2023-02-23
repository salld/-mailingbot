@labeler.message(text=["🏆 | Чемпион по кликам", "топ <numb>", "топ"])
async def top_handler(message, numb=5):
    sql.execute(f"SELECT cash FROM users")
    result = sql.fetchall()
    top_list = []
    n = -1
    for i in list(result):
        n += 1
        top_list.extend(list(result[n]))
    top_list.sort()
    top_list.reverse()
    n = 0
    limit = int(numb)
    l_list = ''
    n_top = -1
    for i in top_list:
        n += 1
        n_top += 1
        if n > limit:
            break
        sql.execute(f"SELECT userid FROM users WHERE cash = '{top_list[n_top]}'")
        top = sql.fetchone()[0]
        ui = await api.users.get(top)
        l_list += f'{n}. {ui[0].first_name} - {top_list[n_top]}$\n'


    await message.answer(f'Топ {numb}:\n\n{l_list}')
