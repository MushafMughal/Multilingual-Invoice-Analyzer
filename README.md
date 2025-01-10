# Multilingual-Invoice-Analyzer 🖼️
Vision Analysis Pro is a powerful image analysis web application powered by Google's Gemini 1.5 Flash AI model. This application allows users to upload images and ask questions about them, receiving detailed AI-powered analysis and insights. Additionally, the second version of the application provides enhanced functionality for bulk processing of English invoices, generating processed Excel files for EDA or audit purposes.

---

## 🌟 Features

### Version 1: Image Analysis
- **Advanced Image Analysis**: Leverages Google's Gemini 1.5 Flash model for state-of-the-art image understanding.
- **Interactive Interface**: Clean and modern UI built with Streamlit.
- **Real-time Processing**: Get instant analysis of your uploaded images.
- **User-friendly Design**: Intuitive interface with smooth animations and responsive design.
- **Flexible Question Handling**: Ask any question about your uploaded image and get detailed responses.
![image](https://github.com/user-attachments/assets/c0bdff85-dd04-472c-9434-964363f56552)
![image](https://github.com/user-attachments/assets/2b6295c4-4898-4b07-8fd3-bad9dacd9039)

### Version 2: Invoice Processing
- **Bulk Invoice Processing**: Enhanced functionality to process multiple English invoices in bulk.
- **Data Extraction**: Extracts key information such as client details, company information, invoice IDs, and financial amounts.
- **Excel Output**: Generates processed Excel files for easy EDA (Exploratory Data Analysis) or audit purposes.
- **AI-Powered Refinement**: Uses AI to refine and clean extracted descriptions for better readability and accuracy.
![image](https://github.com/user-attachments/assets/01817ead-0406-404f-bc50-efc858d29c34)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Streamlit
- Google Generative AI API key
- Google Cloud credentials for Document AI (for Version 2)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/AbdulQadeer-55/Multilingual-Invoice-Analyzer.git
cd Multilingual-Invoice-Analyzer
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

### Configuration

1. Obtain a Google API key for Gemini:
   - Visit the [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy your API key

2. Update the API key in the application:
   - Open `app.py`
   - Replace `"YOUR_API_KEY"` with your actual API key

### Running the Application

1. Start the Streamlit server:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

## 🖥️ Usage

### Version 1: Image Analysis
1. **Upload an image** using the file uploader.
2. **Enter a question** about the image in the provided text area.
3. **Click the "Analyze Image" button** to get detailed insights.

### Version 2: Invoice Processing
1. **Upload an invoice file** (PDF or JPEG).
2. The application will **automatically process the file** and extract relevant data.
3. **View the processed data** in a tabular format and **download it as an Excel file**.

---

## 🛠️ Technologies Used
- **Streamlit**: For building the web application interface.
- **Google Gemini 1.5 Flash**: For advanced image analysis and text refinement.
- **Google Document AI**: For extracting structured data from invoices.
- **Pandas**: For data manipulation and Excel file generation.

---

## 📂 Project Structure
```
Multilingual-Invoice-Analyzer/
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── README.md          # Project documentation
└── .gitignore         # Git ignore file
```

## ⚠️ Important Notes

- Ensure your API key is kept secure and never commit it to version control
- The application requires an active internet connection for API calls
- Image analysis capabilities depend on the Gemini model's limitations
- Supported image formats: JPG, JPEG, PNG

For additional support or issues, please open an issue in the GitHub repository.
