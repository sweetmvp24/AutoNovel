import streamlit as st
import requests
import json

def generate_text(prompt, model="claude-3-opus-20240229", max_tokens=2000, temperature=0.5, api_key="", api_url=""):
    headers = {
        'Accept': 'application/json',
        'Authorization': f"Bearer {api_key}",
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }

    payload = json.dumps({
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": "You are a world-class author. Write the requested content with great skill and attention to detail.",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    try:
        response = requests.post(api_url, headers=headers, data=payload)
        response.raise_for_status()
        response_text = response.json()["choices"][0]["message"]["content"]
        return response_text.strip()
    except requests.exceptions.RequestException as e:
        return f"Error occurred while generating text: {e}"
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return f"Error occurred while parsing response: {e}"

# Streamlit UI
st.title('Text Generation App')

api_key = st.text_input('API Key:', type="password")
api_url = st.text_input('API URL:')
prompt = st.text_area('Prompt:')
model = st.selectbox('Model:', ['claude-3-opus-20240229', 'Other Model'])
max_tokens = st.slider('Max Tokens:', min_value=100, max_value=2000, value=2000)
temperature = st.slider('Temperature:', min_value=0.0, max_value=1.0, value=0.5)

if st.button('Generate Text'):
    if not api_key or not api_url:
        st.warning('Please provide both an API Key and an API URL.')
    else:
        result = generate_text(prompt, model, max_tokens, temperature, api_key, api_url)
        st.text_area('Generated Text:', value=result, height=300, disabled=True)

# if __name__ == '__main__':
#     st.run()
