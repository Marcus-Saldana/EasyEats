# Easy Eats
EasyEats is a user-friendly web application that leverages AI technology to generate personalized cooking recipes based on user-inputted ingredients, dietary restrictions, and preferences. Designed to simplify meal planning and inspire culinary creativity!
## Features
- **Custom Recipe Generation**: Input your available ingredients and get a customized recipe that matches your dietary needs and cooking time preferences.
- **Dietary Accommodations**: Supports various dietary restrictions such as Vegan, Gluten-Free, Keto, and more.
- **Cuisine Selection**: Choose from a variety of cuisines like Italian, Mexican, Asian, and others to tailor your culinary experience.
- **User-Friendly Interface**: Simple and intuitive UI that makes navigating and using the app straightforward and pleasant.
## Getting Started
### Prerequisites
What you need to install the software:
- Python 3.8 or higher
- pip (Python package installer)
### Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/easyeats.git
cd easyeats
```
2. Set up a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install required packages
```bash
pip install -r requirements.txt
```
4. Set up environment variables
- Create a ```.env``` file in the root directory of the project.
- Add the following line to your ```.env``` file:
```plaintext
GOOGLE_API_KEY='Your-Google-API-Key-Here'
```
### Running the Application
Run the application using Streamlit:
```bash
cd EasyEats
streamlit run PageControl.py
```
