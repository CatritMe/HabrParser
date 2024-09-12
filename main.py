import asyncio
import datetime

from db.database import insert_and_update_data
from habr_parser import get_links

# наиболее популярные хабы в разделе "разработка":
habs = ['https://habr.com/ru/hubs/python/articles/',
        'https://habr.com/ru/hubs/programming/articles/',
        'https://habr.com/ru/hubs/infosecurity/articles/',
        'https://habr.com/ru/hubs/electronics/articles/',
        'https://habr.com/ru/hubs/machine_learning/articles/']


async def main():
    while True:
        for hab in habs:
            links, hab_title = get_links(hab)
            await insert_and_update_data(links, hab, hab_title)
        print(f'парсинг в {datetime.datetime.now()}')
        await asyncio.sleep(600)  # 10 минут


if __name__ == '__main__':
    asyncio.run(main())
