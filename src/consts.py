import os
from dotenv import load_dotenv

load_dotenv()

# BACKEND_URL = 'localhost:8000'
BACKEND_URL = 'http://back.b.aovzerk.ru'

PATH_PREFIX = '/api/delivery-service'

# redis
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

#Key

yandex_key = os.getenv('yandex_key')

yandex_host=os.getenv('yandex_host')

#release
calculate_delivery=os.getenv('calculate_delivery')

delivery_interval =os.getenv('delivery_interval')

list_of_PVZ=os.getenv('list_of_PVZ')

Creating_an_application=os.getenv('Creating_an_application')

Confirmation_of_the_application=os.getenv('Confirmation_of_the_application')

Getting_delivery_intervals=os.getenv('Getting_delivery_intervals')
Order_Editing=os.getenv('Order_Editing')

Cancellation_of_the_application=os.getenv('Cancellation_of_the_application')

Getting_information_about_the_application=os.getenv('Getting_information_about_the_application')


#test url
test_calculate_delivery=os.getenv('test_calculate_delivery')

test_delivery_interval =os.getenv('test_delivery_interval')

test_list_of_PVZ=os.getenv('test_list_of_PVZ')

test_Creating_an_application=os.getenv('test_Creating_an_application')

test_Confirmation_of_the_application=os.getenv('test_Confirmation_of_the_application')

test_Getting_delivery_intervals=os.getenv('test_Getting_delivery_intervals')
test_Order_Editing=os.getenv('test_Order_Editing')

test_Cancellation_of_the_application=os.getenv('test_Cancellation_of_the_application')

test_Getting_information_about_the_application=os.getenv('test_Getting_information_about_the_application')
