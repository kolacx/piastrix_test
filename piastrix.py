import json
import hashlib
import time
import loger

from flask import render_template, redirect, flash, url_for
from urllib.request import Request, urlopen


class Piastrix:

	def __init__(self):

		self.SHOP_ID = 5
		self.SECRED_KEY = 'SecretKey01'
		self.PAY_WAY = 'payeer_rub'


	def pay(self, shop_order_id, currency, amount, description):

		sign = self._sign(shop_id=self.SHOP_ID, shop_order_id=shop_order_id, 
			currency=currency, amount=amount)

		form = {
		    "shop_id": self.SHOP_ID,
		    "shop_order_id": shop_order_id,
		    "currency": currency,
		    "amount": amount,
		    "description": description,
		    "sign": sign,
		}

		loger.save_order(currency, amount, description, shop_order_id)

		return render_template('pay_way/pay.html', data=form)


	def bill(self, shop_order_id, currency, amount, description):

		sign = self._sign(
			shop_id=self.SHOP_ID,
		    shop_order_id=shop_order_id, 
		    shop_currency=currency,
		    shop_amount=amount, 
		    payer_currency=currency)

		data = {
		    "payer_currency": currency,
		    "shop_amount": amount,
		    "shop_currency": currency,
		    "shop_id": self.SHOP_ID,
		    "shop_order_id": shop_order_id,
		    "description": description,
		    "sign": sign,
		}

		request = Request('https://core.piastrix.com/bill/create',
		                          json.dumps(data).encode("utf-8"),
		                          headers={"Content-Type": "application/json"},
		                          method="POST")

		with urlopen(request) as response:

			data = json.loads(response.read())

			if not data["result"]:
				loger.save_log('bill response ERROR:', data)
				flash('Error. Please try again later: {}'.format(data['message']))
				return render_template('main_form.html')
			else:
				data = data["data"]
				loger.save_order(currency, amount, description, shop_order_id)
				return redirect(data["url"])

			




	def invoice(self, shop_order_id, currency, amount, description):

		sign = self._sign(shop_id=self.SHOP_ID,
		                  shop_order_id=shop_order_id, 
		                  currency=currency,
		                  amount=amount, 
		                  payway=self.PAY_WAY)

		data = {
		    "currency": currency,
		    "amount": amount,
		    "shop_id": self.SHOP_ID,
		    "shop_order_id": shop_order_id,
		    "description": description,
		    "payway": self.PAY_WAY,
		    "sign": sign,
		}


		request = Request('https://core.piastrix.com/invoice/create',
		                          json.dumps(data).encode("utf-8"),
		                          headers={"Content-Type": "application/json"},
		                          method="POST")

		with urlopen(request) as response:

			data = json.loads(response.read())

			if not data["result"]:
				loger.save_log('invoice response ERROR:', data)
				flash('Error. Please try again later: {}'.format(data['message']))
				return render_template('main_form.html')
			else:
				data = data["data"]
				loger.save_order(currency, amount, description, shop_order_id)
				return render_template('pay_way/invoice.html', method=data["method"], action=data["url"], form=data["data"])

		


	def _sign(self, **kwargs):

		data = []

		for key in sorted(kwargs.keys()):
			data.append(str(kwargs[key]))

		myhash = hashlib.sha256()

		myhash.update((":".join(data) + self.SECRED_KEY).encode("utf-8"))

		return myhash.hexdigest()