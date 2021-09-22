from django.shortcuts import render
from django.http.response import Http404, JsonResponse
from .models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets

from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
def static_data(request):
    guests = [
        {
            'id': 1,
            "Name": "Omar",
            "mobile": 1123003529,
        },
        {
            'id': 2,
            'name': "yassin",
            'mobile': 1555730223,
        }
    ]
    return JsonResponse (guests, safe=False)


def quering_data(request):
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('guest_name','mobile'))
    }
    return JsonResponse(response)


@api_view(['GET','POST'])
def FBV_List(request):
    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    # POST
    elif request.method == 'POST':
        serializer = GuestSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
        
    # PUT
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    # DELETE
    if request.method == 'DELETE':
        guest.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


class CBV_List(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many = True)
        return Response(serializer.data)
    def post(self, request):
        serializer = GuestSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)


class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExists:
            raise Http404

    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


## Rest Mixins Prevent Code Repetition As (FBVs and CBVs).
class Mixins_List(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset= Guest.objects.all()
    serializer_class= GuestSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class Mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset= Guest.objects.all()
    serializer_class= GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


## Use Generics
class Generics_List(generics.ListCreateAPIView):
    queryset= Guest.objects.all()
    serializer_class= GuestSerializer
    
    ## Security For Specific Views Using Basic Authentication
    # authentication_classes= [BasicAuthentication]
    # permission_classes= [IsAuthenticated]

class Generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset= Guest.objects.all()
    serializer_class= GuestSerializer

    ## Security For Specific Views Using Token Authentication
    authentication_classes= [TokenAuthentication]


## Use ViewSets
class Viewsets_Guest(viewsets.ModelViewSet):
    queryset= Guest.objects.all()
    serializer_class= GuestSerializer
    filter_backends= [filters.SearchFilter]
    search_fields= ['guest_name']

class Viewsets_Movie(viewsets.ModelViewSet):
    queryset= Movie.objects.all()
    serializer_class= MovieSerializer

class Viewsets_Reservation(viewsets.ModelViewSet):
    queryset= Reservation.objects.all()
    serializer_class= ReservationSerializer


## Find a Movie.
@api_view(['GET'])
def find_movie(request):
    movies= Movie.objects.filter(
        movie= request.data['movie']
    )

    serializer= MovieSerializer(movies, many= True)
    return Response(serializer.data)

## Create a Reservation.
@api_view(['POST'])
def create_reservation(request):
    ## Movie
    movie= Movie()
    movie.name= request.data['name']
    movie.hall= request.data['hall']
    movie.save()

    ## Guest
    guest= Guest()
    guest.guest_name= request.data['guest_name']
    guest.mobile= request.data['mobile']
    guest.save()

    ## Reservation
    reservation= Reservation()
    reservation.guest= guest
    reservation.movie= movie
    reservation.save()

    serializer= ReservationSerializer(reservation)
    return Response(serializer.data, status= status.HTTP_201_CREATED)


