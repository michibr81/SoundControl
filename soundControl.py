import subprocess
import time
import json
import sys
import os

class SoundControl:    

    def __init__(self, configFilepath):
        self.Plays = False
        try:
            self.loadConfigData(configFilepath)
            self.disable()
        except:
            raise        
    
    def loadConfigData(self,configFilepath):
        try:   
            with open(configFilepath, 'r') as file:
                self.ConfigData = json.load(file)
        except Exception as error:
            self.ConfigData = None
            print(f"Error loading config data ({configFilepath}): ", error)
            raise 

    def play(self, activationPhrase):
        try:   
            #configData = loadConfigData(self.ConfigFile)
            if self.ConfigData is None:
                return False
            try:
                stream = next( s for s in self.ConfigData["streams"] if str(s["activationWord"]).lower() == activationPhrase.lower())                
            except StopIteration:
                print("Error: Activation word for stream was not found in configuration data!")
                return False

            url = stream["streamUrl"]
            self.playURL(url)
            self.Plays = True
            return True   

        except:
            print("Unexpected error:", sys.exc_info()[0])
            return False

    def playURL(self, streamURL):
        self.disable()   
            
        try:
            if(str(streamURL).endswith(".m3u")):            
                subprocess.Popen(["mplayer -playlist " + str(streamURL)], shell=True)
            else:
                subprocess.Popen(["mplayer " + str(streamURL)], shell=True)
        except:
            print("Failed to start mplayer with radio-stream")
            raise

    def disable(self):
        try:
            subprocess.Popen(["killall mplayer -q"], shell=True)
            time.sleep(1)
            self.Plays = False
        except:
            print("kill mplayer failed")

    def adjustVolume(self, plusOrMinus):    

        if plusOrMinus != "+" and plusOrMinus != "-":
            print("wrong parameter to adjust volume!") 
            return False
    
        try:   
            if self.ConfigData is None:
                return False
            volumeDeviceCardNumber = self.ConfigData["outputDevice"]["cardNumber"]
            volumeDevice = self.ConfigData["outputDevice"]["name"]
            volumeChange = self.ConfigData["volume"]["louderPercentage"]
            command = "amixer -c " + str(volumeDeviceCardNumber)+ " sset '" + str(volumeDevice) + "' " + str(volumeChange) + "%" + plusOrMinus
            print(command)
            subprocess.Popen([command], shell=True)
            return True 
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return False

    def louder(self):
        print("run louder command") 
        return self.adjustVolume("+")

    def quieter(self):    
        print("run quieter command card ") 
        return self.adjustVolume("-") 

    def setMuteState(self, toggleUnMuteOrMute):
        try:
            if self.ConfigData is None:
                return False

            if toggleUnMuteOrMute != "toggle"  and toggleUnMuteOrMute != "mute" and toggleUnMuteOrMute != "unmute":
                return False
            volumeDeviceCardNumber = self.ConfigData["outputDevice"]["cardNumber"]
            volumeDevice = self.ConfigData["outputDevice"]["name"]
            #volumeChange = configData["volume"]["louderPercentage"]
            command = "amixer -q -D pulse -c " + str(volumeDeviceCardNumber)+ " sset " + str(volumeDevice) + f" {toggleUnMuteOrMute}"
            print(command)
            subprocess.Popen([command], shell=True)
            return True 
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return False

    def toggleMute(self):
        return self.setMuteState("toggle")

    def mute(self):
        if self.Plays:
            return self.setMuteState("mute")

    def unmute(self):
        if self.Plays:
            return self.setMuteState("unmute")
        
   
# [START run_application]
if __name__ == '__main__':

    sound = SoundControl("soundControl.config.json")

    sound.volumeLouder()

    sound.play("B5")

    sound.setMuteState("mute")

    sound.setMuteState("unmute")

    sound.volumeLouder()

    sound.volumeLouder()