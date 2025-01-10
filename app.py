import streamlit as st
import os
import pathlib
from PIL import Image
from streamlit_option_menu import option_menu 
import google.generativeai as genai
import pandas as pd
from google.cloud import documentai_v1 as documentai
import os
import pathlib
import textwrap
from IPython.display import display
from IPython.display import Markdown
from tempfile import NamedTemporaryFile


def init_styles():
    st.markdown("""
        <style>
        /* Modern color palette */
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --secondary: #ec4899;
            --accent: #8b5cf6;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --background: #f8fafc;
            --text: #1e293b;
            --text-light: #64748b;
        }

        /* Base styles with smooth scrolling */
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
        }
        
        /* Animated gradient background for header */
        .stApp header {
            background: linear-gradient(-45deg, #6366f1, #ec4899, #8b5cf6, #6366f1);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Modern glass morphism container */
        .glass-container {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 2rem;
            box-shadow: 
                0 4px 6px -1px rgba(0, 0, 0, 0.1),
                0 2px 4px -1px rgba(0, 0, 0, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.7);
        }
        
        /* Floating card effect */
        .content-container {
            background: white;
            border-radius: 16px;
            padding: 0.5rem;
            margin: 1rem 0;
            box-shadow: 
                0 10px 15px -3px rgba(0, 0, 0, 0.1),
                0 4px 6px -2px rgba(0, 0, 0, 0.05);
            transform: translateY(0);
            transition: all 0.3s ease;
        }
        
        .content-container:hover {
            transform: translateY(-5px);
            box-shadow: 
                0 20px 25px -5px rgba(0, 0, 0, 0.1),
                0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        
        /* Modern button design */
        .stButton > button {
            width: 100%;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            letter-spacing: 0.025em;
            text-transform: uppercase;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 12px -1px rgba(99, 102, 241, 0.5);
        }
        
        /* Animated file uploader */
        [data-testid="stFileUploader"] {
            border: 2px dashed var(--primary);
            border-radius: 16px;
            padding: 2rem;
            background: #eef2ff;
            transition: all 0.3s ease;
        }
        
        [data-testid="stFileUploader"]:hover {
            border-color: var(--secondary);
            background: #fdf2f8;
            transform: scale(1.01);
        }
        
        /* Modern input fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border-radius: 12px;
            border: 2px solid #e2e8f0;
            padding: 1rem;
            transition: all 0.3s ease;
            font-size: 1rem;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }
        
        /* Typography */
        h1, h2, h3 {
            color: var(--text);
            font-family: 'Inter', sans-serif;
            letter-spacing: -0.025em;
        }
        
        h1 { 
            font-size: 3rem; 
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        
        h2 { font-size: 2.25rem; }
        h3 { font-size: 1.5rem; }
        
        /* Feature cards with hover effects */
        .feature-card {
            background: white;
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            height: 100%;
            position: relative;
            overflow: hidden;
            transition: all 0.5s ease;
            border: 1px solid #e2e8f0;
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            opacity: 0;
            transition: all 0.5s ease;
            z-index: 1;
        }
        
        .feature-card:hover::before {
            opacity: 0.1;
        }
        
        .feature-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 
                0 20px 25px -5px rgba(0, 0, 0, 0.1),
                0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1.5rem;
            display: block;
            transform: scale(1);
            transition: transform 0.3s ease;
        }
        
        .feature-card:hover .feature-icon {
            transform: scale(1.1);
        }
        
        /* Success/Error messages with animations */
        .stSuccess, .stError {
            border-radius: 12px;
            padding: 1rem;
            animation: slideIn 0.5s ease;
        }
        
        @keyframes slideIn {
            from {
                transform: translateY(-10px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        .stSuccess {
            background: #ecfdf5;
            border: 1px solid var(--success);
            color: #065f46;
        }
        
        .stError {
            background: #fef2f2;
            border: 1px solid var(--error);
            color: #991b1b;
        }
        
        /* Loading spinner animation */
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .stSpinner {
            text-align: center;
            padding: 2rem;
            color: var(--primary);
        }
        
        /* Footer with gradient */
        .footer {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            border-radius: 24px 24px 0 0;
            margin-top: 4rem;
        }
        
        .footer p {
            margin: 0.5rem 0;
            opacity: 0.9;
            font-size: 0.875rem;
            letter-spacing: 0.025em;
        }
        
        /* Image preview container */
        .image-preview {
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        
        .image-preview:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 12px -1px rgba(0, 0, 0, 0.1);
        }
        
        /* Smooth scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--primary);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--primary-dark);
        }
        </style>
    """, unsafe_allow_html=True)

