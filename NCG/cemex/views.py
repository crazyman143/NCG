from django.shortcuts import render, redirect
from django.http import HttpResponse
# class-based views
from django.views import View
# decorator to enforce authentication before loading view
from django.contrib.auth.decorators import login_required
# djson serialization
from django.http import JsonResponse
# built-in messaging framework
from django.contrib import messages

# models for order handling
from cemex.models import Item, Attribute, Option, Order, Order_Item, Order_Item_Detail, Order_Address
# forms
from cemex.forms import ItemOrderForm, ItemDeleteForm
# utility classes/functions
from .utilities import Itemization, Shippinglabel, Email

# used for signing one-time order shipped links
from django.core.signing import dumps, loads


# Cemex Views:


def index(request):
	# currently, we just want to send the user either
	# to the login page, or their profile/orders page
	# if they're already logged in. No home page. 
	
	if request.user.is_authenticated == True:
		return redirect('cemex:my_orders')
	else:
		return redirect('profiles:login')

	# dictionary to pass to template
	output = {}

	# return a render. pass the request, template, and output dictionary
	return render(request, 'cemex/index.html', output )


@login_required	
def new_order(request):
	try:
		# try to get the user's unfinished order (cart)		
		incomplete_order = Order.objects.get(user = request.user, complete = False)
	except:
		# if that doesn't work, create one now
		incomplete_order = Order(user = request.user, complete = False, shipped = False)
		incomplete_order.save()

	if (request.method == 'POST'):	
		# if there is a field called 'thisitemid', it contains the form item 
		# id, and indicates an item form was submitted. Add the item
		# with its chosen attribute/options to the unprocessed order.

		if 'thisitemid' in request.POST:
			if not request.POST['thisitemid'].isdigit():
					return JsonResponse({'form_error' : 'Item not found in database.'})
	
			# fetch the item with POST data
			item = Item.objects.get(id=request.POST['thisitemid'])

			# rebuild and then bind the form
			itemform = ItemOrderForm(request.POST, item=item)

			# validate the form. If successful, build order_item
			# and order_item_detail(s)
			if itemform.is_valid():

				# build an order_item for the order. pass the item and a qty
				order_item = Order_Item(order=incomplete_order, 
										quantity=itemform.cleaned_data['qty'], 
										item=item
										)
				order_item.save()

				# iterate through key/value pairs in form data
				for key, value in itemform.cleaned_data.items():
					# if 'attrib_' is in key, it's an attribute selection
					if 'attrib_' in key:
						# fetch attribute obj. id is in the key
						attribute = Attribute.objects.get(id=key.split('_')[1])
						# option id is the corresponding value
						option = Option.objects.get(id=value)

						# build/save order_item_detail record
						order_item_detail = Order_Item_Detail(order_item=order_item,
															  attribute=attribute,
															  option=option
															  )
						order_item_detail.save()

				# count the order_items in the incomplete order. use this for the cart icon.
				itemcount = Order_Item.objects.filter(order = incomplete_order).count()
				# return the item count back to the browser
				return JsonResponse({'item_count' : itemcount})

			else:
				print('not valid')
				print(itemform.errors.as_json())

				# the errors will be json encoded and send back to the browser where they
				# will be processed and inserted into DOM by JS. 
				return JsonResponse({'validation_error' : itemform.errors.get_json_data(escape_html=True) })

		
	# count the order_items in the incomplete order. use this for the cart icon.
	itemcount = Order_Item.objects.filter(order = incomplete_order).count()

	# all items
	items = Item.objects.all().order_by('name')

	# list of forms to show on the page
	forms = []

	# for each item, generate forms and add to list
	for item in items:
		orderform = ItemOrderForm(item=item)
		forms.append(orderform)
	

	return render(request, 'cemex/new_order.html',{'forms' : forms,'itemcount' : itemcount } )


@login_required	
def confirm_order(request):

	# start a dict to store template data
	output = {}

	# try to get the user's incomplete order
	try:		
		incomplete_order = Order.objects.get(user = request.user, complete = False)
	# if that doesn't work, create one now
	except:
		incomplete_order = Order(user = request.user, complete = False)
		incomplete_order.save()

	if (request.method == 'POST'):
		
		if 'order_item_id' in request.POST:
		# this field is from a delete button.
		# we need to get the order_item based on id and remove it

			# bind the form
			delform = ItemDeleteForm(request.POST)

			if delform.is_valid():
				try:
					# try to delete the order_item if it's in this users incomplete order
					del_item = Order_Item.objects.get(id=delform.cleaned_data['order_item_id'],
													  order=incomplete_order
													  )
					del_item.delete()

					# return 'true' the js watches for this to signal removal of page element
					return JsonResponse({'code' : 'true'})
				except:
					# something went wrong, and order_item wasn't found in incomplete order
					return JsonResponse({'code' : 'false'})




		# if there is a field called 'thisitemid', it contains the item id, 
		# and indicates that an item form was submitted. Add the item
		# with its chosen attribute/options to the unprocessed order.
		if 'thisitemid' in request.POST:

			# fetch the item
			item = Item.objects.get(id=request.POST['thisitemid'])

			# build an order_item for the order, with qty
			order_item = Order_Item(order=incomplete_order, quantity=request.POST['qty'])
			order_item.save()

			# iterate through key/value pairs in post data
			for key, value in request.POST.items():
				# if 'attrib_' is in key, it's an attribute selection
				if 'attrib_' in key:
					# fetch attribute obj. get the id from the POST field
					attribute = Attribute.objects.get(id=key.split('_')[1])
					# option id is the value in the pair
					option = Option.objects.get(id=value)

					# build order_item_detail with the collected data
					order_item_detail = Order_Item_Detail(order_item=order_item,
														  attribute=attribute, option=option
														  )
					order_item_detail.save()
										

	# get all items in order, count them.
	order_items = Order_Item.objects.filter(order=incomplete_order)
	itemcount = order_items.count()

	# if the order has items:
	if order_items.count() > 0:
	
		# list to store item itemizations
		itemizations = []
		
		for order_item in order_items:
		
			itemization = Itemization(item=order_item.item,
									  quantity=order_item.quantity,
									  order_item = order_item
									  )

			order_item_details = Order_Item_Detail.objects.filter(order_item=order_item)
			
			for order_item_detail in order_item_details:
				
				itemization.add_property(attribute=order_item_detail.attribute,
										 option=order_item_detail.option
										)

				
			itemizations.append(itemization)

		output['itemizations'] = itemizations


	# pack output dict for sending to template:

	output['shippinglabel'] = Shippinglabel(user=request.user)	# a shipping label to display
	output['itemcount'] = itemcount								# the item count



	return render(request, 'cemex/confirm_order.html', output )


