import streamlit as st
import anthropic
from datetime import datetime
import json
import pandas as pd

def create_ai_assistant_page():
    """Create the AI Assistant page for bond analytics help"""
    
    st.markdown("## 🤖 AI Bond Analytics Assistant")
    st.markdown("Ask questions about bonds, portfolios, analytics, or get help with the platform.")
    
    # Initialize Anthropic client
    try:
        import os
        
        # Try environment variable first (for deployment), then Streamlit secrets (for local dev)
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        
        if not api_key:
            # Try Streamlit secrets as fallback
            try:
                api_key = st.secrets.get("ANTHROPIC_API_KEY")
            except:
                pass
        
        if not api_key:
            st.error("⚠️ Anthropic API key not configured.")
            st.info("For Railway deployment: Add ANTHROPIC_API_KEY to your environment variables")
            st.info("For local development: Add ANTHROPIC_API_KEY to .streamlit/secrets.toml")
            return
            
        # Initialize client for anthropic version 0.18.1
        client = anthropic.Client(api_key)
    except Exception as e:
        st.error(f"Error initializing AI assistant: {str(e)}")
        return
    
    # Initialize chat history
    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = []
        # Add welcome message
        st.session_state.ai_messages.append({
            "role": "assistant",
            "content": "👋 Hello! I'm your AI bond analytics assistant. I can help you with:\n\n" +
                      "• Understanding bond metrics (YTM, duration, convexity)\n" +
                      "• Analyzing portfolio composition and risk\n" +
                      "• Explaining financial calculations\n" +
                      "• Navigating the platform features\n\n" +
                      "What would you like to know?"
        })
    
    # Create two columns for chat and context
    chat_col, context_col = st.columns([2, 1])
    
    with context_col:
        st.markdown("### 📊 Current Context")
        
        # Load portfolio data if available
        try:
            fund_data = pd.read_csv('data.csv')
            ggi_data = fund_data[fund_data['fund_name'] == 'Guinness Global Investors Fund'].copy()
            
            if not ggi_data.empty:
                # Calculate metrics
                total_value = ggi_data['market_value'].sum()
                num_holdings = len(ggi_data[ggi_data['name'] != 'Cash'])
                avg_yield = pd.to_numeric(ggi_data[ggi_data['name'] != 'Cash']['yield'], errors='coerce').mean()
                
                st.markdown(f"""
                <div style="background-color: #2a2a2a; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                    <h5 style="color: #9DB9D5; margin: 0;">GGI Portfolio</h5>
                    <p style="margin: 0.5rem 0;"><strong>Value:</strong> ${total_value:,.0f}</p>
                    <p style="margin: 0.5rem 0;"><strong>Holdings:</strong> {num_holdings}</p>
                    <p style="margin: 0.5rem 0;"><strong>Avg Yield:</strong> {avg_yield:.2f}%</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Quick actions
                st.markdown("### 🚀 Quick Actions")
                if st.button("📈 Explain my portfolio", use_container_width=True):
                    prompt = "Can you explain the key characteristics of my GGI portfolio based on the current holdings?"
                    st.session_state.ai_input = prompt
                    
                if st.button("🎯 Risk analysis", use_container_width=True):
                    prompt = "What are the main risks in my current bond portfolio?"
                    st.session_state.ai_input = prompt
                    
                if st.button("💡 Optimization tips", use_container_width=True):
                    prompt = "How could I optimize my bond portfolio for better risk-adjusted returns?"
                    st.session_state.ai_input = prompt
                    
        except Exception as e:
            st.info("Portfolio data not available")
    
    with chat_col:
        # Display chat messages
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.ai_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Type your question here...", key="ai_chat_input"):
            # Add user message to chat history
            st.session_state.ai_messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Build context about the portfolio
                        context = build_portfolio_context()
                        
                        # Create system prompt
                        system_prompt = f"""You are an expert bond analytics assistant for Guinness Global Investors. 
                        You have deep knowledge of:
                        - Fixed income securities and bond mathematics
                        - Portfolio risk management and optimization
                        - Financial markets and investment strategies
                        - The Guinness Global Investors platform features
                        
                        Current context:
                        {context}
                        
                        Be helpful, concise, and use specific examples when possible. If asked about calculations,
                        show the formulas. Format your responses with markdown for clarity."""
                        
                        # Get response from Claude Haiku
                        response = client.messages.create(
                            model="claude-3-haiku-20240307",
                            max_tokens=1000,
                            temperature=0.7,
                            system=system_prompt,
                            messages=[
                                {"role": m["role"], "content": m["content"]} 
                                for m in st.session_state.ai_messages[1:]  # Skip welcome message
                            ]
                        )
                        
                        # Display response
                        assistant_response = response.content[0].text
                        st.markdown(assistant_response)
                        
                        # Add to chat history
                        st.session_state.ai_messages.append({
                            "role": "assistant", 
                            "content": assistant_response
                        })
                        
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")
                        if "api_key" in str(e).lower():
                            st.info("Please check your Anthropic API key configuration.")
        
        # Check for quick action input
        if "ai_input" in st.session_state:
            # Trigger the chat input programmatically
            st.rerun()
    
    # Add export chat option
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.ai_messages = [{
                "role": "assistant",
                "content": "Chat cleared. How can I help you with bond analytics today?"
            }]
            st.rerun()
    
    with col2:
        if st.button("💾 Export Chat", use_container_width=True):
            # Export chat history as JSON
            chat_export = {
                "timestamp": datetime.now().isoformat(),
                "messages": st.session_state.ai_messages
            }
            st.download_button(
                label="Download Chat",
                data=json.dumps(chat_export, indent=2),
                file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

def build_portfolio_context():
    """Build context about the current portfolio for the AI"""
    context_parts = []
    
    try:
        # Load portfolio data
        fund_data = pd.read_csv('data.csv')
        ggi_data = fund_data[fund_data['fund_name'] == 'Guinness Global Investors Fund'].copy()
        
        if not ggi_data.empty:
            # Portfolio summary
            total_value = ggi_data['market_value'].sum()
            num_holdings = len(ggi_data[ggi_data['name'] != 'Cash'])
            
            # Clean numeric columns
            ggi_data['yield_numeric'] = pd.to_numeric(ggi_data['yield'], errors='coerce')
            ggi_data['duration_numeric'] = pd.to_numeric(ggi_data['duration'], errors='coerce')
            
            # Calculate weighted metrics
            non_cash = ggi_data[ggi_data['name'] != 'Cash'].copy()
            total_weight = non_cash['weighting'].sum()
            
            if total_weight > 0:
                weighted_yield = (non_cash['yield_numeric'] * non_cash['weighting'] / total_weight).sum()
                weighted_duration = (non_cash['duration_numeric'] * non_cash['weighting'] / total_weight).sum()
            else:
                weighted_yield = 0
                weighted_duration = 0
            
            # Top holdings
            top_holdings = non_cash.nlargest(5, 'weighting')[['name', 'weighting', 'yield_numeric']]
            
            context_parts.append(f"""
Portfolio Overview:
- Total Market Value: ${total_value:,.0f}
- Number of Holdings: {num_holdings}
- Weighted Average Yield: {weighted_yield:.2f}%
- Weighted Average Duration: {weighted_duration:.2f} years

Top 5 Holdings:
""")
            for _, holding in top_holdings.iterrows():
                context_parts.append(f"- {holding['name']}: {holding['weighting']:.1f}% weight, {holding['yield_numeric']:.2f}% yield")
            
            # Regional distribution
            region_dist = non_cash.groupby('region')['weighting'].sum().sort_values(ascending=False)
            context_parts.append("\nRegional Distribution:")
            for region, weight in region_dist.items():
                context_parts.append(f"- {region}: {weight:.1f}%")
                
    except Exception as e:
        context_parts.append("Portfolio data not available for context.")
    
    # Add platform features context
    context_parts.append("""
Platform Features Available:
- Portfolio Valuation: Detailed P&L analysis and risk metrics
- Trade Calculator: Simulate bond sales and portfolio changes
- Bond Calculator: Individual bond analytics and calculations
- Interactive Holdings: Click-through bond details with AG-Grid
- Country Reports: Analysis for Israel, Qatar, Mexico, Saudi Arabia
""")
    
    return "\n".join(context_parts)

# Add custom styles for the AI assistant page
def add_ai_styles():
    st.markdown("""
    <style>
    /* AI Assistant specific styles */
    .stChatMessage {
        background-color: #2a2a2a;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .stChatInput {
        background-color: #2a2a2a;
        border: 1px solid #3a3a3a;
    }
    
    /* Quick action buttons */
    .quick-action-button {
        background-color: #3a3a3a;
        border: 1px solid #4a4a4a;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .quick-action-button:hover {
        background-color: #4a4a4a;
        border-color: #C8102E;
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(
        page_title="AI Assistant - GGI",
        page_icon="🤖",
        layout="wide"
    )
    add_ai_styles()
    create_ai_assistant_page()