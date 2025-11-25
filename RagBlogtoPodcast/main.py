# import os
# import google.generativeai as genai
# from agno.agent import Agent
# from agno.tools.eleven_labs import ElevenLabsTools
# from agno.tools.firecrawl import FirecrawlTools
# from agno.utils.audio import write_audio_to_file
# from agno.utils.log import logger
# import streamlit as st
# import uuid

# st.set_page_config(page_title="Article to Podcast Agent")
# st.title("Beginner Friendly End to End Agent")
# st.sidebar.header("API Keys")

# gemini_api_key = st.sidebar.text_input("Gemini API key", type="password")
# elevenlabs_api_key = st.sidebar.text_input("ElevenLabs API key", type="password")
# firecrawl_api_key = st.sidebar.text_input("Firecrawl API key", type="password")

# keys_provided = all([gemini_api_key, elevenlabs_api_key, firecrawl_api_key])

# url = st.text_input("Enter the blog URL", "")
# generate_button = st.button("Generate podcast", disabled=not keys_provided)

# if not keys_provided:
#     st.warning("Enter all API keys to continue")

# def generate_summary_with_gemini(text, api_key):
#     genai.configure(api_key=api_key)
#     model = genai.GenerativeModel("gemini-1.5-flash")

#     prompt = f"""
#     Convert this blog into a podcast-friendly summary under 2000 characters:

#     {text}
#     """

#     response = model.generate_content(prompt)
#     return response.text

# if generate_button:
#     os.environ["ELEVENLABS_API_KEY"] = elevenlabs_api_key
#     os.environ["FIRECRAWL_API_KEY"] = firecrawl_api_key

#     with st.spinner("Scraping blog and generating podcast..."):
#         try:
#             firecrawl = FirecrawlTools(api_key=firecrawl_api_key)

#             scraped = firecrawl.run(url)
#             blog_content = scraped.text

#             summary = generate_summary_with_gemini(blog_content, gemini_api_key)

#             eleven_agent = Agent(
#                 name="blog-to-podcast",
#                 tools=[
#                     ElevenLabsTools(
#                         voice_id="21m00Tcm4TlvDq8ikWAM",
#                         model_id="eleven_multilingual_v2",
#                         target_directory="audio_generations"
#                     )
#                 ],
#                 instructions=[
#                     "Convert this text summary into a podcast audio:",
#                     summary
#                 ]
#             )

#             result = eleven_agent.run("Generate podcast audio")

#             os.makedirs("audio_generations", exist_ok=True)

#             if result.audio:
#                 filename = f"audio_generations/podcast_{uuid.uuid4()}.wav"

#                 write_audio_to_file(
#                     audio=result.audio[0].base64_audio,
#                     filename=filename
#                 )

#                 st.success("Podcast generated!")

#                 with open(filename, "rb") as f:
#                     audio_bytes = f.read()

#                 st.audio(audio_bytes)
#                 st.download_button(
#                     label="Download Podcast",
#                     data=audio_bytes,
#                     file_name="generated_podcast.wav",
#                     mime="audio/wav"
#                 )
#             else:
#                 st.error("Audio generation failed.")

#         except Exception as e:
#             st.error(f"Error: {e}")
#             logger.error(e)


# import os
# import google.generativeai as genai
# from agno.agent import Agent
# from agno.tools.eleven_labs import ElevenLabsTools
# from firecrawl import FirecrawlApp
# from agno.utils.audio import write_audio_to_file
# from agno.utils.log import logger
# import streamlit as st
# import uuid

# st.set_page_config(page_title="Article to Podcast Agent")
# st.title("Beginner Friendly End to End Agent")
# st.sidebar.header("API Keys")

# gemini_api_key = st.sidebar.text_input("Gemini API key", type="password")
# elevenlabs_api_key = st.sidebar.text_input("ElevenLabs API key", type="password")
# firecrawl_api_key = st.sidebar.text_input("Firecrawl API key", type="password")

