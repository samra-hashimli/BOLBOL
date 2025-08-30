from ..models.comment import Comment
from ..models.product import Product
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status
from ..serializers.comment_serializer import CommentSerializer


class CommentsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, product_id):
        comments = Comment.objects.filter(product_id=product_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, product_id):
        data = request.data
        product = get_object_or_404(id=product_id)
        serializer = CommentSerializer(data=data)

        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)