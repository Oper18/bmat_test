import dateutil.parser

from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Avg

from . import models, serializers


class DSRViewSet(viewsets.ModelViewSet):
    queryset = models.DSR.objects.all()
    serializer_class = serializers.DSRSerializer

    def list(self, request, *args, **kwargs):
        if kwargs.get("id"):
            self.queryset = self.queryset.get(pk=kwargs.get("id"))
            serializer = self.get_serializer(self.queryset)
            return Response(serializer.data)
        return super(DSRViewSet, self).list(request, *args, **kwargs)


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourceSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.\
            filter(
                revenue=self.queryset.aggregate(
                    total_revenue=Avg("revenue")
                )["total_revenue"] * float(kwargs.get("revenue")) / 100
            )
        if request.query_params.get("territory"):
            self.queryset = self.queryset.\
                filter(dsrs__territory__code_2=request.query_params.get("territory"))
        if request.query_params.get("period_start"):
            self.queryset = self.queryset.\
                filter(dsrs__period_start=dateutil.parser.parse(request.query_params.get("period_start")))
        if request.query_params.get("period_end"):
            self.queryset = self.queryset.\
                filter(dsrs__period_end=dateutil.parser.parse(request.query_params.get("period_start")))
        return super(ResourceViewSet, self).list(request, *args, **kwargs)
