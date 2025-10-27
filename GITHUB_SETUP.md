# GitHub Repository Setup

This guide will help you connect this local repository to your GitHub account.

## Quick Setup (Option 1: Using GitHub CLI)

```bash
# Install GitHub CLI if you haven't already
# macOS: brew install gh
# Then authenticate
gh auth login

# Create repository and push
gh repo create fal_serverless_stock_image_inspirations --public --source=. --remote=origin --push
```

## Manual Setup (Option 2: Using Git Commands)

### Step 1: Create a New Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `fal_serverless_stock_image_inspirations`
3. Description: "FAL.ai Serverless deployment for Stock Image Inspirations - AI-powered prompt generation for stock photography"
4. Choose **Public** or **Private**
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### Step 2: Connect Local Repository to GitHub

Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username:

```bash
cd /Users/burak/Desktop/repos/fal_serverless_stock_image_inspirations

# Add remote origin
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/fal_serverless_stock_image_inspirations.git

# Or if you prefer SSH:
# git remote add origin [email protected]:YOUR_GITHUB_USERNAME/fal_serverless_stock_image_inspirations.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Verify Connection

```bash
# Check remote
git remote -v

# Should show:
# origin  https://github.com/YOUR_USERNAME/fal_serverless_stock_image_inspirations.git (fetch)
# origin  https://github.com/YOUR_USERNAME/fal_serverless_stock_image_inspirations.git (push)
```

## Repository Description Suggestion

**Title:** FAL Serverless Stock Image Inspirations

**Description:** 
AI-powered stock image prompt generator deployed on FAL.ai Serverless. Generates creative, optimized prompts with keywords and style tags for professional stock photography.

**Topics/Tags:**
- `fal-ai`
- `serverless`
- `stock-photography`
- `ai-prompts`
- `image-generation`
- `openai`
- `gpt-4`
- `prompt-engineering`

## After Pushing to GitHub

1. **Add repository secrets** (for GitHub Actions, if needed):
   - Go to Settings → Secrets and variables → Actions
   - Add: `OPENAI_API_KEY`, `FAL_API_KEY`

2. **Update README badges** (optional):
   ```markdown
   ![License](https://img.shields.io/github/license/YOUR_USERNAME/fal_serverless_stock_image_inspirations)
   ![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
   ![FAL](https://img.shields.io/badge/FAL-Serverless-purple)
   ```

3. **Enable GitHub Pages** (optional):
   - Settings → Pages → Source: Deploy from main branch

## Collaborative Development

If you want to collaborate:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/fal_serverless_stock_image_inspirations.git
cd fal_serverless_stock_image_inspirations

# Create a branch
git checkout -b feature/new-feature

# Make changes, commit, and push
git add .
git commit -m "Add new feature"
git push origin feature/new-feature

# Then create a Pull Request on GitHub
```

## Keeping it Updated

```bash
# Pull latest changes
git pull origin main

# Make changes
git add .
git commit -m "Your commit message"
git push origin main
```

## Troubleshooting

### Authentication Issues

If you have trouble with HTTPS authentication:
1. Use SSH instead (more secure)
2. Or use GitHub Personal Access Token

To create a PAT:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Select scopes: `repo` (full control)
4. Use the token as password when pushing

### Remote Already Exists

```bash
# Remove existing remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/YOUR_USERNAME/fal_serverless_stock_image_inspirations.git
```

## Next Steps

After pushing to GitHub:
1. Deploy to FAL.ai: `./deploy.sh`
2. Update README with your actual endpoint URL
3. Share with collaborators
4. Set up CI/CD (optional)

## Support

- GitHub Docs: https://docs.github.com
- Git Documentation: https://git-scm.com/doc
- FAL.ai Documentation: https://docs.fal.ai

