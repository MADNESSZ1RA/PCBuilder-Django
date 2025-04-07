from django.db import models

class VideoCard(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    chipset = models.TextField(blank=True, null=True)
    memory = models.TextField(blank=True, null=True)
    core_clock = models.TextField(blank=True, null=True)
    boost_clock = models.TextField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)
    length = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video_card'

class Case(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)
    psu = models.TextField(blank=True, null=True)
    side_panel = models.TextField(blank=True, null=True)
    external_volume = models.TextField(blank=True, null=True)
    internal_35_bays = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'case'


class Cpu(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    core_count = models.IntegerField(blank=True, null=True)
    core_clock = models.TextField(blank=True, null=True)
    boost_clock = models.TextField(blank=True, null=True)
    tdp = models.IntegerField(blank=True, null=True)
    graphics = models.TextField(blank=True, null=True)
    smt = models.BooleanField(blank=True, null=True)
    socket = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cpu'


class CpuCooler(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    rpm = models.TextField(blank=True, null=True)
    noise_level = models.TextField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)
    size = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cpu_cooler'


class InternalHardDrive(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    capacity = models.TextField(blank=True, null=True)
    price_per_gb = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    cache = models.TextField(blank=True, null=True)
    form_factor = models.TextField(blank=True, null=True)
    interface = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'internal_hard_drive'


class Memory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    speed = models.TextField(blank=True, null=True)
    modules = models.TextField(blank=True, null=True)
    price_per_gb = models.TextField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)
    first_word_latency = models.TextField(blank=True, null=True)
    cas_latency = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'memory'


class Motherboard(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    socket = models.TextField(blank=True, null=True)
    form_factor = models.TextField(blank=True, null=True)
    max_memory = models.IntegerField(blank=True, null=True)
    memory_slots = models.IntegerField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'motherboard'


class Os(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    mode = models.TextField(blank=True, null=True)
    max_memory = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'os'
