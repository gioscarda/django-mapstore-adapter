# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import MapStoreResource
from .serializers import (UserSerializer,
                          MapStoreResourceSerializer,)
from ..hooks import hookset

import logging

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class MapStoreResourceViewSet(viewsets.ModelViewSet):
    """ Only Authenticate User perform CRUD Operations on Respective Data
    """
    permission_classes = [IsAuthenticated]
    # queryset = MapStoreResource.objects.all()
    model = MapStoreResource
    serializer_class = MapStoreResourceSerializer

    def get_queryset(self):
        """ Return datasets belonging to the current user """
        queryset = self.model.objects.all()

        # filter to tasks owned by user making request
        queryset = hookset.get_queryset(self, queryset)
        return queryset

    def perform_create(self, serializer):
        """ Associate current user as task owner """
        if serializer.is_valid():
            hookset.perform_create(self, serializer)
            return serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """ Associate current user as task owner """
        if serializer.is_valid():
            hookset.perform_update(self, serializer)
            return serializer.save()
