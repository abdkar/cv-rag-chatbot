# 🚨 Quick Troubleshooting Guide

## 🆘 EMERGENCY FIXES

### App Won't Start
```bash
# 1. Check dependencies
pip install -r requirements.txt

# 2. Test system
python test_system.py

# 3. Check API key in .env file
cat .env | grep GOOGLE_API_KEY
```

### API Errors
```bash
# Test API connectivity
python -c "
from configs.app_config import get_google_api_key
import google.generativeai as genai
genai.configure(api_key=get_google_api_key())
model = genai.GenerativeModel('gemini-1.5-flash-8b')
print('✅ API Working:', model.generate_content('test').text)
"
```

### Port Issues
```bash
# Use different port
streamlit run app_smart.py --server.port=8512
```

### Reset Everything
```bash
# Delete generated files and restart
rm -rf vector_store/ __pycache__/ .streamlit/
python test_system.py
streamlit run app_smart.py --server.port=8511
```

## 📞 Still Having Issues?

1. **Run the full test:** `python test_system.py`
2. **Check logs:** Look in `logs/` directory
3. **Verify API key:** Get new key from [Google AI Studio](https://makersuite.google.com/app/apikey)
4. **Check Python version:** Must be 3.8+
5. **Try fresh install:** Delete `.venv/` and reinstall dependencies

## ✅ Working Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file exists with valid `GOOGLE_API_KEY`
- [ ] `test_system.py` passes all tests
- [ ] Port 8511 available (or use alternative)
- [ ] Internet connection active

## 🎯 Success Command

```bash
python test_system.py && streamlit run app_smart.py --server.port=8511
```

If both commands succeed, your app is working! 🎉
