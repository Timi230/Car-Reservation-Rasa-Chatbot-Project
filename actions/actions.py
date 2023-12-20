# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import mysql.connector
from mysql.connector import errorcode
import aiomysql

from datetime import datetime, timedelta



try:
    cnx = mysql.connector.connect(user='root', password='Hf1fyjd4',
                                host='localhost',
                                database='Car_agency')


except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else :
  print(40*'-')
  print('Connection is established')
  print(40*'-')
  print('\n')
  
# async def create_pool():
#     return await aiomysql.create_pool(
#         host='localhost',
#         user='root',
#         password='Hf1fyjd4',
#         db='Car_agency'
#     )

  

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world" #name of the action t

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class ActionShowAllCars(Action):
    def name(self) -> Text:
        return "action_show_all_cars"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
     
        dispatcher.utter_message("Here is the list of all cars:")

        offset = 0 
            
        stop = self.show_car(dispatcher, tracker, offset)
        print(stop)

        # if stop == 'Get_car':
        #     stop = 'affirm'
        
        print(stop)
        
        while stop == 'affirm':
                
            offset += 20
            stop = self.show_car(dispatcher, tracker, offset)
                
        return []
    
    def show_car(self, dispatcher: CollectingDispatcher, 
                       tracker : Tracker,
                       offset: int):
        
        
        cursor = cnx.cursor()
    
        query = "SELECT Numberplate, brand, type, color FROM car LIMIT 20 OFFSET %s;"
        cursor.execute(query, (offset,))

        column_names = [i[0] for i in cursor.description]
        rows = cursor.fetchall()

        if not rows:
            dispatcher.utter_message("No cars found.")
            return []

        max_widths = [max(len(str(row[i])) for row in rows) for i in range(len(column_names))]

        table_str = "```\n"
        table_str += "|"
        for i, col_name in enumerate(column_names):
            table_str += f" {col_name.ljust(max_widths[i]+5)} |"
        table_str += "\n"

        for row in rows:
            table_str += "|"
            for i, value in enumerate(row):
                table_str += f" {str(value).ljust(max_widths[i]+5)} |"
            table_str += "\n"

        table_str += "```"

        dispatcher.utter_message(table_str)
    
    
        dispatcher.utter_message("Do you want to see the next 20 cars?",
                            buttons=[
                                {"payload": "/affirm", "title": "Yes"},
                                {"payload": "/deny", "title": "No"}
                            ])
        
        last_action = tracker.latest_message["intent"]["name"]
        
        return last_action


class ActionShowAvailableCars(Action):
    def name(self) -> Text:
        return "action_show_available_cars"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
     
        dispatcher.utter_message("Here is the list of all available cars:")

        offset = 0 
            
        stop = self.show_available_car(dispatcher, tracker, offset)
        print(stop)

        # if stop == 'Get_car':
        #     stop = 'affirm'
        
        print(stop)
        
        while stop == 'affirm':
                
            offset += 20
            stop = self.show_available_car(dispatcher, tracker, offset)
                
        return []
    
    def show_available_car(self, dispatcher: CollectingDispatcher, 
                       tracker : Tracker,
                       offset: int):
        
        
        cursor = cnx.cursor()
    
        query = "SELECT Numberplate, brand, type, color FROM car where state= 'Available' LIMIT 20 OFFSET %s;"
        cursor.execute(query, (offset,))

        column_names = [i[0] for i in cursor.description]
        rows = cursor.fetchall()

        if not rows:
            dispatcher.utter_message("No cars found.")
            return []

        max_widths = [max(len(str(row[i])) for row in rows) for i in range(len(column_names))]

        table_str = "```\n"
        table_str += "|"
        for i, col_name in enumerate(column_names):
            table_str += f" {col_name.ljust(max_widths[i]+5)} |"
        table_str += "\n"

        for row in rows:
            table_str += "|"
            for i, value in enumerate(row):
                table_str += f" {str(value).ljust(max_widths[i]+5)} |"
            table_str += "\n"

        table_str += "```"

        dispatcher.utter_message(table_str)
    
    
        dispatcher.utter_message("Do you want to see the next 20 cars?",
                            buttons=[
                                {"payload": "/affirm", "title": "Yes"},
                                {"payload": "/deny", "title": "No"}
                            ])
        
        last_action = tracker.latest_message["intent"]["name"]
        
        return last_action
    
    
