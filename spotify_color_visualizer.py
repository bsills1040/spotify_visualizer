import requests
import cv2
import numpy as np
import matplotlib.pyplot as plt

client_id = "deebc7cb2e0e42728c94e8fb04657733"
client_secret = "3f4ba18d893f428da744780076935db5"

def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")

def get_track_info(track_id):
    url = f"https://api.spotify.com/v1/audio-analysis/{track_id}"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def map_frequency_to_color(freq):
    colormap = plt.get_cmap('viridis')  
    color = colormap(freq)
    color = tuple(int(c * 255) for c in color[:3]) 
    return color

def show_tooltip(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        frequency = frequencies[x // 80]  
        tooltip_text = f"Frequency: {frequency:.2f}"

        tooltip_image = image.copy()

        cv2.putText(tooltip_image, tooltip_text, (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imshow("Track Visualization", tooltip_image)

# Prompt user to enter the track ID
track_id = input("Enter the Spotify track ID: ")

# Check if the track ID exists on Spotify
track_info_response = get_track_info(track_id)

if track_info_response:
    frequencies = track_info_response["segments"][0]["pitches"]

    color_map = [map_frequency_to_color(freq) for freq in frequencies]

    image_width = len(color_map)
    image_height = 300
    image = np.zeros((image_height, image_width * 80, 3), dtype=np.uint8)

    for i, color in enumerate(color_map):
        image[:, i * 80:(i + 1) * 80, :] = color

    cv2.namedWindow("Track Visualization")
    cv2.setMouseCallback("Track Visualization", show_tooltip)
    cv2.imshow("Track Visualization", image)
else:
    print(f"Could not find track ID: {track_id}")

cv2.waitKey(0)
cv2.destroyAllWindows()