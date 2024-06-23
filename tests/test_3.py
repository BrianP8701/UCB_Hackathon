from app.services.TypeformService import TypeformService

typeformService = TypeformService()

print(typeformService.get_all_responses("x53Bondz"))


'''

example response from get_all_responses:

[TypeformResponse(id='sxvrk2jmmp8xac2paousxvrk2d8byy7c', answers=[{'field': {'id': 'Cl9EqQHZ3DCu', 'type': 'short_text', 'ref': '1'}, 'type': 'text', 'text': 'john doe'}, {'field': {'id': 'gnXh8af5LVTt', 'type': 'date', 'ref': '2'}, 'type': 'date', 'date': '1212-04-01T00:00:00.000Z'}, {'field': {'id': 'ynATgcyPNrAK', 'type': 'yes_no', 'ref': '3'}, 'type': 'boolean', 'boolean': True}]), TypeformResponse(id='f0nxvsdxibx050kpk4u6t1f0nxvsjhyf', answers=[{'field': {'id': 'Cl9EqQHZ3DCu', 'type': 'short_text', 'ref': '1'}, 'type': 'text', 'text': 'brian pra'}, {'field': {'id': 'gnXh8af5LVTt', 'type': 'date', 'ref': '2'}, 'type': 'date', 'date': '3333-12-22T00:00:00.000Z'}, {'field': {'id': 'ynATgcyPNrAK', 'type': 'yes_no', 'ref': '3'}, 'type': 'boolean', 'boolean': False}])]
'''
