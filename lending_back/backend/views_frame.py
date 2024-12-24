from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import FrameSerializer
from .models import Frame

@api_view(['GET'])
def get_frames(request):
    frames = Frame.objects.filter(is_enabled=True).order_by('order')
    serializer = FrameSerializer(frames, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_frame(request):
    serializer = FrameSerializer(data=request.data)
    if serializer.is_valid():
        frame = serializer.save()
        return Response(FrameSerializer(frame).data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_frame_by_id(request, pk):    # Получение конкретного фрейма по его ID
    try:
        frame = Frame.objects.get(pk=pk)
    except Frame.DoesNotExist:
        return Response({'error': 'Frame not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = FrameSerializer(frame)
    return Response(serializer.data)


@api_view(['PATCH'])
def update_frame(request, pk):
    try:
        frame = Frame.objects.get(pk=pk)
    except Frame.DoesNotExist:
        return Response({'error': 'Frame not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = FrameSerializer(frame, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_frame(request, pk):
    try:
        frame = Frame.objects.get(pk=pk)
    except Frame.DoesNotExist:
        return Response({'error': 'Frame not found'}, status=status.HTTP_404_NOT_FOUND)

    frame.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



#

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ContentBlock
from .serializers import ContentBlockSerializer

@api_view(['GET'])
def list_content_blocks(request):
    blocks = ContentBlock.objects.filter(enabled=True).order_by('order')
    serializer = ContentBlockSerializer(blocks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_content_block(request, pk):

    try:
        block = ContentBlock.objects.get(pk=pk)
    except ContentBlock.DoesNotExist:
        return Response({"error": "Блок не найден"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ContentBlockSerializer(block)
    return Response(serializer.data)

@api_view(['POST'])
def create_content_block(request):

    serializer = ContentBlockSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_content_block(request, pk):

    try:
        block = ContentBlock.objects.get(pk=pk)
    except ContentBlock.DoesNotExist:
        return Response({"error": "Блок не найден"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ContentBlockSerializer(block, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_content_block(request, pk):

    try:
        block = ContentBlock.objects.get(pk=pk)
    except ContentBlock.DoesNotExist:
        return Response({"error": "Блок не найден"}, status=status.HTTP_404_NOT_FOUND)

    block.delete()
    return Response({"message": "Блок успешно удалён"}, status=status.HTTP_204_NO_CONTENT)