class ActionAskRentalDetails(Action):
    def name(self) -> Text:
        return "action_ask_rental_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message("Sure! I can help you with renting a car")
        
        car_brand = next(tracker.get_latest_entity_values("car_brand"), None)
        car_color = next(tracker.get_latest_entity_values("car_color"), None)
        car_type = next(tracker.get_latest_entity_values("car_type"), None)
        car_rent_duration = next(tracker.get_latest_entity_values("car_rent_duration"), None)
        
        print(car_brand, car_color, car_type, car_rent_duration)
        
        cursor = cnx.cursor()
        
        if car_brand is not None and car_color is not None and car_type is not None :
            query =f"SELECT Numberplate, brand, type, color FROM car WHERE brand = '{car_brand}' AND color = '{car_color}' AND type = '{car_type}' AND state = 'Available';"
            
        elif car_brand is None and car_color is not None and car_type is not None :
            query =f"SELECT Numberplate, brand, type, color FROM car WHERE color = '{car_color}' AND type = '{car_type}' AND state = 'Available';"
        
        elif car_brand is not None and car_color is  None and car_type is not None :
            query =f"SELECT Numberplate, brand, type, color FROM car WHERE brand = '{car_brand}' AND type = '{car_type}' AND state = 'Available';"
            
        elif car_brand is not None and car_color is not None and car_type is None :
            query =f"SELECT Numberplate, brand, type, color FROM car WHERE brand = '{car_brand}' AND color = '{car_color}' AND state = 'Available';"
            
        elif car_brand is None and car_color is None and car_type is not None :
            query =f"SELECT Numberplate, brand, type, color FROM car WHERE type = '{car_type}' AND state = 'Available';"
            
        elif car_brand is None and car_color is not None and car_type is  None :
            query =f"SELECT Numberplate, brand, type, color FROM car WHERE color = '{car_color}' AND state = 'Available';"
            
        elif car_brand is not None and car_color is  None and car_type is  None :
            query =f"SELECT Numberplate, brand, type, color FROM car WHERE brand = '{car_brand}' AND state = 'Available';"
            
        elif car_brand is None and car_color is None and car_type is None and car_rent_duration is None :
            dispatcher.utter_message("Could you please provide more details?")
            return []
                
        cursor.execute(query)

        column_names = [i[0] for i in cursor.description]
        rows = cursor.fetchall()
               
        if not rows:
            dispatcher.utter_message("No cars found.")
            return []

        max_widths = [max(len(str(row[i])) for row in rows) for i in range(len(column_names))]

        table_str = "```\n"
        table_str += "|"
        for i, col_name in enumerate(column_names):
            table_str += f" {col_name.ljust(max_widths[i]+5)} |"
        table_str += "\n"

        for row in rows:
            table_str += "|"
            for i, value in enumerate(row):
                table_str += f" {str(value).ljust(max_widths[i]+5)} |"
            table_str += "\n"

        table_str += "```"

        dispatcher.utter_message(table_str)
        
        if car_rent_duration is not None :
            return [SlotSet('car_rent_duration', car_rent_duration)]
        
        else :
            return []            


class ActionProvideCarInfo(Action):
    def name(self) -> Text:
        return "action_provide_car_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
            car_number_plate = list(tracker.get_latest_entity_values('car_number_plate'))
            print(car_number_plate)
            
            if len(car_number_plate) == 0 and tracker.get_slot('car_number_plate') is not None :
                
                car_number_plate = tracker.get_slot('car_number_plate')
                agency = self.show_car(dispatcher, car_number_plate)
                
                return [SlotSet('agency_city', agency)]
            
            elif len(car_number_plate) == 0 and tracker.get_slot('car_number_plate') is None : 
                
                dispatcher.utter_message("Can you give me car's number plate.")
                return []
              
            else:              
                
                agency = self.show_car(dispatcher, car_number_plate)
                return [SlotSet('car_number_plate', car_number_plate), SlotSet('agency_city', agency)]
        
    def show_car(self, dispatcher: CollectingDispatcher, car_number_plate: str):
        
        cursor = cnx.cursor()

        query = "Select c.*, a.city from car c, agency a where c.agency_ID = a.ID AND  c.Numberplate = '" + car_number_plate[0] +"';"
        cursor.execute(query)

        rows = cursor.fetchall()

        if not rows:
            dispatcher.utter_message("Sorry, I could not find any car with that number plate.")
            return []
        
        msg = "\n ----- Car information ----- \n"
        msg += "Numberplate      : " + car_number_plate[0] + "\n"
        msg += "Brand            : " + str(rows[0][6]) + "\n"
        msg += "Type             : " + str(rows[0][4]) + "\n"
        msg += "Color            : " + str(rows[0][3]) + "\n"
        msg += "Number of doors  : " + str(rows[0][1]) + "\n"
        msg += "Number of seats  : " + str(rows[0][2]) + "\n"
        msg += "Horserpower      : " + str(rows[0][5]) + "\n"
        msg += "Price per houres : " + str(rows[0][7]) + "$\n"
        msg += "Price per day    : " + str(rows[0][8]) + "$\n"
        msg += "State            : " + str(rows[0][9]) + "\n"
        
        if rows[0][9] == "Rented":
            msg += "Date return      : " + str(rows[0][10]) + "\n"
        
        msg += "Location         : " + str(rows[0][-1]) + "\n"

        dispatcher.utter_message(msg)
        
        return str(rows[0][-1])
            
