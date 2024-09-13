"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
import google.generativeai as genai

genai.configure(api_key=os.environ["AIzaSyD40lsR4kucIZ7MluBOnLFz_IGOlJJrlZA"])

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

# TODO Make these files available on the local file system
# You may need to update the file paths
files = [
  upload_to_gemini("Unknown File", mime_type="application/octet-stream"),
]

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "xin chào",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Xin chào! Rất vui được gặp bạn! Bạn có muốn tôi giúp gì không? \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "tôi muốn lấy  API CURAMINHF VỀ LÀM CHAT BOT BẰNG NGÔN NGỮ PYTHON HAY HƯỠNG DẪN TÔI",
      ],
    },
    {
      "role": "model",
      "parts": [
        files[0],
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)