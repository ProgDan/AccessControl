#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
Class in Python 3.5 for incorporation of the RPi.GPIO module to control the GPIO channels of Raspberry Pi.

Credits and License: Created by Erivando Sena, adapted by Daniel Arndt Alves (2019)

 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License.
"""

import RPi.GPIO as GPIO

__author__ = "Daniel Arndt Alves  (Adaptations)"
__copyright__ = "Erivando Sena (2016)"
__email__ = "progdan@gmail.com"
__status__ = "Prototype"


class PinosGPIO(object):
    
    gpio = None

    def __init__(self):
        self.gpio = GPIO
