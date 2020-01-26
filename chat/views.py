import json
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.models import Token
from sorl.thumbnail import get_thumbnail

from chat.api.serializers import ChatSerializer
from .models import Chat, Contact

User = get_user_model()


@login_required
def start_one_to_one_chat(request, user_id):
    # TODO: move it into User model?
    contact_one = Contact.objects.get(user=request.user)
    contact_two = Contact.objects.get(user__id=user_id)

    chat_obj = Chat.objects.annotate(c=Count('participants')). \
        filter(c=2).\
        filter(participants__id=contact_one.id).\
        filter(participants__id=contact_two.id).first()

    if not chat_obj:
        chat_obj = Chat.objects.create()
        chat_obj.participants.add(contact_one)
        chat_obj.participants.add(contact_two)
        chat_obj.save()
    return redirect('react_chat', chat_obj.id)


@login_required
def react_chat(request, chat_id):
    token, created = Token.objects.get_or_create(user=request.user)
    # the_contact = Contact.objects.filter(
    #     # chats__participants__chats__=
    # )
    user_contact, created = Contact.objects.get_or_create(user=request.user)

    title = 'Chat'
    if isinstance(chat_id, int) or chat_id.isdigit():
        chat_obj = get_object_or_404(Chat, id=chat_id, is_group=False)
        if not chat_obj.participants.filter(user=request.user).exists():
            return HttpResponseForbidden()
        target_contact = chat_obj.participants.all().exclude(user=request.user).get()
        title = target_contact.user.username
    else:
        chat_obj = get_object_or_404(Chat, slug=chat_id, is_group=True)
        title = chat_obj.slug
        if not chat_obj.participants.all().filter(user=request.user).exists():
            chat_obj.participants.add(user_contact)

    chat_messages = []

    for msg in chat_obj.messages.all():
        img = get_thumbnail(msg.author.user.profile.avatar, '100x100', crop='center', quality=99)
        chat_messages.append({
            'id': msg.id,
            'author': {
                'id': msg.author.user.id,
                'username': msg.author.user.username,
                # 'avatar': msg.contact.user.profile.avatar.url
                'avatar': img.url
            },
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%MZ'),
            # 'timestamp': str(msg.timestamp),
            'content': msg.content
        })

    initial_state = {
        'auth': {
            'id': request.user.id,
            'token': token.key,
            'username': request.user.username,
            # 'utf8': '✓'
        },
        'chats': [
            ChatSerializer(chat_obj, context={'request': request}).data
        ],
        'messages': chat_messages
    }

    return render(request, 'chat/react_chat.html', {
        'title': title,
        'initial_state': json.dumps(initial_state, ensure_ascii=False),
        'random_hash': str(uuid.uuid4()),
        'chat_obj': chat_obj,
    })


@csrf_exempt
@login_required
def add_contact(request, user_id):
    user_for_contact = get_object_or_404(User, id=user_id)

    contact_list, created = Contact.objects.get_or_create(user=request.user)
    contact_to_add, created = Contact.objects.get_or_create(user=user_for_contact)
    contact_list.friends.add(contact_to_add)

    return HttpResponse('Added')


@csrf_exempt
@login_required
def remove_contact(request, user_id):
    user_for_contact = get_object_or_404(User, id=user_id)

    contact_list, created = Contact.objects.get_or_create(user=request.user)
    contact_to_remove, created = Contact.objects.get_or_create(user=user_for_contact)
    contact_list.friends.remove(contact_to_remove)
    return HttpResponse('Removed')


@login_required
def index(request):
    rooms_objects = Chat.objects.filter(is_group=True)
    rooms = []
    for room in rooms_objects:
        participants = room.participants.count()
        rooms.append({
            'slug': room.slug,
            'participants_count': participants
        })
    return render(request, 'chat/index.html', {
        'rooms': rooms
    })


@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    })


def get_last_10_messages(chatId):
    if str(chatId).isdigit():
        chat = get_object_or_404(Chat, id=chatId)
    else:
        # TODO: ...
        chat = Chat.objects.first()

    return chat.messages.order_by('-timestamp').all()[:10]


def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Contact, user=user)


"""
from django.utils.safestring import mark_safe
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from .models import Chat, Contact

User = get_user_model()

# Create your views here.
def index(request):
    return render(request, 'chat/index.html', {})



def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]


def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Contact, user=user)


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)


@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    })


"""