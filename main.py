import requests
# car api
url = "https://car-api2.p.rapidapi.com/api/trims"
# url https://car-api2.p.rapidapi.com/api/trims followed by id number will give the record of te tabels from the api
querystring = {"verbose":"yes","sort":"id","direction":"asc","limit":"25","year":2020}
#  taking 25 records from api with year set as 2020

# host and api key
headers = {
	"X-RapidAPI-Key": "e9983c2065mshaf33398be4b091dp132915jsnb3a831923739",
	"X-RapidAPI-Host": "car-api2.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
# fetcing ids from api for each record
information= response.json()["data"]
database_value = []
# fetching data from api using ids for all the required tabels
for i in range (0,25):
	url="https://car-api2.p.rapidapi.com/api/trims/"+ str(information[i]['id'])
	# print(url)
	response = requests.request("GET", url, headers=headers, params=querystring)
	database_value.append(response.json())

print(database_value)