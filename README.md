# Ethiopian Medical Data Warehouse

This project scrapes Ethiopian medical business data from **Telegram channels**, cleans and processes the data, stores it in a **data warehouse**, and applies **object detection using YOLO** for image analysis.

## 📌 Features
- ✅ **Telegram Bot Scraper** - Extracts messages and images from public channels
- ✅ **Data Cleaning & Transformation** - Processes scraped data for consistency
- ✅ **Object Detection with YOLO** - Detects relevant objects in images
- ✅ **Data Warehouse Integration** - Stores structured data for analysis
- ✅ **Logging & Monitoring** - Tracks scraping activity

---

## 📂 Project Structure
```
📂 ethiopian_medical_business_scraper
│── 📂 data_scraper
│   │── bot_scraper.py       # Scrapes Telegram messages
│   │── image_scraper.py     # Downloads images
│   │── config.py            # Stores API keys
│   │── logging_config.py    # Logging setup
│
│── 📂 data_processing
│   │── clean_data.py        # Cleans and transforms data
│   │── process_images.py    # Prepares images for YOLO
│
│── 📂 object_detection
│   │── yolo_detection.py    # YOLO object detection
│   │── model_config.py      # YOLO settings
│
│── 📂 data_warehouse
│   │── database_setup.py    # Sets up database
│   │── insert_data.py       # Inserts cleaned data into DB
│
│── 📂 utils
│   │── helpers.py           # Utility functions
│   │── constants.py         # Stores channel names
│
│── 📂 logs
│   │── scraper.log          # Logs scraping activity
│
│── 📂 data
│   │── raw/
│   │   │── messages.json    # Raw scraped messages
│   │   │── images/         # Downloaded images
│   │── cleaned/
│   │   │── cleaned_data.csv # Processed data
│
│── requirements.txt         # Dependencies
│── README.md                # Project documentation
│── .gitignore               # Ignore unnecessary files
```

---

## 🔧 Installation
### 1️⃣ **Clone the repository**
```bash
git clone https://github.com/your-username/ethiopian_medical_business_scraper.git
cd ethiopian_medical_business_scraper
```

### 2️⃣ **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 3️⃣ **Install dependencies**
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage
### **1️⃣ Set Up Telegram Bot**
- Go to Telegram and search for `BotFather`
- Type `/newbot` and follow the instructions
- Copy the **Bot Token** and paste it in `config.py`

### **2️⃣ Run the Telegram Scraper**
```bash
python data_scraper/bot_scraper.py
```

### **3️⃣ Process & Clean the Data**
```bash
python data_processing/clean_data.py
```

### **4️⃣ Run Object Detection (YOLO)**
```bash
python object_detection/yolo_detection.py
```

### **5️⃣ Insert Data into Database**
```bash
python data_warehouse/insert_data.py
```

---

## ⚙️ Configuration
Store API credentials in `config.py`:
```python
BOT_TOKEN = "your-telegram-bot-token"
DATABASE_URL = "sqlite:///data/medical_data.db"
```

---

## 🛠 Dependencies
- **Python 3.8+**
- **Telethon** (For Telegram scraping)
- **Pandas** (Data processing)
- **SQLite/PostgreSQL** (Database)
- **YOLOv5** (Object detection)

Install all dependencies using:
```bash
pip install -r requirements.txt
```

---

## 🔍 Logs & Monitoring
All logs are stored in `logs/scraper.log`. You can monitor scraping progress here.

---

## 🤝 Contribution
Feel free to submit **pull requests** or report issues! 🚀

---

## 📝 License
This project is licensed under the **MIT License**.