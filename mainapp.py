import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("WYNN747/Burmese-GPT-main-sentence")
model = AutoModelForCausalLM.from_pretrained("WYNN747/Burmese-GPT-main-sentence")

# Initialize the text generation pipeline
@st.cache_resource
def load_generator():
    generator = pipeline('text-generation', model=model, tokenizer=tokenizer, device=0)
    return generator

generator = load_generator()

st.title("Generate Text")
prompt = st.text_area('Enter your prompt:', height=5)
generate_button = st.button("Generate")

max_length = st.sidebar.slider('Max length', 50, 500, step=10, value=150)
temperature = st.sidebar.slider('Temperature', 0.1, 1.0, step=0.1, value=0.7)
num_return_sequences = st.sidebar.slider('Number of return sequences', 1, 5, step=1, value=1)

if generate_button and prompt:
    with st.spinner("Generating Text.."):
        generated_texts = generator(prompt,
                                    max_length=max_length,
                                    temperature=temperature,
                                    num_return_sequences=num_return_sequences)
        for i, text in enumerate(generated_texts):
            st.write(f"Generated Text {i+1}:")
            st.write(text['generated_text'])