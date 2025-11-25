# import os
# from agno.agent import Agent
# from agno.models.openai import OpenAIChat
# from agno.tools.eleven_labs import ElevenLabsTool
# from agno.tools.firecrawl import FirecrawlTools
# from agno.types.run import RunOutput
# from agno.utils.audio import write_audio_to_file
# from agno.utils.log import logger
# import streamlit as st
# import uuid

# st.set_page_config(page_title="Article to Podcast Agent");
# st.title("Beginner Friendly End to End Agent")
# st.sidebar.header("API keys")

# openai_api_key = st.sidebar.text_input("OpenAI API key", type="password")
# elevenlabs_api_key = st.sidebar.text_input("elevenlabs API key", type="password")
# firecrawl_api_key = st.sidebar.text_input("firecrawl API key", type="password")

# keys_provided = all([openai_api_key,elevenlabs_api_key,firecrawl_api_key])

# url = st.text_input("Enter the URL of the site","")
# generate_button = st.button("Generate podcast",disabled=not keys_provided)

# if not keys_provided:
#     st.warning("Please enter all keys to proceed")

# if generate_button:
#     if url.strip() == "":
#         st.warning("Please enter a blog/post/article url")
#     else:
#         os.environ["OPENAI_API_KEY"] = openai_api_key
#         os.environ["ELEVENLABS_API_KEY"] = elevenlabs_api_key
#         os.environ["FIRECRAWL_API_KEY"] = firecrawl_api_key
        
#         with st.spinner("Processing.....Scarping blog, sumarizing and generatinf podcast!"):
#             try: 
#                 blog_to_podcast_agent = Agent(
#                     name="blog to podcast Agent",
#                     agent_id="blog_to_podcast_agent",
#                     model=OpenAIChat(id="gpt-3.5-turbo"),
#                     tools=[
#                         ElevenLabsTool(
#                             voice_id="ytfieobdisjnoitjndi",
#                             model_id="eleven_multilingual_v2",
#                             target_directory="audio_generations"
#                         ),
#                         FirecrawlTools(),
#                     ],
#                     description="You are AI agent that can generate audio using the ElevenLabs API.",
#                     instructions=[
#                         "When the user provide a blog post URL:",
#                         "1.Use FireCrawlTools to script the blog content",
#                         "2.Create a concise summary of the blog content that is NO MORE than 2000 characters long",
#                         "3.The summary should capture the main points while engaging and conversational."
#                         "4.Use the ElevenLabsTools to convert the summary to audio",
#                         "Ensure the summary is within the 2000 character limit to avoid ElevenLabs API limits."
#                     ],
#                     markdown=True,
#                     debug_mode=True
#                 )
                
#                 podcast: RunOutput = blog_to_podcast_agent.run(
#                     f"Convert the blog content to a podcast: {url}"
#                 )
#                 save_dir = "audio_generations"
#                 os.makedirs(save_dir,exist_ok=True)

#                 if podcast.audio and len(podcast.audio) > 0:
#                     filename = f"{save_dir}/podcast_{uuid.uuid4()}.wav"
#                     write_audio_to_file(
#                         audio=podcast.audio[0].base64_audio,
#                         filename=filename
#                     )
#                     st.success("Podcast generated successfully!")
#                     audio_bytes = open(filename,"rb").read()

#                     st.audio(audio_bytes, format="audio/wav")
#                     st.download_button(
#                         label ="Download Podcast",
#                         data=audio_bytes,
#                         file_name="generated_podcast.wav",
#                         mime="audio/wav"
#                     )
#                 else:
#                     st.error("No audio was generated. Please try again.")
            
#             except Exception as e:
#                 st.error(f"An error occured:{e}")
#                 logger.error(f"Streamlit app error: {e}")

import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.eleven_labs import ElevenLabsTools
from agno.tools.firecrawl import FirecrawlTools
# from agno.types.run import RunOutput
from agno.utils.audio import write_audio_to_file
from agno.utils.log import logger
import streamlit as st
import uuid

st.set_page_config(page_title="Article to Podcast Agent")
st.title("Beginner Friendly End to End Agent")
st.sidebar.header("API keys")

openai_api_key = st.sidebar.text_input("OpenAI API key", type="password")
elevenlabs_api_key = st.sidebar.text_input("ElevenLabs API key", type="password")
firecrawl_api_key = st.sidebar.text_input("Firecrawl API key", type="password")

keys_provided = all([openai_api_key, elevenlabs_api_key, firecrawl_api_key])

url = st.text_input("Enter the URL of the site", "")
generate_button = st.button("Generate podcast", disabled=not keys_provided)

if not keys_provided:
    st.warning("Please enter all keys to proceed")

if generate_button:
    if url.strip() == "":
        st.warning("Please enter a blog/post/article URL")
    else:
        os.environ["OPENAI_API_KEY"] = openai_api_key
        os.environ["ELEVENLABS_API_KEY"] = elevenlabs_api_key
        os.environ["FIRECRAWL_API_KEY"] = firecrawl_api_key
        
        with st.spinner("Processing... Scraping blog, summarizing and generating podcast!"):
            try: 
                blog_to_podcast_agent = Agent(
                    name="blog-to-podcast-agent",
                    # agent_id="blog_to_podcast_agent",
                    model=OpenAIChat(id="gpt-4o-mini"),
                    tools=[
                        ElevenLabsTools(
                            voice_id="21m00Tcm4TlvDq8ikWAM",
                            model_id="eleven_multilingual_v2",
                            target_directory="audio_generations"
                        ),
                        FirecrawlTools(),
                    ],
                    description="You are an AI agent that generates podcast audio from blog posts.",
                    instructions=[
                        "When the user provides a blog post URL:",
                        "1. Use FirecrawlTools to scrape the blog content.",
                        "2. Summarize it into under 2000 characters.",
                        "3. Keep the summary engaging and podcast friendly.",
                        "4. Convert the summary into audio using ElevenLabs."
                    ],
                    markdown=True,
                    debug_mode=True
                )

                podcast = blog_to_podcast_agent.run(
                    f"Convert the blog content to a podcast: {url}"
                )

                save_dir = "audio_generations"
                os.makedirs(save_dir, exist_ok=True)

                if podcast.audio:
                    filename = f"{save_dir}/podcast_{uuid.uuid4()}.wav"
                    
                    write_audio_to_file(
                        audio=podcast.audio[0].base64_audio,
                        filename=filename
                    )

                    st.success("Podcast generated successfully!")
                    
                    with open(filename, "rb") as f:
                        audio_bytes = f.read()

                    st.audio(audio_bytes, format="audio/wav")
                    st.download_button(
                        label="Download Podcast",
                        data=audio_bytes,
                        file_name="generated_podcast.wav",
                        mime="audio/wav"
                    )
                else:
                    st.error("No audio was generated. Please try again.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
                logger.error(f"Streamlit app error: {e}")

