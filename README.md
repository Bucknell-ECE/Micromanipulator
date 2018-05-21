# Micromanipulator

![Demonstration](https://ws2.sinaimg.cn/large/006tKfTcly1freqzbwdykj31kw16okjm.jpg)

## Table of Contents
--------------------
* [Overview](#Overview)
* [What is a Micromanipulator](#Whatisamicromanipulator)
* [Installation](#Installation)
* [Testing and Configuration](#Configuration)
* [Main Features](#Mainfeatures)
  * [Position Mode](#PositionMode)
  * [Main Modules](#Mainmodules)
* [Parts Links](#Partslink)
* [License](#License)

<a name="Overview"></a>
## Overview
-------------------
Dr. Paliulis, who is working for the Biology department at Bucknell University, is performing research on chromosomes. 
In order to perform her research, Dr. Paliulis needs to utilize a glass needle to perform her test under microscope. The main objective is to use a small, sharp glass needle to probe cells under a microscope. A joystick is used for both position and velocity movement.Three M3-LS-1.8-6 Linear Smart Stages from New Scale Technologies were used to control and drive the needle. The micromanipulator offers sensitivity adjustment, speed control, set and return home. The project was previously installed and developed on arduino and was later
transported to raspberry pi platform. 

<a name="Whatisamicromanipulator"></a>
## What is a Micromanipulator?
---------------------
A [micromanipulator](https://en.wikipedia.org/wiki/Micromanipulator) is the device that is used to do manipulation and interact with testing samples under microscope. The Micromanipulator is controlled by a joystick and driven with three linear smart stages. The micromanipulator can achieve the precision of level of movement that couldn't be achieved by human hands and manual tools. 

<a name="Installation"></a>
## Installation
----------------------
Waiting to be added

<a name="Mainfeatures"></a>
## Main Features
---------------------
<a name="PositionMode"></a>
### Position Mode
The designed micromanipulator provides user with position mode. The microneedle will be placed on the preset "home" position on the microscope stage. The user can also later redefine the "home" position by using "set home" key on Joystick. The user can move the Joystick to adjust the X and Y position of the microneedle and then pressed "ZUp" or "ZDown" button to adjust the Z position. When the user finishe operation and release all buttons, the microneedle will automatically return back to the "home" position.  

### Joystick Configuration ###
![Joystick Diagram](https://ws2.sinaimg.cn/large/006tKfTcly1frew6yvbapj31e20xw4qp.jpg "Joystick Configuration")


<a name="Mainmodules"></a>
### Modules

<a name="Configuration"></a>
## Configuration
--------------
### Joystick Guide
Button 3: Z Up
Button 4: Z Down
Button 8: Z sensitivity increase
Button 9: Z sensitivity decrease
Button 10: Reset Home to the center of stage
Button +/- : Adjusting the sensitivity of X and Y. Due to configuration issue, the "-" sign represent maximum sensitivity, the "+" sign
represent minimum sensitivity

<a name="Partslink"></a>
## Parts Links:
------------------
+ Link to Dozuki tutorial: ########

+ Link to Parts List: 
https://drive.google.com/open?id=1ucY0XXdSG67SAkqAeAms21Gy_4KU3A-f

+ CONN USB JACK TYPE A HORIZON R/A 151-1080-ND
https://www.digikey.com/scripts/DkSearch/dksus.dll?Detail&itemSeq=261244052&uq=636622310614761080

+ CRYSTAL 12MHZ 12PF SMD 535-13381-1-ND
https://www.digikey.com/scripts/DkSearch/dksus.dll?Detail&itemSeq=261244104&uq=636622310614771081

+ Hirose Electric Co Ltd FH12-10S-0.5SH(55) HFJ110CT-ND
https://www.digikey.com/scripts/DkSearch/dksus.dll?Detail&itemSeq=261244151&uq=636622310614771081

+ Maxim Integrated MAX3421EEHJ+ MAX3421EEHJ+-ND
https://www.digikey.com/scripts/DkSearch/dksus.dll?Detail&itemSeq=261244279&uq=636622310614771081

+ Texas Instruments LM386MX-1/NOPB LM386MX-1/NOPBCT-ND
https://www.digikey.com/scripts/DkSearch/dksus.dll?Detail&itemSeq=261244418&uq=636622310614781082

+ KEMET C0402C220J5GACTU 399-1015-1-ND
https://www.digikey.com/scripts/DkSearch/dksus.dll?Detail&itemSeq=261245631&uq=636622310614781082

+ Samtec Inc. SSQ-118-03-T-D SAM1204-18-ND
https://www.digikey.com/scripts/DkSearch/dksus.dll?Detail&itemSeq=261245662&uq=636622310614791083

+ Recom Power RAC06-05SC 945-1409-5-ND
https://www.digikey.com/scripts/DkSearch/dksus.dll?Detail&itemSeq=261245724&uq=636622310614791083

+ Qualtek 703W-00/53 Q219-ND
https://www.digikey.com/scripts/DkSearch/dksus.dll?Detail&itemSeq=261246023&uq=636622310614791083

+ Keystone Electronics 4527 36-4527-ND
https://www.digikey.com/scripts/DkSearch/dksus.dll?Detail&itemSeq=261246232&uq=636622310614801084

+ Adafruit Industries LLC 254 1528-1462-ND
https://www.digikey.com/scripts/DkSearch/dksus.dll?Detail&itemSeq=261246277&uq=636622310614801084


<a name="License"></a>
## License
-------------------
Waiting to be added
