import requests
import json, base64
def query_agent_api(query):
    # Define the URL for the deployed agent API
    url = "http://127.0.0.1:8000/agent"  # Update with actual deployed URL if needed
    
    # Send POST request with the query and optional location
    payload = {
        "query": query
    }
    
    response = requests.post(url, json=payload)
    
    # Ensure that we have a valid response
    if response.status_code == 200:
        return response.json().get("response")
    else:
        return "Error in API request"
def text_to_audio(text):
  url = "https://api.sarvam.ai/text-to-speech"

  payload = {
      "inputs": [text],
      "target_language_code": "en-IN",
      "speaker": "meera",
      "pitch": 0,
      "pace": 1.0,
      "loudness": 2.0,
      "speech_sample_rate": 8000,
      "enable_preprocessing": True,
      "model": "bulbul:v1"
  }
  headers = {"Content-Type": "application/json", 'API-Subscription-Key': '002fe8be-b61e-4d76-a78f-1720b3cc9797'}

  response = requests.request("POST", url, json=payload, headers=headers)
  data = json.loads(response.text)
  base64_string = data["audios"][0]

# Decode the Base64 string
  audio_data = base64.b64decode(base64_string)

  # Write the decoded data to a .wav file
  with open("output_audio.wav", "wb") as wav_file:
      wav_file.write(audio_data)
  return"output_audio.wav"
import gradio as gr

def process_query(query):
    # Step 1: Send the query to the deployed API and get the response
    response_text = query_agent_api(query)
    
    # Step 2: Convert the response text to audio
    audio_file = text_to_audio(response_text)
    
    # Return the response text and the path to the audio file
    return response_text, audio_file

# Define the Gradio interface
iface = gr.Interface(
    fn=process_query,  # The function that processes the query
    inputs=[
        gr.Textbox(label="Query"),  # Text input for the user query
    ],
    outputs=[
        gr.Textbox(label="Response Text"),  # Output the response text
        gr.Audio(label="Response Audio")  # Output the response as audio
    ],
    title="Smart Agent Query Interface",
    description="Enter a query to get a response in both text and audio formats."
)

# Launch the interface
iface.launch()
