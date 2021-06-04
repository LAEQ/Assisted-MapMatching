# LAEQ-Cartographic Correlation

A QGIS plugin to adjust a GPS track on a network (map-matching) semi-automatically.
<br>
The matching is based on the librairie Leuven.MapMatching.


## Purpose of the plugin

Matching a GPS track with a network is currently a laborious work. You need to select manually every points and place it on the correct segment.
This plugin automaticaly match your points on your network layer and then allow you to modify the result manually


## Installation

First of all you need to open the window "Manage and Install Plugins" in the Plugins option <br>
<img src = "ressources/images/plugin_installation_1.png">

Then enter "LAEQ-MapMatching in the searching tab", select the plugin with the same name
<img src = "ressources/images/plugin_installation_2.png">
Click on install plugin (bottom-right)

Once it's installed, you can start it by clicking on the icon
<img src = "ressources/images/plugin_installation_3.png">

## Usage 

The plugin has a personnal window with 2 tabs: Matching and Settings. <br>
- The Matching tab in the principal tab where you will execute the functionnalities 
- The Settings tab allow you to modify some parameters in the programm. The presettings should be working in most case

The workflow of the plugin is divided into 3 steps : Input, Matching and export
<br><br>

### Step 1: Input
<br>
This step prepare the data to facilitate the work of the map-matching algorithms. It correct the topology of the network and verify the validity of the input. 
You need to fill every fields and execute the two functionnalities to access to the next step.
<br><br>
<img src = "ressources/images/plugin_usage_1.png">
<br><br>
Here is a description of every fields: <br>

- Network layer: This dropDown list show all layers of type **LineString** that are active on QGIS. Select the layer on wich you want to adjust your GPS track
The type MultilineString isn't supported. You can convert your MultiLineString layer to a LineString layer with the tool "Multipart to SingleParts" of QGIS 
- GPS trace layer: 
This dropDown list show all layers of type **Point** that are active on QGIS. Select the layer that you want to match to a network 
- OID (Object identifier): This dropDown list show all the attributes of type **"Integer/Integer64/int/int8"** present in the selected GPS trace. This field must be an unique identifier of every points and is used to order them. A point present earlier on the trace must have a smaller number than another present later.<br>
- Buffer range: This slider represent the maximum distance to find line on the selected network for each trajectory point. The bigger this value is, the longest the computing time 

The functionnality **"Reduce the network"** create a reduced version of the layer given in the Network layer field. The algorithm create a buffer around every point of the GPS trace and only keep the roads intersecting the buffer. One done, a new layer will be added to QGIS : "Reduced Network" and the user will be able to click on "Correct the topology"

The functionnality **"Correct the topology"** check and correct the topology of the network to prevent future errors during the matching. The algorithm controll the presence of four case:
- First is the presence of loop. We consider that a loop is a geometry which has his two extremities touching each other. One a loop is spotted, the method cut it in two at it's center.
- The second is the presence of dangle-nodes. A dangle-nodes exist when an extremity of a line touch another line. The method cut the touched line in two at the connection point IMAGE
-The third is 



## Version and Dependencies

Plugin developped on QGIS 3.18.0

Dependencies: 

- [shapely](https://pypi.org/project/Shapely/) 
Already installed on QGIS windows, You need a version lower than 1.5.17 for linux

## Contact
Director: <br>
- Phillipe Apparicio: philippe.apparicio@inrs.ca

Developeur: <br>
- Jordy Gelb: jordygelb@gmail.com

- David Maignan: ?

- Jérémy Gelb: ?

## License
GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007
