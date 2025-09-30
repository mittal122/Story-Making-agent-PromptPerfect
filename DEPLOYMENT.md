# Vercel Deployment Guide for PromptPerfect

## Quick Setup Steps

### 1. Prepare for Deployment

```bash
# Ensure you're in the project root
cd PromptPerfect

# Install Vercel CLI (if not already installed)
npm install -g vercel

# Login to Vercel
vercel login
```

### 2. Deploy to Vercel

```bash
# Deploy the project
vercel

# Follow the prompts:
# ? Set up and deploy "~/PromptPerfect"? [Y/n] y
# ? Which scope do you want to deploy to? [Your Account]
# ? Link to existing project? [y/N] n
# ? What's your project's name? promptperfect
# ? In which directory is your code located? ./
```

### 3. Set Environment Variables

After deployment, add these environment variables in your Vercel dashboard:

1. Go to your project in Vercel dashboard
2. Click on "Settings"
3. Click on "Environment Variables"
4. Add:

```
GEMINI_API_KEY=your_gemini_api_key_here
SESSION_SECRET=your_random_session_secret
```

### 4. Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the key and paste it in Vercel environment variables

### 5. Redeploy

After setting environment variables:

```bash
vercel --prod
```

## Your app will be live at the URL provided by Vercel!

## Troubleshooting

- **Build fails**: Make sure all files are committed to Git
- **API errors**: Check that GEMINI_API_KEY is set correctly in Vercel
- **404 errors**: Ensure the vercel.json routing is correct

## File Structure for Vercel

```
PromptPerfect/
├── api/
│   ├── index.py              # Python API endpoint
│   ├── gemini_service.py     # AI service
│   └── requirements.txt      # Python deps
├── frontend/frontend/
│   ├── dist/                 # Built React app (generated)
│   ├── src/
│   └── package.json
├── vercel.json               # Vercel configuration
└── package.json             # Root package.json
```
