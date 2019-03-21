from pymumble_py3 import Mumble
from pymumble_py3 import constants
from pymumble_py3 import soundoutput

import pyaudio
import numpy as np
from array import array
import time

IP = "192.168.1.247"
NAME = "FT736R"
CERTFILE = "FT736R.pem"
KEYFILE = "FT736R-keys.pem"

AUDIO_DEVICE_INDEX = 2

ENABLE_TRANSMIT = False

#Setup connection to mumble server
mumble = Mumble(IP,NAME,certfile=CERTFILE,keyfile=KEYFILE,debug=False)

PyAudio = pyaudio.PyAudio()

#Setup stream to radio from mumble if transmit is enabled
stream_to_radio = PyAudio.open(48000,1,pyaudio.paInt16,False,True,None,AUDIO_DEVICE_INDEX,1920,ENABLE_TRANSMIT)

Sound = False

#Send audio from radio to mumble
def SendAudio(in_data,frame_count,time_info,status_flag):
	mumble.sound_output.add_sound(in_data)
	return (None,0)


stream_from_radio = None

#Send audio from mumble to radio
def ProcessSound(user,sound):
	global Sound
	stream_to_radio.write(sound.pcm)
	Sound = True

#Callback for receiving audio from mumble
mumble.callbacks.set_callback(constants.PYMUMBLE_CLBK_SOUNDRECEIVED,ProcessSound)
#Set application name
mumble.set_application_string("HamRadioLink")
#Set codec profile
mumble.set_codec_profile("audio")
#Start mumble client
mumble.start()
#Wait to continue until we connect.
mumble.is_ready()
#Set bandwidth
mumble.set_bandwidth(96000)
#See if we actually connected.
print("Connected: "+str(mumble.connected==constants.PYMUMBLE_CONN_STATE_CONNECTED ))
#Enable callback if we are ready.
mumble.set_receive_sound(ENABLE_TRANSMIT)

stream_from_radio =  PyAudio.open(48000,1,pyaudio.paInt16,True,False,AUDIO_DEVICE_INDEX,None,64,True,None,None,SendAudio)

last_state = False

#Used if transmitting. 

while ENABLE_TRANSMIT:
	if Sound:
		if last_state != Sound:
			#ser.write(10)
			pass
		last_state = True
		Sound = False
	else:
		if last_state != Sound:
			#ser.write(0)
			pass
			last_state = False
	time.sleep(0.2)
    
while True:
    time.sleep(1000)

