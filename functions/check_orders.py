import pprint
import aiohttp
import asyncio
import requests
import aiofiles
from functools import reduce
from datetime import datetime,timedelta

from misc import dp,bot
from methods import get_data as GD
from methods.check_orders_number import Order


async def get_orders_info(session, ordersDetailURL, stocksDetailURL,salesDetailURL, headers, now, user_id):
    messages = []

    today = now.date()

    mounth = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    yesterDay = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday = datetime.strptime(yesterDay, '%Y-%m-%d').date()
    three_mounth = str((now - timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%S"))
    dateFrom = str((now - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"))

    # async with session.get(url = ordersDetailURL, params = {"dateFrom": f"{yesterDay}T00:00:00", "flag": 0} , headers = headers) as responce_orders_today:
    #     orders_yesterday = await responce_orders_today.json()
    #     today_orders_all = 0
    #     today_sum_all = 0
    #
    #     for o in orders_yesterday:
    #         o_date_T = o['date'].split('T')[0]
    #         date_o = datetime.strptime(o_date_T, '%Y-%m-%d').date()
    #
    #         if date_o == today:
    #             today_orders_all += 1
    #             today_sum_all += int(o['totalPrice'] * (1 - o['discountPercent']/100))

    await asyncio.sleep(2)
    async with session.get(url=salesDetailURL, params={'dateFrom': three_mounth, 'flag': 0},headers=headers) as responce_sales:
        if responce_sales.status == 200:
            sell = await responce_sales.json()

    await asyncio.sleep(2)
    async with session.get(url = ordersDetailURL,params ={"dateFrom":three_mounth, "flag": 0}, headers = headers) as responce_orders:
        await asyncio.sleep(1)
        async with session.get(url=stocksDetailURL, params={"dateFrom":three_mounth}, headers=headers) as responce_stocks:
            await asyncio.sleep(2)
            if responce_orders.status == 200 and responce_stocks.status == 200:
                orders_json = await responce_orders.json()
                stocks_json = await responce_stocks.json()
                sales_json = await responce_sales.json()


                if orders_json != None and stocks_json != None and sales_json != None:

                    today_orders_all = 0
                    today_sum_all = 0

                    for o in orders_json:
                        o_date_T = o['date'].split('T')[0]
                        date_o = datetime.strptime(o_date_T, '%Y-%m-%d').date()

                        if date_o == today:
                            today_orders_all += 1
                            today_sum_all += int(o['totalPrice'] * (1 - o['discountPercent'] / 100))

                    for order in orders_json:
                        
                        order_time = order['date'].split('.')[0]
                        order_time = datetime.strptime(order_time, '%Y-%m-%dT%H:%M:%S')

                        timer = datetime.now()
                        last_change = order['lastChangeDate']
                        inner = (timer - timedelta(hours=5)).strftime("%Y-%m-%dT%H:%M:%S")
                        five_minutes = datetime.strptime(inner, '%Y-%m-%dT%H:%M:%S')


                        if order['orderType'] == 'Клиентский' and order['isCancel'] == False and order_time >= five_minutes:
                            
                            gNumber = order['gNumber']
                            flagInfo = Order(gNumber,user_id)

                            if flagInfo.check_order() == False:
                                flagInfo.add_order()
                            else:
                                continue


                            message_order = {}


                            message_order['id'] = gNumber
                            message_order['warehouseName'] = order['warehouseName']
                            message_order['oblast'] = order['oblast']
                            message_order['nmId'] = order['nmId']
                            message_order['subject'] = order['subject']
                            message_order['supplierArticle'] = order['supplierArticle']
                            message_order['date'] = order['date']
                            message_order['price'] = (order['totalPrice'] * (1 - order['discountPercent']/100))
                            
                            basket = ['basket-01.wb.ru', 'basket-02.wb.ru', 'basket-03.wb.ru', 'basket-04.wb.ru',
                                      'basket-05.wb.ru',
                                      'basket-06.wb.ru', 'basket-07.wb.ru', 'basket-08.wb.ru', 'basket-09.wb.ru',
                                      'basket-10.wb.ru',
                                      'basket-11.wb.ru', 'basket-12.wb.ru', 'basket-13.wb.ru']

                            nmId = str(order['nmId'])
                            try:
                                for photo_basket in basket:
                                    if len((str(nmId))) == 9:
                                        photo_url = f'https://{photo_basket}/vol{str(nmId)[0:4]}/part{str(nmId)[0:6]}/{str(nmId)}/images/big/1.webp'
                                    elif len((str(nmId))) == 8:
                                        photo_url = f'https://{photo_basket}/vol{str(nmId)[0:3]}/part{str(nmId)[0:5]}/{str(nmId)}/images/big/1.webp'
                                    else:
                                        pass

                                    if photo_url:
                                        async with session.get(photo_url) as resp:
                                            if resp.status == 200:
                                                f = await aiofiles.open(f"functions/photos/{str(gNumber)}.png",mode="wb")
                                                await f.write(await resp.read())
                                                await f.close()
                                                break


                            except Exception as e:
                                print('[PHOTO ERROR]: ', e)



                            quantity = 0
                            inWayToClient = 0
                            inWayFromClient = 0

                            for stocks in stocks_json:
                                if stocks['nmId'] == order['nmId']:
                                    quantity += stocks['quantity']
                                    inWayToClient += stocks['inWayToClient']
                                    inWayFromClient += stocks['inWayFromClient']


                            message_order['inWayToClient'] = inWayToClient
                            message_order['inWayFromClient'] = inWayFromClient


                            # for sales in sales_json:
                            #     if sales['saleID'].startswith('D') or sales['saleID'].startswith('S') and sales['nmId'] == order['nmId']:
                            #         buyouts += 1
                            #         count += 1
                            #
                            #     if sales['saleID'].startswith('R') and sales['nmId'] == order['nmId']:
                            #         refunds += 1
                            #         count += 1
                            #
                            # if count != 0:
                            #     br_percent = int((buyouts/count)*100)
                            # else:
                            #     br_percent = 0

                            # message_order['refunds'] = refunds
                            # message_order['buyouts'] = f'{br_percent}% ({buyouts}/{count})'
                            # message_order['today_orders_all'] = f'{today_orders_all} на {today_sum_all}'

                            orders = 0
                            buyouts = 0

                            for Or in orders_json:
                                if Or['nmId'] == order['nmId']:
                                    orders += 1
                                    buyouts += 1

                            for Sell in sales_json:
                                if Sell['nmId'] == order['nmId']:

                                    if Sell['saleID'].startswith('R') or Sell['saleID'].startswith('A') or Sell[
                                        'saleID'].startswith('B'):
                                        buyouts -= 1

                            if orders != 0:
                                br_percent = int(buyouts/(orders/100))
                            else:
                                br_percent = 0



                            # message_order['refunds'] = refunds
                            message_order['buyouts'] = f'{br_percent}% ({buyouts}/{orders})'
                            message_order['today_orders_all'] = f'{today_orders_all} на {today_sum_all}'


                            ifSell = False
                            try:
                                if sell != None:
                                    for s in sell:
                                        order_date = s['date']
                                        if s['gNumber'] == gNumber:
                                            ifSell = True
                                        else:
                                            pass
                            except:
                                ifSell = False

                            yesterdayCount = 0
                            todayCount = 0
                            sum_today = 0
                            sum_yesterday = 0
                            counter = 0
                            number = 0
                            
                            for order_yesterday in orders_json:

                                or_date = order_yesterday['date'].split('T')[0]
                                or_date = datetime.strptime(or_date, '%Y-%m-%d').date()
                                
                                if or_date == today:
                                    counter+=1
                                    if or_date['gNumber'] == order['gNumber']:
                                        number = counter
                                    
                                if order_yesterday['nmId'] == order['nmId']:

                                    if or_date == yesterday:
                                        yesterdayCount += 1
                                        sum_yesterday += int(order_yesterday['totalPrice'] * (1 - order_yesterday['discountPercent']/100))
                                    elif or_date == today:
                                        todayCount += 1
                                        sum_today += int(order_yesterday['totalPrice'] * (1 - order_yesterday['discountPercent']/100))
                                else:
                                    pass
                            
                            message_order['ifSell'] = ifSell
                            message_order['todayThis'] = f'{todayCount} на {sum_today}'
                            message_order['yesterdayThis'] = f'{yesterdayCount} на {sum_yesterday}'

                            try:
                                feedbacks = 0
                                rating = 0
                                url = f"https://card.wb.ru/cards/detail?appType=1&curr=rub&dest=123585628&regions=80,38,83,4,64,33,68,70,30,40,86,69,1,31,66,110,48,22,114&spp=31&nm={order['nmId']}"
                                responce_card = requests.get(url).json()
                                for card in responce_card['data']['products']:
                                    brand = card['brand']
                                    feedbacks = card['feedbacks']
                                    rating = card['reviewRating']
                                    for qt in card['sizes'][0]['stocks']:
                                        qty = int(qt['qty'])
                                        quantity += qty

                            except Exception as e:
                                feedbacks = "Ошибка сбора данных"
                                rating = "Ошибка сбора данных"
                            message_order['techSize'] = order['techSize']
                            message_order['quantity'] = quantity
                            message_order['feedbacks'] = feedbacks
                            message_order['rating'] = rating
                            message_order['user_id'] = user_id
                            message_order['brand'] = brand
                            message_order['number'] = number
                            messages.append(message_order)
                        else:
                            continue

            else:
                print(responce_orders.status, responce_stocks.status)
    if messages:
        pprint.pprint(messages)
    else:
        print(user_id, None)

    return messages

async def load_orders_sellers():
    sellers_accouns = GD.select_seller_accounts()

    now = datetime.now()

    connector = aiohttp.TCPConnector(limit_per_host=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []

        for account in sellers_accouns:

            api_key = account[3]
            user_id = account[1]

            headers = {
                "Authorization": api_key
            }

            #reportDetailURL = f'https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod' #Вроде как не нужен, но пока не 100%
            ordersDetailURL = 'https://statistics-api.wildberries.ru/api/v1/supplier/orders' # Отсюда можно выгрузить заказы
            salesDetailURL = 'https://statistics-api.wildberries.ru/api/v1/supplier/sales' # Отсюда - выкупы
            stockDetailURL = 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks' # Склад, отсюда выгружаем возраты/доставки
            task = asyncio.create_task(get_orders_info(session, ordersDetailURL,stockDetailURL,salesDetailURL, headers,now,user_id))
            tasks.append(task)

        values = await asyncio.gather(*tasks)
        return values

async def start():
    data = await load_orders_sellers()
    return data

if __name__ == '__main__':
    #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(start())

