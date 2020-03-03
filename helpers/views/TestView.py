from rest_framework.response import Response
from rest_framework.views import APIView

from wares.serializers import WarehouseSerializer


class TestView(APIView):
    def get(self, request):
        data = [
            {
                'name': 'a',

            },
            {
                'name': 'b',
            },
        ]
        serializer = WarehouseSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            explanation="ha"
        )
        return Response([serializer.data])