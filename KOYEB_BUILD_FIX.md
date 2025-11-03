# Koyeb Build Fix - Exit Code 51

## Problem
Koyeb build fails with exit code 51 - buildpack/build step failed.

## Solutions

### Solution 1: Use Dockerfile Explicitly (RECOMMENDED ✅)

In Koyeb dashboard:

1. **Go to your service settings**
2. **Find "Build & Deploy" or "Advanced" section**
3. **Set Build Type to "Dockerfile"** (instead of "Nixpacks" or "Auto")
4. **Dockerfile Path:** Leave empty or set to `Dockerfile`
5. **Save and redeploy**

This tells Koyeb to use your Dockerfile directly instead of buildpacks.

---

### Solution 2: Fix Buildpack Detection

If Solution 1 doesn't work:

1. **In Koyeb dashboard:**
   - Go to your service settings
   - **Root Directory:** Make sure it's set to `backend`
   - **Build Command:** Leave EMPTY (let Koyeb auto-detect)
   - **Run Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Ensure these files exist in `backend/` directory:**
   - ✅ `requirements.txt`
   - ✅ `Procfile` (with: `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`)
   - ✅ `runtime.txt` (with: `python-3.12.7`)

3. **Redeploy**

---

### Solution 3: Use Nixpacks Config

If Koyeb uses Nixpacks:

1. **Make sure `nixpacks.toml` is in `backend/` directory**
2. **In Koyeb:**
   - Set Build Type to "Nixpacks"
   - Root Directory: `backend`
3. **Redeploy**

---

### Solution 4: Simplify - Remove Tesseract Temporarily

If still failing, try without Tesseract first:

1. **Comment out Tesseract in your code temporarily** to verify build works
2. **Test basic deployment**
3. **Then add Tesseract back**

---

## Quick Fix Steps:

1. **In Koyeb Dashboard:**
   - Service → Settings → Build & Deploy
   - Change "Build Type" to **"Dockerfile"**
   - Save

2. **Redeploy:**
   - Click "Redeploy" or push a new commit

3. **Check Logs:**
   - Service → Logs
   - Watch for specific errors

---

## Most Likely Fix:

**Change Koyeb build type to "Dockerfile"** - This will use your Dockerfile which properly installs Tesseract and all dependencies.

The updated Dockerfile I just created:
- ✅ Installs Tesseract correctly
- ✅ Installs build tools (gcc, g++)
- ✅ Upgrades pip first
- ✅ Uses no-cache for faster builds

---

## If Still Failing:

**Check Koyeb logs** and look for:
- Specific error messages
- Which step fails (setup, install, build, deploy)
- Python version issues
- Missing dependencies

Share the specific error from logs and I can help fix it!

