import os
from typing import Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://chatbot-backend-lime.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Response(BaseModel):
    ans:str
    bot: Optional[str] = "bot1"
    
async def chatbot(input: str)->str:
    import os
    import google.generativeai as genai

    genai.configure(api_key="AIzaSyDeotUkPjCaGQxq77WfT4MOKK3XqJLK-Wk")

        # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-002",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            "I want to create an multilingual chatbot that do functinalities of You are travel planner chatbot, who also suggest itineneary plans for travel according to user preferences\nlike Days, Season, Festivals, Persons, Children, Infants, Travel preferences, Economic classes and many more. You are a sophisticated travel planner chatbot designed to assist users in planning their trips based on various preferences and requirements. Your primary tasks include suggesting itineraries, finding flights, train tickets, and accommodations, and providing travel tips and cultural insights.\nYou have a job to find them flights for entered details from APIs like \nhttps://serpapi.com/search.json?engine=google_flights&departure_id=PEK&arrival_id=AUS&outbound_date=2024-09-28&return_date=2024-10-04&currency=USD&hl=en\nand Websites like https://www.booking.com/flights/index.en-gb.html?aid=304142&label=gen173rf-1FCAsobEITbGUtZ3JhbmRlLXJlc2lkZW5jeUgzWANobIgBAZgBCbgBB8gBDNgBAegBAfgBC4gCAaICE29wZW5hc3Npc3RhbnRncHQuaW-oAgO4AvDI3LcGwAIB0gIkZGExMGNkM2UtNTllMy00YWIxLWJlZmQtMzQ1NzIyZjgzNDZh2AIG4AIB&sid=d3c5b533082ef2141177e6a838ac4166&from=booking&\nand https://www.makemytrip.com/?srsltid=AfmBOoq3yzpn2hhspbGW2UxqFtAznM7f1HiatnyIU-UmE6uWxa7e0egM\nYou should also learn to give train tickets suggestions using Railway APIS http://indianrailapi.com/api/v2/livetrainstatus/apikey/<apikey>/trainnumber/<train_number>/date/<yyyymmdd>/\nhttps://indianrailways.gov.in/ \nYou are also required to help user find hotels or resorts, https://serpapi.com/search.json?engine=google_hotels&q=hotels+in+Ahmedabad&check_in_date=2024-09-28&check_out_date=2024-09-29\nand  \nhttps://www.booking.com/searchresults.en-gb.html?label=gen173rf-1FCAsobEITbGUtZ3JhbmRlLXJlc2lkZW5jeUgzWANobIgBAZgBCbgBB8gBDNgBAegBAfgBC4gCAaICE29wZW5hc3Npc3RhbnRncHQuaW-oAgO4AvDI3LcGwAIB0gIkZGExMGNkM2UtNTllMy00YWIxLWJlZmQtMzQ1NzIyZjgzNDZh2AIG4AIB&sid=d3c5b533082ef2141177e6a838ac4166&closed_msg=10683872&dest_id=-2088270&dest_type=city&hlrd=14&selected_currency=USD\nand https://www.makemytrip.com/hotels/ and many internet tools.\nYou can also refer some websites for travel planning like : https://www.worldpackers.com/articles/first-time-travelers\nand https://www.worldtrips.com/resources/travel-tips-for-beginners and https://www.timandfintravel.com/blog/travel-tips and\nhttps://www.vacationindia.com/travelguide/india-travel-guide-16-tips-when-preparing-for-your-first-trip-to-india/ \nYou should also learn about cultures of places to suggest users for example, https://marquishotels.in/goan-customs/#:~:text=The%20culture%20of%20Goa%20is,the%20Goan%20culture%20even%20today.&text=The%20crafts%20and%20arts%20of,Hindu%2C%20Muslim%20and%20Christian%20origins.\nand https://www.ftd.travel/manali-culture and https://ahmedabad.nic.in/culture-heritage/#:~:text=Ahmedabad%20enjoys%20rich%20cultural%20traditions,Ganesh%20Chaturthi%2C%20Navaratri%20and%20Diwali. and \nhttps://en.wikipedia.org/wiki/Culture_of_India etc. \nYou will always give perfect informations. You are best travel planner. You need to guide for each and every question. As the ultimate travel planner, your goal is to simplify the travel planning process, ensuring users have a memorable and enriching travel experience. You are equipped to handle every aspect of travel planning, from flights and accommodations to cultural insights and travel tips. Always strive for clarity, thoroughness, and responsiveness in your interactions.\n\nQuestion Example 1\nI want to visit Italy for 3 days, give me itinerary plan.\n\nAnswer\nIf you have only 3 days to explore Italy, it’s best to focus on one iconic city or two nearby locations to fully enjoy the experience. I recommend spending your 3 days in Rome with a day trip to Florence, giving you a mix of history, art, and culture.\n\nDay 1: Rome – The Eternal City\n\n\t•\tMorning: Arrive in Rome and check into your hotel.\n\t•\tAncient Rome: Start with a visit to the Colosseum, one of Rome’s most famous landmarks. From there, explore the Roman Forum and Palatine Hill to experience ancient Roman ruins.\n\t•\tAfternoon: Head over to Piazza Navona, a stunning square with fountains and cafés, then visit the Pantheon, one of Rome’s best-preserved ancient monuments.\n\t•\tEvening: Walk through the charming streets to the Spanish Steps, then toss a coin into the Trevi Fountain to ensure your return to Rome. Enjoy dinner in the lively Trastevere neighborhood, known for its authentic Roman cuisine.\n\nDay 2: Vatican City & Florence Day Trip\n\n\t•\tMorning: Start your day early with a visit to Vatican City. Explore St. Peter’s Basilica and St. Peter’s Square. Visit the Vatican Museums and admire the Sistine Chapel painted by Michelangelo.\n\t•\tAfternoon: After lunch, take a high-speed train to Florence (approx. 1.5 hours). Explore the historical city center and visit the Florence Cathedral (Duomo), the Piazza della Signoria, and the Ponte Vecchio.\n\t•\tEvening: Enjoy a Tuscan dinner in Florence before returning to Rome by train.\n\nDay 3: Rome – City Highlights and Departure\n\n\t•\tMorning: Start your final day with a leisurely walk through Villa Borghese Gardens, then visit the Borghese Gallery (optional, if time allows).\n\t•\tAfternoon: Visit Campo de’ Fiori and Piazza Venezia, where you can see the Altare della Patria. If you have time, stop by the Capitoline Hill for a panoramic view of the Roman Forum.\n\t•\tEvening: Depending on your departure time, enjoy one last Italian meal before heading to the airport.\n\nTips:\n\n\t•\tGetting around: Use public transportation, like buses or the metro in Rome, and take high-speed trains for day trips.\n\t•\tPace: This itinerary is fast-paced but gives you a taste of Italy’s two most iconic cities in a short period.\n\nThis plan will give you a whirlwind tour of Italy’s top highlights while ensuring you experience the best of both Rome and Florence!\n\nQuestion Example 2\nI want to book tickets for me, my wife and 2 children from Ahmedabad to Haridwar, I am religious in nature and Prefer vegeterian food. Give me flight tickets and travel plan.\n\nAnswer\nTo help you plan your trip from Ahmedabad to Haridwar, I'll outline a general travel plan and provide guidance on booking your flight tickets. However, please note that I can't access real-time data for flight bookings. You can check the flight availability and book tickets through popular travel booking websites like MakeMyTrip, Cleartrip, or directly from airlines.\n\n### **Travel Plan from Ahmedabad to Haridwar**\n\n#### **Day 1: Arrival in Haridwar**\n- **Flight from Ahmedabad to Dehradun**: Book a flight from Sardar Vallabhbhai Patel International Airport (AMD) in Ahmedabad to Dehradun's Jolly Grant Airport (DED). From Dehradun, you can take a taxi or a train to Haridwar (approx. 1 hour by taxi).\n- **Check-in**: Upon arrival in Haridwar, check into a family-friendly hotel or guesthouse. Look for places that offer vegetarian meals.\n- **Evening**: Visit **Har Ki Pauri** for the Ganga Aarti, a mesmerizing ritual that takes place in the evening, offering a spiritual experience.\n\n#### **Day 2: Explore Haridwar**\n- **Morning**: Visit **Mansa Devi Temple** via the cable car. This temple is dedicated to Goddess Mansa Devi and offers a panoramic view of Haridwar.\n- **Breakfast**: Enjoy a vegetarian breakfast at a local eatery (try some local dishes like **Aloo Puri**).\n- **Afternoon**: Explore the **Chandi Devi Temple**, another important religious site, and visit the **Rajaji National Park** if time permits for a glimpse of nature and wildlife.\n- **Lunch**: Have lunch at a vegetarian restaurant or dhaba in Haridwar.\n- **Evening**: Relax by the Ganges or visit local markets for souvenirs. You can also participate in the evening Ganga Aarti again if you wish.\n\n#### **Day 3: Departure**\n- **Morning**: After breakfast, check out from the hotel.\n- **Travel to Dehradun**: Take a taxi or train back to Dehradun Airport for your return flight to Ahmedabad.\n- **Flight back to Ahmedabad**: Book a flight from Dehradun to Ahmedabad for your return trip.\n\n### **Flight Booking Guidance**\n1. **Search for Flights**:\n   - Use travel booking websites (MakeMyTrip, Cleartrip, or Google Flights).\n   - Enter departure as Ahmedabad (AMD) and arrival as Dehradun (DED).\n   - Select your travel dates and number of passengers (2 adults and 2 children).\n\n2. **Choose a Flight**:\n   - Look for direct flights or the shortest duration available.\n   - Check for airlines that offer vegetarian meal options.\n\n3. **Book Tickets**:\n   - Complete the booking by providing passenger details and making payment.\n\n### **Vegetarian Food Options**\n- Haridwar has numerous vegetarian restaurants and eateries. Some popular options include:\n  - **Chotiwala Restaurant**\n  - **Hoshiyarpuri**\n  - **Mathura Walo Ki Pracheen Dukan**\n\nThis itinerary will provide you with a fulfilling spiritual experience in Haridwar. If you need further assistance with specific flights or hotels, please let me know!\n\nQuestion Example 3\nI am working professional and going to goa to attend some meeting, Book my ticket from Mumbai to Goa and Book hotel for 3 days.\n\nAnswer\nTo assist you with your trip from Mumbai to Goa for a meeting, I’ll outline a general travel plan and provide guidance on booking your flight and hotel. However, I can’t make bookings directly, so I’ll guide you through the process.\n\nTravel Plan from Mumbai to Goa\n\nDay 1: Arrival in Goa\n\n\t•\tFlight from Mumbai to Goa:\n\t•\tSearch for flights from Chhatrapati Shivaji Maharaj International Airport (BOM) in Mumbai to Goa International Airport (GOI), also known as Dabolim Airport.\n\t•\tLook for direct flights for a quick journey (approximately 1 hour).\n\t•\tCheck-in: Upon arrival, check into a hotel in Goa. Depending on your meeting location, consider staying in areas like Panaji, Calangute, or Margao.\n\nDay 2: Meeting and Leisure\n\n\t•\tMorning: Attend your scheduled meeting. Make sure to arrive early to settle in.\n\t•\tAfternoon: After your meeting, explore local cuisine at a nearby restaurant. Try local vegetarian dishes like Goan Vegetable Curry or Vindaloo.\n\t•\tEvening: If time permits, relax at a nearby beach or visit local attractions like Fort Aguada or the Basilica of Bom Jesus.\n\nDay 3: Free Day\n\n\t•\tMorning: Have a leisurely breakfast at your hotel. You could explore nearby beaches or local markets.\n\t•\tAfternoon: Consider visiting places like Dudhsagar Waterfalls or Anjuna Flea Market if you’re interested in shopping.\n\t•\tEvening: Enjoy a sunset at one of Goa’s beautiful beaches like Candolim or Baga Beach.\n\nDay 4: Departure\n\n\t•\tMorning: Check out from your hotel and head to the airport for your flight back to Mumbai.\n\nFlight Booking Guidance\n\n\t1.\tSearch for Flights:\n\t•\tUse travel booking websites like MakeMyTrip, Cleartrip, or Google Flights.\n\t•\tEnter your departure city (Mumbai) and arrival city (Goa), along with your travel dates.\n\t2.\tChoose a Flight:\n\t•\tLook for direct flights and compare prices and timings.\n\t•\tSelect a flight that suits your schedule.\n\t3.\tBook Your Ticket:\n\t•\tComplete the booking by providing passenger details and making payment.\n\nHotel Booking Guidance\n\n\t1.\tSearch for Hotels:\n\t•\tUse websites like Booking.com, MakeMyTrip, or Airbnb to find suitable hotels in Goa.\n\t•\tConsider factors like proximity to your meeting location and amenities.\n\t2.\tSelect a Hotel:\n\t•\tFilter for business-friendly hotels that offer good reviews, Wi-Fi, and dining options.\n\t3.\tBook Your Hotel:\n\t•\tChoose your room type, and confirm the dates (3 nights) and total price.\n\t•\tComplete the booking by entering your information and payment details.\n\nRecommended Hotels in Goa\n\n\t•\tTaj Exotica Resort & Spa, Goa: Luxurious stay with excellent amenities.\n\t•\tNovotel Goa Shrem Hotel: Business-friendly with good meeting facilities.\n\t•\tHotel Mandovi: Located in Panaji, great for business travelers.\n\nFeel free to ask if you need help with specific flight or hotel options, or any other travel-related questions!\n\nQuestion Example 4\nI am going to be in flight for the first time, Book me flight from Mumbai to New york. and also give me some tips. I am nervous.\n\nFlying for the first time can be exciting and a bit nerve-wracking! Here’s a guide to help you with your flight from Mumbai to New York, along with some helpful tips to ease your nerves.\n\nFlight Booking from Mumbai to New York\n\n\t1.\tSearch for Flights:\n\t•\tUse travel booking websites like MakeMyTrip, Cleartrip, or Google Flights.\n\t•\tEnter your departure city (Mumbai) and destination (New York), along with your preferred travel dates.\n\t2.\tChoose a Flight:\n\t•\tLook for direct flights or those with the shortest layover.\n\t•\tConsider flight duration, and check the airlines for their service quality.\n\t3.\tBook Your Ticket:\n\t•\tOnce you find a suitable flight, enter your passenger details and payment information to complete the booking.\n\nTips for Your First Flight\n\n\t1.\tArrive Early:\n\t•\tGet to the airport at least 3 hours before your international flight. This gives you time to check in, go through security, and find your gate.\n\t2.\tStay Informed:\n\t•\tKeep your flight itinerary handy. Familiarize yourself with airport layouts and procedures (check-in, security, boarding).\n\t3.\tPack Smart:\n\t•\tFollow the airline’s baggage policy for carry-on and checked luggage.\n\t•\tKeep essential items (passport, tickets, phone, chargers) in an easily accessible spot.\n\t4.\tDress Comfortably:\n\t•\tWear comfortable clothing and shoes, as you’ll be sitting for an extended period. Layers are a good idea since airplane cabins can get cold.\n\t5.\tStay Hydrated:\n\t•\tDrink water before and during the flight. Airplane cabins can be dry, so staying hydrated is essential.\n\t6.\tMove Around:\n\t•\tIf it’s a long flight, stand up, stretch, and walk around the cabin occasionally to keep your circulation going.\n\t7.\tBring Entertainment:\n\t•\tDownload movies, music, or books to keep yourself entertained during the flight, especially for long hauls.\n\t8.\tSnacks:\n\t•\tAlthough airlines provide meals, it’s a good idea to carry some snacks in case you get hungry.\n\t9.\tPractice Relaxation Techniques:\n\t•\tIf you feel anxious, try deep breathing exercises or listen to calming music. Visualization can also help—imagine a smooth journey.\n\t10.\tTalk to Flight Attendants:\n\n\t•\tIf you’re feeling nervous, let a flight attendant know. They’re trained to help passengers feel comfortable.\n\nFinal Thoughts\n\nRemember, flying is a safe and routine mode of transportation. Many first-time flyers feel nervous, but with these tips, you’ll be better prepared. Focus on the exciting destination you’re headed to and enjoy the journey!\n\nIf you have any specific questions about the flight or need help with the booking process, feel free to ask!",
        ],
        },
        {
        "role": "model",
        "parts": [
            "This is an excellent starting point for a multilingual travel planning chatbot.  To make it a reality, you'll need to integrate several key components:\n\n**1. Natural Language Understanding (NLU) and Dialogue Management:**\n\n* **Multilingual Support:**  This is crucial.  You'll need an NLU engine capable of understanding user input in multiple languages.  Popular choices include Google Cloud NLU, Amazon Comprehend, Microsoft Azure Language Understanding, or open-source options like Rasa.  These services will need to be trained on a substantial dataset of travel-related phrases and questions in each supported language.\n\n* **Intent Recognition:** The NLU engine must identify the user's intention (e.g., \"book a flight,\" \"suggest an itinerary,\" \"find hotels,\" \"get cultural information\").\n\n* **Entity Extraction:** It needs to extract relevant entities from the user's input (e.g., dates, locations, number of travelers, budget, travel preferences).\n\n* **Dialogue Management:** This component manages the conversation flow, guiding the user through the booking process and providing relevant information based on their previous inputs.  It'll need to handle complex scenarios, such as correcting misunderstandings, asking clarifying questions, and managing interruptions.\n\n\n**2. API Integration:**\n\n* **Flight APIs:**  You've listed several sources (SerpAPI, Booking.com, MakeMyTrip).  Each will have its own API documentation and requires an API key for access.  You'll need to write code to interact with these APIs, parse their responses, and present the results to the user in a clear and concise way.  Remember to handle errors gracefully (e.g., flights not found, API downtime).\n\n* **Hotel APIs:** Similar to flight APIs, you'll need to integrate with hotel booking APIs (Booking.com, MakeMyTrip have APIs; Expedia, Hotels.com, etc., also offer them).\n\n* **Train APIs:** The Indian Railways API you mentioned is a good starting point for India-specific train bookings.  You'll likely need additional APIs for other countries' rail systems.\n\n* **Other APIs:** Consider integrating APIs for things like weather forecasts, currency conversion, translation services (if your NLU doesn't handle all languages perfectly), and potentially map APIs to help users visualize their itineraries.\n\n**3. Itinerary Generation:**\n\n* **Algorithm Design:** You'll need to develop algorithms to generate itineraries based on user preferences. This is a complex task involving optimization (finding the best route, minimizing travel time), constraint satisfaction (considering budget, time, and preferences), and potentially recommendation systems (suggesting activities based on user interests).\n\n* **Data Sources:** To enhance itinerary suggestions, consider incorporating data from sources like travel blogs, guidebooks, and review websites.\n\n**4. Cultural Information:**\n\n* **Knowledge Base:** Create a knowledge base of cultural information for various destinations.  This could be a database or a set of structured documents that your chatbot can access.\n\n* **Information Retrieval:**  Implement a system to retrieve and present relevant cultural information based on the user's destination and interests.\n\n\n**5. Technical Stack:**\n\n* **Programming Language:** Python is a popular choice for chatbot development due to its rich ecosystem of libraries for NLU, API integration, and web development.\n\n* **Framework:** Consider using a chatbot framework like Rasa, Dialogflow, or Microsoft Bot Framework to simplify development.\n\n* **Database:** You'll need a database to store user data, itinerary information, and cultural knowledge.\n\n* **Deployment:**  Deploy your chatbot on a platform like Google Cloud, AWS, or Azure.\n\n\n**6. Testing and Iteration:**\n\nThorough testing is essential.  Test your chatbot with various user inputs, languages, and scenarios to identify and fix bugs, and refine its ability to understand and respond to user queries.  Iterative development will be key to improving its performance and accuracy over time.\n\n\n**Example Code Snippet (Conceptual Python with Rasa):**\n\n```python\n# This is a highly simplified example – actual implementation would be much more complex.\nfrom rasa.core.agent import Agent\n\n# ... (Load your Rasa agent, which includes NLU and dialogue management) ...\n\nagent = Agent.load(\"models/current/dialogue\")\n\nuser_input = input(\"Enter your travel request: \")\n\nresponse = agent.handle_text(user_input)\n\n# ... (Process the response, extract entities, interact with APIs, generate itinerary, etc.) ...\n\nprint(\"Chatbot response:\", response)\n```\n\nThis project is ambitious and requires significant programming and data science skills.  Start with a Minimum Viable Product (MVP) focusing on a limited set of functionalities and languages, then gradually expand its capabilities.  Remember to prioritize user experience and design a conversational interface that is intuitive and easy to use.\n",
        ],
        },
    ]
    )

    response = chat_session.send_message(input)

    print(response.text)
    return response
    
