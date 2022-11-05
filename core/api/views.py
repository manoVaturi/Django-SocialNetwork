from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Room, User, Topic, Message
from .serializers import RoomSerializer, TopicSerializer


@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api'
        'GET /api/rooms',
        'GET /api/rooms/:id',
        'GET /api/topics',

    ]
    return Response(routes)


@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_room(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def get_topics(request):
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)
