from uuid import UUID, uuid4

from django.contrib.auth.models import User, Group
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from comic import models
from rest_framework import viewsets, serializers, mixins, permissions

from comic.util import generate_directory


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class DirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Directory

        fields = ['name', 'parent', 'selector', 'thumbnail', 'thumbnail_issue', 'thumbnail_index', 'classification']


class DirectoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows Directories to be viewed.
    """
    queryset = models.Directory.objects.all()
    lookup_field = 'selector'
    serializer_class = DirectorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ComicBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ComicBook
        fields = ['file_name', 'date_added', 'directory', 'selector', 'version', 'thumbnail', 'thumbnail_index']


class ComicBookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.ComicBook.objects.all()
    serializer_class = ComicBookSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['directory', 'selector']


class BrowseSerializer(serializers.Serializer):
    selector = serializers.UUIDField()
    title = serializers.CharField()
    progress = serializers.IntegerField()
    total = serializers.IntegerField()
    type = serializers.CharField()


class BrowseViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BrowseSerializer
    lookup_field = 'selector'

    def list(self, request):
        queryset = []
        for item in generate_directory(request.user):
            queryset.append({
                "selector": item.obj.selector,
                "title": item.name,
                "progress": item.total_read,
                "total": item.total,
                "type": item.item_type
            })
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, selector: UUID):
        queryset = []
        directory = models.Directory.objects.get(selector=selector)
        for item in generate_directory(request.user, directory):
            queryset.append({
                "selector": item.obj.selector,
                "title": item.name,
                "progress": item.total_read,
                "total": item.total,
                "type": item.item_type
            })
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)