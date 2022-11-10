import requests

url = "https://car-api2.p.rapidapi.com/api/trims"

querystring = {"verbose":"yes","sort":"id","direction":"asc","limit":5,"year":2020}

headers = {
	"X-RapidAPI-Key": "e9983c2065mshaf33398be4b091dp132915jsnb3a831923739",
	"X-RapidAPI-Host": "car-api2.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)