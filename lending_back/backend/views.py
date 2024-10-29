from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import TextBlock
from .serializers import TextBlockSerializer

@api_view(['GET'])
def get_text_blocks(request):
    blocks = TextBlock.objects.filter(is_enabled=True)
    serializer = TextBlockSerializer(blocks, many=True)
    return Response(serializer.data)
