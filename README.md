# Tech Market Trend Analyzer

A comprehensive AI-powered market analysis system that automatically collects, processes, and analyzes technology and market trends from RSS feeds. The system uses advanced clustering algorithms and OpenAI's API to generate professional market insights with a modern web interface.

## Features

- **Automated Data Collection**: RSS feed ingestion from major tech news sources
- **AI-Powered Analysis**: OpenAI GPT integration for generating market insights
- **Advanced Clustering**: FAISS vector similarity search with K-means clustering
- **Real-time Dashboard**: Modern web interface with live data updates
- **RESTful API**: Complete FastAPI backend with comprehensive endpoints
- **Data Persistence**: SQLite database with duplicate prevention
- **Scheduled Updates**: Automated 24-hour data refresh cycles
- **Professional UI**: Clean, responsive design with progress tracking

## Technology Stack

### Backend

- **Python 3.10+**: Core application language
- **FastAPI**: Modern web framework for API development
- **SQLite**: Lightweight database for article storage
- **FAISS**: Facebook AI Similarity Search for vector operations
- **OpenAI API**: Large language model integration
- **scikit-learn**: Machine learning algorithms for clustering
- **pandas**: Data manipulation and analysis
- **BeautifulSoup**: HTML parsing for content extraction
- **feedparser**: RSS feed processing

### Frontend

- **HTML5/CSS3**: Modern web standards
- **JavaScript (ES6+)**: Interactive functionality
- **Responsive Design**: Mobile-first approach
- **CSS Grid/Flexbox**: Advanced layout systems

### Data Sources

- TechCrunch RSS feeds
- The Decoder technology news
- VentureBeat market coverage

## Installation

### Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Internet connection for RSS feeds

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd tech_market_trend_analyzer
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv market_env
   # Windows
   market_env\Scripts\activate
   # macOS/Linux
   source market_env/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**

   ```bash
   cp .env.template .env
   ```

   Edit `.env` file and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Initialize the system**
   ```bash
   python app.py
   ```

### API Endpoints

#### System Information

- `GET /` - Homepage
- `GET /dashboard` - Analysis dashboard
- `GET /api/system/info` - System status

#### Data Pipeline

- `GET /api/pipeline/status` - Pipeline status
- `POST /api/pipeline/run` - Start data collection

#### Analysis

- `GET /api/analysis` - Complete market analysis
- `POST /api/analysis/refresh` - Force refresh analysis
- `GET /api/clusters` - Raw cluster data
- `GET /api/clusters/{id}` - Specific cluster details



## Data Flow

1. **Collection**: RSS feeds are automatically parsed and stored
2. **Processing**: Articles are cleaned and deduplicated
3. **Embedding**: OpenAI creates vector embeddings for content
4. **Storage**: FAISS indexes embeddings for similarity search
5. **Clustering**: K-means groups similar articles together
6. **Analysis**: AI generates insights for each cluster
7. **Presentation**: Web dashboard displays formatted results

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Required for AI analysis
- `RSS_UPDATE_INTERVAL`: Hours between updates (default: 24)
- `CLUSTER_COUNT`: Number of article clusters (default: 5)

### Customization Options

- **RSS Sources**: Modify `data/rss_ingest.py` to add feeds
- **Analysis Prompts**: Edit `agent/build_prompt.py` for custom insights
- **UI Styling**: Update `frontend/css/` for visual changes
- **Clustering Parameters**: Adjust in `agent/clusters.py`

