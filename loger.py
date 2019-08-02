# -*- encoding: utf-8 -*-

import time

def save_log(status, message):

	t = time.localtime()
	time_string = time.strftime("%m/%d/%Y, %H:%M:%S", t)

	mess = '{0}: -- {1} -- {2}'.format(str(status), str(message), time_string)

	f = open('error_logs.txt', 'a+', encoding="utf-8")
	f.write(mess +'\n')
	f.close()

def save_order(currency, amount, description, shop_order_id):

	t = time.localtime()
	time_string = time.strftime("%m/%d/%Y, %H:%M:%S", t)

	message = 'Валюта: {0}, Сумма: {1}, Время: {2}, Описание: {3}, ID платежа: {4}'.format(
		str(currency), 
		str(amount), 
		time_string, 
		str(description), 
		str(shop_order_id))

	f = open('order.txt', 'a+', encoding="utf-8")
	f.write(str(message)+'\n')
	f.close()