async def chatbot2(input: str)->str:
    import os
    import google.generativeai as genai

    genai.configure(api_key="AIzaSyDeotUkPjCaGQxq77WfT4MOKK3XqJLK-Wk")

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            "List all flight or train booking options from {departure city} to {destination city} using online platforms like MakeMyTrip, Goibibo, Cleartrip, Expedia, and Kayak. Compare prices in real-time and suggest the best option.\n\nFind and list hotels in {destination} for {number of people}, {budget}, {age of travelers} using booking platforms such as Booking.com, Agoda, Expedia, and MakeMyTrip. Provide price comparisons and booking links, and suggest the best hotel based on user preferences.\n\nCreate a complete itinerary plan for {destination}. Include cost overview, time allocation for each activity, adventure options, and detailed descriptions of each place.\n\nIf user input is not related to flight booking, hotel booking, itinerary planning, or time allocation, respond as a general conversational chatbot.\n\nWhen suggesting flight, train, or hotel bookings, reference the following platforms:\n\nOnline Travel Agency (OTA): MakeMyTrip, Goibibo, Cleartrip, Expedia, Kayak, etc.\nAirline Websites: Mention direct booking options with airlines like IndiGo, Air India, SpiceJet, Go First, etc.",
        ],
        },
        {
        "role": "model",
        "parts": [
            "Okay, I'm ready to help you plan your trip! Please tell me:\n\n1. *Where are you traveling from?* (Departure City)\n2. *Where are you going?* (Destination City)\n3. *When are you traveling?* (Dates)\n4. *How many people are traveling?* (Number of Travelers)\n5. *Are you looking for flight or train booking?\n6. **What's your budget for the trip?\n7. **What kind of experience are you looking for?* (Relaxing, adventurous, cultural, etc.)\n\nOnce I have this information, I can start comparing flight and train options, finding hotels that fit your budget and preferences, and creating a personalized itinerary. \n",
        ],
        },
    ]
    )

    response = chat_session.send_message(input)
    print(response.text)
    return response

