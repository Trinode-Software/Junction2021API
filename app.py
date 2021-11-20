from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy as np
import ast
import json
from flask_cors import CORS
import os



app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)





class Data(Resource):
  def post(self):
    parser = reqparse.RequestParser()  # initialize
        
    parser.add_argument('site', required=True)  # add args
    parser.add_argument('timeperiod', required=True)
    parser.add_argument('interval', required=True)
    parser.add_argument('deviceid', required=False)
    
    args = parser.parse_args()  # parse arguments to dictionary
    
    site = args['site'] # site name, as string
    timeperiod = args['timeperiod'] # wanted timeperiod in seconds, as integer
    interval = args['interval'] # With which time interval do you want the data. In seconds, as integer
    deviceid = args['deviceid'] # wanted device. All if not defined, as integer
    
    script_dir = os.getcwd()
  
    file = 'data/' + site + '/' + site + '.pkl'
    
    
    df_events = pd.read_pickle(os.path.abspath(os.path.join(script_dir, file)), compression='gzip')
    df_events.loc[:, 'timestamp'] = (pd.to_datetime(df_events['timestamp'], utc=True)
                                 .dt.tz_convert('Europe/Helsinki')
                                 .dt.tz_localize(None))
    
    now = pd.Timestamp.utcnow().tz_convert('Europe/Helsinki').tz_localize(None) - pd.Timedelta(120, 'D') - pd.Timedelta(12, 'H')
    previous = now - pd.Timedelta(timeperiod + 'S')
    
    
    df_events.timestamp = df_events.timestamp.dt.floor(str(interval) + 'S')
    df_events = df_events[(df_events['timestamp'] > previous) & (df_events['timestamp'] < now)]
    df_events.loc[:, 'count'] = 1
    
    if deviceid:
      df_events = df_events[df_events['deviceid'] == int(deviceid)]
    df_events = df_events.groupby(['deviceid', 'timestamp']).sum()

    print(df_events)
    return {'data': df_events.to_json()}, 200  # return data with 200 OK
    # # df_events_5min = df_events_5min.drop(['deviceid'], axis=1)
    # df_events_5min = df_events_5min.reindex(pd.date_range(df_events_5min.index.min(), df_events_5min.index.max(), freq='5min')).fillna(0)

class Devices(Resource):
  def post(self):
    parser = reqparse.RequestParser()  # initialize
        
    parser.add_argument('site', required=True)  # add args
    parser.add_argument('deviceid', required=False)
    
    args = parser.parse_args()  # parse arguments to dictionary
    
    site = args['site'] # site name, as string
    deviceid = args['deviceid'] # wanted device. All if not defined, as integer
    
    script_dir = os.getcwd()
  
    file = 'data/' + site + '/' + site + '.json'
    
    
    df_devices = pd.read_json(os.path.abspath(os.path.join(script_dir, file)))
    
    if deviceid:
      df_devices = df_devices[df_devices['deviceid'] == int(deviceid)]
      
    return {'data': list(df_devices.T.to_dict('deviceid').values())}, 200  # return data with 200 OK
  
  
class RealTimeSensors(Resource):
  def post(self):
    parser = reqparse.RequestParser()  # initialize
        
    parser.add_argument('site', required=True)  # add args
    parser.add_argument('currenttime', required=True)
    parser.add_argument('timespan', required=False)
    parser.add_argument('deviceid', required=False)
    
    args = parser.parse_args()  # parse arguments to dictionary
    
    site = args['site'] # site name, as string
    currenttime = args['currenttime'] # wanted timeperiod in seconds, as integer
    timespan = args['timespan'] # With which time interval do you want the data. In seconds, as integer
    deviceid = args['deviceid'] # wanted device. All if not defined, as integer
    
    script_dir = os.getcwd()
  
    file = 'data/' + site + '/' + site + '.pkl'
    
    
    df_events = pd.read_pickle(os.path.abspath(os.path.join(script_dir, file)), compression='gzip')
    df_events.loc[:, 'timestamp'] = (pd.to_datetime(df_events['timestamp'], utc=True)
                                 .dt.tz_convert('Europe/Helsinki')
                                 .dt.tz_localize(None))
    
    # now = pd.Timestamp.utcnow().tz_convert('Europe/Helsinki').tz_localize(None) - pd.Timedelta(120, 'D') - pd.Timedelta(12, 'H')
    previous = ''
    
    if timespan:
      previous = currenttime - pd.Timedelta(timespan + 'S')
      df_events.timestamp = df_events.timestamp.dt.floor(str(timespan) + 'S')
    else:
      previous = currenttime - pd.Timedelta(60*5, 'S')
      df_events.timestamp = df_events.timestamp.dt.floor('300S')
    
    
    
    df_events = df_events[(df_events['timestamp'] >= previous) & (df_events['timestamp'] < currenttime)]
    df_events.loc[:, 'count'] = 1
    
    if deviceid:
      df_events = df_events[df_events['deviceid'] == int(deviceid)]
    df_events = df_events.groupby(['deviceid', 'timestamp']).sum()

    print(df_events)
    return {'data': df_events.to_json()}, 200  # return data with 200 OK
    
