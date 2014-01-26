import pickle, json, requests


url = 'http://localhost:8080/webhooks'
event = pickle.load( open('test_event.pckl', 'rb') )

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

event['event']['event_resource']['description'] = 'WHAT?'
requests.post( url, json.dumps(event) )