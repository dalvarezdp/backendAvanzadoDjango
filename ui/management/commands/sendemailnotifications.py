# -*- coding: utf-8 -*-
from django.core.management import BaseCommand

from ui.models import Post


class Command(BaseCommand):

    help = 'Send e-mail notifications for not notified posts'

    def handle(self, *args, **options):
        self.stdout.write("Retrieving posts to send notifications")
        posts = Post.objects.filter(sent_date__isnull=True)
        self.stdout.write("{0} posts retrieved".format(posts.count()))
        for post in posts:
            self.stdout.write("Sending notifications for post {0}".format(post.pk))
            post.send_notifications()
        self.stdout.write("Finished!")


