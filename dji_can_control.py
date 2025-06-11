#!/usr/bin/env python3
"""Пример кода для приема данных CRSF и отправки сообщений по CAN.

Необходимо настроить последовательный порт и CAN-интерфейс под вашу конфигурацию.
"""

import can
import serial
import struct
import time

SERIAL_PORT = '/dev/ttyAMA0'  # измените на нужный порт
BAUD_RATE = 420000            # стандартная скорость CRSF
CAN_CHANNEL = 'can0'          # can0 или can1

# инициализация устройств
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
except serial.SerialException as exc:
    raise SystemExit(f"Не удалось открыть порт {SERIAL_PORT}: {exc}")

try:
    bus = can.interface.Bus(channel=CAN_CHANNEL, bustype='socketcan')
except can.CanError as exc:
    raise SystemExit(f"Ошибка инициализации CAN: {exc}")


def read_crsf_frame():
    """Чтение одного фрейма CRSF. Возвращает список каналов или None."""
    header = ser.read(1)
    if not header:
        return None
    if header != b'\xc8':  # адрес для приёмника
        return None
    length_bytes = ser.read(1)
    if not length_bytes:
        return None
    length = length_bytes[0]
    payload = ser.read(length)
    if len(payload) != length:
        return None
    if payload[0] != 0x16:  # тип пакета RC Channels Packed
        return None
    # данные каналов занимают 22 байта (16 каналов по 11 бит)
    channels = struct.unpack('<16H', payload[1:33])
    return channels


def send_can_command(yaw, pitch):
    """Отправка простого CAN-сообщения. Настройте форматы под DJI."""
    yaw_val = int(max(min(yaw, 1.0), -1.0) * 100)
    pitch_val = int(max(min(pitch, 1.0), -1.0) * 100)
    data = [yaw_val & 0xFF, pitch_val & 0xFF]
    msg = can.Message(arbitration_id=0x123, data=data, is_extended_id=False)
    try:
        bus.send(msg)
    except can.CanError:
        pass


while True:
    frame = read_crsf_frame()
    if frame:
        yaw = (frame[0] - 992) / 512.0
        pitch = (frame[1] - 992) / 512.0
        send_can_command(yaw, pitch)
    time.sleep(0.01)