# keys_provided = all([gemini_api_key, elevenlabs_api_key, firecrawl_api_key])

# url = st.text_input("Enter the blog URL", "")
# generate_button = st.button("Generate podcast", disabled=not keys_provided)

# if not keys_provided:
#     st.warning("Enter all API keys to continue")

# def generate_summary_with_gemini(text, api_key):
#     genai.configure(api_key=api_key)
#     model = genai.GenerativeModel("gemini-1.5-flash")

#     prompt = f"""
#     Convert this blog into a podcast-friendly summary under 2000 characters:

#     {text}
#     """

#     response = model.generate_content(prompt)
#     return response.text

# if generate_button:
#     os.environ["ELEVENLABS_API_KEY"] = elevenlabs_api_key

#     with st.spinner("Scraping blog and generating podcast..."):
#         try:
#             firecrawl = FirecrawlApp(api_key=firecrawl_api_key)

#             result = firecrawl.scrape_url(
#                 url=url,
#                 params={"formats": ["text"]}
#             )

#             blog_content = result["text"]

#             summary = generate_summary_with_gemini(blog_content, gemini_api_key)

#             eleven_agent = Agent(
#                 name="blog-to-podcast",
#                 tools=[
#                     ElevenLabsTools(
#                         voice_id="21m00Tcm4TlvDq8ikWAM",
#                         model_id="eleven_multilingual_v2",
#                         target_directory="audio_generations"
#                     )
#                 ],
#                 instructions=[
#                     "Convert this text summary into a podcast audio:",
#                     summary
#                 ]
#             )

#             result = eleven_agent.run("Generate podcast audio")

#             os.makedirs("audio_generations", exist_ok=True)

#             if result.audio:
#                 filename = f"audio_generations/podcast_{uuid.uuid4()}.wav"

#                 write_audio_to_file(
#                     audio=result.audio[0].base64_audio,
#                     filename=filename
#                 )

#                 st.success("Podcast generated successfully!")

#                 with open(filename, "rb") as f:
#                     audio_bytes = f.read()

#                 st.audio(audio_bytes)
#                 st.download_button(
#                     label="Download Podcast",
#                     data=audio_bytes,
#                     file_name="generated_podcast.wav",
#                     mime="audio/wav"
#                 )
#             else:
#                 st.error("No audio was generated.")

#         except Exception as e:
#             st.error(f"Error: {e}")
#             logger.error(e)


# import os
# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import google.generativeai as genai
# from elevenlabs import generate, play, save
# import uuid

# st.set_page_config(page_title="Blog to Podcast Agent")
# st.title("Beginner Friendly End to End Agent")

# st.sidebar.header("API Keys")

# gemini_api_key = st.sidebar.text_input("Gemini API Key", type="password")
# elevenlabs_api_key = st.sidebar.text_input("ElevenLabs API Key", type="password")

# url = st.text_input("Enter Blog URL")

# generate_button = st.button("Generate Podcast")

# # ------------------- SCRAPER -------------------

# def extract_blog_text(url):
#     headers = {"User-Agent": "Mozilla/5.0"}
#     response = requests.get(url, headers=headers, timeout=15)

#     soup = BeautifulSoup(response.text, "html.parser")

#     # Remove scripts & styles
#     for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
#         tag.decompose()

#     text = " ".join(p.get_text() for p in soup.find_all("p"))

#     return text[:10000]  # safety limit

# # ------------------- GEMINI SUMMARY -------------------

# def summarize_with_gemini(content, api_key):
#     genai.configure(api_key=api_key)

#     model = genai.GenerativeModel("gemini-1.5-flash")

#     prompt = f"""
#     Summarize this blog for a podcast script.
#     Make it conversational.
#     Keep it under 2000 characters.

#     Blog:
#     {content}
#     """

#     response = model.generate_content(prompt)
#     return response.text

# # ------------------- ELEVENLABS AUDIO -------------------

