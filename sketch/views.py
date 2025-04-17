import cv2
import os
import numpy as np
from django.core.files.base import ContentFile
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response  
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import SketchImage
from .serializers import SketchImageSerializer

# Function to convert an image to a sketch
def convert_to_sketch(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Invalid image format. Please upload a valid image.")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        inverted = cv2.bitwise_not(gray)  # Invert the colors
        blurred = cv2.GaussianBlur(inverted, (21, 21), sigmaX=0, sigmaY=0)  # Apply Gaussian blur
        sketch = cv2.divide(gray, 255 - blurred, scale=256)  # Create the sketch effect

        return sketch
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")

# API View to handle image uploads and sketch generation
class SketchImageViewSet(viewsets.ModelViewSet):
    queryset = SketchImage.objects.all()
    serializer_class = SketchImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            image_path = instance.original.path

            if not os.path.exists(image_path):
                return Response({"error": "File not found"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                sketch = convert_to_sketch(image_path)

                # Save the sketch image as JPG
                _, buffer = cv2.imencode('.jpg', sketch, [cv2.IMWRITE_JPEG_QUALITY, 95])
                instance.sketch.save(f"sketch_{instance.id}.jpg", ContentFile(buffer.tobytes()), save=True)

                return Response({
                    "message": "Sketch created successfully!",
                    "original": instance.original.url,
                    "sketch": instance.sketch.url
                }, status=status.HTTP_201_CREATED)

            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Home Page View
def sketch_converter(request):
    return render(request, 'home.html')
