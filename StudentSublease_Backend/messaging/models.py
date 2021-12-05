from django.db import models
from users import models as user_models
from sublease import models as sublease_models
from django.utils import timezone

class Conversation(models.Model):
    tenant = models.ForeignKey(user_models.SubleaseUser, on_delete=models.CASCADE, null=False)
    listing = models.ForeignKey(sublease_models.StudentListing, on_delete=models.CASCADE, null=False)
    last_notified = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('tenant', 'listing',)

    @classmethod
    def start_conversation(cls, tenant, listing, sender, message):
        conversation = None
        if sender != tenant and sender != listing.lister:
            return None
        try:
            conversation = Conversation.objects.get(tenant=tenant, listing=listing)
            Message.objects.create(conversation=conversation, sender=sender, message=message)
        except Conversation.DoesNotExist:
            conversation = Conversation.objects.create(tenant=tenant, listing=listing)
            Message.objects.create(conversation=conversation, sender=sender, message=message)
        return conversation


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=False)
    sender = models.ForeignKey(user_models.SubleaseUser, on_delete=models.CASCADE, null=False)
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    sent_text_message = models.BooleanField(default=False)

    def __str__(self):
        return self.sender.email + " sent " + self.message + " at " + str(self.date)
