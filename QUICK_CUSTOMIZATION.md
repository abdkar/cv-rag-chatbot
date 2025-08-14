# Quick Start Customization Template

This is a simplified guide for the most common customizations. For detailed instructions, see `CUSTOMIZATION_GUIDE.md`.

## 🚀 Essential Changes (5 minutes)

### 1. Replace Knowledge Base
- **File:** `knowledge_base.txt`
- **Action:** Replace entire content with your CV/resume text

### 2. Update Your Name
- **File:** `app.py` 
- **Line:** ~120
- **Change:**
```python
name_variations = [
    "Your Full Name",      # ← Change this
    "your full name",      # ← and this
    "YOUR FULL NAME",      # ← and this
    "FirstName",           # ← and this
    "LastName"             # ← and this
]
```

### 3. Update Profile Section
- **File:** `app.py`
- **Line:** ~590
- **Change:**
```python
<h1>Your Full Name</h1>                    # ← Your name
<span class='skill-tag'>Your Skill</span>  # ← Your skills
<p>Your professional summary...</p>         # ← Your summary
```

### 4. Update Social Links
- **File:** `app.py`
- **Line:** ~610
- **Change:**
```python
](https://linkedin.com/in/your-profile)     # ← Your LinkedIn
](https://github.com/your-username)         # ← Your GitHub
```

### 5. Replace Profile Photo
- **Action:** Replace `phto.jpg` with your photo (same filename)

---

## 🎭 Prompt Template Customization

**Location:** `app.py`, line ~185-210

### Option 1: More Technical Responses
Replace the existing template with:
```python
template = """
You are the technical AI persona of [YOUR NAME]. Focus on technical depth and implementation details.

Provide specific, actionable information about technologies, methodologies, and technical achievements.

For technical questions: Lead with the technology/approach, then explain implementation.
For experience questions: Focus on technical challenges solved and tools used.

Use the context provided. If technical details are missing, say "I don't have specific technical details about that."

Context: {context}
Question: {question}
Technical Response:
"""
```

### Option 2: More Business-Focused Responses
```python
template = """
You represent [YOUR NAME] from a business impact perspective. Emphasize results, leadership, and strategic value.

Always connect technical work to business outcomes. Quantify impact when numbers are available.

Structure: Business impact → Approach → Results
Focus on leadership, collaboration, and measurable outcomes.

Context: {context}
Question: {question}
Business-Focused Response:
"""
```

### Option 3: More Conversational Responses
```python
template = """
You're having a friendly conversation about [YOUR NAME]'s professional background. Be conversational but professional.

Share experiences naturally, as if you're a colleague describing [YOUR NAME]'s work.
Include specific examples and achievements when available in the context.

Keep responses engaging and personable while staying factual.

Context: {context}
Question: {question}
Conversational Response:
"""
```

---

## 🧪 Quick Test

1. **Start the app:** `streamlit run app.py`
2. **Test these questions:**
   - "Who is [your name]?"
   - "What is [your name]'s experience with [your main skill]?"
   - "Tell me about [your name]'s background"
3. **Verify:** Responses should reflect your content and style

---

## 🛠️ Common Quick Fixes

### Responses too generic?
- Add more detail to your `knowledge_base.txt`
- Make your prompt template more specific

### Wrong information?
- Check your knowledge base has the correct info
- Verify your name validation is working

### Wrong style?
- Adjust the prompt template
- Test different templates from above

---

**Next Steps:** For advanced customizations, color changes, and detailed explanations, see the full `CUSTOMIZATION_GUIDE.md`.
