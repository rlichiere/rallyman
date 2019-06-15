# -*- coding: utf-8 -*-
import string

from django.core.exceptions import ValidationError


class ComplexPasswordValidator(object):
    """
    Validate whether the password character repartition is sufficiently complex.

    If no specific attributes are provided, expect the presence of 1 lowercase
    character, 1 uppercase character, and 1 exotic character at least. Exotic
    dictionary is customizable as well as the number of characters expected for
    each alphabet (lowercase, uppercase and exotic).
    """
    ALPHABET_LOWER = list(string.ascii_lowercase)
    ALPHABET_UPPER = list(string.ascii_uppercase)
    ALPHABET_EXOTICS = ',;:!*^$&(-_)=+*/?.§%µ£°#{[|@]}'

    def __init__(self, min_lower=1, min_upper=1, min_exotic=1, exotics=None):
        self.minLower = min_lower
        self.minUpper = min_upper
        self.minExotic = min_exotic
        self.exotics = exotics if exotics is not None else self.ALPHABET_EXOTICS

    def validate(self, password, user=None):
        _password = list(password)
        _errMsg = 'This password must contains at least %(number)d %(alphabet)s characters.'

        # check that password respect the minLower constraint
        _passwordLowers = [_ for _ in _password if _ in self.ALPHABET_LOWER]
        if len(_passwordLowers) < self.minLower:
            raise ValidationError(_errMsg,
                                  code='password_too_simple',
                                  params={'number': self.minLower, 'alphabet': 'lowercase'})

        # check that password respect the minUpper constraint
        _passwordUppers = [_ for _ in _password if _ in self.ALPHABET_UPPER]
        if len(_passwordUppers) < self.minUpper:
            raise ValidationError(_errMsg,
                                  code='password_too_simple',
                                  params={'number': self.minUpper, 'alphabet': 'uppercase'})

        # check that password respect the minExotic constraint
        _passwordExotics = [_ for _ in _password if _ in self.exotics]
        if len(_passwordExotics) < self.minExotic:
            raise ValidationError(_errMsg,
                                  code='password_too_simple',
                                  params={'number': self.minExotic, 'alphabet': 'exotic'})

    def get_help_text(self):
        _msg = 'The password must contain at least' \
               ' {min_lower} {lower},' \
               ' {min_upper} {upper} and' \
               ' {min_exotic} {exotic} characters'\
            .format(min_lower=self.minLower, lower='lowercase',
                    min_upper=self.minUpper, upper='uppercase',
                    min_exotic=self.minExotic, exotic='exotic')
        return _msg
