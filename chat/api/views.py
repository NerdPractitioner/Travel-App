from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from rest_framework.response import Response

from chat.models import Chat, Contact
from chat.views import get_user_contact
from .serializers import ChatSerializer

User = get_user_model()


@api_view()
@permission_classes([permissions.AllowAny, ])
def chat_list_view(request):
    user = request.user

    # contact = get_user_contact(username)
    user_as_contact = get_object_or_404(Contact, user=user)
    user_chats = user_as_contact.chats.all()

    # queryset = Chat.objects.all()
    # username = request.query_params.get('username', None)
    # if username is not None:
    #     contact = get_user_contact(username)
    #     queryset = contact.chats.all()
    # else:
    #     queryset = Chat.objects.none()

    """
    [
        {
            "id": 1,
            "messages": [],
            "participants": [
                "ak",
                "James"
            ]
        },
        {
            "id": 2,
            "messages": [],
            "participants": [
                "ak",
                "GirlsLoveExample2"
            ]
        },
        {
            "id": 3,
            "messages": [],
            "participants": [
                "ak",
                "mattadorable"
            ]
        }
    ]
    """

    return Response(
        [ChatSerializer(chat, context={'request': request}).data for chat in user_chats]
    )


class ChatListView(ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        queryset = Chat.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            contact = get_user_contact(username)
            queryset = contact.chats.all()
        return queryset


class ChatDetailView(RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.AllowAny, )


class ChatCreateView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ChatUpdateView(UpdateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ChatDeleteView(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )
