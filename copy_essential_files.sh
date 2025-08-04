#!/bin/bash
# Copy essential files for XTrillion demo

echo "Copying essential Python files..."

# Core modules that the demo imports
cp ../welcome_page.py . 2>/dev/null || echo "No welcome_page.py"
cp ../user_guide.py . 2>/dev/null || echo "No user_guide.py"
cp ../sidebar_demo.py . 2>/dev/null || echo "No sidebar_demo.py"
cp ../chatbot_demo.py . 2>/dev/null || echo "No chatbot_demo.py"
cp ../credit_reports.py . 2>/dev/null || echo "No credit_reports.py"
cp ../report_utils.py . 2>/dev/null || echo "No report_utils.py"
cp ../bond_information.py . 2>/dev/null || echo "No bond_information.py"
cp ../qa_engine5.py . 2>/dev/null || echo "No qa_engine5.py"
cp ../streamlit_deep_dive_radio_wrapped.py . 2>/dev/null || echo "No streamlit_deep_dive_radio_wrapped.py"

# Check if pages directory exists
if [ -d "../pages" ]; then
    mkdir -p pages
    cp ../pages/*.py pages/ 2>/dev/null || echo "No pages to copy"
fi

# Copy any data files
cp ../credentials.json . 2>/dev/null || echo "No credentials.json"

echo "Files copied. Now checking what we have..."
ls -la *.py | wc -l
echo "Python files in current directory"