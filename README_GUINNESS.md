# Guinness Global Investors Portfolio Platform

A modern, interactive portfolio management platform built with Streamlit for Guinness Global Investors, featuring institutional-grade bond analytics powered by XTrillion.

![Guinness Global Investors](https://img.shields.io/badge/Guinness-Global%20Investors-C8102E?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39.0-FF4B4B?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python)

## 🚀 Live Demo

**Production**: https://xtrillion-deploy-production.up.railway.app/

## ✨ Features

### 📊 Portfolio Analytics
- **Interactive Holdings Table** - Click any bond for detailed analytics
- **Smart Visualizations** - Pie charts for ESG, NFA ratings, and regional distribution
- **Portfolio Summary Cards** - Key metrics at a glance
- **Export Capabilities** - Download data as CSV or charts as HTML

### 💰 Valuation Tools
- **Comprehensive P&L Analysis** - Position-level profit/loss tracking
- **Risk Analytics** - Duration, convexity, and scenario analysis
- **Market Scenarios** - Stress testing with interactive heatmaps
- **Yield Analysis** - Distribution and bucketing analytics

### 🧮 Bond Calculator
- **Single Bond Analysis** - Detailed bond calculations
- **Bulk Processing** - Upload and analyze multiple bonds
- **Google Sheets Integration** - Direct connection to spreadsheets
- **Real-time Calculations** - Powered by XTrillion API

### 🌍 Country Reports
- Detailed credit research and analysis for:
  - 🇮🇱 Israel
  - 🇶🇦 Qatar
  - 🇲🇽 Mexico
  - 🇸🇦 Saudi Arabia

## 🛠️ Technology Stack

- **Frontend**: Streamlit 1.39.0 with st.navigation
- **Visualization**: Plotly for interactive charts
- **Data Grid**: AG-Grid for interactive tables
- **Analytics**: XTrillion Bond Analytics API
- **Styling**: Custom CSS with official Guinness brand colors
- **Deployment**: Railway with GitHub integration

## 🎨 Brand Colors

```python
Primary Red:        #C8102E  (Pantone 186 C)
Secondary Blue:     #21315C  (Pantone 534 C)
Light Blue:         #236192  (Pantone 647 C)
Lighter Blue:       #9DB9D5  (Pantone 644 C)
Teal:              #6BBBAE  (Pantone 536 C)
Beige:             #D6D2C4  (Pantone 7527 C)
Grey:              #808285  (Black 60%)
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/xtrillion-deploy.git
cd xtrillion-deploy
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run xtrillion_guinness_nav.py
```

4. Open your browser to `http://localhost:8501`

## 📁 Project Structure

```
xtrillion-deploy/
├── xtrillion_guinness_nav.py    # Main application entry
├── report_utils.py               # Portfolio visualization
├── portfolio_valuation.py        # Valuation analytics
├── bond_calculator_mockup.py     # Bond calculator UI
├── interactive_holdings_table.py # AG-Grid implementation
├── welcome_page_guinness_nav.py  # Welcome page
├── data.csv                      # GGI portfolio data
├── requirements.txt              # Python dependencies
└── CLAUDE.md                     # AI assistant guide
```

## 🔧 Configuration

### Environment Variables
```bash
# API Configuration (optional)
XTRILLION_API_KEY=your_api_key
XTRILLION_API_URL=https://api.xtrillion.com

# Development Settings
STREAMLIT_THEME_BASE=dark
STREAMLIT_SERVER_PORT=8501
```

### Custom Settings
Edit `xtrillion_guinness_nav.py` to modify:
- Navigation structure
- Page titles and icons
- Color schemes
- Default portfolios

## 📊 Usage Examples

### View Portfolio Holdings
1. Navigate to "GGI Portfolio" from the sidebar
2. View pie charts showing portfolio composition
3. Click "Interactive Grid" view mode
4. Click any bond to see detailed analytics

### Run Scenario Analysis
1. Go to "Portfolio Valuation"
2. Select "Market Scenarios" tab
3. View impact of rate changes on portfolio
4. Export results for reporting

### Calculate Bond Analytics
1. Open "Bond Calculator"
2. Enter bond details or ISIN
3. Click "Calculate Analytics"
4. View YTM, duration, and other metrics

## 🔒 Security

- No sensitive data stored in code
- API keys managed via environment variables
- Read-only access to portfolio data
- Secure HTTPS deployment

## 🐛 Known Issues

1. **AG-Grid Compatibility**: Requires `streamlit-aggrid` installation
2. **Date Formatting**: Settlement dates must be datetime objects
3. **Custom Domain**: Redirect loop on dev.x-trillion.ai

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is proprietary software owned by Guinness Global Investors.

## 👥 Team

- **Development**: XTrillion Engineering Team
- **Design**: Guinness Global Investors
- **API**: XTrillion Bond Analytics

## 📞 Support

For issues or questions:
- Internal: Contact IT Support
- External: support@xtrillion.com

---

*Built with ❤️ by XTrillion for Guinness Global Investors*