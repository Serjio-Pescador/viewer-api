from django.http import (
    JsonResponse,
    Http404,
    HttpResponse,
)
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from uuid import uuid4
import psycopg2
from datetime import datetime, timezone
from .models import Finishing, FinishingItem
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import FinishingItemSerializer, FinishingSerializer
import json as JSON
import environ
import os
from .filters import FinishingViewSet



env = environ.Env()

DATABASE_HOST = os.getenv('DATABASE_HOST') == 'localhost'

connection = psycopg2.connect(host=env('DB_HOST'), port=5432, user="postgres", password="postgrespw",
                              database="simpleviewer")
cursor = connection.cursor()




@api_view(['GET'])
def home(request):
    return HttpResponse("Api Viewer")


@api_view(['GET'])
def items_api(request, **kwargs):
    list_items = FinishingItem.objects.all()
    parameters = request.GET.dict()
    if parameters.get('id') is not None:
        list_items = FinishingItem.objects.filter(id=parameters.get('id', None))
    elif parameters.get('finishing') is not None:
        list_items = FinishingItem.objects.filter(finishing=parameters.get('finishing', None))
    elif parameters.get('uuid') is not None:
        list_items = FinishingItem.objects.filter(uuid=parameters.get('uuid', None))

    serializer = FinishingItemSerializer(list_items, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'PUT'])
def room_checklist(request, uuid=None, **kwargs, ):

    if request.method == 'GET':
        query = Finishing.objects.all()
        parameters = request.GET.dict()
        if parameters.get('roomUuid') is not None:
            query = Finishing.objects.filter(room_uuid=parameters.get('roomUuid', None))
        elif parameters.get('id') is not None:
            query = Finishing.objects.filter(id=parameters.get('id', None))
        elif parameters.get('uuid') is not None:
            query = Finishing.objects.filter(uuid=parameters.get('uuid', None))
        serializer = FinishingSerializer(query, many=True)
        # return JsonResponse({"content": serializer.data})
        return HttpResponse(JSON.dumps({"content": serializer.data}, ensure_ascii=False),
         content_type="application/json")


    elif request.method == 'POST':
        data = request.data
        checklist = Finishing()
        if checklist is not None:
            checklist.room_uuid = data.get("roomUuid", None)
            checklist.uuid = uuid4()
            checklist.room_name = data.get("roomName", None)
            checklist.room_number = data.get("roomNumber", None)
            checklist.model_file = data.get("modelFile", None)
            checklist.containerUuid = data.get("containerUuid")
            checklist.create_by = data.get("createBy", 'demo-user-uuid')
            checklist.save()
            id = checklist.id
            items_list = data.get("finishingList")

            for item in items_list:
                create_finishing_item(finishing_item=item, finishing_id=id)
            query = Finishing.objects.filter(uuid=checklist.uuid)
            serializer = FinishingSerializer(query, many=True)
            return JsonResponse(data=serializer.data[0], status=status.HTTP_201_CREATED)
        else:
            return Response(checklist.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'PUT':
        query = request.data
        if query is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            db_item = FinishingItem.objects.filter(uuid=uuid)
            serializer = FinishingItemSerializer(db_item, many=True)
            item_update(query)
            updated_item = FinishingItem.objects.filter(uuid=uuid)
            serializer = FinishingItemSerializer(updated_item, many=True)
            json = JSONRenderer().render(serializer.data[0])
            return Response(json, status=status.HTTP_202_ACCEPTED)



def create_finishing_item(finishing_item, finishing_id: int):
    today_now = datetime.now(timezone.utc)
    db_finishing_item = FinishingItem(
        uuid=uuid4(),
        type=finishing_item['type'],
        name=finishing_item['name'],
        mark=finishing_item['mark'],
        units=finishing_item['units'],
        factUnits=finishing_item["factUnits"],
        unitType=finishing_item["unitType"],
        dateCreate=today_now,
        dateUpdate=today_now,
        # status=status_item(finishing_item['status']),
        status=finishing_item['status'],
        comment=finishing_item['comment'],
        finishing_id=finishing_id
    )
    db_finishing_item.save()
    return db_finishing_item.id




def item_update(data):
    fact_units = str(data['factUnits'])
    date_update = str(datetime.now(timezone.utc))
    status_item = str(data['status'])
    comment = str(data['comment'])
    uuid = str(data['uuid'])
    uuid_checklist = data['id']
    print((fact_units, date_update, status_item, comment, uuid))

    with connection.cursor() as cur:
        query = """UPDATE finishing_item SET "dateUpdate" = %s, "factUnits" = %s, status = %s, comment = %s WHERE uuid = %s;"""
        cur.execute(query, (date_update, fact_units, status_item, comment, uuid))
        connection.commit()
        update_date_checklist = """UPDATE finishing SET "date_update" = %s WHERE uuid = %s;"""
        cur.execute(update_date_checklist, (date_update, uuid_checklist))
        connection.commit()
        cur.execute(f"SELECT * FROM finishing_item WHERE uuid='{uuid}';")
        data = cur.fetchone()
        connection.commit()
    return data



# @api_view(['PUT'])
# def items(request, uuid:str, id:str):
#     query = request.data
#     if query is None:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     else:
#         db_item = FinishingItem.objects.filter(uuid=uuid)
#         serializer = FinishingItemSnippetSerializer(query, data=db_item)
#         print("here", db_item)
#         if serializer.is_valid():
#             serializer.save()
#             print(serializer.validated_data)
#             return Response(serializer.data)
#         return HttpResponse("serializer")