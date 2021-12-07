from django.shortcuts import render, redirect
from .models import *
import json
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from account.models  import *
import pandas as pd

def home(request):
	context = {}
	
	'''
	f = open('C:/Users/adran/Desktop/WeSell/src/products/coord.txt', 'r')
	ll = []
	for line in f:
		stripped_line = line.strip()
		ll.append([stripped_line])
	l2 = []
	for x in ll:
		for i in x:
			i = i.replace('\t', '')
			i = i.replace("°", '.')
			i = i.replace("'", '')
			i = i.replace("Â", '')
			l2.append(i.split())
	l3 = []
	for j in l2:
		if len(j) == 4:
			j[0] = j[0]+ ' ' +j[1]
			j.remove(j[1])
		elif len(j) == 5:
			j[0] = j[0] + ' ' + j[1] + j[2]
			j.remove(j[1])
			j.remove(j[2])
		l3.append(j)
	print(l3)
	for city in l3:
		City.objects.create(name = city[0], latitude = city[1], longitude = city[2])
	'''
	products = Product.objects.all()
	categories = Category.objects.all()
	counties = City.objects.all()
	if request.user.is_authenticated:
		last_list = []
		for i in products:
			dictt={
			'product':'',
			'is_fav' : '' 
			}
			req_profile = Profile.objects.get(pk=request.user.id)
			is_fav = False
			favourite = Favourite.objects.get(user = req_profile)
			if i in favourite.products.all():
				is_fav = True
			dictt['product'] = i
			dictt['is_fav'] = is_fav
			last_list.append(dictt)
		context['all_products'] = last_list
	else:
		context['products'] = products
	context['products'] = products
	context['counties'] = counties
	context['categories'] = categories
	return render(request, 'products/home.html', context)

def product_view(request, pr_id):
	context = {}
	product = Product.objects.get(pk = pr_id)
	product_images = Product_Image.objects.filter(product_name = product.id)
	if request.user.is_authenticated:
		req_profile = Profile.objects.get(pk=request.user.id)
		is_fav = False
		favourite = Favourite.objects.get(user = req_profile)
		if product in favourite.products.all():
			is_fav = True
		context['is_fav'] = is_fav
		
		all_chats  = ChatRoomName.objects.all()
		all_rooms= []
		for i in all_chats:
			all_rooms.append(i.name)
		req_id = request.user.id
		seller_id = product.seller.id
		product_id = pr_id
		first_option = f"{req_id}_{seller_id}_{product_id}" 
		second_option = f"{seller_id}_{req_id}_{product_id}"
		if first_option in all_rooms:
			room_q = ChatRoomName.objects.get(name = first_option)
			context['room_name'] = room_q
		elif second_option in all_rooms:
			room_q = ChatRoomName.objects.get(name = second_option)
			context['room_name'] = room_q
		else:
			if req_id != seller_id:
				room_q = ChatRoomName(name = first_option)
				room_q.save()
				context['room_name'] = room_q
		is_req = False
		if request.user.id == product.seller.id:
			is_req = True 
		context['is_req'] = is_req
	context['product'] = product
	context['product_images'] = product_images
	return render(request, 'products/product_page.html', context)
def delete_product_view(request, pr_id):
	product = Product.objects.get(pk=pr_id)
	all_rooms = ChatRoomName.objects.all()
	for i in all_rooms:
		name = i.name
		result = name.split('_')
		if result[2] == str(pr_id):
			i.delete()
	product.delete()
	return redirect('account:account', profile_id=request.user.id)




def sell_product_view(request):
	context = {}
	categories = Category.objects.all()
	counties = City.objects.all()
	currencies = Currency.objects.all()
	account = Profile.objects.get(pk = request.user.id)
	if request.POST:
		seller = Profile.objects.get(pk = request.user.id)
		title = request.POST['title']
		category = Category.objects.get(name = request.POST['category-choose'])
		description = request.POST['description-fill']
		price = request.POST['price']
		money_type = Currency.objects.get(name = request.POST['money-type'])
		localization = City.objects.get(name = request.POST['coming-from'])
		product = Product.objects.create(
			seller = seller,
			title = title,
			category = category,
			description = description,
			price = price,
			money_type = money_type,
			localization = localization
			)
		images = request.FILES.getlist('image-upload')
		pr_name = Product.objects.get(pk=product.id)
		for image in images:
			photo = Product_Image.objects.create(
				product_name = pr_name,
				image = image
				)
		product.principal_img = Product_Image.objects.filter(product_name = product.id)[0]
		product.save()
		messages.success(request, 'Your announcement has been added!')
		return redirect('products:product', pr_id=product.id)
	context['account'] = account
	context['counties'] = counties
	context['categories'] = categories
	context['currencies'] = currencies
	return render(request, 'products/sell_product.html', context)

def category_search_view(request, category_name):
	context = {}
	category = Category.objects.get(name = category_name)
	products = Product.objects.filter(category = category)
	if request.user.is_authenticated:
		last_list = []
		for i in products:
			dictt={
			'product':'',
			'is_fav' : '' 
			}
			req_profile = Profile.objects.get(pk=request.user.id)
			is_fav = False
			favourite = Favourite.objects.get(user = req_profile)
			if i in favourite.products.all():
				is_fav = True
			dictt['product'] = i
			dictt['is_fav'] = is_fav
			last_list.append(dictt)
		context['all_products'] = last_list
	else:
		context['products'] = products
	products_len = len(products)
	context['products_len'] = products_len
	context['category'] = category
	return render(request, 'products/category_search.html', context)

