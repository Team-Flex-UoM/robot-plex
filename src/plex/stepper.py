#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

def init(pin1, pin2, pin3, pin4):
    global in1, in2, in3, in4
    in1 = pin1
    in2 = pin2
    in3 = pin3
    in4 = pin4
    
    # setting up
    GPIO.setmode( GPIO.BCM )
    GPIO.setup( in1, GPIO.OUT )
    GPIO.setup( in2, GPIO.OUT )
    GPIO.setup( in3, GPIO.OUT )
    GPIO.setup( in4, GPIO.OUT )

    # initializing
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )

def rotate(direction, rounds):
    step_sleep = 0.001
    step_count = 4096
    totla_step_count = step_count*rounds
    step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
    motor_pins = [in1,in2,in3,in4]
    motor_step_counter = 0 
    i = 0
    for i in range(totla_step_count):
        for pin in range(0, len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
        if direction=="down":
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction=="up":
            motor_step_counter = (motor_step_counter + 1) % 8
        else: # defensive programming
            print( "uh oh... direction should *always* be either True or False" )
            cleanup()
            exit( 1 )
        time.sleep( step_sleep )
    cleanup()
    exit(1)

def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.cleanup()

init(17,18,27,22)
rotate("up",2)