class ActionConfirmRental(Action):
    def name(self) -> Text:
        return "action_confirm_rental"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        car_number_plate = list(tracker.get_latest_entity_values('car_number_plate'))
        car_rent_duration = next(tracker.get_latest_entity_values("car_rent_duration"), None)
        
        if car_rent_duration is None :
            car_rent_duration = tracker.get_slot('car_rent_duration')
            
            if car_rent_duration is None :
                dispatcher.utter_message("Can you give me the duration of the rental.")
                return []
            
            else :
                
                car_rent_duration = int(car_rent_duration)
            
                if len(car_number_plate) == 0 and tracker.get_slot('car_number_plate') is not None :
                    
                    car_number_plate = tracker.get_slot('car_number_plate')
                    self.rent_car(dispatcher, car_number_plate, car_rent_duration)
                    
                    return []
                
                elif len(car_number_plate) == 0 and tracker.get_slot('car_number_plate') is None : 
                    
                    dispatcher.utter_message("Can you give me car's number plate.")
                    return []
                    
                else:              
                    
                    self.rent_car(dispatcher, car_number_plate, car_rent_duration)
                    return [SlotSet('car_number_plate', car_number_plate)]
        
    def rent_car(self, dispatcher: CollectingDispatcher, car_number_plate: str, days_to_add: int):
        
        cursor = cnx.cursor()
        
        current_date = datetime.now()
        new_date = current_date + timedelta(days=days_to_add) 
        
        formatted_date = new_date.strftime("%Y-%m-%d")
        
        update_query = ("UPDATE car "
                        f"SET state = 'Rented', date_return = '{formatted_date}' "
                        f"WHERE Numberplate = '{car_number_plate[0]}';")

        print(update_query)
        cursor.execute(update_query)
        
        msg = " Validation of the rental of the car with the number plate : " + car_number_plate[0] + "\n"

        dispatcher.utter_message(msg)
        
        return []
        
class ActionProvideAgencyInfo(Action):
    def name(self) -> Text:
        return "action_provide_agency_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print('je suis la')
        agency = next(tracker.get_latest_entity_values("agency_city"), None)
        
        print(agency)
        
        if agency is None :
            agency = tracker.get_slot('agency_city')
            print(agency)
            
            if agency is None :
                
                query = "SELECT address, city, service, contact FROM agency;"
                self.show_agency(dispatcher, query, agency)
                return []
            
            else :
                query = "SELECT address, city, service, contact FROM agency WHERE city = '" + agency + "';"
                self.show_agency(dispatcher, query,agency)
                return [SlotSet('agency_city', agency)]
        
        else :
            query = f"SELECT address, city, service, contact FROM agency WHERE city = '{agency}';"
            self.show_agency(dispatcher, query, agency)
            print(type(agency))
            return [SlotSet('agency_city', agency)]    
                    
    
    def show_agency(self, dispatcher, query, agency):
        
        cursor = cnx.cursor()
        cursor.execute(query)

        column_names = [i[0] for i in cursor.description]
        rows = cursor.fetchall()
        
        if not rows:
            dispatcher.utter_message("No cars found.")
            return []

        max_widths = [max(len(str(row[i])) for row in rows) for i in range(len(column_names))]

        table_str = f"Here is the information for {agency}' agency : \n"
        table_str += "```\n"
        table_str += "|"
        for i, col_name in enumerate(column_names):
            table_str += f" {col_name.ljust(max_widths[i]+5)} |"
        table_str += "\n"

        for row in rows:
            table_str += "|"
            for i, value in enumerate(row):
                table_str += f" {str(value).ljust(max_widths[i]+5)} |"
            table_str += "\n"

        table_str += "```"

        dispatcher.utter_message(table_str)

class ActionShowCarAgency(Action):
    def name(self) -> Text:
        return "action_get_car_in_agency_city"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        
        agency = next(tracker.get_latest_entity_values("agency_city"), None)
        
        if agency is None :
            agency = tracker.get_slot('agency_city')
            
            if agency is None :
                
                dispatcher.utter_message("Can you give me the name of the agency.")
                return []
            
            else :
                query = "SELECT Numberplate, brand, type, color FROM car WHERE agency_ID = (SELECT ID FROM agency WHERE city = '" + agency + "');"
                self.show_agency(dispatcher, query, agency)
                
                return [SlotSet('agency_city', agency)]
        
        else :
            query = f"SELECT Numberplate, brand, type, color FROM car WHERE agency_ID = (SELECT ID FROM agency WHERE city = '{agency}');"
            self.show_agency(dispatcher, query, agency)
            
            return [SlotSet('agency_city', agency)]

    def show_agency(self, dispatcher, query, agency):
        
        cursor = cnx.cursor()
        cursor.execute(query)

        column_names = [i[0] for i in cursor.description]
        rows = cursor.fetchall()
        
        print(rows)

        if not rows:
            dispatcher.utter_message("No cars found.")
            return []

        max_widths = [max(len(str(row[i])) for row in rows) for i in range(len(column_names))]

        table_str = f"Here is the list of all cars in the agency {agency} : \n"
        table_str += "```\n"
        table_str += "|"
        for i, col_name in enumerate(column_names):
            table_str += f" {col_name.ljust(max_widths[i]+5)} |"
        table_str += "\n"

        for row in rows:
            table_str += "|"
            for i, value in enumerate(row):
                table_str += f" {str(value).ljust(max_widths[i]+5)} |"
            table_str += "\n"

        table_str += "```"

        dispatcher.utter_message(table_str)