# def generate_podcast_audio(text, api_key):
#     audio = generate(
#         api_key=api_key,
#         text=text,
#         voice="Rachel",
#         model="eleven_multilingual_v2"
#     )

#     filename = f"podcast_{uuid.uuid4()}.wav"
#     save(audio, filename)

#     return filename

# # ------------------- MAIN LOGIC -------------------

# if generate_button:

#     if not gemini_api_key or not elevenlabs_api_key:
#         st.error("Please enter both API keys")
#         st.stop()

#     if not url:
#         st.error("Enter a blog URL")
#         st.stop()

#     with st.spinner("Scraping blog..."):
#         blog_text = extract_blog_text(url)

#     with st.spinner("Summarizing using Gemini..."):
#         summary = summarize_with_gemini(blog_text, gemini_api_key)

#     with st.spinner("Generating Podcast Audio..."):
#         audio_file = generate_podcast_audio(summary, elevenlabs_api_key)

#     st.success("Podcast created successfully!")

#     with open(audio_file, "rb") as f:
#         st.audio(f.read(), format="audio/wav")

#     st.download_button(
#         label="Download Podcast",
#         data=open(audio_file, "rb").read(),
#         file_name="podcast.wav",
#         mime="audio/wav"
#     )



import requests
import streamlit as st
from bs4 import BeautifulSoup
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from elevenlabs import save


# ------------------ BLOG SCRAPER ------------------
def scrape_blog(url):
    response = requests.get(url, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.find_all("p")
    text = " ".join([p.text for p in paragraphs])

    return text


# ------------------ GEMINI SUMMARIZER ------------------
def summarize_with_gemini(text, api_key):
    genai.configure(api_key=api_key)

    # THIS MODEL WORKS WITH YOUR API VERSION
    model = genai.GenerativeModel("models/gemini-1.0-pro")

    prompt = f"""
    Summarize the following blog into a podcast script.
    Limit it under 2000 characters.
    Make it clear, simple and engaging.

    Blog content:
    {text}
    """

    response = model.generate_content(prompt)

    return response.text


# ------------------ ELEVENLABS AUDIO ------------------
def generate_audio(summary, eleven_api_key):
    client = ElevenLabs(api_key=eleven_api_key)

    audio = client.text_to_speech.convert(
        voice_id="21m00Tcm4TlvDq8ikWAM",   # Rachel voice
        model_id="eleven_multilingual_v2",
        text=summary
    )

    filename = "podcast.wav"
    save(audio, filename)

    return filename


# ------------------ STREAMLIT APP ------------------

st.set_page_config(page_title="Blog to Podcast AI")

st.title("🎙️ Blog to Podcast Generator (Gemini + ElevenLabs)")

st.sidebar.header("API Keys")

gemini_key = st.sidebar.text_input("Gemini API Key", type="password")
eleven_key = st.sidebar.text_input("ElevenLabs API Key", type="password")

url = st.text_input("Enter Blog URL")

if st.button("Generate Podcast"):

    if not gemini_key or not eleven_key:
        st.error("❌ Please provide both API keys")
        st.stop()

    if not url.strip():
        st.error("❌ Enter a valid blog URL")
        st.stop()

    with st.spinner("🔍 Scraping blog..."):
        blog_text = scrape_blog(url)

    with st.spinner("🧠 Summarizing with Gemini..."):
        summary = summarize_with_gemini(blog_text, gemini_key)

    st.subheader("📜 Podcast Script")
    st.write(summary)

    with st.spinner("🎧 Generating Audio..."):
        audio_file = generate_audio(summary, eleven_key)

    st.success("✅ Podcast Generated Successfully!")

    with open(audio_file, "rb") as f:
        audio_bytes = f.read()

    st.audio(audio_bytes, format="audio/wav")

    st.download_button(
        "Download Podcast",
        data=audio_bytes,
        file_name="podcast.wav"
    )


