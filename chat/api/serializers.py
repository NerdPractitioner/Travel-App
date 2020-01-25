from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from chat.models import Chat, Contact
# from chat.views import get_user_contact


class ContactUserNamesSerializer(serializers.StringRelatedField):

    def to_representation(self, value):
        return value.user.username

    def to_internal_value(self, value):
        return value


def serialize_author(user):
    img = get_thumbnail(user.profile.avatar, '100x100', crop='center', quality=99)
    return {
        'id': user.id,
        'username': user.username,
        # 'avatar': p.user.profile.avatar.url
        'avatar': img.url
    }

class ChatSerializer(serializers.ModelSerializer):
    # participants = ContactSerializer(many=True)
    participants_names = ContactUserNamesSerializer(source='participants', many=True)
    participants = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ('id',
                  # 'messages',
                  'participants', 'participants_names', 'title')
        read_only = ('id', 'title')

    def get_participants(self, instance):
        result = []
        for p in instance.participants.all():
            result.append(serialize_author(p.user))
        return result

    def get_title(self, instance):
        # if instance.p
        contacts = instance.participants.exclude(user_id=self.context['request'].user.id)
        # p = instance.participants.count()
        # if instance.participants.count() == 2:
        #     # self.context['request'].user.id
        #     return 'pass'
        return ','.join([contact.user.username for contact in contacts])

    def create(self, validated_data):
        raise NotImplemented()
        print(validated_data)
        participants = validated_data.pop('participants')
        chat = Chat()
        chat.save()
        for username in participants:
            contact = get_user_contact(username)
            # user = get_object_or_404(User, username=username)
            # get_object_or_404(Contact, user=user)
            chat.participants.add(contact)
        chat.save()
        return chat


# do in python shell to see how to serialize data

# from chat.models import Chat
# from chat.api.serializers import ChatSerializer
# chat = Chat.objects.get(id=1)
# s = ChatSerializer(instance=chat)
# s
# s.data
