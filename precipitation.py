from flask import Flask,jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect
import pandas as pd

engine=create_engine('sqlite:///Resources/hawaii.sqlite')
conn=engine.connect()


Base=automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


app=Flask(__name__)

@app.route('/')
def home():

    return(f'Welcome to Precipitation Data API<br/>'
           f'Available Routs:<br/>'
           f'api/v1.0/precipitation<br/>'
           f'/api/v1.0/stations<br/>'
           f'/api.v1.0/tobs'
    )
    
@app.route('/api/v1.0/precipitation')
def precipitation():

    session=Session(engine)
    data_precipitation=session.query(Measurement.date,Measurement.prcp).all()
    
    precipitation_list=[]
    for date,prcp in data_precipitation:
        precipitation_dict={}
        precipitation_dict['date']=date
        precipitation_dict['prcp']=prcp
        precipitation_list.append(precipitation_dict)

    return jsonify(precipitation_list)

@app.route('/api/v1.0/stations')


def stations():

    session=Session(engine)
    data_station=session.query(Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()

    station_list=[]
    for station,name,latitude,longitude,elevation in data_station:
        station_dict={}
        station_dict['station']=station
        station_dict['name']=name
        station_dict['latitude']=latitude
        station_dict['longitude']=longitude
        station_dict['elevation']=elevation
        station_list.append(station_dict)
    return jsonify(station_list)

@app.route('/api.v1.0/tobs')

def tobs():
    
    session=Session(engine)
    data_tobs=session.query(Measurement.station,Measurement.date,Measurement.tobs).filter(Measurement.date >'2016-08-23').all()

    tobs_list=[]
    for station,date,tobs in data_tobs:
        dict_tobs={}
        dict_tobs['station']=station
        dict_tobs['date']=date
        dict_tobs['tobs']=tobs
        tobs_list.append(dict_tobs)
    return jsonify(tobs_list)


@app.route('/api.v1.0/<date>')
def dates(date):
    session=Session(engine)
    
    list_dates=[]
    list_tobs=[]
    for i,t in session.query(Measurement,Measurement):
        list_dates.append(i.date)
        list_tobs.append(i.tobs)
    dictionary=dict(zip(list_dates,list_tobs))


    avg_temp={}
    temp_dict={}
    final_list=[]
    for i in dictionary.keys():
         if i>=str(date):
            final_list.append(dictionary[str(i)])
            temp_dict['Max Temperature']=max(final_list)
            temp_dict['Min Temperature']=min(final_list)
            temp_dict['Avg Temperatre']=round(sum(final_list)/len(final_list),2)
   
    return jsonify(temp_dict)

    @app.route('/api.v1.0/<start>:<finish>')
    def starttofinish(start,finish):
        list_dates=[]
        list_tobs=[]
        for i,t in session.query(Measurement,Measurement):
            list_dates.append(i.date)
            list_tobs.append(i.tobs)
        dictionary=dict(zip(list_dates,list_tobs))
    
        temp_dict={}
        final_list_full=[]
        for i in dictionary.keys():
            if i >=str(start) and i<=str(finish):
                final_list_full.append(dictionary[str(i)])
                temp_dict['Max Temperature']=max(final_list_full)
                temp_dict['Min Temperature']=min(final_list_full)
                temp_dict['Avg Temperature']=round(sum(final_list_full)/len(final_list_full),2)
            
        return(temp_dict)

    

if __name__ == "__main__":
    app.run(debug=True, port=5009)