@login_required	
def place_order(request):

	# start a dict to store template data
	output = {}

	# the user has 'placed' the order.
	# we need to:
	#	set the order complete status to True,
	#	generate itemizations again so we can email them
	#	copy profile address to Order_Address 
	#	send the email. 
	#	let the user know its processing
	# 	return them to their orders page.

	# try to get the user's incomplete order (cart)
	try:		
		incomplete_order = Order.objects.get(user=request.user, complete=False)
	# if that doesn't work, they shouldn't be here
	except:
		return redirect('cemex:new_order')
	
	# list to store item itemizations
	itemizations = []
	
	# for all items for the incomplete order
	for order_item in  incomplete_order.order_item_set.all():
	
		# build itemization
		itemization = Itemization(item=order_item.item,
								  quantity=order_item.quantity,
								  order_item = order_item
								  )

		# for all item details in this item
		for order_item_detail in order_item.order_item_detail_set.all():
			
			# add itemization property
			itemization.add_property(attribute=order_item_detail.attribute,
									 option=order_item_detail.option
									 )
			
		itemizations.append(itemization)

	# copy profile address to order address record for this order
	order_address = Order_Address(order=incomplete_order)
	order_address.first_name = request.user.first_name
	order_address.last_name = request.user.last_name
	order_address.email = request.user.email
	order_address.address1 = request.user.profile.address1
	order_address.address2 = request.user.profile.address2
	order_address.city = request.user.profile.city
	order_address.state = request.user.profile.state
	order_address.zip = request.user.profile.zip
	order_address.phone = request.user.profile.phone
	order_address.save()

	# shipping label goes in the email and recorded in db
	shippinglabel = Shippinglabel(order=incomplete_order)

	# used in the email for mark as shipped link
	linkhash = dumps(incomplete_order.id, salt='shiplinks')

	# build the email
	email = Email(itemizations=itemizations, 
					order=incomplete_order, 
					label=shippinglabel,
					linkhash = linkhash,
					shippinglabel = shippinglabel
					)
	
	incomplete_order.complete = True
	incomplete_order.save()
	email.send()
	
	message = ('<strong>Success:</strong> Your order with id ' 
			   + str(incomplete_order.id) 
			   + ' has been sent.'
			   )
	messages.add_message(request, messages.SUCCESS, message)
	
	return redirect('cemex:my_orders')


@login_required	
def my_orders(request):

	# start a dict to store template data
	output = {}

	# Collect newest 25 completed user orders
	orders = Order.objects.filter(user=request.user, complete = True).order_by('-datetime')[0:25]

	# pack output dict for sending to template:
	output['orders'] = orders
	output['shippinglabel'] = Shippinglabel(user=request.user)	# a shipping label to display

	return render(request, 'cemex/my_orders.html', output )


@login_required	
def review_order(request, order_id):

	# start a dict to store template data
	output = {}

	# get order
	order = Order.objects.get(id=order_id, user=request.user)

	# get all items in order
	order_items = Order_Item.objects.filter(order=order)

	
	# list to store item itemizations
	itemizations = []
	totalqty = 0
	
	for order_item in order_items:
		totalqty += order_item.quantity
		itemization = Itemization(item=order_item.item,
								  quantity=order_item.quantity,
								  order_item = order_item
								  )

		order_item_details = Order_Item_Detail.objects.filter(order_item=order_item)
		
		for order_item_detail in order_item_details:
			
			itemization.add_property(attribute=order_item_detail.attribute,
								     option=order_item_detail.option
								     )

		itemizations.append(itemization)


	
	# pack output dict for sending to template:
	output['itemizations'] = itemizations
	output['order'] = order
	output['totalqty'] = totalqty
	output['shippinglabel'] = Shippinglabel(order=order)

	return render(request, 'cemex/review_order.html', output )


def ship_order(request, linkhash):

	try:
		# links are considered valid 6 weeks
		order_id = loads(linkhash, salt='shiplinks', max_age=3628800)

		# get order
		order = Order.objects.get(id=order_id)

		# mark shipped
		order.shipped = True
		order.save()
		result = True
	except:
		result = False

	return render(request, 'cemex/ship_order.html', {'result':result} )