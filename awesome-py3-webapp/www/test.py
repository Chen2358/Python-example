import asyncio
import aiomysql

from config import configs

import orm
loop = asyncio.get_event_loop()

async def test():
	# pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
	#                                     user='root', password='',db='test', loop=loop)

	pool = await orm.create_pool(loop=loop, **configs.db)
	with (await pool) as conn:
		cur = await conn.cursor()
		await cur.execute('select * from students')
		result = await cur.fetchall()
		print(result)
	pool.close()
	await pool.wait_closed()

loop.run_until_complete(test())
