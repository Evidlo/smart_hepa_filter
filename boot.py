print('starting')
from machine import Pin
import network
import time
import ntptime

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    execfile('password.py')
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
        pass

print('network config:', sta_if.ifconfig())
ntptime.settime()

# ensure filter boot up
time.sleep(10)

p_enabled = Pin(13, Pin.IN)
p_led = Pin(2, Pin.OUT)
p_rot_a = Pin(26, Pin.IN)
p_rot_b = Pin(25, Pin.IN)
p_enable = Pin(33, Pin.IN)
p_enable.off()
p_rot_a.off()
p_rot_b.off()

def increase_speed():
    p_rot_a.init(mode=Pin.OUT)
    p_rot_b.init(mode=Pin.OUT)
    p_rot_a.off()
    time.sleep(.1)
    p_rot_b.off()
    time.sleep(.1)
    p_rot_a.on()
    time.sleep(.1)
    p_rot_b.on()
    time.sleep(.1)
    p_rot_a.off()
    time.sleep(.1)
    p_rot_b.off()
    p_rot_a.init(mode=Pin.IN)
    p_rot_b.init(mode=Pin.IN)
    time.sleep(.1)

def decrease_speed():
    p_rot_a.init(mode=Pin.OUT)
    p_rot_b.init(mode=Pin.OUT)
    p_rot_b.off()
    time.sleep(.1)
    p_rot_a.off()
    time.sleep(.1)
    p_rot_b.on()
    time.sleep(.1)
    p_rot_a.on()
    time.sleep(.1)
    p_rot_b.off()
    time.sleep(.1)
    p_rot_a.off()
    p_rot_a.init(mode=Pin.IN)
    p_rot_b.init(mode=Pin.IN)
    time.sleep(.1)

def enable():
    if p_enabled.value() == 0:
        p_enable.init(mode=Pin.OUT)
        time.sleep(.1)
        p_enable.init(mode=Pin.IN)
        time.sleep(.1)

def disable():
    if p_enabled.value() == 1:
        p_enable.init(mode=Pin.OUT)
        time.sleep(.1)
        p_enable.init(mode=Pin.IN)
        time.sleep(.1)

print('loop begin')
while True:
    utc_hour, utc_minute = time.localtime()[3:5]
    if utc_hour == 8 and utc_minute == 0:
        # double enable needed when in sleep mode
        enable()
        enable()
        increase_speed()
        increase_speed()
        increase_speed()
        p_led.on()
        print('on')
    else:
        # double disable needed when in sleep mode
        disable()
        disable()
        p_led.off()
        print('off')

    time.sleep(60)

