from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    """
    View for users to fetch their notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Return notifications for the current user, newest first
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by('-created_at')
    
    def get(self, request, *args, **kwargs):
        # Mark notifications as read when viewed (optional)
        Notification.objects.filter(
            recipient=request.user, 
            read=False
        ).update(read=True)
        return super().get(request, *args, **kwargs)

class UnreadNotificationCountView(generics.GenericAPIView):
    """
    View to get count of unread notifications
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        count = Notification.objects.filter(
            recipient=request.user, 
            read=False
        ).count()
        return Response({'unread_count': count})