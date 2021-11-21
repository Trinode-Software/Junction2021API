# Junction 2021 API

This is the IntelligentSpaceAPI for the Helvar challenge "Brighter Spaces: Intelligent Lighting" in Junction 2021. This API forms the backbone of our
submission and provides modified information for our three examples of practical applications.

THIS API COULD BE SOLD AS A SERVICE TO SOFTWARE PARTIES.

The three practical applications are:
 - HomeSecure (https://homesecuritydemo.web.app/)
 - FluidOffice (https://fluidoffice.web.app/)
 - Movement Path Prediction

The API is hosted in heroku and may be accessed from https://helvar-api.herokuapp.com

 
This API offers seven different endpoints:

    POST(/realtime_sensors)

    {
        site, required=True (String value that defines the site. Currently has to be site_1 as it is the only uploaded data),
        currenttime, required=True (defines the current time in string format, e.g. 2021-07-22 19:58:20.233518)
        timespan, required=False (From how long time period you want the data? Given as integer value in seconds. Default value is 300)
        deviceid, required=False (defines a device for which you want the data. If not defined the API returns data for all devices on the site)
    }

Gives sensor-level information of activities based on user-defined timestamps. If realtime information would be provided by sensors, this could be
attached to a webhook to create for example notifications on apps. Practical in for example corridoors with multiple doors to better understand how
often certain points are passed. One idea we had was to track hospital patients' movements during quiet hours.

    POST(/realtime_rooms)

     {
        site, required=True (String value that defines the site. Currently has to be site_1 as it is the only uploaded data),
        currenttime, required=True (defines the current time in string format, e.g. 2021-07-22 19:58:20.233518)
        timespan, required=False (From how long time period you want the data? Given as integer value in seconds. Default value is 300)
        roomid, required=False (defines a room for which you want the data. If not defined the API returns data for all rooms on the site)
    }
    
Gives room-level information of activities. A room has one or many sensors. HomeSecure and FluidOffice use this to provide the user with information
on trespassers or bookable space usage. Could maybe be used to notify cleaning personnel about room priorities. Using this endpoint requires enriching the data with room ids.

    POST(/realtime_sites)

    {
        site, required=True (String value that defines the site. Currently has to be site_1 as it is the only uploaded data),
        currenttime, required=True (defines the current time in string format, e.g. 2021-07-22 19:58:20.233518)
        timespan, required=False (From how long time period you want the data? Given as integer value in seconds. Default value is 300)
    }
    
Provides for example statistical information on entire buildings or wings. A site contains multiple rooms. This site information could be sold to for
example Google Maps to backup their visiting hours statistics.
    
    POST(/transitions)

    {
        site, required=True (String value that defines the site. Currently has to be site_1 as it is the only uploaded data)
        startpoint, required=False (Defines for which device/node you want the transition vector. If not defined the whole transition matrix is returned. String)
        timestep, required=True (Defines how long ahead we are looking. One step is 15 seconds so with value 1 we are looking for the probabilities after 15 seconds. Integer)
    }
    
Generates a transition matrix between sensor points. This relates to the idea that movements inside buildings can be modelled using random walks
(Markov chains). The transition matrix gives us the probabilities that a certain sensor is triggered after another sensor is triggered. This can
be used to further understand personnel movement. We limit possible transitions with walk speed.
    
    POST(/heatmap)

    {
        site, required=True (String value that defines the site. Currently has to be site_1 as it is the only uploaded data)
    }
    
Generates a movement (location difference) heatmap by using the /transition -endpoint. This is done by first calculating the most active sensors
and using these as the startpoints for the Markov chain transitions. This may sound weird as we don't see walk starting points as binary (you
either are somewhere or aren't) but more like continuous (there's a x% chance that you might be here). The movement heatmap seems to give us a good overview of the most-used paths inside a building.

    POST(/data)

    {
        site, required=True (String value that defines the site. Currently has to be site_1 as it is the only uploaded data),
        timeperiod, required=True (From how long time period you want the data? Given as integer value in seconds.)
        interval, required=True (In how big intervals you want to group the data e.g. all events during 5min time period could be grouped together. Given as integer value in seconds)
        deviceid, required=False (defines a device for which you want the data. If not defined the API returns data for all devices on the site)
    }

This endpoint may be used to retrieve activation amount per device for specified time period before current time. The data points are grouped to user chosen intervals. This could be used for example to track if some sensor has been activated during the past 2 minutes and the data could be viewed on some dashboard.

    POST(/sensor_locations)

    {
        site, required=True (String value that defines the site. Currently has to be site_1 as it is the only uploaded data),
        deviceid, required=False (defines a device for which you want the data. If not defined the API returns data for all devices on the site)
    }

This endpoint is purely to help impementing solutions as it tells the locations of devices on a site.
