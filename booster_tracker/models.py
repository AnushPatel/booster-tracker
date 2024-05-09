from django.db import models

# Create your models here.

RECOVERY_METHODS = [("EXPENDED", "expended"), ("OCEAN_SURFACE", "ocean"), ("DRONE_SHIP", "ASDS"), ("GROUND_PAD", "landing zone"), ("PARACHUTE", "parachute")]
LAUNCH_OUTCOMES = [("SUCCESS", "success"), ("FAILURE", "failure"), ("PARTIAL FAILURE", "partial failure")]
LANDING_METHOD_OUTCOMES = [("SUCCESS", "success"), ("FAILURE", "failure"), ("PRECLUDED", "precluded")]
BOAT_TYPES = [("TUG", "tug"), ("FAIRING_RECOVERY", "fairing recovery"), ("SUPPORT", "support")]
STAGE_TYPES = [("BOOSTER", "booster"), ("SECOND_STAGE", "second stage")]
SPACECRAFT_TYPES = [("CARGO", "cargo"), ("CREW", "crew")]
STAGE_LIFE_OPTIONS = [("ACTIVE", "active"), ("RETIRED", "retired"), ("EXPENDED", "expended"), ("LOST", "lost")]

class Operator(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Rocket(models.Model):
    name = models.CharField(max_length=100)
    provider = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Stage(models.Model):
    name = models.CharField(max_length=20)
    rocket = models.ForeignKey(Rocket, on_delete=models.CASCADE)
    version = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=STAGE_TYPES)
    status = models.CharField(max_length=20, choices=STAGE_LIFE_OPTIONS, default="ACTIVE")
    photo = models.ImageField(upload_to='stage_photos/', null=True, blank=True)

    def __str__(self):
        return self.name

class Spacecraft(models.Model):
    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20, blank=True, null=True)
    version = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20, choices=SPACECRAFT_TYPES)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)

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
    name = models.CharField(max_length=200, unique=True)
    orbit = models.ForeignKey(Orbit, on_delete=models.CASCADE)
    mass = models.CharField(max_length=200)
    customer = models.CharField(max_length=200)
    launch_outcome = models.CharField(max_length=200, choices=LAUNCH_OUTCOMES, blank=True, null=True)

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
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, null=True, blank=True)
    landing_zone = models.ForeignKey(LandingZone, on_delete=models.CASCADE, null=True, blank=True)
    method = models.CharField(max_length=200, choices=RECOVERY_METHODS)
    method_success = models.CharField(max_length=200, choices=LANDING_METHOD_OUTCOMES, null=True, blank=True)
    recovery_success = models.BooleanField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        if self.stage and self.stage.name:
            return f"{self.stage.name} recovery"
        return("Unknown recovery")
    
class FairingRecovery(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, limit_choices_to={"type": "FAIRING_RECOVERY"}, null=True, blank=True)
    catch = models.BooleanField()
    recovery = models.CharField(max_length=200)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    flights = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Fairing Recoveries"

    def __str__(self):
        if self.boat:
            return f"Fairing recovery with {self.boat.name}"
        return "Unknown fairing recovery"

class TugOnLaunch(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, limit_choices_to={"type": "TUG"})

    class Meta:
        verbose_name_plural = "Tugs on Launch"

    def __str__(self):
        if self.boat:
            return self.boat.name
        
class SupportOnLaunch(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, limit_choices_to={"type": "SUPPORT"})

    class Meta:
        verbose_name_plural = "Support ships on launch"
    
    def __str__(self):
        if self.boat:
            return self.boat.name
    
class SpacecraftOnLaunch(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    spacecraft = models.ForeignKey(Spacecraft, on_delete=models.CASCADE)
    splashdown_time = models.DateTimeField("Splashdown Time", null=True)

    class Meta:
        verbose_name_plural = "Dragon on launch"
    
    def __str__(self):
        if self.spacecraft:
            return f"{self.spacecraft.name} on launch"
        
class PadUsed(models.Model):
    rocket = models.ForeignKey(Rocket, on_delete=models.CASCADE)
    pad = models.ForeignKey(Pad, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='rocket_pad_photos/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Pads used"
    
    def __str__(self):
        if self.pad:
            return f"{self.pad.name}"