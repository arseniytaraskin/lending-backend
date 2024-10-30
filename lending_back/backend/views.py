from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TextBlock
from .serializers import TextBlockSerializer

@api_view(['GET'])
def get_text_blocks(request):
    blocks = TextBlock.objects.filter(is_enabled=True)
    serializer = TextBlockSerializer(blocks, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_text_blocks(request):
    serializer = TextBlockSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_text_blocks(request, pk):
    #сначал проверю есть ли в целом текстовый блок под указанным id на странице
    try:
        text_block = TextBlock.objects.get(pk=pk)
    except TextBlock.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    serializer = TextBlockSerializer(text_block, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
