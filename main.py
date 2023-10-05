# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
import random
import requests
import pprint as pp
import boto3
def my_printer(item):
	print(f"Pokemon Name: {item['Name']['S']}")
	print(f"Pokemon Abilites: ",end="")
	for abil in item['Poke_Abilites']['SS']:
		print(abil, end=", ")
	print()
	print(f"Pokemon Types: ",end="")
	for typ in item['Types']['SS']:
		print(typ, end=", ")
	print()

def role_a_poke():
	random_int = random.randint(0,1272)
	API_URL = f"https://pokeapi.co/api/v2/pokemon?offset={random_int}&limit=20"
	response = requests.get(API_URL)
	res=response.json()
	name_url=res["results"]
	name_choice=random.choice(name_url)
	name_id=name_choice["url"]
	my_id=name_id.split("/")
	my_id=my_id[-2]
	name_choice=name_choice["name"]

	API_URL = f"https://pokeapi.co/api/v2/pokemon/{name_choice}"
	response = requests.get(API_URL)
	res=response.json()
	return my_id,res

load_dotenv()	
tbl_name = 'pokemon-table'

client = boto3.client('dynamodb',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
    aws_session_token=os.environ.get('AWS_SESSION_KEY'),  # Default to None if not present
    region_name=os.environ.get('AWS_REGION')
)

print("Welcome to Role a Poke Game")

try:
    response = client.create_table(
        TableName=tbl_name,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'Name',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'Name',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    
    # Use a waiter to wait for table creation to complete
    waiter = client.get_waiter('table_exists')
    waiter.wait(TableName=tbl_name)
    print(f"Table {tbl_name} created successfully!")

except client.exceptions.ResourceInUseException:
    print(f"Table {tbl_name} already exists.")

except Exception as e:
    print(f"An error occurred: {e}")

flag=True
while flag:
	print()
	play=input("do you wish to roll a pokemon?:(y/n) ")
	while play != "y" and play != "n":
		play=input("Enter a valid choice. y - to roll a pokemon, n - to exit: ")
	if play == "y":
		poke_id,pokemon=role_a_poke()
		poke_name=pokemon["species"]["name"]
		response = client.get_item(TableName=tbl_name, Key={'id': {'N': poke_id}, 'Name': {'S': poke_name}})
		item=response.get("Item")
		if item:
			print(f"Rolled {poke_name} It's already in the database")
			my_printer(item)
		else:
			print(f"{poke_name} was not found in the database and it's being added..")
			abilities_list=[]
			for abil in pokemon["abilities"]:
				abilities_list.append(abil["ability"]["name"])
			types_list=[]
			for typ in pokemon["types"]:
				types_list.append(typ["type"]["name"])
			item={'id': {'N': poke_id}, 'Name': {'S': poke_name}, 'Poke_Abilites': {'SS': abilities_list}, 'Types': {'SS': types_list}}
			response = client.put_item(TableName=tbl_name, Item=item)
			#response = client.get_item(TableName=tbl_name, Key={'id': {'N': poke_id}, 'Name': {'S': poke_name}})
			#item=response.get("Item")
			my_printer(item)
		
		
	elif play == "n":
		print()
		print("GoodBye, Have a Lovely Week..")
		flag=False
		continue

	

