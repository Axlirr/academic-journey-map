# Academic Journey Map 🎓

A powerful visualization service for tracking and visualizing academic progress, skills, and goals. Built with FastAPI, Plotly, and NetworkX.

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0%2B-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🌟 Features

### Interactive Visualizations
- **Skill Network**: Interactive network graph showing relationships between skills, courses, and projects
- **Progress Timeline**: Chronological visualization of academic achievements and milestones
- **Skill Radar**: Radar chart comparing skill proficiencies across categories
- **Goal Progress**: Visual tracking of academic and career goals

### Advanced Capabilities
- 🚀 Real-time data processing with AI insights
- 💾 Efficient caching system for improved performance
- 📤 Multiple export formats (HTML, PNG, SVG, PDF, JSON, CSV)
- 📊 Interactive and responsive visualizations
- 🔒 Secure authentication and authorization
- 📱 Mobile-friendly responsive design

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Redis (for caching)
- PostgreSQL (for database)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Axlirr/academic-journey-map.git
cd academic-journey-map
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate   # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
python scripts/init_db.py
```

6. Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 Documentation

### API Documentation
- Interactive API docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- [Detailed API Documentation](docs/visualizations_api.md)

### Example Usage

```python
from academic_journey_client import AcademicJourneyAPI

# Initialize client
api = AcademicJourneyAPI(api_key="your_api_key")

# Generate skill network visualization
skill_network = api.visualizations.get_skill_network(
    user_id=123,
    min_proficiency=7,
    category_filter="Programming"
)

# Export as PDF
skill_network.export(format="pdf", filename="skill_network.pdf")
```

## 🛠️ Development

### Project Structure
```
academic-journey-map/
├── app/
│   ├── main.py           # FastAPI application
│   ├── models/           # Database models
│   ├── routes/           # API routes
│   ├── schemas/          # Pydantic schemas
│   ├── visualization/    # Visualization logic
│   └── utils/           # Utility functions
├── tests/               # Test suite
├── docs/               # Documentation
├── scripts/            # Utility scripts
└── requirements.txt    # Dependencies
```

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
# Format code
black .

# Check types
mypy .

# Lint code
flake8
```

## 🔧 Configuration

The service can be configured using environment variables or a `.env` file:

```env
# Server Configuration
PORT=8000
WORKERS=4
DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@localhost/dbname

# Redis Cache
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Security
SECRET_KEY=your-secret-key
API_KEY_HEADER=X-API-Key

# Visualization Settings
CACHE_DURATION=3600
MAX_NODES=1000
EXPORT_PATH=/path/to/exports
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the amazing web framework
- [Plotly](https://plotly.com/) for interactive visualizations
- [NetworkX](https://networkx.org/) for network analysis
- [Redis](https://redis.io/) for caching
- All our contributors and users

## 📞 Support

- 📧 Email: support@academic-journey-map.com
- 💬 Discord: [Join our community](https://discord.gg/academic-journey)
- 🐛 Issues: [GitHub Issues](https://github.com/Axlirr/academic-journey-map/issues)

## 🚀 Roadmap

### Upcoming Features
- [ ] Machine learning-based skill recommendations
- [ ] Integration with learning platforms
- [ ] Collaborative project visualization
- [ ] Custom visualization themes
- [ ] Mobile app

### Recently Added
- [x] Export functionality
- [x] Caching system
- [x] AI-powered insights
- [x] Interactive visualizations

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/Axlirr/academic-journey-map?style=social)
![GitHub forks](https://img.shields.io/github/forks/Axlirr/academic-journey-map?style=social)
![GitHub issues](https://img.shields.io/github/issues/Axlirr/academic-journey-map)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Axlirr/academic-journey-map)