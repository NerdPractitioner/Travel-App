from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(
        User, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        # contact list(friends) of self.user
        return 'Contacts of %r, with %s friends' % (self.user.username, self.friends.count())


class Message(models.Model):
    author = models.ForeignKey(
        Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey('Chat', related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return 'from {} to chat #{}'.format(self.author.user.username, self.chat.id)


class Chat(models.Model):
    title = models.TextField(blank=True)
    slug = models.CharField(blank=True, max_length=64)
    is_group = models.BooleanField(default=False)

    participants = models.ManyToManyField(
        Contact, related_name='chats', blank=True)
    # messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        # return "#{}".format(self.pk)
        participants = ','.join([p.user.username for p in self.participants.all()])
        return '#%s participants: %s' % (self.pk, participants)
