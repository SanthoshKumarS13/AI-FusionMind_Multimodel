import streamlit as st
import requests
import os
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

# API keys for other features (optional)
Image_Token = os.getenv('Image_generation')
Content_Token = os.getenv('ContentGeneration')
Image_prompt_token = os.getenv('Prompt_generation')

# API Headers for external services (optional)
Image_generation = {"Authorization": f"Bearer {Image_Token}"}
Content_generation = {
    "Authorization": f"Bearer {Content_Token}",
    "Content-Type": "application/json"
}
Image_Prompt = {
    "Authorization": f"Bearer {Image_prompt_token}",
    "Content-Type": "application/json"
}

# Text-to-Image Model API URLs
image_generation_urls = {
    "black-forest-labs/FLUX.1-schnell": "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell",
    "CompVis/stable-diffusion-v1-4": "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4",
    "black-forest-labs/FLUX.1-dev": "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
}

# Default content generation model
content_models = {
    "llama-3.1-70b-versatile": "llama-3.1-70b-versatile",
    "llama3-8b-8192": "llama3-8b-8192",
    "gemma2-9b-it": "gemma2-9b-it",
    "mixtral-8x7b-32768": "mixtral-8x7b-32768"
}

# Load the translation model and tokenizer locally
@st.cache_resource
def load_translation_model():
    model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-one-mmt")
    tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-one-mmt")
    return model, tokenizer

# Function to perform translation locally
def translate_text_local(text):
    model, tokenizer = load_translation_model()
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    translated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"])
    translated_text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    return translated_text

# Function to query Groq content generation model (optional)
def generate_content(english_text, max_tokens, temperature, model):
    url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a creative and insightful writer."},
            {"role": "user", "content": f"Write educational content about {english_text} within {max_tokens} tokens."}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    response = requests.post(url, json=payload, headers=Content_generation)
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        st.error(f"Content Generation Error: {response.status_code}")
        return None

# Function to generate image prompt (optional)
def generate_image_prompt(english_text):
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a professional Text to image prompt generator."},
            {"role": "user", "content": f"Create a text to image generation prompt about {english_text} within 30 tokens."}
        ],
        "max_tokens": 30
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=Image_Prompt)
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        st.error(f"Prompt Generation Error: {response.status_code}")
        return None

# Function to generate an image from the prompt (optional)
def generate_image(image_prompt, model_url):
    data = {"inputs": image_prompt}
    response = requests.post(model_url, headers=Image_generation, json=data)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Image Generation Error {response.status_code}: {response.text}")
        return None

