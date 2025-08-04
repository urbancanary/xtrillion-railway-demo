# CLAUDE.md - Guinness Global Investors Platform

This file provides guidance to Claude Code (claude.ai/code) when working with the Guinness Global Investors portfolio management platform.

## Repository Overview

This is the **Guinness Global Investors Platform** - a modern Streamlit-based portfolio management and analytics application featuring institutional-grade bond analytics powered by the XTrillion API.

## Project Structure

### Main Application
- **`xtrillion_guinness_nav.py`** - Main application entry point using st.navigation
- **Base URL**: https://xtrillion-deploy-production.up.railway.app/
- **Development URL**: https://xtrillion-deploy-production-0e63.up.railway.app/

### Core Modules

#### Portfolio Analytics
- **`report_utils.py`** - Portfolio visualization and reporting functions
  - Pie charts for ESG, NFA ratings, and regional distribution
  - Interactive holdings table with AG-Grid support
  - Export functionality (CSV, HTML)
  - Portfolio summary cards
  - Search and filter capabilities

#### Valuation & Analysis
- **`portfolio_valuation.py`** - Comprehensive portfolio valuation page
  - Position-level P&L analysis
  - Yield and duration analytics
  - Risk metrics and scenario analysis
  - Market scenario stress testing
  - Interactive charts and heatmaps

#### Bond Calculator
- **`bond_calculator_mockup.py`** - Advanced bond calculator interface
  - Single bond calculations
  - Google Sheets integration
  - Portfolio batch processing
  - Bulk upload and analysis

#### Interactive Features
- **`interactive_holdings_table.py`** - AG-Grid powered interactive table
  - Click-to-view bond details
  - Real-time price charts (mock data)
  - Scenario analysis per bond
  - Advanced analytics expandable sections

#### UI Components
- **`welcome_page_guinness_nav.py`** - Branded welcome page
- **`logo_utils.py`** - Logo handling and encoding utilities
- **`user_guide.py`** - User documentation
- **`bond_information.py`** - Bond information display

### Branding & Design

#### Official Guinness Color Palette
```python
color_palette = [
    "#C8102E",  # Pantone 186 C - Primary Red
    "#21315C",  # Pantone 534 C - Secondary Primary Dark Blue
    "#236192",  # Pantone 647 C - Secondary Blue
    "#9DB9D5",  # Pantone 644 C - Secondary Light Blue
    "#6BBBAE",  # Pantone 536 C - Secondary Teal
    "#D6D2C4",  # Pantone 7527 C - Secondary Beige
    "#808285",  # Black 60% - Grey
]
```

