import google.generativeai as genai

genai.configure(api_key="AIzaSyC5dxBOcVON1srncD0fu1PTqSyyZYrEYuk")

model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content("Give me 3 hijab tips for round face")

print(response.text)
