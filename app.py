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
        st.error(f"Error occurred while sending request: {e}")
        return None
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        st.error(f"Error occurred while parsing response: {e}")
        return None

def generate_title(plot):
    prompt_title = f"Here is the plot for the book: {plot}\n\n--\n\nRespond with a great Chinese title for this book. Only respond with the Chinese title, nothing else is allowed."
    response = generate_text(prompt_title, model, max_tokens, temperature, api_key, api_url)
    return response if response else None

def generate_chapters(plot_outline, num_chapters, writing_style, instruction):
    chapters = []
    for i in range(num_chapters):
        if chapters:
            prev_content = chapters[-1]
        else:
            prev_content = ""
        prompt_chapter = f'''Create chapter {i+1} of the book, in the writing style of {writing_style}, \
        based on the following plot outline:\n{plot_outline}\n and previous chapter content:\n{prev_content}\n \
        The creation of the chapter should follow the following instructions:\n{instruction}'''
        chapter = generate_text(prompt_chapter, model, max_tokens, temperature, api_key, api_url)
        if chapter:
            chapters.append(chapter)
            st.write(f"第{i+1}章已生成.")
            st.text_area(f"第{i+1}章内容：", value=chapter, height=300, disabled=False)
            st.download_button(f"下载第{i+1}章", chapter, file_name=f"第{i+1}章.txt")
        else:
            st.error(f"Failed to generate chapter {i+1}. Skipping.")

    return chapters
# Streamlit UI
st.title('小说自动生成器')

#api_key = st.text_input('API Key:', type='password')
api_key = st.selectbox('API Key:', ['sk-vT990qm3zTd8IgtcF670Ec285aB64fC9Bb4362F6E49e30Fd'])
#api_url = st.text_input('API URL:')
api_url = st.selectbox('API URL:', ['https://api.gptapi.us/v1/chat/completions'])
writing_style = st.text_input("写作风格", value="网文玄幻小说")
book_description = st.text_area("小说故事背景：", value="在一个名为天武大陆的异世界,主角秦尘是一位拥有极高炼药和血脉修炼天赋的武域上神，却因被心爱的女人和挚友背叛而陨落。数百年后，秦尘的意识在大玄国的一名同名少年体内意外觉醒，从此开始了一段新的征程。")
instruction = st.text_area('内容生成调教指令:', value="1.每个章节内容描述一个完整的事件或者冲突,并且能推动故事发展。2.相邻章节内容之间过渡要自然、合理,不要有突兀的感觉。 3.每个章节字数大概在#1500字#左右,不要太短或太长。")
num_chapters = st.number_input("章节数：", min_value=1, value=10)
model = st.selectbox('大模型:', ['claude-3-haiku', 'claude-3-haiku-20240229','claude-3-haiku-20240307', 'claude-3-sonnet','gpt-4-turbo-preview','claude-3-opus-20240229', 'gpt-3.5-turbo-0613'])
max_tokens = st.slider('最大输出字数:', min_value=100, max_value=4000, value=3000)
temperature = st.slider('想象力指数:', min_value=0.0, max_value=1.0, value=0.5)

prompt_plot = f'''Create a detailed plot outline for a {num_chapters}-chapter book in the writing style of {writing_style}, \
based on the following description:\n\n{book_description}\n\nThe creation of the plot should follow the following instructions:\n\n{instruction}'''
if st.button('开始自动生成'):
    if not api_key or not api_url:
        st.warning('Please provide both an API Key and an API URL.')
    else:
        plot_outline = generate_text(prompt_plot, model, max_tokens, temperature, api_key, api_url)
        title = generate_title(plot_outline)
        plot_outline = f"{title}\n\n{plot_outline}" if title else plot_outline
        st.text_area('小说故事大纲如下:', value=plot_outline, height=300, disabled=False)
        st.download_button("下载小说大纲", plot_outline, file_name=f"{title}小说大纲.txt")

        chapters = generate_chapters(plot_outline, num_chapters, writing_style, instruction)