main_df_columns = ["CLIENT", "COMPANY", "DESCRIPTION", "INVOICE_ID", "NET_AMOUNT", "VAT_AMOUNT", "TOTAL_AMOUNT"]
# Initialize session state for 'main_df' if it doesn't exist
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = pd.DataFrame(columns=main_df_columns)  # Initialize as an empty DataFrame


def refine_description(description):

  model = genai.GenerativeModel(model_name='gemini-1.5-flash')
  safe = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]


  response = model.generate_content(
      f"""This text contains descriptions of items extracted from an invoice. Each new item description is comma separated. Although this is not necessary that after comma there must be information for new item, it can be contain extra info comma seprated so you have to double check if its item or some other stuff. A description can contain single item name or multiple item name. Each description have noises like \n or irrelevant text etc. In most cases text coming after \n is not about item name but its about item information and other stuff which is irrelevant for us. So check if you find potential item name after \n take it otherwise ignore it.
  For each item description, identify the most likely name of the item. The item name can be a single word or a phrase. Give me only the name form it, I dont want any explanation. and if there are multiple name give me in single line comma separated.
  NOTE: DOUBLE CHECK IF YOU ARE MISSING ANY ITEM NAME OR NOT. IF YES THEN MUST ADD IT.

  {description}
  """, safety_settings= safe)

  # Strip and split the text to remove any newline characters
  cleaned_response = " ".join(response.text.split())

  return cleaned_response

def convert_amount(raw_value):
    if ('.' not in raw_value and ',' in raw_value ) and (raw_value.count(',') == 1):
        if len(raw_value.split(',')[1]) == 3:
            raw_value = raw_value.replace(',', '')
        else:
            raw_value = raw_value.replace(',', '.')
    elif ('.' in raw_value and ',' in raw_value ) and (raw_value.find(',') > raw_value.find('.')):
        raw_value = raw_value.replace('.', '').replace(',', '.')
    else:
        raw_value = raw_value.replace(',', '')

    try:
        return float(raw_value)
    except ValueError:
        return None

def extract_and_insert(api_df):
    # Define the mapping of the types to our main dataframe columns
    type_to_columns = {
        "CLIENT": ["receiver_name", "ship_to_name","ship_to_address","remit_to_name"],
        "COMPANY": ["supplier_name","company"],
        "DESCRIPTION": ["line_item/description"],
        "INVOICE_ID": ["invoice_id"],
        "NET_AMOUNT": ["net_amount"],
        "VAT_AMOUNT": ["vat/tax_amount","total_tax_amount"],
        "TOTAL_AMOUNT": ["total_amount"]
    }

    # Create a dictionary to hold the values
    new_data = {col: None for col in main_df_columns}

    # Iterate through the API dataframe
    for _, row in api_df.iterrows():
        type_ = row["Type"]
        raw_value = row["Raw Value"]

        # Check which column the type matches
        for column_name, types in type_to_columns.items():
            if type_ in types:
                if column_name == "DESCRIPTION":
                    if new_data[column_name]:
                        new_data[column_name] += ", " + refine_description(raw_value)
                    else:
                        new_data[column_name] = refine_description(raw_value)
                elif new_data[column_name] is None:
                    if column_name in ["NET_AMOUNT", "VAT_AMOUNT", "TOTAL_AMOUNT"]:
                        new_data[column_name] = convert_amount(raw_value)
                    else:
                        new_data[column_name] = raw_value

    # Special handling for multiple types
    for col_name in ["CLIENT", "COMPANY", "VAT_AMOUNT"]:
        if new_data[col_name] is None:
            for type_ in type_to_columns[col_name]:
                match = api_df[api_df["Type"] == type_]
                if not match.empty:
                    new_data[col_name] = match.iloc[0]["Raw Value"]
                    break

    # Calculate VAT_amount if not found
    if new_data["VAT_AMOUNT"] is None:
        net_amount = new_data["NET_AMOUNT"]
        total_amount = new_data["TOTAL_AMOUNT"]
        if net_amount is not None and total_amount is not None:
            new_data["VAT_AMOUNT"] = total_amount - net_amount

    # Calculate Total_amount if not found
    if new_data["TOTAL_AMOUNT"] is None:
        net_amount = new_data["NET_AMOUNT"]
        vat_amount = new_data["VAT_AMOUNT"]
        if net_amount is not None and vat_amount is not None:
            new_data["TOTAL_AMOUNT"] = net_amount + vat_amount

    # Append the new data to the main dataframe
    st.session_state['main_df'].loc[len(st.session_state['main_df'])] = new_data

    return st.session_state['main_df']

