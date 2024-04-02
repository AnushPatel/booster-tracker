#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 23:07:03 2024

@author: trevorsesnic
"""

import sys
print(sys.path)
sys.path.append("")


import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "launches_project.settings")
django.setup()


from booster_tracker.models import *
from django.db import transaction
from dateutil import parser
from datetime import datetime, timedelta, date
from itertools import islice
from matplotlib.ticker import FuncFormatter
from enum import StrEnum

import matplotlib.dates as dates
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import statistics
import math

class ClassLaunch:
    def __init__(self, time: datetime, rocket: str, boosters, booster_flights: list[int], payload: str, mass: str, orbit: str, customer: str, launch_outcome: str, location, booster_landing_outcomes: list[str], landing_zones, secondstage, secondstage_flights: int, \
                booster_lat: float, booster_long: float, booster_support, booster_tug: str, fairing_flights: list[str], fairings_recovered: list[str], fairing_recovery_boats, fairing_lat: float, fairing_long: float, second_stage_recovery_location):
        self.time = time
        self.rocket = rocket
        self.boosters: list[Booster] = boosters
        self.booster_flights = booster_flights
        self.payload = payload
        self.mass = mass
        self.orbit = orbit
        self.customer = customer
        self.launch_outcome = launch_outcome
        self.location: ClassPad = location
        self.pad_turnaround = None
        self.booster_turnaround = []
        self.company_turnaround = None
        self.zone_turnaround = []
        self.booster_landing_outcomes = booster_landing_outcomes
        self.landing_zones: list[ClassLandingZone] = landing_zones
        self.secondstage: SecondStage = secondstage
        self.secondstage_flights = secondstage_flights
        self.booster_lat = booster_lat
        self.booster_long = booster_long
        self.booster_support: list[SupportShip] = booster_support
        self.booster_tug = booster_tug
        self.fairing_flights = fairing_flights
        self.fairings_recovered = fairings_recovered
        self.fairing_recovery_boats: list[ClassFairingRecovery] = fairing_recovery_boats
        self.fairing_lat = fairing_lat
        self.fairing_long = fairing_long
        self.second_stage_recovery_location: ClassLandingZone = second_stage_recovery_location

    def __str__(self):
        return f"{self.payload}"
    
    def __repr__(self):
        return str(self)


class Component(StrEnum):
    BOOSTER = "booster"
    FAIRING = "fairing"
    SECONDSTAGE = "secondstage"

class RocketOptions(StrEnum):
    FALCON_9 = "Falcon 9"
    FALCON_HEAVY = "Falcon Heavy"
    FALCON_1 = "Falcon 1"
    STARSHIP = "Starship"
    FALCON = "Falcon"
    ALL = "all"

class RocketFamilyOptions(StrEnum):
    FALCON = "Falcon"
    STARSHIP = "Starship"
    ALL = "all"

class EventOptions(StrEnum):
    LAUNCH = "launch"
    BOOSTER_LANDING = "booster landing"
    FAIRING_RECOVERY = "fairing recovery"
    SECONDSTAGE_LANDING = "second stage landing"

class LaunchCalculator:
    def __init__(self, name: str):
        self.launches: list[ClassLaunch] = []
        self.name = name

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return str(self)

    def __eq__(self, object): #This function allows for checking if the booster/pad already exists; if the name is the same later in the code we ignore it
        return self.name == object.name
    
    def num_launches(self) -> int:
        return len(self.launches)

    def avg_min_turnaround(self, num_launches: int = 1) -> tuple:
        turnaround_times = []
        
        for index, _ in islice(enumerate(self.launches), num_launches, None):
            turnaround_times.append((self.launches[index].time - self.launches[index - num_launches].time).total_seconds() / 86400)
        
        if len(turnaround_times) == 0:
            return 0, 0
        else:
            return statistics.mean(turnaround_times), min(turnaround_times)
        
    def last_turnaround(self, num_launches: int = 1) -> float:
        if not len(self.launches) < 1 + num_launches:
            return((self.launches[len(self.launches)-1].time - self.launches[len(self.launches)-(num_launches+1)].time).total_seconds() / 86400)
        
class Booster(LaunchCalculator):
    def __init__(self, name: str, rocket: str, version: str):
        self.rocket = rocket
        self.version = version
        super().__init__(name=name)
    

class SecondStage(LaunchCalculator):
    def __init__(self, name: str, rocket: str, version: str):
        self.rocket = rocket
        self.version = version
        super().__init__(name=name)


class ClassPad(LaunchCalculator):
    def __init__(self, name: str):
        super().__init__(name=name)


class ClassLandingZone(LaunchCalculator):
    def __init__(self, name: str):
        super().__init__(name=name)
        self.fullname = ""
    

class ClassFairingRecovery(LaunchCalculator):
    def __init__(self, name: str):
        super().__init__(name=name)


class TugSupport(LaunchCalculator):
    def __init__(self, name: str):
        super().__init__(name=name)


class SupportShip(LaunchCalculator):
    def __init__(self, name: str):
        super().__init__(name=name)


class GetSheets(LaunchCalculator):
    with open('ChronologicalOrder.csv') as csvfile:
        reader = list(csv.reader(csvfile))
        reader.pop(0)

    def __init__(self, name):
        super().__init__(name=name)
        self.boosters: list[Booster] = []
        self.launch_pads: list[ClassPad] = []
        self.landing_zones: list[ClassLandingZone] = []
        self.secondstages: list[SecondStage] = []
        self.support_ships: list[SupportShip] = []
        self.tugs: list[TugSupport] = []
        self.fairing_recovery_ships: list[ClassFairingRecovery] = []
        self.__get_sheet_data__()
    
    def __get_or_add_object__(self, name: str, search_list: list[LaunchCalculator], object: LaunchCalculator, **kwargs) -> LaunchCalculator:
        if name == "None" or name == "N/A":
            return None

        for obj in search_list:
            if str(obj.name) == name:
                return obj
        
        obj = object(name, **kwargs)
        search_list.append(obj)
        return obj
    
    def __parse_falcon_9_row__(self, row: list[str], launch_boosters: list[Booster]):
        booster_name = row[2].split("-", 1)[0].split("B",1)[1]
        booster_version = row[1].replace("F9 ", "")
        booster = self.__get_or_add_object__(booster_name, self.boosters, Booster, rocket="Falcon 9", version=booster_version)
        launch_boosters.append(booster)

    def __parse_falcon_heavy_row__(self, row: list[str], launch_boosters: list[Booster]):
        booster_name = row[2]
        booster_versions = row[1].split(",")

        for index, booster_name in enumerate(booster_name.split(",")):
            booster_name = booster_name.split("-", 1)[0].split("B",1)[1]
            booster_version = booster_versions[index]

            if index == 0:
                booster = self.__get_or_add_object__(booster_name, self.boosters, Booster, rocket="Falcon Heavy", version=booster_version.replace("FH ", ""))
            else:
                booster = self.__get_or_add_object__(booster_name, self.boosters, Booster, rocket="Falcon 9", version=booster_version.replace("F9 ", "").lstrip(" "))

            launch_boosters.append(booster)


    def __parse_starship_row__(self, row: list[str], launch_boosters: list[Booster]) -> SecondStage:
        booster_name = row[2].split("-", 1)[0].split("B",1)[1]
        booster_version = row[1].replace("F9 ", "")

        booster = self.__get_or_add_object__(booster_name, self.boosters, Booster, rocket="Starship", version=booster_version)
        launch_boosters.append(booster)
        
        secondstage_name = row[4].split("-", 1)[0].split("S",1)[1]
        secondstage_version = row[3]

        return self.__get_or_add_object__(secondstage_name, self.secondstages, SecondStage, rocket="Starship", version=secondstage_version)

    def __get_sheet_data__(self):
        for row in self.reader:
            launch_boosters: list[Booster] = [] #This array is used to store objects of boosters, which are later added to the launch
            booster_flights: list[int] = []
            launch_pad: ClassPad = self.__get_or_add_object__(row[5], self.launch_pads, ClassPad) #Create the launch pad
            launch_landing_zones: list[ClassLandingZone] = []
            launch_landing_outcome: list[str] = []
            secondstage: SecondStage = None
            secondstage_flights: int = 1
            support_ships: list[SupportShip] = []
            tugs: list[TugSupport] = []
            fairing_recovery_outcome: list[str] = []
            fairing_num_flights: list[str] = []
            fairing_recovery_ships: list[ClassFairingRecovery] = []
            rocket: str = ""
            second_stage_landing_zone: ClassLandingZone = None

            #Get information for Falcon 9, Falcon Heavy, and Starship. Logic is slighly different for each, which is why it's abstracted above
            if row[1].startswith("F1"):
                rocket = "Falcon 1"
            
            if row[1].startswith("F9"):
                self.__parse_falcon_9_row__(row, launch_boosters)
                rocket = "Falcon 9"

            if row[1].startswith("FH"):
                self.__parse_falcon_heavy_row__(row, launch_boosters)
                rocket = "Falcon Heavy"
            
            if row[1].startswith("SH"):
                secondstage = self.__parse_starship_row__(row, launch_boosters)
                rocket = "Starship"
        

            if not row[18] == "N/A": #Get fairing recovery outcomes
                for fairing_recovery in row[18].split("/"):
                    fairing_recovery_outcome.append(fairing_recovery.lstrip(" ").rstrip(" "))

            if not row[19] == "N/A": #Get fairing flight numbers
                for fairing_flight in row[19].split("/"):
                    fairing_num_flights.append(fairing_flight.lstrip(" ").rstrip(" "))

            if not row[20] == "N/A": #Creates the fairing recovery ships
                for ship in row[20].split("/"):
                    fairing_recovery_ships.append(self.__get_or_add_object__(ship.lstrip(" ").rstrip(" "), self.fairing_recovery_ships, ClassFairingRecovery))

            if not row[16] == "N/A": #Creates the support ships
                for ship in row[16].split("/"):
                    support_ships.append(self.__get_or_add_object__(ship.lstrip(" ").rstrip(" "), self.support_ships, SupportShip))

            if not row[17] == "N/A": #Creates the tugs
                for ship in row[17].split("/"):
                    tugs.append(self.__get_or_add_object__(ship.lstrip(" ").rstrip(" "), self.tugs, TugSupport))
            
            for j, zone in enumerate(row[12].replace(" ", "").split("/")): #Create the landing zones
                if not rocket == "Starship":
                    landing_zone = self.__get_or_add_object__(zone, self.landing_zones, ClassLandingZone)
                    launch_landing_zones.append(landing_zone)
                else:
                    if j == 0:
                        landing_zone = self.__get_or_add_object__(zone, self.landing_zones, ClassLandingZone)
                        launch_landing_zones.append(landing_zone)
                    if j == 1:
                        landing_zone = self.__get_or_add_object__(zone, self.landing_zones, ClassLandingZone)
                        second_stage_landing_zone = landing_zone
            
            for outcome in row[13].split("/"): #Create booster landing recovery
                outcome = outcome.lstrip(" ")
                outcome = outcome.rstrip(" ")
                launch_landing_outcome.append(outcome)


            #Now that we know the pad and boosters, simply define everything in class of launches.
            launch = ClassLaunch(
                time=parser.parse(row[0].replace('(planned)','')),
                rocket=rocket,
                boosters=launch_boosters,
                booster_flights=booster_flights,
                payload=row[7],
                mass=row[8],
                orbit=row[9],
                customer=row[10],
                launch_outcome=row[11],
                location=launch_pad,
                booster_landing_outcomes=launch_landing_outcome,
                landing_zones=launch_landing_zones,
                secondstage=secondstage,
                secondstage_flights=secondstage_flights,
                booster_lat=row[14],
                booster_long=row[15],
                booster_support=support_ships,
                booster_tug=tugs,
                fairing_flights=fairing_num_flights,
                fairings_recovered=fairing_recovery_outcome,
                fairing_recovery_boats=fairing_recovery_ships,
                fairing_lat=row[21],
                fairing_long=row[22],
                second_stage_recovery_location=second_stage_landing_zone)
            self.launches.append(launch)

            #This last section of the code is adding the launch to all of the objects. This ensures that the launch is in the object and the object is in the launch
            if second_stage_landing_zone is not None:
                self.__get_or_add_object__(second_stage_landing_zone.name, self.landing_zones, ClassLandingZone).launches.append(launch)

            for booster in launch_boosters: 
                self.__get_or_add_object__(booster.name, self.boosters, Booster, rocket=booster.rocket, version=booster.version).launches.append(launch)
                launch.booster_turnaround.append(booster.last_turnaround())
                booster_flights.append(len(booster.launches))

            for zone in launch_landing_zones:
                if not zone is None:
                    self.__get_or_add_object__(zone.name, self.landing_zones, ClassLandingZone).launches.append(launch)
                    launch.zone_turnaround.append(zone.last_turnaround())

            for support_ship in support_ships:
                if not support_ship is None:
                    self.__get_or_add_object__(support_ship.name, self.support_ships, SupportShip).launches.append(launch)
            
            for tug in tugs:
                self.__get_or_add_object__(tug.name, self.tugs, TugSupport).launches.append(launch)
            
            if secondstage:
                secondstage.launches.append(launch)
                secondstage_flights = len(secondstage.launches)
            
            for ship in fairing_recovery_ships:
                ship.launches.append(launch)

            launch.company_turnaround = self.last_turnaround()
            launch_pad.launches.append(launch)
            launch.pad_turnaround = launch_pad.last_turnaround()
            launch.secondstage_flights = secondstage_flights
            launch.booster_flights = booster_flights
    


falcon_data = GetSheets("SpaceX")

for zone in falcon_data.landing_zones:
    if zone is not None:
        if zone.name == "LZ-1":
            zone.fullname = "Landing Zone 1"
        if zone.name == "LZ-2":
            zone.fullname = "Landing Zone 2"
        if zone.name == "LZ-4":
            zone.fullname = "Landing Zone 4"
        if zone.name == "OCISLY":
            zone.fullname = "Of Course I Still Love You"
        if zone.name == "JRtI":
            zone.fullname = "Just Read the Instructions"
        if zone.name == "ASoG":
            zone.fullname = "A Shortfall of Gravitas"


for booster in falcon_data.boosters:
    booster.name = "B"+booster.name
    Stage.objects.get_or_create(name=booster.name, rocket=Rocket.objects.get_or_create(name=str(booster.rocket))[0], version=booster.version, type="BOOSTER")

for landing_zone in falcon_data.landing_zones:
    LandingZone.objects.get_or_create(name=landing_zone.fullname, nickname=landing_zone.name)

for second_stage in falcon_data.secondstages:
    second_stage.name = "S"+second_stage.name
    Stage.objects.get_or_create(name=second_stage.name, rocket=Rocket.objects.get_or_create(name=str(second_stage.rocket))[0], version=second_stage.version, type="SECOND_STAGE")

for pad in falcon_data.launch_pads:
    fullname = ""
    if pad.name == "SLC-40":
        fullname = "Space Launch Complex 40"
    elif pad.name == "SLC-4E":
        fullname = "Space Launch Complex 4 East"
    elif pad.name == "LC-39A":
        fullname == "Launch Complex 39A"
    elif pad.name == "OLP-A":
        fullname == "Orbital Launch pad A"
    elif pad.name == "Omelek Island":
        fullname = "Omelek Island"

    Pad.objects.get_or_create(name=fullname, nickname=pad.name)

for launch in falcon_data.launches:
    Rocket.objects.get_or_create(name=launch.rocket)
    Orbit.objects.get_or_create(name=launch.orbit)

    launch_outcome = "SUCCESS"

    if "Partial" in launch.launch_outcome:
        launch_outcome = "PARTIAL FAILURE"
    elif "Failure" in launch.launch_outcome:
        launch_outcome = "FAILURE"

    Launch.objects.get_or_create(time=launch.time, pad=Pad.objects.get(nickname=launch.location), rocket=Rocket.objects.get(name=launch.rocket), name=launch.payload, orbit=Orbit.objects.get(name=launch.orbit), mass=launch.mass, customer=launch.customer, launch_outcome=launch_outcome)

    for index, booster in enumerate(launch.boosters):
        method="EXPENDED"
        method_success = True
        recovery_success = False
        latitude = float(launch.booster_lat) if launch.booster_lat not in ['N/A', ''] else None
        longitude = float(launch.booster_long) if launch.booster_long not in ['N/A', ''] else None


        if launch.landing_zones[index] is not None and launch.landing_zones[index].name is not None and (launch.landing_zones[index].name == "LZ-1" or launch.landing_zones[index].name == "LZ-2" or launch.landing_zones[index].name == "LZ-4"):
            method = "GROUND_PAD"
        if launch.landing_zones[index] is not None and launch.landing_zones[index].name is not None and (launch.landing_zones[index].name == "OCISLY" or launch.landing_zones[index].name == "JRtI" or launch.landing_zones[index].name == "ASoG"):
            method = "DRONE_SHIP"
        if "trolled" in launch.booster_landing_outcomes[index]:
            method = "OCEAN_SURFACE"

        if "Failure" in launch.booster_landing_outcomes[index] or "Uncontrolled" in launch.booster_landing_outcomes[index]:
            method_success = False

        if "Success" in launch.booster_landing_outcomes[index]:
            recovery_success = True

        if launch.landing_zones[index] is not None:
            with transaction.atomic():
                launch_instance, _ = Launch.objects.get_or_create(name=launch.payload)
                stage_instance, _ = Stage.objects.get_or_create(name=booster.name)
                landing_zone_instance, _ = LandingZone.objects.get_or_create(name=launch.landing_zones[index].fullname)
                
                StageAndRecovery.objects.get_or_create(
                    launch=launch_instance,
                    stage=stage_instance,
                    landing_zone=landing_zone_instance,
                    method=method,
                    method_success=method_success,
                    recovery_success=recovery_success,
                    latitude=latitude,
                    longitude=longitude
                )

        else:
            with transaction.atomic():
                launch_instance, _ = Launch.objects.get_or_create(name=launch.payload)
                stage_instance, _ = Stage.objects.get_or_create(name=booster.name)
                StageAndRecovery.objects.get_or_create(
                        launch=launch_instance,
                        stage=stage_instance,
                        landing_zone=None,
                        method=method,
                        method_success=method_success,
                        recovery_success=recovery_success,
                        latitude=latitude,
                        longitude=longitude
                    )
    

    if launch.secondstage is not None:
        method="EXPENDED"
        method_success = True
        recovery_success = False

        if "ocean" in launch.booster_landing_outcomes[1]:
            method = "OCEAN_SURFACE"

        if "Failure" in launch.booster_landing_outcomes[1] or "Uncontrolled" in launch.booster_landing_outcomes[index]:
            method_success = False

        if "Success" in launch.booster_landing_outcomes[1]:
            recovery_success = True

        if len(launch.landing_zones) == 2 and launch.landing_zones[1] is not None:
            with transaction.atomic():
                launch_instance, _ = Launch.objects.get_or_create(name=launch.payload)
                stage_instance, _ = Stage.objects.get_or_create(name=booster.name)
                landing_zone_instance, _ = LandingZone.objects.get_or_create(name=launch.landing_zones[index].fullname)
                
                StageAndRecovery.objects.get_or_create(
                    launch=launch_instance,
                    stage=stage_instance,
                    landing_zone=landing_zone_instance,
                    method=method,
                    method_success=method_success,
                    recovery_success=recovery_success,
                    latitude=None,
                    longitude=None
                )

        else:
            with transaction.atomic():
                launch_instance, _ = Launch.objects.get_or_create(name=launch.payload)
                stage_instance, _ = Stage.objects.get_or_create(name=launch.secondstage.name)
                StageAndRecovery.objects.get_or_create(
                        launch=launch_instance,
                        stage=stage_instance,
                        landing_zone=None,
                        method=method,
                        method_success=method_success,
                        recovery_success=recovery_success,
                        latitude=None,
                        longitude=None
                    )




    for index, fairing_recovery in enumerate(launch.fairings_recovered):
        if len(launch.fairing_recovery_boats) == 1:
            launch.fairing_recovery_boats.append(launch.fairing_recovery_boats[0])
        
        catch = False
        recovered = "Yes"
        flights = launch.fairing_flights[index]

        if fairing_recovery == "":
            recovered = "TBD"
        else:
            recovered = fairing_recovery.replace(" (Catch)","")

        latitude = float(launch.fairing_lat) if launch.fairing_lat not in ['N/A', '', 'Unknown'] else None
        longitude = float(launch.fairing_long) if launch.fairing_long not in ['N/A', '', 'Unknown'] else None

        if launch.fairings_recovered is not None and launch.fairings_recovered[index] is not None and "Catch" in launch.fairings_recovered[index]:
            catch = True

        if not len(launch.fairing_recovery_boats) == 0:
            with transaction.atomic():
                launch_instance, _ = Launch.objects.get_or_create(name=launch.payload)
                boat_instance, _ = Boat.objects.get_or_create(name=launch.fairing_recovery_boats[index], type="FAIRING_RECOVERY")

                FairingRecovery.objects.create(
                    launch=launch_instance,
                    boat=boat_instance,
                    catch=catch,
                    recovery=recovered,
                    latitude=latitude,
                    longitude=longitude,
                    flights=flights
                )
    for support in launch.booster_support:
        with transaction.atomic():
            launch_instance, _ = Launch.objects.get_or_create(name=launch.payload)
            boat_instance, _ = Boat.objects.get_or_create(name=support.name, type="SUPPORT")
        SupportOnLaunch.objects.get_or_create(launch=launch_instance, boat=boat_instance)
    
    for tug in launch.booster_tug:
        with transaction.atomic():
            launch_instance, _ = Launch.objects.get_or_create(name=launch.payload)
            boat_instance, _ = Boat.objects.get_or_create(name=tug.name, type="TUG")
        TugOnLaunch.objects.get_or_create(launch=launch_instance, boat=boat_instance)

