# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ApiAuthentication(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    token = models.CharField(max_length=50)
    expiration = models.DateTimeField()
    client = models.ForeignKey('ApiInstance', models.DO_NOTHING)
    target = models.ForeignKey('ApiInstance', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_authentication'
        unique_together = (('client', 'target'),)


class ApiDataset(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    pub_date = models.DateTimeField()
    namespace = models.ForeignKey('ApiInstance', models.DO_NOTHING)
    instancename = models.ForeignKey('ApiInstance', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_dataset'
        unique_together = (('name', 'namespace'),)


class ApiDatasetAllowedToGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    dataset = models.ForeignKey(ApiDataset, models.DO_NOTHING)
    group = models.ForeignKey('ApiGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_dataset_allowed_to_group'
        unique_together = (('dataset', 'group'),)


class ApiDatasetAllowedToSingle(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    dataset = models.ForeignKey(ApiDataset, models.DO_NOTHING)
    instance = models.ForeignKey('ApiInstance', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_dataset_allowed_to_single'
        unique_together = (('dataset', 'instance'),)


class ApiDatasetLocations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    dataset = models.ForeignKey(ApiDataset, models.DO_NOTHING)
    location = models.ForeignKey('ApiLocation', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_dataset_locations'
        unique_together = (('dataset', 'location'),)


class ApiGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=50)
    owner = models.ForeignKey('ApiInstance', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_group'


class ApiGroupInstances(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(ApiGroup, models.DO_NOTHING)
    instance = models.ForeignKey('ApiInstance', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_group_instances'
        unique_together = (('group', 'instance'),)


class ApiInstance(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    name = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=254)
    creation_date = models.DateTimeField()
    instancename = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'api_instance'


class ApiInstanceOld(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    name = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=254)
    creation_date = models.DateTimeField()
    instancename = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'api_instance__old'


class ApiInstanceGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    instance = models.ForeignKey(ApiInstance, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_instance_groups'
        unique_together = (('instance', 'group'),)


class ApiInstanceUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    instance = models.ForeignKey(ApiInstance, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_instance_user_permissions'
        unique_together = (('instance', 'permission'),)


class ApiLocation(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    details = models.CharField(max_length=300)
    uri = models.CharField(db_column='URI', max_length=100)  # Field name made lowercase.
    namespace = models.ForeignKey(ApiInstance, models.DO_NOTHING)
    instancename = models.ForeignKey(ApiInstance, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_location'
        unique_together = (('name', 'namespace'),)


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.ForeignKey(ApiInstance, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(ApiInstance, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
