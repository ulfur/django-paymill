import requests


url = 'http://localhost:8080/webhooks'

body = '''{
    "event":{
        "event_type":"client.updated",
        "event_resource":{
            "id":"client_cdcc9709ffcef07f9286",
            "email":"ulfurk@ulfurk.com",
            "description":"Ulfur Kristjansson (And now?)",
            "created_at":1388418081,
            "updated_at":1388831265,
            "app_id":null,
            "payment":[],
            "subscription":null
        },
        "created_at":1388831265,
        "app_id":null
    }
}'''


requests.post( url, body )