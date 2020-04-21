from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import zomatopy
import email_rasa
import json

t1_t2_cities = ['Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai', 'Ahmedabad', 'Pune', 'Agra', 'Ajmer', 'Aligarh', 
                'Amravati', 'Amritsar', 'Asansol', 'Aurangabad', 'Bareilly', 'Belgaum', 'Bhavnagar', 'Bhiwandi', 'Bhopal', 
                'Bhubaneswar', 'Bikaner', 'Bilaspur', 'Bokaro Steel City', 'Chandigarh', 'Coimbatore', 'Nagpur', 'Cuttack', 
                'Dehradun', 'Dhanbad', 'Bhilai', 'Durgapur', 'Erode', 'Faridabad', 'Firozabad', 'Ghaziabad', 'Gorakhpur', 'Gulbarga',
                'Guntur', 'Gwalior', 'Gurgaon', 'Guwahati', 'Hamirpur', 'Hubli–Dharwad', 'Indore', 'Jabalpur', 'Jaipur', 'Jalandhar', 
				'Jammu', 'Jamnagar', 'Jamshedpur', 'Jhansi', 'Jodhpur', 'Kakinada', 'Kannur', 
                'Kanpur', 'Kochi', 'Kottayam', 'Kolhapur', 'Kollam', 'Kozhikode', 'Kurnool', 'Ludhiana', 'Lucknow', 'Madurai', 
                'Malappuram', 'Mathura', 'Goa', 'Mangalore', 'Meerut', 'Moradabad', 'Mysore', 'Nanded', 'Nashik', 'Nellore', 'Noida', 
                'Palakkad', 'Patna', 'Perinthalmanna', 'Pondicherry', 'Purulia', 'Prayagraj', 'Raipur', 'Rajkot', 'Rajahmundry', 
                'Ranchi', 'Rourkela', 'Salem', 'Sangli', 'Shimla', 'Siliguri', 'Solapur', 'Srinagar', 'Thiruvananthapuram', 
                'Thrissur', 'Tiruchirappalli', 'Tirur', 'Tirupati', 'Tirunelveli', 'Tiruppur', 'Tiruvannamalai', 'Ujjain', 
                'Bijapur', 'Vadodara', 'Varanasi', 'Vasai-Virar', 'Vijayawada', 'Vellore', 'Warangal', 'Surat', 'Visakhapatnam']

t1_t2_cities_list = [x.lower() for x in t1_t2_cities]

# Check if the location exists. using zomato api.if found then save it, else utter not found.
class ActionValidateLocation(Action):
	def name(self):
		return 'action_check_location'

	def run(self, dispatcher, tracker, domain):
		print('inside action_check_location')
		loc = tracker.get_slot('location')
		city = str(loc)
		if city.lower() not in t1_t2_cities_list:
			dispatcher.utter_message("We do not operate in that area yet,  Can you please specify some other location")
			return [SlotSet('location',None)]
		else:
			return [SlotSet('location',loc)]

