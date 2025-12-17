# API Setup Guide for JobMatchAI

## Required API Keys

You need to sign up for these FREE APIs to enable job searching:

---

## 1. Adzuna API (FREE - UK Jobs) ⭐ **RECOMMENDED**

**What it does:** Fetches jobs from multiple UK job boards (Indeed, Reed, CV-Library, etc.)

**Setup Time:** 5 minutes

**Steps:**
1. Go to: **https://developer.adzuna.com/signup**
2. Fill in:
   - Email: Your email
   - Name: Your name
   - Description: "Student project for job search automation"
3. Click "Create Account"
4. Check your email for confirmation
5. Once confirmed, go to: **https://developer.adzuna.com/dashboard**
6. Copy your:
   - **App ID** (looks like: `12345678`)
   - **API Key** (looks like: `abc123def456ghi789jkl012mno345pq`)

**Free Tier:** 250 API calls/month (more than enough for our demo)

**Documentation:** https://developer.adzuna.com/docs

---

## 2. Reed API (FREE - UK Jobs) ⭐ **RECOMMENDED**

**What it does:** Accesses Reed.co.uk job listings (one of UK's largest job boards)

**Setup Time:** 3 minutes

**Steps:**
1. Go to: **https://www.reed.co.uk/developers/jobseeker**
2. Click "Get your API key"
3. Fill in the form:
   - Email: Your email
   - Name: Your name
   - Company: "University Project"
   - Description: "AI-powered job search assistant for coursework"
4. Submit form
5. Check your email - they'll send your API key immediately
6. Copy your **API Key** (looks like: `a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6`)

**Free Tier:** Unlimited API calls! 🎉

**Documentation:** https://www.reed.co.uk/developers/jobseeker

---

## 3. JSearch API via RapidAPI (FREE Tier Available) 

**What it does:** Aggregates jobs from Google Jobs, LinkedIn, Indeed, Glassdoor globally

**Setup Time:** 5 minutes

**Steps:**
1. Go to: **https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch**
2. Click "Sign Up" (top right) if you don't have RapidAPI account
3. Once logged in, click "Subscribe to Test"
4. Choose **FREE Plan** (Basic - 2,500 requests/month)
5. Click "Subscribe"
6. Go to "Code Snippets" tab
7. Copy your **RapidAPI Key** from the headers (looks like: `xyz123abc456def789ghi012jkl345mno`)

**Free Tier:** 2,500 API calls/month

**Documentation:** https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch

---

## 4. OpenAI API (You already have this! ✓)

**What it does:** Powers cover letter generation and CV analysis

**Status:** Already configured in your NeuroLearn project

**We'll reuse your existing key!**

---

## Save Your API Keys

Once you have all your keys, create a file called `.env` in the `JobMatchAI/backend` folder:

```env
# Adzuna API
ADZUNA_APP_ID=your_app_id_here
ADZUNA_API_KEY=your_api_key_here

# Reed API
REED_API_KEY=your_api_key_here

# JSearch API (RapidAPI)
RAPIDAPI_KEY=your_rapidapi_key_here

# OpenAI API
OPENAI_API_KEY=your_existing_openai_key
```

---

## Quick Links Summary

1. **Adzuna:** https://developer.adzuna.com/signup
2. **Reed:** https://www.reed.co.uk/developers/jobseeker
3. **JSearch (RapidAPI):** https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch

---

## Notes

- All three job APIs are **completely FREE** for our usage level
- No credit card required for free tiers
- Setup takes ~15 minutes total
- APIs are legal and approved for educational/research use

---

## Need Help?

If you encounter any issues during signup, let me know and I'll help troubleshoot!

Once you have the API keys, paste them into the `.env` file and we're ready to start fetching jobs! 🚀
