from django.db import models
from django.contrib.auth.models import User
from main.models import Cpu, Motherboard, Memory, Case, CpuCooler, InternalHardDrive, Os, VideoCard, PowerSupply

class SavedBuild(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    build_name = models.CharField(max_length=100, blank=True, null=True)

    cpu = models.ForeignKey(Cpu, on_delete=models.SET_NULL, blank=True, null=True)
    motherboard = models.ForeignKey(Motherboard, on_delete=models.SET_NULL, blank=True, null=True)
    memory = models.ForeignKey(Memory, on_delete=models.SET_NULL, blank=True, null=True)
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, blank=True, null=True)
    cpu_cooler = models.ForeignKey(CpuCooler, on_delete=models.SET_NULL, blank=True, null=True)
    hdd = models.ForeignKey(InternalHardDrive, on_delete=models.SET_NULL, blank=True, null=True)
    os = models.ForeignKey(Os, on_delete=models.SET_NULL, blank=True, null=True)
    video_card = models.ForeignKey(VideoCard, on_delete=models.SET_NULL, blank=True, null=True)
    powersupply = models.ForeignKey(PowerSupply, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"SavedBuild #{self.id} by {self.user} | {self.build_name or 'No Name'}"