# CV RAG Chatbot Customization Guide

This guide explains how to customize your CV RAG Chatbot to work with your own content and preferences.

## 📚 Table of Contents
1. [Changing the Knowledge Base](#changing-the-knowledge-base)
2. [Customizing the Prompt Template](#customizing-the-prompt-template)
3. [Personalizing the Profile](#personalizing-the-profile)
4. [Advanced Customizations](#advanced-customizations)
5. [Testing Your Changes](#testing-your-changes)

---

## 📝 Changing the Knowledge Base

### Step 1: Update Your CV Content

The knowledge base is stored in `knowledge_base.txt`. Replace this file with your own CV/resume content.

**Location:** `/knowledge_base.txt`

**Format:** Plain text file with your professional information

**Best Practices:**
```text
# Example structure for knowledge_base.txt

PERSONAL INFORMATION
Name: [Your Full Name]
Title: [Your Professional Title]
Location: [Your Location]
Email: [Your Email]
LinkedIn: [Your LinkedIn URL]

PROFESSIONAL SUMMARY
[Write a comprehensive summary of your professional background]

WORK EXPERIENCE
Company: [Company Name]
Position: [Your Position]
Duration: [Start Date] - [End Date]
Achievements:
- [Specific achievement with metrics]
- [Another achievement with impact]

EDUCATION
Degree: [Your Degree]
University: [University Name]
Year: [Graduation Year]
Relevant coursework: [Relevant subjects]

SKILLS
Technical Skills: [List your technical skills]
Soft Skills: [List your soft skills]
Certifications: [List your certifications]

PROJECTS
Project Name: [Project Name]
Description: [Project description with technologies used]
Impact: [Measurable impact or results]
```

### Step 2: Update Name Validation

In `app.py`, update the name validation function to recognize your name:

**Location:** `app.py`, line ~120

```python
def validate_name_in_content(content: str) -> bool:
    """Check if the content contains your name"""
    name_variations = [
        "Your Full Name",           # Replace with your actual name
        "your full name",           # Lowercase version
        "YOUR FULL NAME",           # Uppercase version
        "Your First Name",          # Just first name
        "Your Last Name",           # Just last name
        "YourNickname"              # Any nickname you use
    ]
    content_lower = content.lower()
    return any(name.lower() in content_lower for name in name_variations)
```

---

## 🎭 Customizing the Prompt Template

The prompt template controls how the AI responds. It's located in `app.py` around line 185.

### Current Prompt Template Location
**File:** `app.py`  
**Function:** `load_rag_pipeline()`  
**Variable:** `template`

### Understanding the Template Structure

```python
template = """
You are the professional AI persona of [YOUR NAME]. Use ONLY the Context. Do not invent or speculate.

Write naturally and concisely in third person ("he/she"). Do not say "according to the context." Quantify only when numbers appear in the Context.

If the question is identity/overview (e.g., "who is…", "tell me about…"), produce a polished 2–3 sentence paragraph. Otherwise, write one direct opening sentence followed by 3 compact bullets with **Bold labels** (≤2 words) and a colon.

If the needed facts are missing: "I do not have that information in the current context."
If the question is personal/out-of-scope (contact, family, salary, religion, politics):
"I do not have information on that topic. For details, it would be best to speak with [YOUR NAME] directly."

Context
{context}

Question
{question}

Answer:
"""
```

### Customization Options

#### 1. **Response Style**
Change the writing style by modifying these parts:

```python
# For more casual responses:
"Write in a friendly, conversational tone as if you're [YOUR NAME]'s colleague..."

# For more formal responses:
"Provide professional, detailed responses representing [YOUR NAME]'s expertise..."

# For more technical responses:
"Focus on technical details and implementation specifics when answering..."
```

#### 2. **Response Format**
Modify the format requirements:

```python
# For longer responses:
"produce a detailed 3-4 sentence paragraph with specific examples"

# For bullet-heavy responses:
"write a brief opening sentence followed by 5-7 detailed bullets"

# For narrative style:
"write in narrative form, telling the story of [YOUR NAME]'s experience"
```

#### 3. **Personality Traits**
Add personality characteristics:

```python
# Add personality context:
"[YOUR NAME] is known for being detail-oriented, innovative, and collaborative. Reflect these traits in responses."

# Add communication style:
"Communicate with enthusiasm about technical challenges and problem-solving."
```

### Example Custom Templates

#### Template 1: Technical Focus
```python
template = """
You are representing [YOUR NAME], a technical professional. Focus on technical depth and implementation details.

Provide specific, actionable information. Include technologies, methodologies, and measurable outcomes when available in the context.

For technical questions: Lead with the technology/approach, then explain implementation and results.
For experience questions: Focus on technical challenges solved and tools used.
For project questions: Emphasize architecture, scale, and technical impact.

If information is missing: "I don't have specific technical details about that in my knowledge base."

Context: {context}
Question: {question}
Technical Response:
"""
```

#### Template 2: Business Focus
```python
template = """
You represent [YOUR NAME] from a business impact perspective. Emphasize results, leadership, and strategic thinking.

Always connect technical work to business value. Quantify impact when numbers are available in the context.

Structure responses as: Business impact → Approach → Results
Use active voice and emphasize leadership and collaboration.

If business metrics aren't available: "While I can share the technical approach, specific business metrics would need to be discussed directly with [YOUR NAME]."

Context: {context}
Question: {question}
Business-Focused Response:
"""
```

#### Template 3: Storytelling Style
```python
template = """
You are sharing [YOUR NAME]'s professional story. Make responses engaging and narrative-driven.

Paint a picture of challenges, solutions, and growth. Use storytelling elements while staying factual.

For experience: "During [time/project], [YOUR NAME] faced [challenge] and approached it by [solution]..."
For skills: "Over the course of [time period], [YOUR NAME] developed expertise in [area] through [specific examples]..."

Keep stories grounded in the provided context. Don't embellish beyond what's stated.

Context: {context}
Question: {question}
Story-driven Response:
"""
```

---

## 👤 Personalizing the Profile

### Update Profile Information

**Location:** `app.py`, around line 580 in the profile section

1. **Name and Title**
```python
<h1 style='font-size: 1.8rem; margin-bottom: 0.5rem; font-weight: 700;'>
    Your Full Name                    # Replace with your name
</h1>
```

2. **Skill Tags**
```python
<span class='skill-tag'>Your Skill 1</span>      # Replace with your skills
<span class='skill-tag'>Your Skill 2</span>
<span class='skill-tag'>Your Skill 3</span>
<span class='skill-tag'>Your Skill 4</span>
```

3. **Professional Description**
```python
<p style='font-size: 0.9rem; line-height: 1.4; opacity: 0.9;'>
    Your professional summary here...              # Replace with your summary
</p>
```

4. **Social Links**
```python
# Update all the links to your profiles
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](YOUR_LINKEDIN_URL)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](YOUR_GITHUB_URL)
```

### Update Profile Photo

Replace `phto.jpg` with your own photo:
1. Add your photo as `phto.jpg` in the root directory
2. Or update the file path in the CSS section around line 240

---

## 🎨 Advanced Customizations

### 1. Quick Start Questions

**Location:** `app.py`, around line 620

```python
# Update the quick start buttons with questions relevant to your field
with col1:
    if st.button("🔚 Your Topic 1", use_container_width=True):
        st.session_state.suggested_query = "Your relevant question 1"
with col2:
    if st.button("🔧 Your Topic 2", use_container_width=True):
        st.session_state.suggested_query = "Your relevant question 2"
```

### 2. Color Scheme

**Location:** `app.py`, around line 240 in the CSS section

```css
/* Change the primary color from #003147 to your preferred color */
.hero-card { background: #YOUR_COLOR !important; }
.stButton > button { background: #YOUR_COLOR; }
```

### 3. AI Model Settings

**Location:** `app.py`, around line 165

```python
llm = GoogleGenerativeAI(
    model="gemini-2.0-flash-exp",  # You can change the model
    temperature=0.3,               # Adjust creativity (0.0-1.0)
    timeout=15                     # Adjust timeout
)
```

### 4. Text Chunking

**Location:** `app.py`, around line 175

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,    # Increase for longer context, decrease for more precise
    chunk_overlap=200,  # Adjust overlap between chunks
    length_function=len
)
```

---

## 🧪 Testing Your Changes

### 1. Test Locally
```bash
# Start the application
streamlit run app.py

# Test with different questions to verify your changes
```

### 2. Test Knowledge Base
1. Upload your CV through the file upload feature
2. Ask questions about different sections
3. Verify the AI finds relevant information

### 3. Test Prompt Changes
1. Ask the same question before and after prompt changes
2. Compare response style and format
3. Adjust the prompt based on results

### 4. Clear Cache
```python
# If responses seem cached, clear the cache:
st.cache_resource.clear()
```

---

## 📋 Checklist for Complete Customization

- [ ] Replace `knowledge_base.txt` with your CV content
- [ ] Update name validation function with your name
- [ ] Customize the prompt template for your desired response style
- [ ] Update profile name, title, and description
- [ ] Replace skill tags with your skills
- [ ] Update social media links
- [ ] Replace profile photo (`phto.jpg`)
- [ ] Customize quick start questions
- [ ] Test the application with various questions
- [ ] Adjust prompt template based on testing results

---

## 🚨 Common Issues and Solutions

### Issue: "Name not found" warnings
**Solution:** Make sure your name variations in `validate_name_in_content()` exactly match what's in your knowledge base.

### Issue: Generic or irrelevant responses
**Solution:** 
1. Check that your knowledge base has sufficient detail
2. Adjust the prompt template to be more specific
3. Reduce chunk_size for more precise retrieval

### Issue: AI not following the response format
**Solution:** Make the format instructions in the prompt template more explicit and include examples.

### Issue: Missing information in responses
**Solution:** 
1. Verify the information exists in your knowledge base
2. Try rephrasing questions to match your content
3. Check if the information is in separate chunks

---

## 💡 Pro Tips

1. **Iterative Improvement:** Start with small changes and test frequently
2. **Content Quality:** More detailed knowledge base = better responses
3. **Prompt Engineering:** Spend time refining your prompt template - it's the most impactful change
4. **User Testing:** Have others ask questions to identify gaps
5. **Regular Updates:** Keep your knowledge base current with new experiences

---

**Need Help?** If you run into issues, check the main README.md for general troubleshooting or create an issue in the repository.
