from django.db import models


class ChatLog(models.Model):
    """chating log """
    message = models.CharField(max_length=255)
    update_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.message
