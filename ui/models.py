from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.db import models
from django.utils.timezone import now


class Post(models.Model):

    owner = models.ForeignKey(User)
    image = models.FileField()
    description = models.TextField(blank=True, null=True)
    sent_date = models.DateTimeField(null=True, default=None)

    def send_notifications(self):
        self.sent_date = now()
        self.save()
        mails_to_notify = list()
        for user in self.get_users_to_notify():
            mails_to_notify.append(
                (
                    "{0} has published a new post".format(self.owner.username),  # subject
                    self.description,  # message
                    self.owner.email,  # from
                    [user.email]  # recipient list
                )
            )
        send_mass_mail(mails_to_notify)

    def get_users_to_notify(self):
        return User.objects.exclude(pk=self.owner.pk)

    def __str__(self):
        return self.image.url
