import streamlit as st
from pathlib import Path 
import google.generativeai as genai

from api_key import api_key

#configure genai with key
genai.configure(api_key=api_key)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

system_prompt="""

As a highly skilled medical pratitioner specializing in image analysis,you are tasked with examining medicsl images for a renowned hospital.Your expertise is crucial in identifying any anomalies,diseases,or issues that may be present in the images.

Your Responsibilities include:

1.Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal features.
2.Findings Report: Document all observed anomalies or signs of disease. Clearly articulate your findings.
3.Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further testing or consultations.
4.Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:

1.Scope of Response: Only respond if the image pertains to human health issues.
2.Clarity of Image: In cases where the image quality impedes clear analysis, note that certain details may be inconclusive.
3.Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions. 
4.Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis carefully."

Please provide me an output response with these 4 headings

"""
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

st.set_page_config(page_title="MedInsight",page_icon=":robot:")

st.image("logo.jpg",width=120)

st.title("MedInsights")

st.subheader("An Application That Can Help To Analyze Medical Images!")

uploaded_file=st.file_uploader("Upload The Image For Analysis",type=["png","jpg","jpeg"])
if uploaded_file:
    st.image(uploaded_file,width=300,caption="Uploaded Image")
submit_button=st.button("Generate The Analysis")

if submit_button:
    #process the uploaded image
    image_data=uploaded_file.getvalue()

    image_parts=[
        {
            "mime_type":"image/jpeg",
            "data":image_data
        },
    ]
    #making prompt ready
    prompt_parts=[

        image_parts[0],
        system_prompt,
    ]
    
    st.image(image_data,width=250)
    

    st.title("Here Is The Analysis Based On Your Image:")

    #generate response
    response=model.generate_content(prompt_parts)
    print(response.text)

    st.write(response.text)
    



