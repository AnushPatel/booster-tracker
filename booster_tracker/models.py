from django.db import models

# Create your models here.

RECOVERY_METHODS = [("EXPENDED", "expended"), ("OCEAN_SURFACE", "ocean"), ("DRONE_SHIP", "ASDS"), ("GROUND_PAD", "landing zone")]
LAUNCH_OUTCOMES = [("SUCCESS", "success"), ("FAILURE", "failure"), ("PARTIAL FAILURE", "partial failure")]
BOAT_TYPES = [("TUG", "tug"), ("FAIRING_RECOVERY", "fairing recovery"), ("SUPPORT", "support")]
STAGE_TYPES = [("BOOSTER", "booster"), ("SECOND_STAGE", "second stage")]

class Rocket(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Stage(models.Model):
    name = models.CharField(max_length=20)
    rocket = models.ForeignKey(Rocket, on_delete=models.CASCADE)
    version = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=STAGE_TYPES)

    def __str__(self):
        return self.name

class Boat(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200, choices=BOAT_TYPES)

    def __str__(self):
        return self.name

class Orbit(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Pad(models.Model):
    name = models.CharField(max_length=200)
    nickname = models.CharField(max_length=10)

    def __str__(self):
        return self.nickname

class Launch(models.Model):
    time = models.DateTimeField("Launch Time")
    pad = models.ForeignKey(Pad, on_delete=models.CASCADE)
    rocket = models.ForeignKey(Rocket, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    orbit = models.ForeignKey(Orbit, on_delete=models.CASCADE)
    mass = models.CharField(max_length=200)
    customer = models.CharField(max_length=200)
    launch_outcome = models.CharField(max_length=200, choices=LAUNCH_OUTCOMES)

    class Meta:
        verbose_name_plural = "Launches"
        ordering = ["-time"]

    def __str__(self):
        return self.name

class LandingZone(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class StageAndRecovery(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    landing_zone = models.ForeignKey(LandingZone, on_delete=models.CASCADE, null=True)
    method = models.CharField(max_length=200, choices=RECOVERY_METHODS)
    method_success = models.BooleanField(null=True)
    recovery_success = models.BooleanField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Stages and Recoveries"

class FairingRecovery(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, limit_choices_to={"type": "FAIRING_RECOVERY"})
    catch = models.BooleanField()
    recovery = models.CharField(max_length=200)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    flights = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Fairing Recoveries"

class TugOnLaunch(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, limit_choices_to={"type": "TUG"})

    class Meta:
        verbose_name_plural = "Tugs on Launch"
        
class SupportOnLaunch(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, limit_choices_to={"type": "SUPPORT"})

    class Meta:
        verbose_name_plural = "Support ships on launch"