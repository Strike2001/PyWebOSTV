# PyWebOSTV
[![Build Status](https://api.travis-ci.org/supersaiyanmode/PyWebOSTV.svg?branch=develop)](https://travis-ci.org/supersaiyanmode/PyWebOSTV)
[![Coverage Status](https://coveralls.io/repos/github/supersaiyanmode/PyWebOSTV/badge.svg?branch=master)](https://coveralls.io/github/supersaiyanmode/PyWebOSTV?branch=master)

### Why another Library?
I looked at a few libraries. The LGWebOSRemote repository by
[klattimer](https://github.com/klattimer/LGWebOSRemote) is definitely a good library, but it has a few problems:
 - Meant to be used with Python 2.x.
 - Assumes all the users of the library would like to save the credentials to ~/.lgtv.json.
 - Assumes only a single command will be fired and waited on at any given time (ctrl+F for self.__waiting_callback)
 - Mouse/Keyboard not supported.

This SDK is a tiny attempt at overcoming some of the above problems.


### Current status?
At the moment, I haven't been able to do any kind of extensive testing. No unit test cases too! Current status: Works for me! :)

Currently working on more controls and unit test cases. Upon testing, I will upload it to PyPI.

### How to use it?

```
from pywebostv.discovery import *
from pywebostv.connection import *
from pywebostv.controls import *
store = {}
# If you know the IP of your TV (quicker)
# client = WebOSClient(<YOUR_IP>)
# or to detect it automatically, but slower
client = WebOSClient.discover()[0]
client.connect()
for status in client.register(store):
    if status == WebOSClient.PROMPTED:
        print("Please accept the connect on the TV!")
    elif status == WebOSClient.REGISTERED:
        print("Registration successful!")
```
    
#### Media Controls

```
media = MediaControl(client)
media.volume_up()
media.volume_down()
media.get_volume()
media.set_volume(<int>)
media.mute(<mute status as boolean>)
media.play()
media.pause()
media.stop()
media.rewind()
media.fast_forward()
```
    
#### System Controls

```
system = SystemControl(client)
system.notify("This is a notification message!")
system.power_off()
system.info()
```

#### Application Controls

```
app = ApplicationControl(client)
apps = app.list_apps()
launch_info = app.launch(apps[0], content_id="...", params=...)
app.close(launch_info)
```
    
#### Mouse and Button Controls

You need to execute the first two commands.
```
inp = InputControl(client)
inp.connect_input()
inp.move(10, 10) # Moves mouse
inp.click()
inp.up()
inp.down()
inp.left()
inp.right()
inp.home()
inp.back()

# Following 3 lines are valid only when an input field is focussed on TV.
inp.type("This sends keyboard input!")
inp.enter()  # Return key.
inp.delete(10)  # Backspace 10 chars

inp.disconnect_input()
```

#### Source Controls

```
sources = SourceControl(client)
sources.set_source(list[0])
```

More controls coming soon!


# Credits
 - [klattimer](https://github.com/klattimer/LGWebOSRemote) for his library! Since WebOS team decided against providing any sort of documentation, his repository was extremely useful for an initial implementation
 - As far as input controls are concerned, they are based on the Java package written by [Connect-SDK folks](https://github.com/ConnectSDK/Connect-SDK-Android-Core/tree/master/src/com/connectsdk/service/webos)!
