# Junction 2021 API

This is the IntelligentSpaceAPI for the Helvar challenge "Brighter Spaces: Intelligent Lighting" in Junction 2021. This API forms the backbone of our
submission and provides modified information for our three examples of practical applications.

THIS API COULD BE SOLD AS A SERVICE TO SOFTWARE PARTIES.

The three practical applications are:
 - HomeSecure (https://homesecuritydemo.web.app/)
 - FluidOffice (https://fluidoffice.web.app/)
 - Movement Path Prediction
 
This API offers seven different endpoints:

    /realtime_sensors

Gives sensor-level information of activities based on user-defined timestamps. If realtime information would be provided by sensors, this could be
attached to a webhook to create for example notifications on apps. Practical in for example corridoors with multiple doors to better understand how
often certain points are passed. One idea we had was to track hospital patients' movements during quiet hours.

    /realtime_rooms
    
Gives room-level information of activities. A room has one or many sensors. HomeSecure and FluidOffice use this to provide the user with information
on trespassers or bookable space usage. Could maybe be used to notify cleaning personnel about room priorities. Using this endpoint requires enriching the data with room ids.

    /realtime_sites
    
Provides for example statistical information on entire buildings or wings. A site contains multiple rooms. This site information could be sold to for
example Google Maps to backup their visiting hours statistics.
    
    /transitions
    
Generates a transition matrix between sensor points. This relates to the idea that movements inside buildings can be modelled using random walks
(Markov chains). The transition matrix gives us the probabilities that a certain sensor is triggered after another sensor is triggered. This can
be used to further understand personnel movement. We limit possible transitions with walk speed.
    
    /heatmap
    
Generates a movement (location difference) heatmap by using the /transition -endpoint. This is done by first calculating the most active sensors
and using these as the startpoints for the Markov chain transitions. This may sound weird as we don't see walk starting points as binary (you
either are somewhere or aren't) but more like continuous (there's a x% chance that you might be here). The movement heatmap gives us 

    /data

This endpoint may be used to retrieve activation amount per device for specified time period. The data points are grouped to user chosen intervals. This could be used for example to track if some sensor has been activated during the past 2 minutes and the data could be viewed on some dashboard.

    /sensor_locations

This endpoint is purely to help impementing solutions as it tells the locations of devices on a site.
