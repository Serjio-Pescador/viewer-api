from django.db import models


class Finishing(models.Model):

    class Meta:
        db_table = 'finishing'
        # ordering = ['date_update'].sort(reverse=False)

    id = models.AutoField(primary_key=True, auto_created=True, unique=True)
    uuid = models.CharField(unique=True, null=False, max_length=250, db_index=True)
    room_uuid = models.CharField(null=False, max_length=250, db_index=True)
    room_name = models.CharField(null=False, max_length=250, db_index=True)
    model_file = models.CharField(null=False, max_length=250, db_index=True)
    # project_id = models.CharField(null=False, max_length=250, db_index=True)
    containerUuid = models.CharField(null=False, max_length=250, db_index=True)
    # container_id = models.CharField(null=False, max_length=250, db_index=True)
    date_create = models.DateTimeField(auto_now=True, null=False, db_index=True)
    date_update = models.DateTimeField(auto_now_add=True, null=False, db_index=True)
    room_number = models.CharField(null=False, max_length=250, db_index=True)
    created_by = models.CharField(null=False, max_length=250, db_index=True, default="by RSA")
    finishingList = models.ManyToOneRel("finishing_id", to="FinishingItem", field_name="finishing_id")

    def __str__(self):
        return self.uuid


class FinishingItem(models.Model):

    class Meta:
        db_table = 'finishing_item'
        ordering = ['dateUpdate'].sort(reverse=False)

    id = models.AutoField(primary_key=True, auto_created=True, unique=True)
    uuid = models.CharField(unique=True, null=False, max_length=50, db_index=True)
    type = models.CharField(null=False, max_length=250, db_index=True)
    name = models.CharField(null=False, max_length=250, db_index=True)
    mark = models.CharField(null=False, max_length=250, db_index=True)
    units = models.CharField(null=False, max_length=250, db_index=True)
    factUnits = models.CharField(null=False, max_length=250, db_index=True)
    unitType = models.CharField(null=False, max_length=250, db_index=True)
    dateCreate = models.DateTimeField(auto_created=True, null=False, db_index=True)
    dateUpdate = models.DateTimeField(auto_now_add=True, null=False, db_index=True)
    status = models.CharField(null=False, default='AWAIT', max_length=50, db_index=True)
    comment = models.CharField(null=False, max_length=250, db_index=True)
    finishing = models.ForeignKey("Finishing", related_name='finishingList',on_delete=models.CASCADE)

    def __str__(self):
        return self.name
