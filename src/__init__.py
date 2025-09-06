"""
ICBC Appointment Checker Package

A Python-based automation tool that monitors the ICBC road test booking system
for earlier appointment openings and sends alerts when available.
"""

__version__ = "1.0.0"
__author__ = "ICBC Appointment Checker Team"
__description__ = "Automated ICBC Road Test Appointment Monitor"

from .config import Config
from .notifier import Notifier
from .icbc_checker import ICBCAppointmentChecker

__all__ = ['Config', 'Notifier', 'ICBCAppointmentChecker']
