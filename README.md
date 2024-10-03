# CVD Prediction Dissertation

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

## Installation

To run this project on your local machine, follow these steps:

### Prerequisites
Ensure you have the following software installed:
- **Python 3.x**: You can download it from [python.org](https://www.python.org/downloads/).
- **pip**: Python package manager (comes with Python installation).
- **Flask**: A web framework for Python. It will be installed in the next step.
- **Git**: Version control system (optional for cloning the repository).
- **wkhtmltopdf**: For PDF generation. Download from [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) and install it.

### Clone the Repository
Open your terminal or command prompt and run the following command to clone the repository:

```bash
git clone https://github.com/Varshithrthum/CVD_Prediction_Dissertation.git
cd CVD_Prediction_Dissertation
# Create a virtual environment
python -m venv venv
# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
# Install required packages from requirements.txt
pip install -r requirements.txt

running the app
python app.py

runing the tests

pytest and name of the file

ex:
pytest scenairo_testing.py

