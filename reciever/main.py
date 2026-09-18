from machine import Pin, time_pulse_us
from time import sleep

ir = Pin(16, Pin.IN, Pin.PULL_UP)
led = Pin(14, Pin.OUT)
led.off()

MORSE = {
    'A': '.-', 'B': '-...', 'C': '-.-.',
    'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..',
    'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-',
    'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..',
    '9': '----.'
}

UNIT = 0.2


def receive_byte():
    while True:
        start_low = time_pulse_us(ir, 0, 1000000)

        if 3000 < start_low < 5000:
            start_high = time_pulse_us(ir, 1, 7000)

            if 3000 < start_high < 5000:
                break

    value = 0

    for i in range(8):
        low = time_pulse_us(ir, 0, 2500)
        if low < 0:
            return None

        high = time_pulse_us(ir, 1, 3000)
        if high < 0:
            return None

        if high > 1100:
            value |= (1 << i)

    return value


def blink_symbol(symbol):
    led.on()

    if symbol == '.':
        sleep(UNIT)
    else:
        sleep(UNIT * 3)

    led.off()
    sleep(UNIT)


def play_morse(text):
    print("MORSE:")

    for char in text:
        if char == ' ':
            print("/", end=" ")
            sleep(UNIT * 7)
            continue

        if char not in MORSE:
            continue

        code = MORSE[char]
        print(code, end=" ")

        for symbol in code:
            blink_symbol(symbol)

        sleep(UNIT * 2)

    print()


message = ""
print("Cekam IR poruku...")

while True:
    value = receive_byte()

    if value is None:
        continue

    if value == 10:
        print()
        print("Primljena poruka:", message)
        play_morse(message)
        message = ""
        print("Cekam novu poruku...")
    else:
        if 32 <= value <= 126:
            char = chr(value)
            message += char
            print(char, end="")
