# main/views.py
from django.shortcuts import render
import matplotlib.pyplot as plt
import os
from django.conf import settings
import io
import base64
import numpy as np
import json
import psycopg2
import random 
from datetime import datetime, timedelta



try:
    connection = psycopg2.connect(
        host="127.0.0.1",
        port="5432",
        database="memestore",
        user="postgres",
        password="pgadmin"
    )
 
    print("Database connected")
except Exception as e:
    print("Error:",e)
    print("Database connection failed")

connection.autocommit = True
cursor = connection.cursor()







def dashboard(request):
    template_path = os.path.join('main', 'dashboard.html')
    print(f'Template Path: {template_path}')

    # Google Charts Data

    # Google Charts Data
    cursor.execute("SELECT year, sales, expenses, profit FROM chart")
    google_chart_data = cursor.fetchall()
    google_chart_data = [[year, sales, expenses, profit] for year, sales, expenses, profit in google_chart_data]

    # Convert Google Charts data to JSON
    google_chart_data_json = json.dumps(google_chart_data)

    # ApexCharts Data
    cursor.execute("SELECT x, y FROM candlestick_data")
    apex_chart_data = cursor.fetchall()
    apex_chart_data = [{'x': row[0], 'y': row[1]} for row in apex_chart_data]

    # Convert ApexCharts data to JSON
    apex_chart_data_json = json.dumps(apex_chart_data)

    # ApexCharts Options
    chart_options = {
        'chart': {
            'type': 'candlestick',
            'height': 350
        },
        'title': {
            'text': 'CandleStick Chart',
            'align': 'left'
        },
        'xaxis': {
            'type': 'datetime'
        },
        'yaxis': {
            'tooltip': {
                'enabled': True
            }
        }
    }

   # graph data
    cursor.execute("SELECT x, y1, y2 FROM your_table_name")
    db_data = cursor.fetchall()

    graph_data = [
        {
            'x': entry[0],
            'y': [entry[1], entry[2]]
        }
        for entry in db_data
    ]


    # home data
    cursor.execute("SELECT x, y FROM north_data")
    north_data = cursor.fetchall()

    cursor.execute("SELECT x, y FROM south_data")
    south_data = cursor.fetchall()

    north_chart_data = [{'x': entry[0], 'y': entry[1]} for entry in north_data]
    south_chart_data = [{'x': entry[0], 'y': entry[1]} for entry in south_data]

     
    # index data
    cursor.execute("SELECT x, y1, y2 from line")
    db_data = cursor.fetchall()

    index_data = [
        {
            'x': entry[0],
            'y': [entry[1], entry[2]]
        }
        for entry in db_data
    ]


   #redar data
 
    cursor.execute("SELECT series_1, series_2, series_3 FROM radar_data")
    radar_data = cursor.fetchall()

    # Transpose the data to separate it into series
    transposed_data = list(zip(*radar_data))

    redar_data = [
        {'name': f'Series {i+1}', 'data': list(series)}
        for i, series in enumerate(transposed_data)
    ]


   #register data
    cursor.execute("SELECT name, squarearea FROM countrysquarearea")
    db_data = cursor.fetchall()

    # Transform the data
    pizza_data = [[name, squarearea] for name, squarearea in db_data]

    print(pizza_data)

    cursor.execute("SELECT speed_value FROM speed")
    db_data = cursor.fetchall()

    speed_value = db_data[0][0] if db_data else 0  # If result is None, set speed_value to 0


    cursor.execute("SELECT fruit_name, servings FROM trade_data")  
    db_data = cursor.fetchall()
    print("DB Data:", db_data)

    # Prepare data for rendering in the template
    trade_data = [{'fruit_name': fruit_name, 'servings': servings} for fruit_name, servings in db_data]

    

    # Convert ApexCharts options to JSON
    chart_options_json = json.dumps(chart_options)

    context = {
        'chart_data': google_chart_data_json,
        'candlestick_data': apex_chart_data_json,
        'chart_options': chart_options_json,
        'graph_data': graph_data,
        'north_chart_data': north_chart_data, 
        'south_chart_data': south_chart_data,
        'index_data': index_data,
        'redar_data': redar_data,
        'pizza_data': pizza_data,
        'speed_value': speed_value,
        'trade_data': trade_data
    }

    return render(request, template_path, context)

