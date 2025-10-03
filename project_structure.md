# 🌱 CropGuard AI - Complete Project Structure

## 📁 File Organization

```
cropguard-ai/
├── backend/
│   ├── main.py                 # Main FastAPI application
│   ├── config.py              # Configuration settings
│   ├── models/
│   │   ├── __init__.py        # Models package init
│   │   ├── disease_db.py      # Disease and pesticide database
│   │   └── ai_engine.py       # AI detection engine
│   ├── api/
│   │   ├── __init__.py        # API package init
│   │   ├── routes.py          # API route handlers
│   │   └── utils.py           # Utility functions
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── index.html             # Main HTML file
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css     # Stylesheet
│   │   ├── js/
│   │   │   └── app.js         # JavaScript functionality
│   │   └── images/            # Static images
├── scripts/
│   ├── start.sh               # Startup script
│   ├── demo.py                # Demo and testing script
│   └── install.sh             # Installation script
├── docs/
│   ├── README.md              # Main documentation
│   ├── FEATURES.md            # Feature overview
│   └── API_DOCS.md            # API documentation
└── tests/
    ├── test_api.py            # API tests
    └── test_frontend.py       # Frontend tests
```