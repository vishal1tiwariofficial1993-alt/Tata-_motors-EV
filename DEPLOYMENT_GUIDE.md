# Deploy Tata Motors EV App on Vercel

## Prerequisites
- GitHub account
- Vercel account (free at https://vercel.com)
- Git installed on your machine

## Step-by-Step Deployment

### 1. **Initialize Git Repository**
```bash
cd "c:\Users\vtt529465\OneDrive - TATA MOTORS LTD\Pictures\Camera Roll\tata-ev-app"
git init
git add .
git commit -m "Initial commit: Tata Motors EV Web Application"
```

### 2. **Push to GitHub**
- Create a new repository on GitHub (https://github.com/new)
- Name it `tata-ev-app`
- Don't initialize with README
- Copy the commands from GitHub and run:
```bash
git remote add origin https://github.com/YOUR-USERNAME/tata-ev-app.git
git branch -M main
git push -u origin main
```

### 3. **Deploy to Vercel**

#### Option A: Using Vercel Dashboard (Easiest)
1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Click "Import Git Repository"
4. Select your `tata-ev-app` repository
5. Configure project:
   - **Framework Preset**: Other
   - **Root Directory**: ./
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
6. Click "Deploy"
7. Wait for deployment to complete
8. Your app will be live at `https://your-project.vercel.app`

#### Option B: Using Vercel CLI
```bash
# Install Vercel CLI globally
npm install -g vercel

# Deploy from project directory
cd "c:\Users\vtt529465\OneDrive - TATA MOTORS LTD\Pictures\Camera Roll\tata-ev-app"
vercel

# Follow the prompts
# Choose "Y" when asked to link to existing project
# Select your account and project
```

### 4. **Set Environment Variables (if needed)**
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add any environment variables:
   - `FLASK_ENV`: production
   - `FLASK_APP`: backend/app.py
3. Re-deploy to apply changes

### 5. **Custom Domain (Optional)**
1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

## Project Structure for Vercel
```
tata-ev-app/
├── api/
│   └── index.py              # Serverless function handler
├── backend/
│   ├── app.py                # Flask application
│   ├── modules/              # Business logic modules
│   ├── templates/            # HTML templates
│   ├── static/               # CSS and JavaScript
│   ├── requirements.txt       # Python dependencies
│   └── test_app.py          # Tests
├── vercel.json               # Vercel configuration
├── wsgi.py                   # WSGI entry point
├── .vercelignore            # Files to ignore
├── .gitignore               # Git ignore
└── README.md                # Project documentation
```

## Important Notes

1. **Python Runtime**: Vercel supports Python 3.8+
2. **Cold Start**: Serverless functions may have a slight delay on first request
3. **Memory Limit**: 512MB for serverless functions (sufficient for this app)
4. **Pricing**: Free tier includes 100GB bandwidth/month
5. **Auto-deployments**: Every push to main branch auto-deploys

## Troubleshooting

### Issue: 502 Bad Gateway
- Check `requirements.txt` has all dependencies
- Verify Flask is version 2.3.3 or compatible
- Check Vercel logs: Dashboard → Project → Deployments → View Details

### Issue: Missing static files
- Ensure static files are in `backend/static/`
- Check paths in templates are correct
- Verify CSS and JS are loading (check browser console)

### Issue: Templates not found
- Verify `templates/` directory exists in `backend/`
- Check `render_template()` paths in app.py

## After Deployment

1. **Share your live URL**: `https://your-project.vercel.app`
2. **Test all features**:
   - Try EV Recommender
   - Test Range Simulator
   - Use Cost Comparison
   - Find Chargers
   - Book Test Drive
   - Chat with AI

3. **Monitor performance**: Dashboard → Analytics

## Update & Redeploy

To update your app after making changes:
```bash
git add .
git commit -m "Update: description of changes"
git push origin main
```
Vercel will automatically redeploy!

## Support

- Vercel Docs: https://vercel.com/docs
- Flask Docs: https://flask.palletsprojects.com
- GitHub: https://github.com

---

**Your app is ready to go global! 🚀⚡**