def get_gemini_response(input_text, image, prompt):
    genai.configure(api_key='AIzaSyAafhNET6vH1Fn1NQaKGPGBiDU00g4WymQ')
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    raise FileNotFoundError("No file uploaded")


def display_features():
    cols = st.columns(3)
    
    features = [
        {
            "icon": "🧠",
            "title": "AI-Powered Analysis",
            "description": "Advanced image understanding with Gemini 1.5 Flash technology"
        },
        {
            "icon": "⚡",
            "title": "Instant Results",
            "description": "Get detailed insights about your images in seconds"
        },
        {
            "icon": "🎯",
            "title": "Precise Insights",
            "description": "Accurate and detailed analysis for any type of image"
        }
    ]
    
    for col, feature in zip(cols, features):
        with col:
            st.markdown(f"""
                <div class="feature-card">
                    <span class="feature-icon">{feature['icon']}</span>
                    <h3 style="font-size: 1.25rem; margin: 1rem 0;">{feature['title']}</h3>
                    <p style="color: var(--text-light);">{feature['description']}</p>
                </div>
            """, unsafe_allow_html=True)

def main():    
    init_styles()
    
    st.markdown("""
        <div style="text-align: center; padding: 3rem 0;">
            <h1>Vision Analysis Pro</h1>
            <p style="font-size: 1.25rem; color: var(--text-light); max-width: 600px; margin: 0 auto;">
                Unlock the power of AI vision analysis with our cutting-edge platform
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        selected = option_menu(menu_title=None,options=["Version 1","Version 2"],orientation='horizontal',
                    styles={
                        "nav-link": {"--hover-color": "#ca4fae9e"}, 
                        "nav-link-selected": {"background-color": "#ca4fae"}
                        })
        
        if selected == "Version 1":
            
            cols = st.columns([1, 1])
            
            with cols[0]:
                with st.container():
                    st.markdown('<div class="content-container">', unsafe_allow_html=True)
                    st.markdown("""
                        <h3 style="display: flex; align-items: center; gap: 0.5rem;">
                            📸 Upload Image
                        </h3>
                    """, unsafe_allow_html=True)
                    uploaded_file = st.file_uploader(
                        "Drop your image here or click to browse",
                        type=["jpg", "jpeg", "png"],
                        help="Supported formats: JPG, JPEG, PNG"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with st.container():
                    st.markdown('<div class="content-container">', unsafe_allow_html=True)
                    st.markdown("""
                        <h3 style="display: flex; align-items: center; gap: 0.5rem;">
                            💭 Ask Question
                        </h3>
                    """, unsafe_allow_html=True)
                    input_text = st.text_area(
                        "",
                        placeholder="What would you like to know about this image?",
                        height=100
                    )
                    analyze_button = st.button("✨ Analyze Image")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with cols[1]:
                st.markdown('<div class="content-container">', unsafe_allow_html=True)
                st.markdown("""
                    <h3 style="display: flex; align-items: center; gap: 0.5rem;">
                        🔍 Analysis Results
                    </h3>
                """, unsafe_allow_html=True)
                
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    st.markdown('<div class="image-preview">', unsafe_allow_html=True)
                    st.image(image, caption="", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if analyze_button and uploaded_file and input_text:
                    try:
                        with st.spinner("🤔 Analyzing your image..."):
                            image_data = input_image_setup(uploaded_file)
                            input_prompt = """
                            You are an expert in analyzing images and providing detailed, insightful responses.
                            Please analyze the provided image and answer the question thoughtfully.
                            """
                            response = get_gemini_response(input_prompt, image_data, input_text)
                            st.success("✨ Analysis Complete!")
                            st.markdown(f">{response}")
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <h2 style="text-align: center; margin-bottom: 2rem;">
                    ✨ Features
                </h2>
            """, unsafe_allow_html=True)
            display_features()
            
            st.markdown("""
                <div class="footer">
                    <p>© 2024: Gimini Vision Pro Leveraged. All rights reserved.</p>
                    <p>
                    <p>Created by Mushaf Sibtain</p>
                </div>
            """, unsafe_allow_html=True)

    if selected == "Version 2":

        genai.configure(api_key='AIzaSyAafhNET6vH1Fn1NQaKGPGBiDU00g4WymQ')
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'flash-freehold-444814-q8-4b0bb8c06184.json'

        def online_process(
            project_id: str,
            location: str,
            processor_id: str,
            file_path: str,
            mime_type: str,
        ) -> documentai.Document:
            """
            Processes a document using the Document AI Online Processing API.
            """

            opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}

            # Instantiates a client
            documentai_client = documentai.DocumentProcessorServiceClient(client_options=opts)

            # The full resource name of the processor, e.g.:
            # projects/project-id/locations/location/processor/processor-id
            # You must create new processors in the Cloud Console first
            resource_name = documentai_client.processor_path(project_id, location, processor_id)

            # Read the file into memory
            with open(file_path, "rb") as file:
                file_content = file.read()

            # Load Binary Data into Document AI RawDocument Object
            raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)

            # Configure the process request
            request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

            # Use the Document AI client to process the sample form
            result = documentai_client.process_document(request=request)

            return result.document


        PROJECT_ID = "flash-freehold-444814-q8"
        LOCATION = "us"  # Format is 'us' or 'eu'
        PROCESSOR_ID = "11c46f109eb2cdcd"  # Create processor in Cloud Console

        # Streamlit app for uploading invoice files
        st.title("Invoice File Processor")

        # File uploader for invoices
        uploaded_file = st.file_uploader(
            "Upload your invoice file (PDF or JPEG)", 
            type=["pdf", "jpg", "jpeg"]
        )

        if uploaded_file is not None:
            # Determine MIME type based on file extension
            if uploaded_file.type == "application/pdf":
                MIME_TYPE = "application/pdf"
            elif uploaded_file.type in ["image/jpeg", "image/jpg"]:
                MIME_TYPE = "image/jpeg"
            else:
                st.error("Unsupported file type!")
                st.stop()

            # Save the uploaded file to a temporary location
            with NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name  # Get the temporary file path

            # Process the file using the online_process function
            document = online_process(
                project_id=PROJECT_ID,
                location=LOCATION,
                processor_id=PROCESSOR_ID,
                file_path=temp_file_path,
                mime_type=MIME_TYPE,
            )

            types = []
            raw_values = []
            normalized_values = []
            confidence = []

            # Grab each key/value pair and their corresponding confidence scores.
            for entity in document.entities:
                types.append(entity.type_)
                raw_values.append(entity.mention_text)
                normalized_values.append(entity.normalized_value.text)
                confidence.append(f"{entity.confidence:.0%}")

                # Get Properties (Sub-Entities) with confidence scores
                for prop in entity.properties:
                    types.append(prop.type_)
                    raw_values.append(prop.mention_text)
                    normalized_values.append(prop.normalized_value.text)
                    confidence.append(f"{prop.confidence:.0%}")

            # Create a Pandas Dataframe to print the values in tabular format.
            df = pd.DataFrame(
                {
                    "Type": types,
                    "Raw Value": raw_values,
                    "Normalized Value": normalized_values,
                    "Confidence": confidence,
                }
            )

            # Extract and insert new data
            new_data = extract_and_insert(df)

            # Display the DataFrame
            st.dataframe(new_data)


if __name__ == "__main__":
    main()