def main_search_view(request):
	context = {}
	if request.POST:
		main_search = request.POST['main-search']
		local = request.POST['selecting']
		if len(main_search) > 0:
			return redirect('products:all-search', localization=local, word=main_search)
		else:
			return redirect('products:all-searching', localization=local)

def all_search2_view(request, localization):
	context = {}
	localization = City.objects.get(name = localization)
	products = Product.objects.filter(localization = localization)
	last_list = []
	for i in products:
		last_list.append(i)
	if request.user.is_authenticated:
		l_l = []
		for i in last_list:
			dictt={
			'product':'',
			'is_fav' : '' 
			}
			req_profile = Profile.objects.get(pk=request.user.id)
			is_fav = False
			favourite = Favourite.objects.get(user = req_profile)
			if i in favourite.products.all():
				is_fav = True
			dictt['product'] = i
			dictt['is_fav'] = is_fav
			l_l.append(dictt)
		context['all_dicts'] = l_l
	else:
		context['products'] = last_list
	context['products_len'] = len(last_list)
	context['local'] = localization
	return render(request, 'products/all-search2.html', context)

def all_search_view(request, localization, word):
		context = {}
		localization = City.objects.get(name = localization)
		search_results = Product.objects.filter(title__icontains=word)
		last_list = []
		for i in search_results:
			if localization != 'All Country':
				if i.localization == localization:
					last_list.append(i)
			else:
				last_list.append(i)
		if request.user.is_authenticated:
			l_l = []
			for i in last_list:
				dictt={
				'product':'',
				'is_fav' : '' 
				}
				req_profile = Profile.objects.get(pk=request.user.id)
				is_fav = False
				favourite = Favourite.objects.get(user = req_profile)
				if i in favourite.products.all():
					is_fav = True
				dictt['product'] = i
				dictt['is_fav'] = is_fav
				l_l.append(dictt)
			context['all_dicts'] = l_l
		else:
			context['products'] = last_list
		context['products_len'] = len(last_list)
		context['main_search'] = word
		context['local'] = localization
		return render(request, 'products/all_search.html', context)

def add_favourite_list(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	profile = Profile.objects.get(pk = request.user.id)
	product = Product.objects.get(pk = productId)
	favourite, created = Favourite.objects.get_or_create(user = profile)
	if action == "add":
		favourite.products.add(product)
	elif action == "remove":
		favourite.products.remove(product)
	favourite.save()
	return JsonResponse('item was added', safe = False)


def favourites_view(request):
	context = {}
	if request.user.is_authenticated:
		req_profile = Profile.objects.get(pk=request.user.id)
		favourite = Favourite.objects.get(user = req_profile)
		fav_products = favourite.products.all()
		last_list = []
		for i in fav_products:
			last_list.append(i)
		context['products'] = last_list
	return render(request, 'products/favourites.html',context)

def room_view(request, room_name, user_id):
	context = {}
	if request.user.is_authenticated:
		user_id = request.user.id
		room = ChatRoomName.objects.get(name = room_name)
		all_messages = Message.objects.filter(room = room)
		mesaje = []
		for i in all_messages:
			mes_dict = {
			'mesaj' : '',
			'is_same':''
			}
			is_same = False
			if str(i.user_id) == str(request.user.id):
				is_same = True
			mes_dict['mesaj'] = i
			mes_dict['is_same'] = is_same
			mesaje.append(mes_dict)
			context['mesaje'] = mesaje
		if len(room_name) == 5:
			product_number = room_name[-1]
		elif len(room_name) == 6:
			product_number = room_name[-2:]
		elif len(room_name) == 7:
			product_number = room_name[-3:]
		product = Product.objects.get(pk = product_number)
		context['product'] = product
		context['user_id'] = user_id
		context['room_name'] =room_name
	return render(request, 'products/room.html', context)

def messages_view(request):
	context = {}
	chat_r = ChatRoomName.objects.all()
	pk = request.user.id 
	rooms = []
	for i in chat_r:
		rooms.append(i.name)
	final_list = []
	for j in rooms:
		chat_dict = {
			'room' : '',
			'user' : '',
			'product' : ''
		}
		word = j.split('_')
		if word[0] == str(pk) or word[1] == str(pk): 
			valid_room = ChatRoomName.objects.get(name = j)
			if word[0] == str(pk):
				user_id = word[1]
			elif word[1] == str(pk):
				user_id = word[0]
			user = Profile.objects.get(pk = user_id)
			product = Product.objects.get(pk = word[2])
			messages = Message.objects.filter(room = valid_room)
			if messages:
				chat_dict['room'] = valid_room
				chat_dict['user'] = user
				chat_dict['product'] = product
				final_list.append(chat_dict)
			else:
				continue
	context['chat_dicts'] = final_list
	return render(request, 'products/messages.html', context)