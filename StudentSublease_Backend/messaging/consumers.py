import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from users.models import SubleaseUser
import messaging.models as messaging_models

class MessageConsumer(WebsocketConsumer):
    def connect(self):
        conversation_pk = self.scope['url_route']['kwargs']['conversation']
        user_pk = self.scope['url_route']['kwargs']['user']
        try:
            self.user = SubleaseUser.objects.get(pk=user_pk)
            self.conversation = messaging_models.Conversation.objects.get(pk=conversation_pk)
            if self.conversation.tenant.pk != self.user.pk and self.conversation.listing.lister.pk != self.user.pk:
                return
        except:
            return
        self.conversation_name = 'chat_%s' % conversation_pk

        # Join conversation
        async_to_sync(self.channel_layer.group_add)(
            self.conversation_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave conversation
        async_to_sync(self.channel_layer.group_discard)(
            self.conversation_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_pk = text_data_json['sender']
        sender_pk = int(sender_pk)

        sender = self.conversation.listing.lister
        if sender_pk == self.conversation.tenant.pk:
            sender = self.conversation.tenant

        messaging_models.Message.objects.create(conversation=self.conversation, sender=sender, message=message, read=False)

        # Send message to conversation
        async_to_sync(self.channel_layer.group_send)(
            self.conversation_name,
            {
                'type': 'send_message',
                'message': message,
                'sender' : sender_pk,
                'conversation' : self.conversation.pk
            }
        )

    # Receive message from conversation
    def send_message(self, event):
        message = event['message']
        sender_pk = event['sender']
        sender_pk = int(sender_pk)

        sender = self.conversation.listing.lister
        if sender_pk == self.conversation.tenant.pk:
            sender = self.conversation.tenant
        if not sender_pk == self.user.pk:
            message_object = messaging_models.Message.objects.filter(conversation=self.conversation, sender=sender, message=message).last()
            message_object.read = True
            message_object.save()

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender' : sender_pk,
            'conversation' : self.conversation.pk
        }))