class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_search_restaurants'
		
	def run(self, dispatcher, tracker, domain):
		print('inside action_search_restaurants')
		config={ "user_key":"4e1f866b3e095dbcee9ab0a18801b12d"}
		zomato = zomatopy.initialize_app(config)
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		budget = tracker.get_slot('budget')
		if loc is not None:
			print('location :'+loc)
		if cuisine is not None:	
			print('cuisine :'+cuisine)
		if budget is not None:	
			print('budget :'+budget)
		location_detail=zomato.get_location(loc, 1)
		d1 = json.loads(location_detail)
		lat=d1["location_suggestions"][0]["latitude"]
		lon=d1["location_suggestions"][0]["longitude"]
		cuisines_dict={'Chinese':25,'Mexican':30,'Italian':55,'American':1,'South Indian':85,'North Indian':50}
		#cuisine types change with city?
		results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)),100)
		d = json.loads(results)
		response=""
		count=0
		if d['results_found'] == 0:
			response= "no results"
		else:
			count=0
			for restaurant in d['restaurants'] :
				# temp=restaurant['restaurant']['name']+':'+restaurant['restaurant']['location']['address']+':'+str(restaurant['restaurant']['user_rating']['aggregate_rating'])+':'+str(restaurant['restaurant']['average_cost_for_two'])
				# print(temp)
				if(count<5):
					if(budget=='basic' and restaurant['restaurant']['average_cost_for_two']<300):
						response=response+ "Found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+" has been rated "+str(restaurant['restaurant']['user_rating']['aggregate_rating'])+"\n"
						count=count+1
					if(budget=='standard' and restaurant['restaurant']['average_cost_for_two']>=300 and restaurant['restaurant']['average_cost_for_two']<=700):
						response=response+ "Found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+" has been rated "+ str(restaurant['restaurant']['user_rating']['aggregate_rating'])+"\n"
						count=count+1
					if(budget=='premium' and restaurant['restaurant']['average_cost_for_two']>700):
						response=response+ "Found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+" has been rated "+str(restaurant['restaurant']['user_rating']['aggregate_rating'])+"\n"
						count=count+1
				else:
					break
				
		print(response)
		dispatcher.utter_message(response)
		return [SlotSet('location',loc)]

class ActionEMailRestaurants(Action):
	def name(self):
		return 'action_email_restaurants'

	def run(self, dispatcher, tracker, domain):
		print('inside action_email_restaurants')
		config={ "user_key":"4e1f866b3e095dbcee9ab0a18801b12d"}
		zomato = zomatopy.initialize_app(config)
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		budget = tracker.get_slot('budget')
		email = tracker.get_slot('email')
		if loc is not None:
			print('location :'+loc)
		if cuisine is not None:	
			print('cuisine :'+cuisine)
		if budget is not None:	
			print('budget :'+budget)
		if email is not None:	
			print('email :'+email)
		location_detail=zomato.get_location(loc, 1)
		d1 = json.loads(location_detail)
		lat=d1["location_suggestions"][0]["latitude"]
		lon=d1["location_suggestions"][0]["longitude"]
		cuisines_dict={'Chinese':25,'Mexican':30,'Italian':55,'American':1,'South Indian':85,'North Indian':50}
		#cuisine types change with city?
		results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)),100)
		d = json.loads(results)
		response=""
		if d['results_found'] == 0:
			response= "no results"
		else:
			count=0
			for restaurant in d['restaurants'] :
				# temp=restaurant['restaurant']['name']+':'+restaurant['restaurant']['location']['address']+':'+str(restaurant['restaurant']['user_rating']['aggregate_rating'])+':'+str(restaurant['restaurant']['average_cost_for_two'])
				# print(temp)
				if(count<10):
					if(budget=='basic' and restaurant['restaurant']['average_cost_for_two']<300):
						response=response+ "Found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+" with avg budget "+ str(restaurant['restaurant']['average_cost_for_two'])+" with rating "+ restaurant['restaurant']['user_rating']['aggregate_rating']+"\n"
						count=count+1
					if(budget=='standard' and restaurant['restaurant']['average_cost_for_two']>=300 and restaurant['restaurant']['average_cost_for_two']<=700):
						response=response+ "Found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+" with avg budget "+ str(restaurant['restaurant']['average_cost_for_two'])+" with rating "+ restaurant['restaurant']['user_rating']['aggregate_rating']+"\n"
						count=count+1
					if(budget=='premium' and restaurant['restaurant']['average_cost_for_two']>700):
						response=response+ "Found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+" with avg budget "+ str(restaurant['restaurant']['average_cost_for_two'])+" with rating "+ restaurant['restaurant']['user_rating']['aggregate_rating']+"\n"
						count=count+1
				else:
					break
		email_rasa.send_mail(response,email)
		dispatcher.utter_message("email sent")
		


		

	

