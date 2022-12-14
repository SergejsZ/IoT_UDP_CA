import RPi.GPIO as GPIO
import time, threading

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-f0b1216d-3419-4c2c-bb29-9d7389a11e21'
pnconfig.publish_key = 'pub-c-07659b0d-b4ed-4fed-a636-dabd418f94f3'
pnconfig.user_id = "dawids-pi"
pubnub = PubNub(pnconfig)

my_channel = "sergejs_sd3b_pi_channel"

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost
        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel('sergejs_sd3b_pi_channel').message('Finnaly Connected, Hello World !').pn_async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.
    def message(self, pubnub, message):
        # Handle new message stored in message.message
        print(message.message)


pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('sergejs_sd3b_pi_channel').execute()

PIR_pin = 23
Buzzer_pin = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_pin, GPIO.IN)
GPIO.setup(Buzzer_pin, GPIO.OUT)

def beep(repeat):
    for i in range(0, repeat):
        for pulse in range(60):
            GPIO.output(Buzzer_pin, True)
            time.sleep(0.001)
            GPIO.output(Buzzer_pin, False)
            time.sleep(0.001)
        time.sleep(0.001)

def motion_detection():
    while True:
        if GPIO.input(PIR_pin):
            print("Motion detected")
            pubnub.publish().channel('sergejs_sd3b_pi_channel').message('dawids_motion_detected').pn_async(my_publish_callback)
            beep(4)
        time.sleep(1)

if __name__ == '__main__':
    sensors_thread = threading.Thread(target=motion_detection)
    sensors_thread.start()
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(my_channel).execute()
