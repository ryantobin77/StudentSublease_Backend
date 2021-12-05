from django.shortcuts import render
from django.db.models import Max
from sublease.models import StudentListing
import users
from .models import Conversation, Message
from users.models import SubleaseUser
from django.http import JsonResponse, HttpResponse
from sublease.models import StudentListing
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_messages(request):
    result_messages = list()
    if request.method != "GET":
        return JsonResponse(result_messages, safe=False, status="400")
    conversation_pk = request.GET.get('conversation', None)
    user_pk = request.GET.get('user_pk', None)
    if conversation_pk is None or user_pk is None:
        return JsonResponse(result_messages, safe=False, status="400")
    try:
        conversation = Conversation.objects.get(pk=conversation_pk)
        user = SubleaseUser.objects.get(pk=user_pk)
    except:
        return JsonResponse(result_messages, safe=False, status="400")
    Message.objects.filter(conversation=conversation, read=False).exclude(sender=user).update(read=True)
    messages_db = Message.objects.filter(conversation=conversation).order_by('date')
    for message in messages_db:
        message_data = {
            'sender' : message.sender.pk,
            'message' : message.message,
            'date' : message.date.fromtimestamp(message.date.timestamp(), None).strftime("%m/%d/%Y %I:%M %p"),
        }
        result_messages.append(message_data)
    return JsonResponse(result_messages, safe=False, status="200")


@csrf_exempt
def get_conversations(request):
    if request.method != "GET" or 'user_pk' not in request.GET:
        return HttpResponse(status=400)
    try:
        user = SubleaseUser.objects.get(pk=request.GET['"user_pk'])
    except SubleaseUser.DoesNotExist:
        return HttpResponse(status=400)

    conversations_db = Conversation.objects.filter(tenant=user)
    listings = StudentListing.objects.filter(lister=user)
    for listing in listings:
        conversations_db |= Conversation.objects.filter(listing=listing)
    conversations_db = conversations_db.annotate(latest_conversation=Max('message__date')).order_by('latest_conversation')
    result_conversations = list()
    for conversation in conversations_db:
        is_lister = bool(user == conversation.listing.lister)
        first_name = conversation.tenant.first_name if is_lister else conversation.listing.lister.first_name
        last_name = conversation.tenant.last_name if is_lister else conversation.listing.lister.last_name
        last_message = conversation.message_set.last()
        if last_message is not None and last_message.sender != user and last_message.read == False:
            has_new_message = True
        else:
            has_new_message = False

        user_pk = conversation.tenant.pk
        user_email = conversation.tenant.email
        if user.pk == conversation.tenant.pk:
            user_pk = conversation.listing.lister.pk
            user_email = conversation.listing.lister.email

        conversation_data = {
            'pk' : str(conversation.pk),
            'title' : conversation.listing.title,
            'firstName' : first_name,
            'lastName' : last_name,
            'lister' : conversation.listing.lister.pk,
            'lastMessage' : last_message.message if last_message is not None else None,
            'date' : last_message.date.fromtimestamp(last_message.date.timestamp(), None).strftime("%m/%d/%Y %I:%M %p") if last_message is not None else None,
            'has_new_message' : has_new_message,
            'user_pk' : user_pk,
            'user_email' : user_email,
            'listing_pk' : conversation.listing.pk,
        }
        result_conversations.append(conversation_data)
    return JsonResponse(result_conversations, safe=False, status="200")


@csrf_exempt
def start_conversation(request):
    if request.method == "POST" and "tenant_pk" in request.POST and "listing_pk" in request.POST and "sender_pk" in request.POST and "message" in request.POST:
        try:
            tenant = SubleaseUser.objects.get(pk=request.POST["tenant_pk"])
            listing = StudentListing.objects.get(pk=request.POST["listing_pk"])
            sender = SubleaseUser.objects.get(pk=request.POST["sender_pk"])
        except:
            return HttpResponse(status=400)
        conversation = Conversation.start_conversation(tenant=tenant, listing=listing, sender=sender, message=request.POST["message"])
        result = {
            'pk' : conversation.pk
        }
        return JsonResponse(result, safe=False, status="200")
    else:
        return HttpResponse(status=400)
