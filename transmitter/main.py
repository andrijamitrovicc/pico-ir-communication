from machine import Pin, PWM
from time import sleep_us, sleep_ms

ir = PWM(Pin(15))
ir.freq(38000)
ir.duty_u16(0)


def burst(us):
    ir.duty_u16(32768)
    sleep_us(us)
    ir.duty_u16(0)


def pauza(us):
    sleep_us(us)


def send_byte(value):
    # Start
    burst(4000)
    pauza(4000)

    # 8 bits, least-significant bit first
    for i in range(8):
        bit = (value >> i) & 1
        burst(600)

        if bit == 0:
            pauza(600)
        else:
            pauza(1600)

    burst(600)
    sleep_ms(10)


def send_message(text):
    for char in text:
        send_byte(ord(char))

    # 10 marks the end of the message
    send_byte(10)


while True:
    text = input("Unesi poruku: ").upper()
    print("Saljem:", text)
    send_message(text)
    print("Poruka poslata.")
