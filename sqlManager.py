import sqlite3
import datetime
import time

from sqlite3 import Error

class sqlliteManager:
    def __init__(self,db_file):
        """ create a database connection to a SQLite database """
        self.connection = None
        self.db_file = db_file
        try:
            self.connection = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        

    def createTables(self):
        # Create table
        try:
            cur = self.connection.cursor()
            cur.execute('''CREATE TABLE flights
               (now date,
                aircraft_code text, 
                airline_iata text, 
                  airline_icao text, 
                  altitude real, 
                  callsign text,
                  destination_airport_iata text,
                  ground_speed real,
                  heading real,
                  icao_24bit text,
                  id text,
                  latitude real,
                  longitude real )''')
        except Error as e:
            print(e)

    def insertFlightIntoTable(self,flight):
        # This is the qmark style:
        cur = self.connection.cursor()
        cur.execute("insert into flights values (?, ?)", (flight.aircraft_code,flight.airline_iata)) 

    def insertFlightsIntoTable(self,flights):
        # This is the qmark style:
        self.connection = sqlite3.connect(self.db_file)
        cur = self.connection.cursor()
        flightsList = []
        
        now = datetime.datetime.now()

        for flight in flights:
           flightsList.append([
              now,
             flight.aircraft_code , 
              flight.airline_iata , 
               flight.airline_icao , 
               flight.altitude , 
               flight.callsign ,
               flight.destination_airport_iata ,
               flight.ground_speed ,
               flight.heading ,
                flight.icao_24bit ,
                flight.id ,
                 flight.latitude,
                 flight.longitude ]) 
        try:
            cur.executemany("insert into flights values (?,?, ?,?,?,?,?,?, ?,?,?,?,?)", flightsList)
        except sqlite3.IntegrityError:
            print("couldn't add Python twice")

        
        # Save (commit) the changes
        self.connection.commit()
# Print the table contents
        for row in self.connection.execute("select count(*) from flights"):
            print(row)

        cur.fetchall()
        self.connection.close()