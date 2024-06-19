from os import path, mkdir
from shutil import rmtree

from django.core.management.base import BaseCommand

from config.settings.base import BASE_DIR


class Command(BaseCommand):
    help = 'For creating new django app'

    def add_arguments(self, parser):
        # take app name
        parser.add_argument('app_name', type=str, help='Enter App name')

    def handle(self, *args, **options):
        app_name = options['app_name']
        app_name_capitalize = "".join([name.capitalize() for name in app_name.split("_")])

        base_dir = path.join(BASE_DIR, "apis", app_name)

        if path.exists(base_dir):
            # ask user if he wants to overwrite the app
            # if yes, delete the app and create new one
            # if no, exit
            self.stdout.write(self.style.ERROR(f"{app_name} app already exists"))
            # get user input
            user_input = input("Do you want to overwrite the app? (y/n): ")
            if user_input == "y":
                self.stdout.write(self.style.SUCCESS(f"Deleting {app_name} app"))
                # delete app recursively
                rmtree(base_dir)

        # create app folder
        if not path.exists(base_dir):

            self.stdout.write(self.style.SUCCESS(f"Creating {app_name} app"))
            mkdir(base_dir)

            # create app folder structure
            self.stdout.write(self.style.SUCCESS(f"Creating {app_name} app structure"))
            mkdir(path.join(base_dir, "migrations"))

            # create app files
            self.stdout.write(self.style.SUCCESS(f"Creating {app_name} app files"))


            ## __init__ .py
            with open(path.join(base_dir, "__init__.py"), "w") as f:
                f.write("")



            ## serializers.py
            with open(path.join(base_dir, "serializers.py"), "w") as f:
                f.write("from rest_framework import serializers \n")
                f.write(f"from django.core.exceptions import ObjectDoesNotExist \n")
                f.write(f"from django.contrib.auth import get_user_model \n")
                f.write(f"User = get_user_model() \n\n")

                f.write(f"from apps.{app_name}.models import {app_name_capitalize} \n\n")

                f.write(f"class {app_name_capitalize}Serializer(serializers.ModelSerializer): \n")
                f.write(f"    class Meta: \n")
                f.write(f"        model = {app_name_capitalize} \n")
                f.write(f"        fields = '__all__' \n")



            ## tests.py
            with open(path.join(base_dir, "tests.py"), "w") as f:
                f.write("from django.test import TestCase \n\n")



            ## urls.py
            with open(path.join(base_dir, "urls.py"), "w") as f:
                f.write("from django.urls import path \n\n")
                f.write(f"from apps.{app_name}.views import {app_name_capitalize}View \n\n")
                f.write("urlpatterns = [ \n")
                f.write(f"    path('', {app_name_capitalize}View.as_view(), name='list'), \n")
                f.write(f"    path('<int:pk>/', {app_name_capitalize}View.as_view(), name='details'), \n")
                f.write(f"] \n")



            ## views.py
            with open(path.join(base_dir, "views.py"), "w") as f:
                f.write(f"from rest_framework.views import APIView \n")
                f.write(f"from rest_framework import generics \n")
                f.write(f"from django.db.models import Q \n")
                f.write(f" \n")

                f.write(f"from rest_framework.exceptions import ValidationError \n")
                f.write(f"from rest_framework import status \n")
                f.write(f"from rest_framework.response import Response \n")
                f.write(f"from django_filters.rest_framework import DjangoFilterBackend \n")
                f.write(f"from rest_framework_simplejwt.authentication import JWTAuthentication \n")
                f.write(f"from rest_framework.permissions import (IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly) \n")
                f.write(f"\n")

                f.write(f"from django.contrib.auth import get_user_model \n")
                f.write(f"User = get_user_model() \n")

                f.write(f"\n")
                f.write(f"from apps.core.utils import (api_success, api_error) \n")

                f.write(f"\n")
                f.write(f"from apps.{app_name}.models import {app_name_capitalize} \n")
                f.write(f"from apps.{app_name}.serializers import {app_name_capitalize}Serializer \n")
                f.write("from jupiter.utils import ApiBaseView \n\n\n\n\n")


                f.write(f"class {app_name_capitalize}View(ApiBaseView): \n")
                f.write(f"    class Meta: \n")
                f.write(f"        model = {app_name_capitalize} \n")
                f.write(f"        serializer = {app_name_capitalize}Serializer \n")

            self.stdout.write(self.style.SUCCESS(f"{app_name} app created successfully"))


        else:
            self.stdout.write(self.style.ERROR(f"{app_name} app already exists"))

        # self.stdout.write(self.style.WARNING("Done. Don't forget to add app to INSTALLED_APPS in settings.py"))
