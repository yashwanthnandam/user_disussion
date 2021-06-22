import json
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.response import Response

from .documents.user_documents import userDocument
from .models import Tags
# Create your views here.
from rest_framework.decorators import api_view

from .serializers import *


@transaction.atomic
@api_view(['POST'])
def CreateUser(request):
    data = request.data
    try:

        tags = Tags.objects.filter(name=data['tags'])
        if len(tags) == 0:
            tags = Tags.objects.create(name=data['tags'])

        user = CustomUser.objects.create_user(
            username=data['phone_number'],
            first_name=data['name'],
            phone_number=data['phone_number'],
            email=data['email'],
        )
        tags=tags.get()
        tags.user.add(user)
        tags.save()
        user.save()
        message = {'detail': 'User created successfully'}
        return Response(message, status=status.HTTP_201_CREATED)
    except:
        transaction.rollback(True)
        message = {'detail': 'User with this details already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@transaction.atomic
@api_view(['PUT'])
def updateUser(request, pk):
    try:
        data = request.data
        user = CustomUser.objects.get(id=pk)
        if len(user) == 0:
            message = {'detail': 'update details not filled properly'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        user.first_name = data['name']
        user.username = data['email']
        user.email = data['email']
        user.phone_number = data['phone_number']
        tags = Tags.objects.filter(name=data['tags'])
        if len(tags) == 0:
            tags = Tags.objects.create(name=data['tags'])
        tags = tags.get()
        user = user.get()
        tags.user.add(user)

        tags.save()
        user.save()

        message = {'detail': 'User updated successfully'}
        return Response(message, status=status.HTTP_201_CREATED)
    except:
        transaction.rollback(True)
        message = {'detail': 'Error while updation'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@transaction.atomic
@api_view(['DELETE'])
def deleteUser(request, pk):
    userForDeletion = CustomUser.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')

@transaction.atomic
@api_view(['GET'])
def users_based_on_tag(request):
    data = request.data
    try:

        tags = Tags.objects.filter(name=data['tags'])

        if len(tags) == 0:
            message = {'detail': 'No such tags exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        tag = CustomUser.objects.filter(tags=tags.get())
        users=[]
        for i in tag:
            users.append(i.first_name)
        message={'users':json.dumps(users)}
        return Response(message, status=status.HTTP_200_OK)
    except:
        transaction.rollback(True)
        message = {'detail': 'User with this details already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@csrf_exempt
def user_search(request):
    q = request.data.get('q')
    users = []
    if q:

        try:
            user_name = userDocument.search().query('match', text=q)
            for i in iter(user_name):
                users.append(i.text)
        except:
            pass
            # print(discussions)
    else:
        post = ''

        message = {'discussion': json.dumps(users)}
        return Response(message, status=status.HTTP_200_OK)

@transaction.atomic
@api_view(['GET'])
@csrf_exempt
def discussion_search(request):
    q = request.data.get('q')
    discussions = []
    if q:

        try:
            post = discussionDocument.search().query('match', text=q)
            for i in iter(post):
                discussions.append(i.text)
        except:
            pass
            # print(discussions)
    else:
        post = ''

        message = {'discussion': json.dumps(discussions)}
        return Response(message, status=status.HTTP_200_OK)

@transaction.atomic
@api_view(['GET'])
def CreateDiscussion(request):
    # Discussion can only be created when user_id is provided,tags is provided,
    # if the tag that is provided does not exist for the user as well as in the data base, then new tag is created

    try:
        data = request.data
        tags = data['tags']
        user_id = request.data['user_id']
        if (user_id == ''):
            transaction.rollback(True)
            message = {'detail': 'please provide user_id'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        if (data['tags'] == ''):
            transaction.rollback(True)
            message = {'detail': 'please provide tags'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.get(id = user_id)
        discussion = Discussion.objects.create(text=data['text'])
        tags = Tags(name=data['tags'])
        tags.save()
        tags.user.add(user)
        tags.discussion.add(discussion)
        tags.save()

        message = {'discussion': 'discussion is created'}
        return Response(message, status=status.HTTP_200_OK)

    except:
        transaction.rollback(True)
        message = {'detail': 'User with this details already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@transaction.atomic
@api_view(['PUT'])
def updateDiscussion(request, pk):
    try:
        data = request.data
        discussion = Discussion.objects.get(id=pk)
        if len(discussion) == 0:
            message = {'detail': 'update details not filled properly'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        discussion.text = data['text']
        discussion.save()
        message = {'detail': 'Discussion updated successfully'}
        return Response(message, status=status.HTTP_201_CREATED)
    except:
        transaction.rollback(True)
        message = {'detail': 'Error while updation'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteDiscussion(request, pk):
    discussion = Discussion.objects.get(id=pk)
    discussion.delete()
    return Response('Discussion was deleted')


@api_view(['GET'])
def discussion_based_on_tags(request, pk):
    data = request.data
    tag = Tags.objects.get(id=pk)
    discussions = tag.discussion_set.all()
    message = {'detail': json.dumps(discussions)}
    return Response(message, status=status.HTTP_201_CREATED)