class RealTimeRooms(Resource):
  def post(self):
    parser = reqparse.RequestParser()  # initialize
    
    parser.add_argument('site', required=True)  # add args
    parser.add_argument('roomid', required=False)  # add args
    parser.add_argument('currenttime', required=True)
    parser.add_argument('timespan', required=False)
    
    args = parser.parse_args()  # parse arguments to dictionary
    
    site = args['site'] # site name, as string
    roomid = args['roomid']
    currenttime = args['currenttime'] # wanted timeperiod in seconds, as integer
    timespan = args['timespan'] # With which time interval do you want the data. In seconds, as integer
    
    script_dir = os.getcwd()
  
    file = 'data/' + site + '/' + site + '.pkl'
    
    
    df_events = pd.read_pickle(os.path.abspath(os.path.join(script_dir, file)), compression='gzip')
    df_events.loc[:, 'timestamp'] = (pd.to_datetime(df_events['timestamp'], utc=True)
                                 .dt.tz_convert('Europe/Helsinki')
                                 .dt.tz_localize(None))
     
    
  
    file = 'data/' + site + '/' + site + '.json'
    df_devices = pd.read_json(os.path.abspath(os.path.join(script_dir, file)))
    
    
    
    # now = pd.Timestamp.utcnow().tz_convert('Europe/Helsinki').tz_localize(None) - pd.Timedelta(120, 'D') - pd.Timedelta(16, 'H')
    # currenttime = now
    previous = ''
    currenttime = pd.Timestamp(currenttime)
    if timespan:
      previous = currenttime - pd.Timedelta(timespan + 'S')
      df_events.timestamp = df_events.timestamp.dt.floor(str(timespan) + 'S')
    else:
      previous = currenttime - pd.Timedelta(60*5, 'S')
      df_events.timestamp = df_events.timestamp.dt.floor('300S')
    
    df_events = df_events[(df_events['timestamp'] >= previous) & (df_events['timestamp'] < currenttime)]
    df_events = df_devices.merge(df_events, how='inner', left_on='deviceid', right_on='deviceid')
    df_events = df_events.drop(['deviceid'], axis=1)
    df_events = df_events.drop(['x'], axis=1)
    df_events = df_events.drop(['y'], axis=1)
    df_events = df_events.drop(['timestamp'], axis=1)
    df_events.loc[:, 'count'] = 1
    
    if roomid:
      df_events = df_events[df_events['roomid'] == int(roomid)]
    df_events = df_events.groupby('roomid', group_keys='roomid').sum()
    
    
    

    return {'data': df_events.to_dict()}, 200  # return data with 200 OK
  
  
