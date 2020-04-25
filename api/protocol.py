from regex_patterns import regex_for_field
from regex_patterns import regex_for_coordinates
from regex_patterns import regex_for_current_temperature
from regex_patterns import regex_for_target_temperature
from regex_patterns import regex_for_progress
from socket_handler import send_and_receive


import re


class GCode(str):
    REQUEST_CONTROL = 'M601 S1'
    GET_INFO = 'M115'
    GET_HEAD_POS = 'M114'
    GET_TEMP = 'M105'
    GET_PROGRESS = 'M27'
    GET_STATUS = 'M119'


def send_gcode(printer_address, code: str) -> str:
    """
    Send gcode to the printer
    :param printer_address: ip address
    :param code: gcode
    :return: the unhandled printer reply
    """
    send_and_receive(printer_address, GCode.REQUEST_CONTROL)
    return send_and_receive(printer_address, code)


def get_info(printer_address):
    """ Returns an object with basic printer information such as name etc."""
    info_result = send_gcode(printer_address, GCode.GET_INFO)

    printer_info = {}
    info_fields = ['Type', 'Name', 'Firmware', 'SN', 'X', 'Tool Count']
    for field in info_fields:
        regex_string = regex_for_field(field)
        printer_info[field] = re.search(regex_string, info_result).groups()[0]

    return printer_info


def get_head_position(printer_address):
    """ Returns the current x/y/z coordinates of the printer head. """
    info_result = send_gcode(printer_address, GCode.GET_HEAD_POS)

    printer_info = {}
    printer_info_fields = ['X', 'Y', 'Z']
    for field in printer_info_fields:
        regex_string = regex_for_coordinates(field)
        printer_info[field] = re.search(regex_string, info_result).groups()[0]

    return printer_info


def get_temp(printer_address):
    """ Returns printer temp. Both targeted and current. """
    info_result = send_gcode(printer_address, GCode.GET_TEMP)

    regex_temp = regex_for_current_temperature()
    regex_target_temp = regex_for_target_temperature()
    temp = re.search(regex_temp, info_result).groups()[0]
    target_temp = re.search(regex_target_temp, info_result).groups()[0]

    return {'Temperature': temp, 'TargetTemperature': target_temp}


def get_progress(printer_address):
    info_result = send_gcode(printer_address, GCode.GET_PROGRESS)

    regex_groups = re.search(regex_for_progress(), info_result).groups()
    printed = int(regex_groups[0])
    total = int(regex_groups[1])

    if total == 0:
        percentage = 0
    else:
        percentage = int(float(printed) / total * 100)

    return {'BytesPrinted': printed,
            'BytesTotal': total,
            'PercentageCompleted': percentage}


def get_status(printer_address):
    """ Returns the current printer status. """
    info_result = send_gcode(printer_address, GCode.GET_STATUS)

    printer_info = {}
    printer_info_fields = ['Status', 'MachineStatus', 'MoveMode', 'Endstop']
    for field in printer_info_fields:
        regex_string = regex_for_field(field)
        printer_info[field] = re.search(regex_string, info_result).groups()[0]

    return printer_info


def run_gcode(printer_address, code):
    """ Run generic gcode. What will work is trial and error """
    return send_and_receive(printer_address, code)