#### UI Design Principles
- Dark theme (#1f1f1f background)
- Consistent spacing and margins
- Fixed pie chart positioning across tabs
- Responsive column layouts
- Professional typography

## Key Features

### 1. Portfolio Management
- **GGI Wealthy Nations Bond Fund** - Flagship portfolio
- **SKEWNBF** - Shin Kong Emerging Wealthy Nations Bond Fund
- **SKESBF** - Shin Kong Environmental Sustainability Bond Fund
- Automatic cash allocation for incomplete portfolios

### 2. Interactive Analytics
- **Holdings Table**
  - Standard table view with hover effects
  - Interactive AG-Grid view with click-for-details
  - Export to CSV functionality
  - Advanced search and filtering

- **Visualization**
  - Pie charts for portfolio composition
  - Regional, ESG, and NFA rating distributions
  - Consistent chart positioning across tabs
  - Export charts as HTML

### 3. Valuation Tools
- Position-level P&L tracking
- Portfolio-wide risk metrics
- Scenario analysis and stress testing
- Duration and convexity analysis
- Interactive heatmaps for rate scenarios

### 4. Bond Calculator
- Single bond analytics
- Google Sheets integration for bulk processing
- Mock data for demonstration
- Advanced parameter configuration

### 5. Country Reports
- Detailed credit research for:
  - Israel
  - Qatar
  - Mexico
  - Saudi Arabia
- Economic indicators and forecasts
- Credit rating agency assessments

## Development Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run xtrillion_guinness_nav.py

# Alternative with specific port
streamlit run xtrillion_guinness_nav.py --server.port 8502
```

### Deployment
```bash
# Deploy to Railway (automatic via GitHub integration)
git add .
git commit -m "Update message"
git push origin main

# Manual deployment
railway up
```

## Navigation Structure

```
Main
├── Welcome (/)
├── GGI Portfolio (/ggi)
├── SKEWNBF (/skewnbf)
└── SKESBF (/skesbf)

Country Reports
├── Israel (/israel)
├── Qatar (/qatar)
├── Mexico (/mexico)
└── Saudi Arabia (/saudi-arabia)

Tools
├── Portfolio Valuation (/valuation)
├── Bond Calculator (/calculator)
└── User Guide (/guide)
```

## Data Sources

### Portfolio Data
- **Local CSV**: `data.csv` contains GGI portfolio holdings
- **API Integration**: Fetches fund data from XTrillion API
- **Mock Data**: Used for demonstrations and testing

### Database References
- Country reports from credit research database
- Bond analytics from XTrillion calculation engine

## Recent Updates

### UI/UX Improvements
- ✅ Implemented st.navigation for modern UI
- ✅ Added portfolio summary cards
- ✅ Fixed pie chart positioning consistency
- ✅ Added interactive AG-Grid holdings table
- ✅ Implemented click-for-bond-details functionality
- ✅ Added export functionality for charts and data
- ✅ Optimized screen space by removing redundant headers
- ✅ Fixed tab visibility with proper color contrast
- ✅ Applied official Guinness brand colors throughout

### Technical Enhancements
- ✅ Fixed Google Sheets date column compatibility
- ✅ Added loading indicators and progress bars
- ✅ Implemented search functionality in holdings table
- ✅ Added tooltips for financial terms
- ✅ Created comprehensive portfolio valuation page
- ✅ Built bond calculator with multiple input methods

## Known Issues & Solutions

### Deployment Issues
- **Railway Custom Domain**: Redirect loop on dev.x-trillion.ai - pending fix
- **Cold Start**: Initial load may take a few seconds

### Data Handling
- **Date Formats**: Settlement dates must use pd.to_datetime() for compatibility
- **Cash Allocation**: Automatically adds cash slice if portfolio < 100%
- **ISIN Lookup**: Limited coverage - use bond descriptions when possible

## Future Enhancements

### High Priority
- [ ] Real-time bond price data integration
- [ ] Portfolio performance metrics (YTD, 1Y, 3Y, 5Y returns)
- [ ] PDF report generation
- [ ] Portfolio rebalancing tool
- [ ] Risk concentration dashboard

### Medium Priority
- [ ] Trade execution integration
- [ ] Alert system for portfolio metrics
- [ ] Historical performance tracking
- [ ] Benchmark comparison tools
- [ ] Mobile-optimized views

### Nice to Have
- [ ] Dark/light theme toggle
- [ ] Advanced charting options (treemap, bubble charts)
- [ ] Sparklines in data tables
- [ ] Export to Excel with formatting

## Code Style Guidelines

### Python
- Use type hints where appropriate
- Follow PEP 8 conventions
- Document functions with docstrings
- Handle errors gracefully with try/except

### Streamlit
- Use consistent column layouts
- Apply custom CSS sparingly
- Implement loading states for long operations
- Use session state for preserving user selections

### UI/UX
- Maintain consistent color palette
- Ensure adequate contrast for readability
- Provide user feedback for all actions
- Keep navigation intuitive and flat

## Security Considerations

- No hardcoded API keys or credentials
- Use environment variables for sensitive data
- Validate all user inputs
- Implement proper error handling
- No direct database connections from frontend

## Performance Optimization

- Cache expensive computations with @st.cache_data
- Lazy load heavy components
- Minimize API calls with intelligent caching
- Use efficient data structures
- Implement pagination for large datasets

## Testing

### Manual Testing Checklist
- [ ] All navigation links work correctly
- [ ] Charts display consistently across tabs
- [ ] Export functionality works for all data types
- [ ] Interactive grid shows bond details on click
- [ ] Portfolio calculations are accurate
- [ ] Error states are handled gracefully

### Common Test Scenarios
1. Load each portfolio and verify data
2. Switch between chart tabs rapidly
3. Export data in various formats
4. Search and filter holdings
5. Click bonds in interactive grid
6. Run scenario analysis

## Support & Documentation

- **User Guide**: Available in the Tools menu
- **API Documentation**: See google_analysis10 project
- **Issue Tracking**: GitHub Issues
- **Deployment Logs**: Railway dashboard

---

*Last Updated: January 2025*
*Version: 2.0 - Guinness Global Investors Edition*