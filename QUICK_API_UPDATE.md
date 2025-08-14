# 🔑 **WHEN YOU GET A NEW API KEY - SIMPLE STEPS**

## 📋 **2-Step Solution:**

### **Step 1: Update API Key**
```bash
# Edit your .env file
nano /home/amir/CV_RAG_OP/.env

# Change this line:
GOOGLE_API_KEY=your_new_api_key_here
```

### **Step 2: One-Click Restart**
```bash
cd /home/amir/CV_RAG_OP
bash quick_restart.sh
```

**That's it!** Your app will restart with the new API key! 🎉

---

## 🎯 **What the script does for you:**

✅ **Stops** the old app  
✅ **Tests** your new API key  
✅ **Starts** the app with new key  
✅ **Shows** you the working URL  

## 📱 **Your App URL:**
http://localhost:8511

---

## ⚡ **Quick Commands Reference:**

| Task | Command |
|------|---------|
| **Restart with new key** | `bash quick_restart.sh` |
| **Check if app is running** | `pgrep -f streamlit` |
| **View app logs** | `tail -f logs/app.log` |
| **Stop app** | `pkill -f "streamlit run"` |

---

## 🔄 **Quota Reset Schedule:**

- **Free Tier:** Every 24 hours
- **Paid Tier:** Usually within 1 hour
- **Auto-Recovery:** App automatically works when quota resets

**No restart needed when quota naturally resets!** 🚀
