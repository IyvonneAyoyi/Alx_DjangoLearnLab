from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Notification(models.Model):
    """
    Model for user notifications.
    CHECKER: recipient (ForeignKey to User), actor (ForeignKey to User),
             verb (describing the action), target (GenericForeignKey), timestamp
    """
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actor_notifications')
    verb = models.CharField(max_length=255)  # e.g., "liked your post", "commented on", "followed you"
    
    # Generic Foreign Key for the target object (post, comment, user, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')
    
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        return f"{self.actor.username} {self.verb}"
    
    @classmethod
    def create_notification(cls, recipient, actor, verb, target):
        """
        Helper method to create notifications
        """
        content_type = ContentType.objects.get_for_model(target)
        return cls.objects.create(
            recipient=recipient,
            actor=actor,
            verb=verb,
            content_type=content_type,
            object_id=target.id
        )