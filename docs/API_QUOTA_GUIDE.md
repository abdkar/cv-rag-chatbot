# 🔄 API Quota Reset Guide - Quick Recovery

**When you see "API Quota Temporarily Exceeded"**

## 🚨 **What's Happening:**
- Your Google Gemini API has reached its usage limit
- **Free Tier:** Quotas reset every 24 hours
- **Paid Tier:** Usually resolves within an hour
- This is **normal** and happens to everyone!

## 🔧 **Solution 1: Update API Key (Instant Fix)**

### **Step 1: Update Your API Key**
```bash
# Open your .env file
nano /home/amir/CV_RAG_OP/.env

# Update this line with your new API key:
GOOGLE_API_KEY=your_new_api_key_here
```

### **Step 2: One-Click Restart**
```bash
cd /home/amir/CV_RAG_OP && bash quick_restart.sh
```

## 🔧 **Solution 2: Wait for Quota Reset (Free)**

### **Free Tier Schedule:**
- **Reset Time:** Every 24 hours from first usage
- **Typical Reset:** Around the same time you started yesterday
- **Auto-Recovery:** Your app will automatically work when quota resets

### **Paid Tier Schedule:**
- **Reset Time:** Usually within 1 hour
- **Faster Recovery:** Much higher limits

## ⚡ **Quick Restart Script**

I'll create a **one-click restart** script for you:

### **Usage:**
```bash
# When you update your API key, just run:
cd /home/amir/CV_RAG_OP
bash quick_restart.sh
```

### **What it does:**
1. ✅ Kills any running app instances
2. ✅ Tests your new API key
3. ✅ Starts the app with updated configuration
4. ✅ Shows you the working URL

## 🎯 **Smart Features Already Built-In:**

### **Auto-Monitoring:**
- ✅ Your app **automatically detects** when quota resets
- ✅ **No manual restart needed** when quota returns
- ✅ **Smart fallback** to other models if one hits quota

### **Model Fallback Chain:**
1. **Primary:** gemini-2.0-flash
2. **Fallback 1:** gemini-1.5-flash-8b  
3. **Fallback 2:** gemini-1.5-pro
4. **Fallback 3:** gemini-pro

### **User-Friendly Messages:**
- Clear quota status in the sidebar
- Helpful instructions for users
- Professional handling of API limits

## 📱 **Current App Status:**

### **When Quota is Exceeded:**
- ✅ **App still works** with professional profile display
- ✅ **Knowledge base** remains accessible
- ✅ **Beautiful UI** stays intact
- ✅ **Auto-monitoring** shows quota status

### **When Quota Resets:**
- ✅ **Automatic recovery** - no restart needed
- ✅ **Full chat functionality** returns
- ✅ **All features** work normally

## 💡 **Pro Tips:**

### **For Frequent Usage:**
1. **Upgrade to Paid Tier** - Much higher limits
2. **Multiple API Keys** - Rotate between them
3. **Monitor Usage** - Check quota in Google Cloud Console

### **For Development:**
1. **Test Locally** - Use the quick restart script
2. **Monitor Limits** - App shows quota status
3. **Smart Fallbacks** - Multiple models available

## 🔄 **Quick Commands:**

### **Check API Status:**
```bash
cd /home/amir/CV_RAG_OP && python -c "
from configs.app_config import get_google_api_key, ModelConfig
import google.generativeai as genai
genai.configure(api_key=get_google_api_key())
model = genai.GenerativeModel(ModelConfig.PRIMARY_MODEL)
response = model.generate_content('test', generation_config={'max_output_tokens': 5})
print('✅ API Working!')
"
```

### **Restart App:**
```bash
cd /home/amir/CV_RAG_OP && bash quick_restart.sh
```

### **View App:**
```bash
# Your app URL:
http://localhost:8511
```

---

**Bottom Line:** Your app is **smart** and handles quota issues gracefully. When you get a new API key, just update `.env` and run the restart script! 🚀
