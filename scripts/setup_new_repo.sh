#!/bin/bash

# 🚀 Rag_CVChat_pro Repository Setup Script
# This script helps you create and push to your new private GitHub repository

echo "🚀 Setting up Rag_CVChat_pro private repository..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "app_organized.py" ]; then
    echo -e "${RED}❌ Error: Please run this script from the CV_RAG_OP directory${NC}"
    exit 1
fi

echo -e "${BLUE}📁 Current directory: $(pwd)${NC}"
echo ""

# Step 1: Commit the new README
echo -e "${YELLOW}📚 Step 1: Updating README for new repository...${NC}"
git add README.md GITHUB_SETUP_GUIDE.md
git commit -m "📚 Prepare for Rag_CVChat_pro private repository

✨ Added:
- Professional README with comprehensive documentation
- Setup guide for new private repository
- Complete architecture overview
- Usage instructions and examples
- Docker deployment configuration

🎯 Ready for private repository creation"

echo -e "${GREEN}✅ README updated and committed${NC}"
echo ""

# Step 2: Show repository creation instructions
echo -e "${YELLOW}🔗 Step 2: Create GitHub Repository${NC}"
echo "Please follow these steps manually:"
echo ""
echo "1. Go to: https://github.com/new"
echo "2. Repository name: Rag_CVChat_pro"
echo "3. Description: Professional CV RAG Chatbot with Modular Architecture"
echo "4. ✅ Set as PRIVATE"
echo "5. ❌ Don't initialize with README (we have our own)"
echo "6. Click 'Create repository'"
echo ""

# Step 3: Wait for user confirmation
read -p "Press Enter after you've created the repository on GitHub..."
echo ""

# Step 4: Add remote and push
echo -e "${YELLOW}🔗 Step 3: Connecting to new repository...${NC}"

# Add new remote
git remote add rag-pro https://github.com/abdkar/Rag_CVChat_pro.git

echo -e "${GREEN}✅ Remote added${NC}"

# Push to new repository
echo -e "${YELLOW}📤 Step 4: Pushing code to new repository...${NC}"
echo "This may take a moment..."

if git push rag-pro main; then
    echo -e "${GREEN}✅ Successfully pushed to new repository!${NC}"
    echo ""
    echo -e "${BLUE}🎉 Repository Setup Complete!${NC}"
    echo ""
    echo -e "${GREEN}📍 Your new private repository:${NC}"
    echo "   🌐 https://github.com/abdkar/Rag_CVChat_pro"
    echo ""
    echo -e "${GREEN}📋 What's included:${NC}"
    echo "   ✅ Professional modular architecture"
    echo "   ✅ Comprehensive documentation"
    echo "   ✅ Working CV RAG chatbot"
    echo "   ✅ Docker deployment setup"
    echo "   ✅ All organized source code"
    echo ""
    echo -e "${YELLOW}🚀 Next steps:${NC}"
    echo "   1. Visit your repository to verify everything is there"
    echo "   2. Configure repository settings (issues, wiki, etc.)"
    echo "   3. Add collaborators if needed"
    echo "   4. Consider creating your first release tag"
    echo ""
else
    echo -e "${RED}❌ Error pushing to repository${NC}"
    echo "This might happen if:"
    echo "1. Repository doesn't exist yet"
    echo "2. Authentication issues"
    echo "3. Network connectivity"
    echo ""
    echo "Manual push command:"
    echo "git push rag-pro main"
fi

echo ""
echo -e "${BLUE}📊 Repository status:${NC}"
git remote -v
echo ""
echo -e "${GREEN}🎯 Setup script completed!${NC}"
