import json 

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, ChatRoomName

class ChatConsumer(AsyncWebsocketConsumer):
	
	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = f'chat_{self.room_name}'

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
			)

		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
			)

	async def receive(self, text_data):
		data = json.loads(text_data)
		message = data['message']
		user_id = data['user_id']
		r = data['room']

		room = await self.room_info(r)

		await self.save_message(user_id,room,message)

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type' : 'chat_message',
				'message' : message,
				'user_id' : user_id

			}
		)

	async def chat_message(self,event):
		message = event['message']
		user_id = event['user_id']

		await self.send(text_data = json.dumps({
			'message' : message,
			'user_id' : user_id
			})
		)

	@sync_to_async
	def room_info(self, r):
		room = ChatRoomName.objects.get(name = r)
		return room

	@sync_to_async
	def save_message(self, user_id, room, message):
		
		Message.objects.create(user_id = user_id, room = room, content=message)
