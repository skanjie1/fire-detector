# Import the following modules
import requests
import json

# Function to send Push Notification


def pushbullet_noti(title, body):

	TOKEN = 'o.6YbycEy0SbBdwi2go5Pf9BPBJIwYfaHH' # Pass your Access Token here
	# Make a dictionary that includes, title and body
	msg = {"type": "note", "title": title, "body": body}
	# Sent a posts request
	resp = requests.post('https://api.pushbullet.com/v2/pushes',
						data=json.dumps(msg),
						headers={'Authorization': 'Bearer ' + TOKEN,
								'Content-Type': 'application/json'})
	if resp.status_code != 200: # Check if fort message send with the help of status code
		raise Exception('Error', resp.status_code)
	else:
		print('Message sent')


pushbullet_noti("WARNING!", "A fire accident has occurred")
