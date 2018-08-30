from django import forms

# importing this for use with user profiles:
from django.contrib.auth.models import User

# importing item models
from .models import Item, Attribute, Option

# importing order models:
from .models import Order, Order_Item, Order_Item_Detail

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div
from crispy_forms.bootstrap import InlineField


class ItemOrderForm(forms.Form):
	def __init__(self, *args, **kwargs):

		if 'item' in kwargs:
			item = kwargs.pop('item')

			self.name = item.name
			self.desc = item.description
			self.id	  = item.id
			self.number = item.number
			if item.image:
				self.image = item.image.url

		super(ItemOrderForm, self).__init__(*args, **kwargs)
		
		attrib_set = item.get_attributes()
		
		for attrib in attrib_set:

			finalopts = []
			opt_set = attrib.get_options()

			for opt in opt_set:
				finalopts.append([str(opt.id),opt.name])

			fieldname = str('attrib_' + str(attrib.id) + '_')

			self.fields[fieldname] = forms.ChoiceField(choices = finalopts,
														label=attrib.name
													)	

		self.fields['qty'] = forms.IntegerField(label='Quantity',
												min_value=1,
												max_value=5000,
												required=True,
												initial=1
												)

		self.fields['thisitemid'] = forms.IntegerField(widget=forms.HiddenInput(), initial = self.id)

		self.helper = FormHelper(self)
		#self.helper.form_class = 'form-horizontal'
		self.helper.form_tag = False
		self.helper.all().wrap(Div, css_class="col-md-4")
		self.helper.all().wrap_together(Div, css_class="form-row")


class ItemDeleteForm(forms.Form):
	order_item_id = forms.IntegerField(widget=forms.HiddenInput())
