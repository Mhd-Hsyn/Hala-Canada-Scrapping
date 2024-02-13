import requests, json

url = "https://halacanada.netwave-tech.com/api/store/post"


# all_json_data= json.load(open ("all_posts_data.json", "r"))
all_json_data= json.load(open ("all_posts_data_arabic.json", "r"))


for data in all_json_data:

  # print( data['title'])
  # print( type(data['title']))

  print( f"\n\n{data['image_url']}")
  # print( type(data['content']))
  
  payload = {
    'title': f"{data['title']}",
    'description': f"{data['content']}",
    'image': f"{data['image_url']}",
    # "language": "en"
    "language": "ar"
    }
  
  headers = {
    'Accept': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)