async def chatbot3(input:str)->str:

    import os
    import google.generativeai as genai

    genai.configure(api_key="AIzaSyDeotUkPjCaGQxq77WfT4MOKK3XqJLK-Wk")

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-002",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            "Compare flight prices from {departure city} to {destination city} using platforms like MakeMyTrip (https://www.makemytrip.com/), Goibibo (https://www.goibibo.com/), Cleartrip (https://www.cleartrip.com/), Expedia (https://www.expedia.co.in/), and Kayak (https://www.kayak.co.in/). List the ticket prices for each platform and suggest the best airline option. Display the results in a tabular form with the airline, price, and booking link.\n\nProvide a list of hotels in {destination} for {number of people}, {budget}, {dates}, and {age of travelers} using Booking.com (https://www.booking.com/), Agoda (https://www.agoda.com/), Expedia (https://www.expedia.co.in/), and MakeMyTrip (https://www.makemytrip.com/). Compare room options and rates, displaying them in a tabular form with hotel name, price, amenities, and booking link. Suggest the best hotel option for the user.\n\nSuggest transportation options in {destination} including rental cars, public transport, and ride-sharing services. Provide pricing details and links for rental car booking sites such as Ola (https://www.olacabs.com/), Rapido (https://www.rapido.bike/), Uber (https://www.uber.com/in/en/), Hertz (https://www.hertz.com/rentacar/reservation/), Avis (https://www.avis.co.in/), and Turo (https://turo.com/).\n\nNotify the user about the check-in and check-out times for hotels in {destination}. Provide details and recommendations for early check-in or late check-out if available.\n\nIf passport required then, provide information on passport and visa requirements for traveling to {destination}. Ensure the user is aware of the necessary documents well in advance of the travel date. Ask user , if passport is required or not.\n\nInform the user about any local events or festivals happening during their stay in {destination}. Include the dates, description, and suggestions on how to participate or attend the events.\n\n\n\n",
        ],
        },
        {
        "role": "model",
        "parts": [
            "I cannot access real-time information, including live pricing from websites, current events, and availability for flights and hotels.  My responses will be based on hypothetical data and general information.  To get accurate results, you need to visit the websites listed and input your specific travel details.\n\n\nHowever, I can provide you with a template for organizing the information you gather.  Replace the bracketed placeholders with your actual information.\n\n\n*Part 1: Flight Comparison\n\n| Platform       | Airline       | Price (INR) | Booking Link                               |\n|-----------------|----------------|-------------|-------------------------------------------|\n| MakeMyTrip      | [Airline Name] | [Price]     | [Link]                                    |\n| Goibibo         | [Airline Name] | [Price]     | [Link]                                    |\n| Cleartrip       | [Airline Name] | [Price]     | [Link]                                    |\n| Expedia         | [Airline Name] | [Price]     | [Link]                                    |\n| Kayak           | [Airline Name] | [Price]     | [Link]                                    |\n\n\nSuggested Best Airline Option:* [Based on your price and preference comparison -  e.g.,  \"Indigo for its budget-friendly fares.\"]\n\n\n*Part 2: Hotel Comparison\n\n(Replace bracketed information with details from your search)\n\n| Platform       | Hotel Name        | Price (INR) | Amenities                               | Booking Link                               |\n|-----------------|--------------------|-------------|-------------------------------------------|-------------------------------------------|\n| Booking.com     | [Hotel Name]       | [Price]     | [List Amenities: e.g., Pool, Wifi, Breakfast] | [Link]                                    |\n| Agoda           | [Hotel Name]       | [Price]     | [List Amenities]                         | [Link]                                    |\n| Expedia         | [Hotel Name]       | [Price]     | [List Amenities]                         | [Link]                                    |\n| MakeMyTrip      | [Hotel Name]       | [Price]     | [List Amenities]                         | [Link]                                    |\n\n\nSuggested Best Hotel Option:* [Based on your budget, amenities, and preferences - e.g., \"The Grand Hotel for its excellent location and included breakfast.\"]\n\n\n\n*Part 3: Transportation Options in [Destination City]\n\nThis section requires you to check the individual websites for pricing as it varies greatly by time of day, demand, and distance.\n\n *Rental Cars:\n    * Hertz: [Link]  (Provide estimated price range based on your search)\n    * Avis: [Link]   (Provide estimated price range based on your search)\n    * Turo: [Link]   (Provide estimated price range based on your search)\n\n *Ride-Sharing Services:\n    * Ola: [Link] (Prices vary greatly based on distance and time of day.)\n    * Rapido: [Link] (Prices vary greatly based on distance and time of day.)\n    * Uber: [Link] (Prices vary greatly based on distance and time of day.)\n\n *Public Transport:* [Describe options available in [Destination City], including bus routes, metro, trains, etc., with estimated fares if available.]\n\n\n*Part 4: Hotel Check-in/Check-out Times\n\nStandard check-in time for most hotels is [Typical check-in time, e.g., 2 PM], and check-out is typically [Typical check-out time, e.g., 12 PM].  Early check-in and late check-out may be available for an additional fee.  Contact the hotel directly to inquire about availability and fees.\n\n\n\nPart 5: Passport and Visa Requirements\n\nIs a passport required for your trip to [Destination City]? [Yes/No]\n\n(If Yes):*  Please note that you will need a valid passport with at least [Number] months of validity remaining beyond your travel dates.  You may also require a visa depending on your citizenship. Check the [Destination Country]'s embassy or consulate website for the most up-to-date visa requirements.  Please ensure you have sufficient time to process your visa application.\n\n\n\n*Part 6: Local Events and Festivals*\n\nI do not have access to real-time event information.  To find out about local events and festivals during your stay in [Destination City], please search online using terms such as \"[Destination City] events [Month, Year]\" or check local tourism websites.\n\n\nRemember to replace the bracketed information with your specific details and conduct your own research on the websites provided to get accurate and up-to-date information.\n",
        ],
        },
    ]
    )

    response = chat_session.send_message(input)

    print(response.text)
    return response


@app.get("/api/chat")
async def handle_chat(ans: str = Query(...), bot: Optional[str] = Query("bot1")):
    try:
        # Get the user input from query parameters
        user_input = ans
        bot_input = bot

        # Decide which bot to use based on bot_input
        if bot_input == "bot1":
            chatbot_response = await chatbot(user_input)
        elif bot_input == "bot2":
            chatbot_response = await chatbot(user_input)  # Placeholder for bot2
        else:
            chatbot_response = await chatbot(user_input)  # Placeholder for other bots

        response_data = chatbot_response.to_dict()
        return JSONResponse(content={"response": response_data})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    
# @app.post("/api/chat")
# async def handle_chat(chat: Response):
#     user_input = chat.ans
#     bot_input = chat.bot
#     if(bot_input=="bot1"):
#         chatbot_response = await chatbot(user_input)
#     elif(bot_input=="bot2"):
#         chatbot_response = await chatbot(user_input)
#     else :
#         chatbot_response = await chatbot3(user_input)
    
#     chatbot_response = chatbot_response.to_dict()
#     return JSONResponse(content=chatbot_response)
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)