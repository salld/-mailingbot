@labeler.message(text=["топ <numb>", "топ"])
@labeler.message(payload={"cmd": "5"})
async def top_handler(message, numb=5):
    if int(numb) > 15:
        numb = 15
    sql.execute(f"SELECT clicks FROM users")
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
    l_clicks = du(message, "clicks")
    for i in top_list:
        n += 1
        n_top += 1
        if n > limit:
            break
        sql.execute(f"SELECT userid FROM users WHERE clicks = '{top_list[n_top]}'")
        top = sql.fetchone()[0]
        sql.execute(f"SELECT crown FROM users WHERE userid = '{top}'")
        crown = sql.fetchone()[0]
        ui = await api.users.get(top)
        l_list += f'{n}. [id{ui[0].id}|{ui[0].first_name} {ui[0].last_name}] {crown}👑 -- {task(top_list[n_top])} кликов\n'
    
    myclicks = du(message, "clicks")
    me = top_list.index(myclicks) + 1
    f = l_list.find(str(message.from_id))
    # if f == -1:
    await message.answer(f'🏆 | Чемпионы по кликам:\n\n{l_list}\n\n❗В конце сезона чемпион по кликам получает награду.\n(🏅Вы на {me} месте)')
