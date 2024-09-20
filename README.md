**TransArt: A Multimodal Application for Vernacular Language Translation and Image Synthesis**

**Overview**

This is my 5th project.The **TransArt Project** is designed to demonstrate the integration of language translation and creative AI by converting Tamil text into English and generating relevant Text content and images based on the translated content. This project showcases how deep learning, transformers, and Hugging Face models can be used to bridge the gap between language processing and visual content generation.

**Skills Gained**

- Deep Learning
- Transformer Models
- Hugging Face APIs
- Streamlit Web Applications
- Python Programming

**Problem Statement**
TransArt aims to develop a user-friendly, web-based application that can:
1. Translate text from Tamil to English using a neural machine translation model.
2. Produce creative written content based on the translated text
3. Generate images based on the translated English text using a text-to-image model.Enriching multimedia offerings.

**Objective**
To deploy a pre-trained or fine-tuned model using **Hugging Face Spaces**, making it accessible through a web application built with **Streamlit**.

**Business Use Cases**

- **Educational Tools**: Enhance learning by combining translated text with relevant images for better understanding.
- **Creative Content Generation**: Streamline the creation of visual content for digital marketing, presentations, or educational materials.

**Approach**

**Model Selection**

- **Translation Model**:
  ***For Translation I have researched 5 models out of that I have concluded one model***
  [facebook/mbart-large-50-many-to-one-mmt](https://huggingface.co/facebook/mbart-large-50-many-to-one-mmt) for Tamil to English translation.
  
- **Content and image prompt generation model**:
  ***For this I have tried and applied 4 different model You can choose the model as per your preference and i have provide the link for Groq you can find the model used in documentation***
  [Groq API](https://console.groq.com/playground)
  
- **Image Generation Model**:
  ***For this I have tried and applied 3 different model You can choose the model as per your preference you can find the model used in documentation***
  [FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell) for generating images from the translated English text.

**Application Development**

- **Frontend**: Built with Streamlit to provide an interactive user interface.
- **Backend**: Powered by Hugging Face APIs for translation and image generation and for content and prompt generation I have used a models through Groq API.

**Deployment**
- Deployed on **Hugging Face Spaces**, offering a scalable, accessible web-based solution.

**Features**

- **Text Translation**: Translates Tamil input into English using a neural machine translation model.
- **Image Generation**: Automatically generates images based on the translated text using a pre-trained text-to-image model.
- **Creative Text Generation**: Produces English creative text that complements the visual output.

**Results**
- **Functional Web Application**: Provides a seamless, user-friendly interface for translation,content and image generation.
- **Scalable Deployment**: Easily deployable and scalable through Hugging Face Spaces.
  
## App Link

[FusionMind-Multimodel](https://huggingface.co/spaces/Santhosh1325/FusionMind_TransArt_V2)
