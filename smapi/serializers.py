from rest_framework import serializers
from .models import Finishing, FinishingItem



class FinishingItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinishingItem
        fields = '__all__'

    def validate_id(self, value):
        if value in None:
            raise serializers.ValidationError('Invalid value')
        return value

    def create(self, validated_data):
        return FinishingItem.objects.create(**validated_data)


class FinishingSerializer(serializers.ModelSerializer):
    finishingList = FinishingItemSerializer(many=True, read_only=True)

    class Meta:
        model = Finishing

        # fields = '__all__'
        fields = ['id', 'uuid', "room_uuid", 'room_name', "model_file", "date_create",
                  "date_update", "containerUuid", "room_number", "created_by", "finishingList"]


class FinishingItemSnippetSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=50)
    uuid = serializers.CharField(max_length=50)
    factUnits = serializers.CharField(max_length=50)
    status = serializers.CharField(max_length=50)
    comment = serializers.CharField(max_length=250)

    def validate_id(self, value):
        if value in None:
            raise serializers.ValidationError('Invalid value')
        return value

    # def create(self, validated_data):
    #     return FinishingItem.objects.create(**validated_data)

    def update_finishing_item(self, instance, validated_data):
        instance.status = instance.get('status')
        instance.factUnits = instance.get("factUnits")
        instance.comment = instance.get('comment')
        instance.date_update = instance.get('dateUpdate')
        instance.save()
        return instance