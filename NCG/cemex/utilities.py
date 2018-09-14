from django.db import models

# Needed for sending new order emails
from django.core.mail import send_mail
from django.conf import settings

# Needed for using templates to render emails
from django.template.loader import get_template

# Itemization class uses this form
from .forms import ItemDeleteForm

# used to build shipping label based on profile
from profiles.forms import UserProfileForm

# used for signing one-time order shipped email
from django.core.signing import dumps, loads

# used for generating shipping labels from user or order
from cemex.models import Order_Address

# Utility Classes/Functions:

class Itemization:
	# Used in the order confirmation view. 
	# represents an entry in an itemized list
	# containing item, each attribute/value,
	# and item quantity. accepts various order
	# model instances to build the itemization.
	
	def __init__(self, item=False, quantity=False, order_item=False):
		self.item = item
		self.properties = {}
		self.quantity = quantity
		self.order_item_id = order_item.id

		# generate a deletion form which is used on the confirm_order view. 
		self.del_form = ItemDeleteForm()
		# set the value of the form to this order_item
		self.del_form.fields['order_item_id'].initial = self.order_item_id

	def __str__(self):
		return self.item.name
		
	def add_property(self, attribute, option):
	# method to add attribute/option dict pairs to
	# the 'properties' attribute. In the template
	# we iterate through it to list user choices.

		self.properties[attribute.name] = option.name
		return


class Shippinglabel:
	# Used in order confirmation and review order views.
	# displays paragraph of shipping info

	def __init__(self, **kwargs):
		
		linebreak = '<br />'

		if 'user' in kwargs:

			user = kwargs['user']
			
			self.label = user.first_name + ' ' + user.last_name + linebreak
			self.label += user.profile.address1 + linebreak
			self.label += user.profile.address2 + linebreak
			self.label += user.profile.city + linebreak
			self.label += user.profile.state + linebreak
			self.label += user.profile.zip + linebreak
			self.label += user.profile.phone + linebreak
			self.label += user.email + linebreak
			# fix any duplicate line breaks
			self.label = self.label.replace(linebreak + linebreak, linebreak)

		elif 'order' in kwargs:

			order = Order_Address.objects.get(order=kwargs['order'])

			self.label = order.first_name + ' ' + order.last_name + linebreak
			self.label += order.address1 + linebreak
			self.label += order.address2 + linebreak
			self.label += order.city + linebreak
			self.label += order.state + linebreak
			self.label += order.zip + linebreak
			self.label += order.phone + linebreak
			self.label += order.email + linebreak
			# fix any duplicate line breaks
			self.label = self.label.replace(linebreak + linebreak, linebreak)
		
	def __str__(self):
		return self.label


class Email:
	# Class for sending order details to the office in an email.

	def __init__(self, itemizations,  order, label, linkhash):
		self.subject = 'You have a new CEMEX order'
		
		output = {
					'first_name' : order.user.first_name,
					'last_name': order.user.last_name,
					'date': order.datetime.date,
					'time' : order.datetime.time,
					'itemizations' : itemizations,
					'linkhash' : linkhash
				}

		template = get_template('cemex/html_email.html')
		self.html_message =  template.render(output)
	
	def send(self):

		send_mail(	subject=self.subject, 
					message=self.html_message,
					html_message=self.html_message,
					from_email = settings.EMAIL_HOST_USER,
					recipient_list = settings.EMAIL_RECIPIENT_LIST				
				)
		return