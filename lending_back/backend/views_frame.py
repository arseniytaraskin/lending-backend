from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import FrameSerializer, TemplateBlockSerializer
from .models import Frame, TemplateBlock

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



# ниже представления для шаблонных блоков

@api_view(['GET'])
def get_template_blocks(request):
    template_blocks = TemplateBlock.objects.all()
    serializer = TemplateBlockSerializer(template_blocks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_template_block(request): # Создание нового шаблонного блока
    serializer = TemplateBlockSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_template_block_by_id(request, pk): # получение по id
    try:
        template_block = TemplateBlock.objects.get(pk=pk)
    except TemplateBlock.DoesNotExist:
        return Response({'error': 'TemplateBlock not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TemplateBlockSerializer(template_block)
    return Response(serializer.data)


@api_view(['PATCH'])
def update_template_block(request, pk):
    try:
        template_block = TemplateBlock.objects.get(pk=pk)
    except TemplateBlock.DoesNotExist:
        return Response({'error': 'TemplateBlock not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TemplateBlockSerializer(template_block, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_template_block(request, pk):
    try:
        template_block = TemplateBlock.objects.get(pk=pk)
    except TemplateBlock.DoesNotExist:
        return Response({'error': 'TemplateBlock not found'}, status=status.HTTP_404_NOT_FOUND)
    template_block.delete()
    return Response({'message': 'TemplateBlock deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
