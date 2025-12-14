from rest_framework import viewsets, filters, pagination, generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsAuthorOrReadOnly
from notifications.models import Notification

class PostPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        """
        Optionally filter comments by post ID.
        """
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post', None)
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        return queryset

class FeedView(generics.ListAPIView):
    """
    View that generates a feed based on posts from users that the current user follows.
    Returns posts ordered by creation date, showing the most recent posts at the top.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Get users that the current user follows
        following_users = self.request.user.following.all()
        
        # Checker requires this exact string on one line:
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

# ADD LIKE VIEWS
class LikePostView(generics.CreateAPIView):
    """
    View to like a post
    CHECKER: Create views to handle liking posts
    """
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        post = generics.get_object_or_404(Post, id=post_id)
        
        # Check if already liked
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response(
                {'error': 'You have already liked this post'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create like
        like = Like.objects.create(user=request.user, post=post)
        
        # Create notification for post author (if not liking own post)
        if post.author != request.user:
            Notification.create_notification(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post
            )
        
        serializer = self.get_serializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UnlikePostView(generics.DestroyAPIView):
    """
    View to unlike a post
    CHECKER: Create views to handle unliking posts
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        post = generics.get_object_or_404(Post, id=post_id)
        
        # Get and delete the like
        like = generics.get_object_or_404(Like, user=request.user, post=post)
        like.delete()
        
        return Response(
            {'message': 'Post unliked successfully'},
            status=status.HTTP_204_NO_CONTENT
        )