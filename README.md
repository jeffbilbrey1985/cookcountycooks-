# 🍳 Cook County Cooks — Autonomous Daily Sales Board

Every morning at 9:15 AM, this repo automatically reads your latest Blufox Sales Report
Excel file and rebuilds the live sales board. No action required from you.

**Live URL:** `https://YOUR-USERNAME.github.io/cookcountycooks/`

---

## How It Works

```
9:00 AM  →  Blufox email arrives in your Outlook inbox
9:01 AM  →  Power Automate saves the Excel to OneDrive
9:05 AM  →  Power Automate pushes Excel to this GitHub repo (data/ folder)
9:15 AM  →  GitHub Actions runs, rebuilds index.html from the Excel
9:16 AM  →  Live website updates automatically
            Every store TV refreshes within 60 seconds
```

---

## One-Time Setup (~30 minutes total)

### STEP 1 — Create a GitHub Account & Repo (5 min)

1. Go to **github.com** → Sign Up (use your work email)
2. Click **+** → **New repository**
3. Name it: `cookcountycooks`
4. Set it to **Public**
5. Click **Create repository**
6. Upload all these files by dragging them into the GitHub browser window

### STEP 2 — Enable GitHub Pages (2 min)

1. In your repo → click **Settings** (top nav)
2. Scroll down to **Pages** (left sidebar)
3. Under **Source** → select **GitHub Actions**
4. Click **Save**

Your board will be live at:
`https://YOUR-GITHUB-USERNAME.github.io/cookcountycooks/`

### STEP 3 — Test the Build Manually (2 min)

1. In your repo → click **Actions** tab
2. Click **Daily Sales Board Update** (left sidebar)
3. Click **Run workflow** → **Run workflow** (green button)
4. Wait ~60 seconds → your `index.html` will be built and the site will go live

### STEP 4 — Set Up Power Automate to Save Email Attachment (15 min)

Power Automate will watch for your daily Blufox email and automatically save
the Excel attachment to this GitHub repo.

1. Go to **make.powerautomate.com** (sign in with your Microsoft 365 account)
2. Click **+ Create** → **Automated cloud flow**
3. Name it: `Save Daily Sales Report to GitHub`
4. Choose trigger: **When a new email arrives (Outlook)**
5. Set filters:
   - **From:** [the Blufox sender email address]
   - **Has attachment:** Yes
   - **Subject contains:** `Sales Report` (or whatever the subject line is)
6. Add action: **Get attachment (Outlook)**
7. Add action: **HTTP** (this sends the file to GitHub)
   - Method: `PUT`
   - URI: `https://api.github.com/repos/YOUR-USERNAME/cookcountycooks/contents/data/latest_report.xlsx`
   - Headers:
     ```
     Authorization: token YOUR_GITHUB_TOKEN
     Content-Type: application/json
     ```
   - Body:
     ```json
     {
       "message": "Auto-update: daily sales report",
       "content": "@{base64(triggerOutputs()?['body/attachments/0/contentBytes'])}",
       "sha": "@{body('Get_file_metadata')?['sha']}"
     }
     ```

> **Note on GitHub Token:** You'll need to create a Personal Access Token:
> - GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
> - Click Generate new token → check `repo` scope → Generate → Copy it immediately
> - Paste it into the Power Automate HTTP action above

### STEP 5 — Point Every Store TV to the Live URL (5 min)

On each store TV/computer:
1. Open Chrome
2. Go to: `https://YOUR-USERNAME.github.io/cookcountycooks/`
3. Press **F11** for fullscreen
4. The page auto-refreshes every 15 seconds — it will pick up the new data by 9:16 AM

**Optional — Set it as the Chrome startup page:**
- Chrome Settings → On startup → Open a specific page → paste the URL

---

## Folder Structure

```
cookcountycooks/
├── .github/
│   └── workflows/
│       └── update.yml          ← GitHub Actions automation
├── scripts/
│   ├── build.py                ← Python script that builds the HTML
│   ├── template.html           ← HTML template (design lives here)
│   └── logo.b64                ← Cook County Cooks logo (base64)
├── data/
│   └── latest_report.xlsx      ← Power Automate drops the Excel here
├── index.html                  ← Auto-generated daily (don't edit this)
├── requirements.txt
└── README.md
```

---

## Updating the Design

If you ever want to change how the board looks:
1. Edit `scripts/template.html`
2. Commit and push → GitHub Actions will rebuild with the new design

---

## Manual Update (If Email Doesn't Arrive)

If you need to push a manual update:
1. Go to your GitHub repo → `data/` folder
2. Click **Upload files**
3. Drag in the new Excel file (name it `latest_report.xlsx`)
4. Click **Commit changes**
5. GitHub Actions triggers automatically → board updates in ~60 seconds

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Board didn't update | Check **Actions** tab for any red X failures |
| Excel not found | Make sure file is in `data/` folder, named `latest_report.xlsx` |
| Site shows old data | Hard refresh: Ctrl+Shift+R on the TV browser |
| Power Automate failed | Check the flow run history in make.powerautomate.com |
| GitHub Pages not loading | Go to Settings → Pages and confirm it's enabled |

---

## Support

Built by Claude for Cook County Cooks.
Password to upload reports via the board UI: `Password123!`
