from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import CartItemSerializer
from .models import CartItem


class CartItemViews(APIView):
    def post(self, request):
        # Create a serializer instance with the request data
        serializer = CartItemSerializer(data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():
            # Save the valid data to create a new CartItem
            serializer.save()

            # Return a success response with the created data
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            # Return an error response with details on validation errors
            return Response(
                {"status": "error", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request, id=None):
        # Get all model fields as valid query parameters
        model_fields = [field.name for field in CartItem._meta.fields]

        # Get all valid query parameters from the request
        query_params = request.GET
        filtered_params = {
            field: query_params[field] for field in model_fields if field in query_params
        }

        # If an 'id' is provided, retrieve a single item
        if id:
            item = get_object_or_404(CartItem, id=id, **filtered_params)
            serializer = CartItemSerializer(item)
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        # If no 'id' is provided, retrieve a list of items with optional filtering
        items = CartItem.objects.filter(**filtered_params)
        serializer = CartItemSerializer(items, many=True)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, id):
        # Use get_object_or_404 to handle the case where the item is not found
        item = get_object_or_404(CartItem, id=id)

        # Use partial=True to allow partial updates
        serializer = CartItemSerializer(item, data=request.data, partial=True)

        # Validate and save the updated data
        if serializer.is_valid():
            serializer.save()

            # Return a success response with the updated data
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            # Return an error response with details on validation errors
            return Response(
                {"status": "error", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, id):
        item = get_object_or_404(CartItem, id=id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
