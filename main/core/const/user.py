# -*- coding: utf-8 -*-
from django.contrib.auth.models import User


""" Constants relatives to User """


""" Authentication """

USERNAME__MIN_LENGTH = 1
USERNAME__MAX_LENGTH = User._meta.get_field('username').max_length

PASSWORD__MIN_LENGTH = 12
PASSWORD__MAX_LENGTH = User._meta.get_field('password').max_length

FIRST_NAME__MIN_LENGTH = 0
FIRST_NAME__MAX_LENGTH = User._meta.get_field('first_name').max_length

LAST_NAME__MIN_LENGTH = 0
LAST_NAME__MAX_LENGTH = User._meta.get_field('last_name').max_length