# User Guide Section
def show_user_guide():
    st.title("FusionMind User Guide")
    st.write("""
### Welcome to the FusionMind User Guide!

### How to use this app:

1. **Input Tamil Text**:
   - You can either select one of the suggested Tamil phrases or input your own text. The app primarily focuses on Tamil inputs, but it supports a wide range of other languages as well (see the list below).

2. **Generate Translations**:
   - Once you've input your text, the app will automatically translate it to English. The translation model is a **many-to-one model**, meaning it can take input from various languages and translate it into English.

3. **Generate Educational Content**:
   - After translating the text into English, the app will generate **educational content** based on the translated input. You can adjust the creativity of the content generation using the temperature slider, and control the length of the output with the token limit setting.

4. **Generate Images**:
   - In addition to generating content, the app can also generate an **image** related to the translated content. You don’t need to worry about creating complex image prompts—FusionMind includes an automatic **image prompt generator** that will convert your input into a well-defined image prompt, ensuring better image generation results.

---

### Features:

- **Multilingual Translation**:
   - FusionMind supports a **many-to-one translation model**, so you can input text in a wide variety of languages, not just Tamil. Below are the supported languages:

     - **Arabic (ar_AR)**, **Czech (cs_CZ)**, **German (de_DE)**, **English (en_XX)**, **Spanish (es_XX)**, **Estonian (et_EE)**, **Finnish (fi_FI)**, **French (fr_XX)**, **Gujarati (gu_IN)**, **Hindi (hi_IN)**, **Italian (it_IT)**, **Japanese (ja_XX)**, **Kazakh (kk_KZ)**, **Korean (ko_KR)**, **Lithuanian (lt_LT)**, **Latvian (lv_LV)**, **Burmese (my_MM)**, **Nepali (ne_NP)**, **Dutch (nl_XX)**, **Romanian (ro_RO)**, **Russian (ru_RU)**, **Sinhala (si_LK)**, **Turkish (tr_TR)**, **Vietnamese (vi_VN)**, **Chinese (zh_CN)**, **Afrikaans (af_ZA)**, **Azerbaijani (az_AZ)**, **Bengali (bn_IN)**, **Persian (fa_IR)**, **Hebrew (he_IL)**, **Croatian (hr_HR)**, **Indonesian (id_ID)**, **Georgian (ka_GE)**, **Khmer (km_KH)**, **Macedonian (mk_MK)**, **Malayalam (ml_IN)**, **Mongolian (mn_MN)**, **Marathi (mr_IN)**, **Polish (pl_PL)**, **Pashto (ps_AF)**, **Portuguese (pt_XX)**, **Swedish (sv_SE)**, **Swahili (sw_KE)**, **Tamil (ta_IN)**, **Telugu (te_IN)**, **Thai (th_TH)**, **Tagalog (tl_XX)**, **Ukrainian (uk_UA)**, **Urdu (ur_PK)**, **Xhosa (xh_ZA)**, **Galician (gl_ES)**, **Slovene (sl_SI)**.

- **Temperature Adjustment**:
   - You can adjust the **temperature** of the content generation. A **higher temperature** makes the content more creative and varied, while a **lower temperature** generates more focused and deterministic responses.

- **Token Limit**:
   - Set the **maximum number of tokens** for content generation. This allows you to control the length of the generated educational content.

- **Auto-Generated Image Prompts**:
   - One of the unique features of FusionMind is the **auto-generated image prompts**. Even if you're not experienced in creating detailed prompts for image generation, the app will take care of this for you. It automatically converts the translated text or content into a well-defined prompt that produces more accurate and high-quality images.

---

Enjoy the multimodal experience with **FusionMind** and explore its powerful translation, content generation, and image generation features!
    """)

# Main Streamlit app
def main():
    # Sidebar Menu
    st.sidebar.title("FusionMind Options")
    page = st.sidebar.radio("Select a page:", ["Main App", "User Guide"])

    if page == "User Guide":
        show_user_guide()
        return

    st.title("🅰️ℹ️ FusionMind ➡️ Multimodal")

    # Sidebar for temperature, token adjustment, and model selection
    st.sidebar.header("Settings")
    temperature = st.sidebar.slider("Select Temperature", 0.1, 1.0, 0.7)
    max_tokens = st.sidebar.slider("Max Tokens for Content Generation", 100, 400, 200)

    # Content generation model selection
    content_model = st.sidebar.selectbox("Select Content Generation Model", list(content_models.keys()), index=0)

    # Image generation model selection
    image_model = st.sidebar.selectbox("Select Image Generation Model", list(image_generation_urls.keys()), index=0)

    # Suggested inputs
    st.write("## Suggested Inputs")
    suggestions = ["தரவு அறிவியல்", "உளவியல்", "ராக்கெட் எப்படி வேலை செய்கிறது"]
    selected_suggestion = st.selectbox("Select a suggestion or enter your own:", [""] + suggestions)

    # Input box for user
    tamil_input = st.text_input("Enter Tamil text (or select a suggestion):", selected_suggestion)

    if st.button("Generate"):
        # Step 1: Translation (Tamil to English)
        if tamil_input:
            st.write("### Translated English Text:")
            english_text = translate_text_local(tamil_input)
            if english_text:
                st.success(english_text)

                # Step 2: Generate Educational Content
                st.write("### Generated Content:")
                with st.spinner('Generating content...'):
                    content_output = generate_content(english_text, max_tokens, temperature, content_models[content_model])
                    if content_output:
                        st.success(content_output)

                # Step 3: Generate Image from the prompt (optional)
                st.write("### Generated Image:")
                with st.spinner('Generating image...'):
                    image_prompt = generate_image_prompt(english_text)
                    image_data = generate_image(image_prompt, image_generation_urls[image_model])
                    if image_data:
                        st.image(image_data, caption="Generated Image")

if __name__ == "__main__":
    main()
