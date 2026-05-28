import streamlit as st
import subprocess
import os
from groq import Groq
from datetime import datetime

st.set_page_config(page_title="AI Content Studio", layout="wide")
st.title("🎬 Personal AI Content Studio")
st.subheader("Multi-Agent Video Editor + Smart Distribution")

# Sidebar
st.sidebar.header("Settings")
groq_key = st.sidebar.text_input("Groq API Key", type="password", help="Get free key from groq.com")
if groq_key:
    client = Groq(api_key=groq_key)

uploaded_file = st.file_uploader("Upload Raw Video", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file:
    input_path = "input_video.mp4"
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Video Uploaded Successfully!")
    st.video(input_path)

    if st.button("🚀 Run Full AI Pipeline", type="primary", use_container_width=True):
        with st.spinner("Multiple AI Agents are working together..."):
            progress_bar = st.progress(0)
            status_text = st.empty()

            final_output = "final_ai_edited_video.mp4"

            # === Agent 1: Sound Enhancement ===
            status_text.info("🔊 Sound Enhancement Agent Running...")
            cmd = [
                'ffmpeg', '-y', '-i', input_path,
                '-af', 'highpass=f=150,lowpass=f=4000,acompressor=threshold=-18dB:ratio=8:attack=5:release=60:makeup=6dB,loudnorm=I=-16:TP=-1.5',
                '-c:v', 'libx264', '-c:a', 'aac', '-b:a', '192k',
                final_output
            ]
            subprocess.run(cmd, capture_output=True)
            progress_bar.progress(40)

            # === Agent 2: Coordinator (LLM) ===
            status_text.info("🧠 Coordinator Agent Analyzing...")
            try:
                prompt = "Act as a professional YouTube content strategist. Give short, useful advice for this video."
                response = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                advice = response.choices[0].message.content
                st.info(f"**Coordinator Agent Advice:** {advice[:400]}...")
            except:
                st.warning("LLM Agent skipped (check Groq key)")
            progress_bar.progress(70)

            # === Final Result ===
            progress_bar.progress(100)
            status_text.success("✅ All Agents Completed Successfully!")

            if os.path.exists(final_output):
                st.video(final_output)

                st.divider()
                st.subheader("📤 Distribution Hub")

                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    with open(final_output, "rb") as f:
                        st.download_button("⬇️ Download Video", f, "AI_Edited_Video.mp4", mime="video/mp4")

                with col2:
                    st.markdown("**YouTube** Ready")
                    st.caption("Upload directly to YouTube Studio")

                with col3:
                    whatsapp_text = "Hey! Check out my new video 👇"
                    st.markdown(f"[📱 Send to WhatsApp](https://wa.me/?text={whatsapp_text}%0A)", unsafe_allow_html=True)

                with col4:
                    st.markdown("**Telegram**")
                    st.caption("Download & Send")

                # Email Template
                st.divider()
                st.subheader("📧 Email Ready")
                subject = f"New Video - {datetime.now().strftime('%B %d, %Y')}"
                body = f"""Hi everyone,

I just published a new video!

Check it out here: [Watch Video]

Best regards,
Sumon"""

                st.text_input("Subject", value=subject)
                st.text_area("Email Body", value=body, height=150)

st.caption("Personal Multi-Agent AI Content Studio | Video + Distribution")
