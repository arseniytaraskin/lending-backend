from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TextBlock, ImageBlock
from .serializers import TextBlockSerializer, ImageBlockSerializer
from django.http import JsonResponse

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
    # Проверка существования текстового блока
    try:
        text_block = TextBlock.objects.get(pk=pk)
    except TextBlock.DoesNotExist:
        return Response({"error": "TextBlock not found"}, status=status.HTTP_404_NOT_FOUND)

    # Обновление блока
    data = request.data
    if "styles" in data:

        existing_styles = text_block.styles or {}
        new_styles = data.get("styles", {})
        updated_styles = {**existing_styles, **new_styles}  # Слияние стилей
        data["styles"] = updated_styles

    serializer = TextBlockSerializer(text_block, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_text_block(request, pk):
    try:
        text_block = TextBlock.objects.get(pk=pk)
    except TextBlock.DoesNotExist:
        return Response({"error": "Текстовый блок не найден"}, status=status.HTTP_404_NOT_FOUND)

    text_block.delete()
    return Response({"message": "Текстовый блок успешно удален"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_text_block_by_id(request, pk):
    try:
        text_block = TextBlock.objects.get(pk=pk)
        serializer = TextBlockSerializer(text_block)
        return Response(serializer.data)
    except:
        return Response({"error": "Текстовый блок не найден"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_images(request):
    images = ImageBlock.objects.all()
    serialized_images = [
        {
            'id': image.id,
            'image': image.image.url,
            'description': image.description,
            'is_enabled': image.is_enabled,
            'styles': image.styles
        }
        for image in images
    ]
    return JsonResponse(serialized_images, safe=False)

@api_view(['GET'])
def get_image_by_id(request, pk):
    try:
        image_block = ImageBlock.objects.get(pk=pk)
        serialized_image = {
            'id': image_block.id,
            'image': image_block.image.url,
            'description': image_block.description,
            'is_enabled': image_block.is_enabled,
            'styles': image_block.styles
        }
        return JsonResponse(serialized_image, safe=False)
    except ImageBlock.DoesNotExist:
        return Response({"error": "Изображение не найдено"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT', 'PATCH'])
def update_image(request, pk):
    try:
        image_block = ImageBlock.objects.get(pk=pk)
    except ImageBlock.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ImageBlockSerializer(image_block, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_image(request):
    try:
        if 'image' not in request.FILES:
            return Response({"error": "Пожалуйста, добавьте файл изображения"}, status=status.HTTP_400_BAD_REQUEST)

        # добавил проверку на то что переданный файл это картинка, а также выставил ограничение на размер передаваемого файла
        uploaded_file = request.FILES['image']
        max_size_mb = 10
        if uploaded_file.size > max_size_mb * 1024 * 1024:
            return Response({"error": f"Размер изображения не должен превышать {max_size_mb} МБ"}, status=status.HTTP_400_BAD_REQUEST)

        allowed_content_types = ['image/jpeg', 'image/png']
        if uploaded_file.content_type not in allowed_content_types:
            return Response({"error": "Разрешены только изображения в формате JPEG и PNG"}, status=status.HTTP_400_BAD_REQUEST)


        serializer = ImageBlockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_image(request, pk):
    try:
        image_block = ImageBlock.objects.get(pk=pk)
    except ImageBlock.DoesNotExist:
        return Response({"error": "Изображение не найдено"}, status=status.HTTP_404_NOT_FOUND)

    if image_block.image:
        image_block.image.delete(save=False)

    image_block.delete()
    return Response({"message": "Изображение успешно удалено"}, status=status.HTTP_200_OK)




