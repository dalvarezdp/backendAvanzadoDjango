from celery import shared_task
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

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if self.sent_date is None:
            # send_notifications_for_post(self.pk)  # mandamos las notificaciones de manera síncrona
            send_notifications_for_post.delay(self.pk)  # mandamos a celery la tarea de enviar las notificaciones en background

    def __str__(self):
        return self.image.url


@shared_task
def send_notifications_for_post(post_id):
    try:
        post = Post.objects.get(pk=post_id)
        print("Sending post {0} notifications...".format(post.pk))
        post.send_notifications()
        print("Finished")
    except Post.DoesNotExist:
        print("Post {0} does not exist".format(post.pk))


