#!/bin/bash
# 🔄 Quick Restart Script for CV RAG Chatbot
# Use this script when you update your API key or need to restart the app

echo "🔄 Quick Restart - CV RAG Chatbot"
echo "=================================="

# Kill any existing streamlit processes
echo "🛑 Stopping existing app instances..."
pkill -f "streamlit run" 2>/dev/null || echo "   No running instances found"

# Wait a moment
sleep 2

# Test API key
echo ""
echo "🔍 Testing API key..."
cd /home/amir/CV_RAG_OP

python -c "
import sys
sys.path.append('.')
try:
    from configs.app_config import get_google_api_key, ModelConfig
    import google.generativeai as genai
    
    api_key = get_google_api_key()
    if not api_key or api_key == 'your_api_key_here':
        print('❌ API key not found or not updated!')
        print('📝 Please update your .env file with a valid GOOGLE_API_KEY')
        exit(1)
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(ModelConfig.PRIMARY_MODEL)
    response = model.generate_content('test', generation_config={'max_output_tokens': 5})
    
    print('✅ API Key: Working!')
    print(f'✅ Model: {ModelConfig.PRIMARY_MODEL}')
    print(f'✅ Response: {response.text}')
    
except Exception as e:
    error_str = str(e)
    if 'quota' in error_str.lower() or '429' in error_str:
        print('🚨 API Quota Exceeded')
        print('⏰ Please wait for quota reset or use a new API key')
        print('📱 App will run in quota-safe mode')
    else:
        print(f'❌ API Error: {error_str}')
        print('📝 Please check your API key in .env file')
"

api_test_result=$?

echo ""
echo "🚀 Starting CV RAG Chatbot..."

# Start the app
nohup streamlit run app_smart.py --server.port=8511 --server.address=0.0.0.0 > logs/app.log 2>&1 &

# Wait for startup
sleep 3

# Check if app started
if pgrep -f "streamlit run" > /dev/null; then
    echo "✅ App started successfully!"
    echo ""
    echo "📱 Your CV RAG Chatbot is running at:"
    echo "   🌐 http://localhost:8511"
    echo ""
    if [ $api_test_result -eq 0 ]; then
        echo "🎉 Status: Full functionality available"
        echo "💬 Chat feature: Active"
        echo "📄 Knowledge base: Available"
        echo "🔍 Smart retrieval: Working"
    else
        echo "⚠️  Status: Quota-safe mode"
        echo "📄 Profile display: Available"
        echo "🔗 Social links: Working"
        echo "💬 Chat: Will auto-enable when quota resets"
    fi
    echo ""
    echo "🔄 To restart again: bash quick_restart.sh"
    echo "📖 For help: See docs/API_QUOTA_GUIDE.md"
else
    echo "❌ Failed to start app"
    echo "📋 Check logs: tail -f logs/app.log"
fi

echo ""
echo "=================================="