class RealTimeSites(Resource):
  def post(self):
    parser = reqparse.RequestParser()  # initialize
    
    parser.add_argument('site', required=False)  # add args
    parser.add_argument('currenttime', required=True)
    parser.add_argument('timespan', required=False)
    
    args = parser.parse_args()  # parse arguments to dictionary
    
    site = args['site'] # site name, as string
    currenttime = args['currenttime'] # wanted timeperiod in seconds, as integer
    timespan = args['timespan'] # With which time interval do you want the data. In seconds, as integer
    
    script_dir = os.getcwd()

    sites = []
    
    if site:
      sites = [site]
    else:
      sites = ['site_1']
      
    returnArray = []
    for i in range(len(sites)):
      file = 'data/' + sites[i] + '/' + sites[i] + '.pkl'
      
      
      df_events = pd.read_pickle(os.path.abspath(os.path.join(script_dir, file)), compression='gzip')
      df_events.loc[:, 'timestamp'] = (pd.to_datetime(df_events['timestamp'], utc=True)
                                  .dt.tz_convert('Europe/Helsinki')
                                  .dt.tz_localize(None))  
      
      
      # now = pd.Timestamp.utcnow().tz_convert('Europe/Helsinki').tz_localize(None) - pd.Timedelta(120, 'D') - pd.Timedelta(16, 'H')
      # currenttime = now
      previous = ''
      currenttime = pd.Timestamp(currenttime)
      if timespan:
        previous = currenttime - pd.Timedelta(timespan + 'S')
        df_events.timestamp = df_events.timestamp.dt.floor(str(timespan) + 'S')
      else:
        previous = currenttime - pd.Timedelta(60*5, 'S')
        df_events.timestamp = df_events.timestamp.dt.floor('300S')
      
      df_events = df_events[(df_events['timestamp'] >= previous) & (df_events['timestamp'] < currenttime)]

      df_events.loc[:, 'count'] = 1
      
      newObject = {
        "site": sites[i],
        "count": int(df_events.count(axis=0)['count'])
      }
      returnArray.append(newObject)
    
    
    

    return {'data': returnArray}, 200  # return data with 200 OK
  
  
class Transition(Resource):
  def post(self):
    parser = reqparse.RequestParser()  # initialize
    
    parser.add_argument('site', required=True)  # add args
    parser.add_argument('startpoint', required=False)
    parser.add_argument('timestep', required=True)
    
    args = parser.parse_args()  # parse arguments to dictionary
    
    site = args['site'] # site name, as string
    startpoint = args['startpoint']
    timestep = args['timestep']
    
    script_dir = os.getcwd()

    file = 'data/' + site + '/' + site + '.pkl'
    
    df_events = pd.read_pickle(os.path.abspath(os.path.join(script_dir, file)), compression='gzip')
    df_events.loc[:, 'timestamp'] = (pd.to_datetime(df_events['timestamp'], utc=True)
                                .dt.tz_convert('Europe/Helsinki')
                                .dt.tz_localize(None))  
    
    df_events.timestamp = df_events.timestamp.dt.floor('15S')
    df_events = df_events.drop_duplicates()

    timestamps = {}
    for row in df_events.itertuples():
      key = str(row.timestamp)
      if key in timestamps.keys():
        timestamps[key].append(row.deviceid)
      else:
        timestamps[key] = [row.deviceid]
      
    data = timestamps.copy()
    devices = []
    newObject = {
      'total': 0
    }
    
    file = 'data/' + site + '/' + site + '.json'    
    df_devices = pd.read_json(os.path.abspath(os.path.join(script_dir, file)))
    
    devicesCount = int(df_devices.count(axis=0)['deviceid'])
    
    for i in range(devicesCount):
      newObject[i] = 0

    devicesCloseEnough = []

    for row1 in df_devices.itertuples():
      array = []
      for row2 in df_devices.itertuples():
        distance = np.sqrt((row2.x - row1.x)**2 + (row2.y - row1.y)**2)
        if distance <= 600:
          array.append(row2.deviceid)
      devicesCloseEnough.append(array)
      
    devices = []
    for i in range(devicesCount):
      devices.append(newObject.copy())
      

    for object in data.values():
      for device1 in object:
        devices[device1]['total'] += 1
        for device2 in object:
          if device2 in devicesCloseEnough[device1] and not device1 == device2:
            devices[device1][device2] += 1


    devicesAsObjects = devices.copy()

    deviceMatrix = []
    for device in devicesAsObjects:
      sum = 0
      for i in range(devicesCount):
        sum += device[i]
        
      row = []
      for i in range(devicesCount):
        row.append(device[i] / sum)
      
      deviceMatrix.append(row)
      
    numpyMatrix = np.matrix(deviceMatrix)
    power = np.linalg.matrix_power(numpyMatrix, int(timestep) + 1)
    
    if startpoint:
      return {'data': power.tolist()[int(startpoint)]}, 200
    else:
      return {'data': power.tolist()}, 200
  

api.add_resource(Data, '/data')
api.add_resource(Devices, '/sensor_locations')
api.add_resource(RealTimeSensors, '/realtime_sensors')
api.add_resource(RealTimeRooms, '/realtime_rooms')
api.add_resource(RealTimeSites, '/realtime_sites')
api.add_resource(Transition, '/transition')





if __name__ == '__main__':
    app.run()  # run our Flask app