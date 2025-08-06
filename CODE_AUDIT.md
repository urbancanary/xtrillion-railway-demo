# Code Audit - Guinness App

## Currently Active Files (Used in Navigation)

### Core Entry Point
- ✅ `guinness_app.py` - Main application with st.navigation

### Active Page Components
- ✅ `welcome_page_guinness_nav_fixed.py` - Welcome page
- ✅ `report_utils.py` - Fund portfolio reports (GGI, SKEWNBF, SKESBF)
- ✅ `credit_reports.py` - Country reports (Israel, Qatar, Mexico, Saudi Arabia)
- ✅ `portfolio_valuation.py` - Portfolio valuation tool
- ✅ `user_guide.py` - User documentation
- ✅ `debug_deployment.py` - Debug information page

### Supporting Modules
- ✅ `logo_utils.py` - Logo handling
- ✅ `chatbot_demo.py` - Chatbot functionality (imported but not in nav)
- ✅ `bond_information.py` - Bond info tab (imported but not in nav)

### Temporarily Disabled (Keep for Future)
- 🟡 `bond_calculator_mockup.py` - Bond calculator (commented out in nav)
- 🟡 `trade_calculator.py` - Trade calculator (commented out in nav)
- 🟡 `ai_assistant.py` - AI assistant (commented out in nav)

### Data/API Files
- ✅ `fetch_data.py` - Data fetching utilities
- ✅ `openai_utils.py` - OpenAI integration
- ✅ `qa_engine5.py` - Q&A engine

## Files to Archive

### Duplicate/Old Versions
- ❌ `welcome_page.py` - Using welcome_page_guinness_nav_fixed.py instead
- ❌ `welcome_page_guinness.py` - Another duplicate
- ❌ `welcome_page_guinness_nav.py` - Another duplicate
- ❌ `sidebar_demo.py` - Using sidebar_guinness.py instead
- ❌ `old_pages/` folder - Already identified as old

### Utility Scripts (One-time use)
- ❌ `adjust_cash_allocation.py` - One-time adjustment script
- ❌ `calculate_bond_analytics.py` - One-time calculation
- ❌ `create_ggi_portfolio.py` - One-time portfolio creation
- ❌ `fix_cost_calculation.py` - One-time fix
- ❌ `fix_ggi_portfolio_calcs.py` - One-time fix

### Possibly Unused
- ❓ `interactive_holdings_table.py` - Check if used by report_utils.py
- ❓ `streamlit_deep_dive_radio_wrapped.py` - Check if still needed

## Navigation Structure

```python
pages = {
    "Main": [
        welcome_page,        # welcome_page_guinness_nav_fixed.py
        ggi_portfolio,       # report_utils.py
        skewnbf_portfolio,   # report_utils.py
        skesbf_portfolio,    # report_utils.py
    ],
    "Country Reports": [
        israel_report,       # credit_reports.py
        qatar_report,        # credit_reports.py
        mexico_report,       # credit_reports.py
        saudi_arabia_report, # credit_reports.py
    ],
    "Tools": [
        portfolio_valuation, # portfolio_valuation.py
        # bond_calculator,   # bond_calculator_mockup.py (DISABLED)
        # trade_calculator,  # trade_calculator.py (DISABLED)
        # ai_assistant,      # ai_assistant.py (DISABLED)
        user_guide,          # user_guide.py
        debug_page,          # debug_deployment.py
    ]
}
```

## Deployment Method

Currently using:
- **Platform**: Railway
- **URL**: dev.x-trillion.ai
- **Branch**: Likely main or development
- **Entry**: `streamlit run guinness_app.py`

## Recommendations

1. **Create `archive/` folder** in the app directory
2. **Move unused files** to archive
3. **Keep disabled features** (bond_calculator, trade_calculator, ai_assistant) for future use
4. **Create automated documentation** generator
5. **Set up testing framework**