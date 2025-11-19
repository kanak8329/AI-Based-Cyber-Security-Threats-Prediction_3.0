# AI-driven-cybersecurity-threat-prediction-

🛡️ CyberShield AI - ML-Powered Threat Detection Platform

<div align="center">




[![TensorFlow 2.14](https://img.shields.io/badge/TensorFlow-2.14-orange.svg)](https://tensorflow.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2-blue.svg)](https://reactjs.org)

**AI-powered cybersecurity platform with 95%+ accuracy**

[Demo](https://github.com/user-attachments/assets/0330b050-3ed0-4545-82a9-b7cc5ba6b7e8)

• [Documentation](ml_training/docs/MODELS.md) 

</div>

## Deployment Link 
[Click Me](https://cybershield-platform.vercel.app/)

## 🌟 Features

- 🤖 **ML-Powered Detection** - Ensemble models with 95%+ accuracy
- 📊 **Visual Analytics** - Interactive charts and real-time dashboards
- 🔍 **Multi-Format Support** - Analyze files, URLs, APIs, and network traffic
- 💬 **AI Assistant** - Natural language explanations of threats
- 📈 **Risk Forecasting** - Predict future security risks
- 🎯 **CVE Database** - Auto-updated vulnerability scanning

## 🏗️ Architecture
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   React     │────▶│   FastAPI    │────▶│  ML Models  │
│  Frontend   │     │   Backend    │     │  (Ensemble) │
└─────────────┘     └──────────────┘     └─────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │   Database   │
                    │  (Optional)  │
                    └──────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- 8GB RAM minimum
- (Optional) NVIDIA GPU for training

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/cybershield-platform.git
cd cybershield-platform

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Download pre-trained models
python ../scripts/download_models.py

# Start backend
uvicorn app.main:app --reload

# In new terminal, setup frontend
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173`

## 📊 Model Performance

| Model | Accuracy | Speed | Size |
|-------|----------|-------|------|
| Threat Detector | 95.3% | 50ms | 225MB |
| Malware Classifier | 97.1% | 100ms | 434MB |
| Anomaly Detector | 89.0% | 75ms | 188MB |

## 🗂️ Project Structure
```
cybershield-platform/
├── frontend/          # React application
├── backend/           # FastAPI server + ML models
├── ml_training/       # Training scripts & notebooks
├── datasets/          # Training datasets
├── docs/              # Documentation
└── docker/            # Docker configuration
```

See [STRUCTURE.md](docs/STRUCTURE.md) for detailed structure.

## 📚 Documentation

- [API Documentation](docs/API.md)
- [Model Documentation](docs/MODELS.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)

## 🔬 Training Your Own Models
```bash
cd ml_training

# Download datasets
python scripts/download_datasets.py

# Train threat detection model
python scripts/train_threat_detector.py

# Train malware classifier
python scripts/train_malware_classifier.py

# Evaluate all models
python scripts/evaluate_models.py
```

## 📈 Datasets Used

- [CICIDS2017](https://www.unb.ca/cic/datasets/ids-2017.html) - Network traffic (2.8M samples)
- [Kaggle Malware](https://www.kaggle.com/datasets/khaledelmadawy/malware-detection) - Malware samples (500K samples)
- [PhishTank](https://www.phishtank.com/) - Phishing URLs (100K samples)
- [NVD](https://nvd.nist.gov/) - CVE database (daily updates)

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md)

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Acknowledgments

- TensorFlow Team
- scikit-learn Contributors
- FastAPI Framework
- React Community
