## Vercel Python API Deployment

This project is ready for deployment on Vercel as a Python serverless function.

### Structure
- `api/index.py`: Main Flask app entry point (Vercel serverless function)
- `requirements.txt`: Python dependencies
- `static/` and `templates/`: For HTML/CSS/JS assets

### Steps to Deploy
1. Push your changes to GitHub.
2. Go to [Vercel](https://vercel.com/) and import your GitHub repository.
3. Vercel will auto-detect the `api` directory and deploy your Python API.
4. Your Flask routes will be available as serverless endpoints.

**Note:** Vercel is not designed for full Flask servers, but for serverless functions. For full backend hosting, consider Render or Railway.
