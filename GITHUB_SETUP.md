# Pushing to GitHub

## Prerequisites

- Git installed (`brew install git`)
- GitHub account
- GitHub CLI (optional but recommended: `brew install gh`)

---

## Step 1: Create .gitignore

```bash
cd ~/Documents/MusicOrganizer

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
.Python
*.so
.env
venv/
ENV/

# macOS
.DS_Store
._*

# Temp files
*.log
*.tmp
/tmp/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Output files
tagging_results.json
music_metadata.txt
EOF
```

---

## Step 2: Initialize Git Repository

```bash
cd ~/Documents/MusicOrganizer

# Initialize repo
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Music organizer scripts for Rekordbox

- enrich_tags.py: MusicBrainz API tag enrichment
- resort_by_tags.py: Genre-based file organization
- organize_music.sh: Artist/Album organization
- organize_by_genre.sh: Manual genre mapping organization
- Documentation for all scripts

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Step 3: Create GitHub Repository

### Option A: Using GitHub CLI (recommended)

```bash
# Login to GitHub (first time only)
gh auth login

# Create repo and push
gh repo create MusicOrganizer --public --source=. --remote=origin --push
```

### Option B: Manual via GitHub.com

1. Go to https://github.com/new
2. Repository name: `MusicOrganizer`
3. Description: `Scripts to organize music files for Rekordbox with MusicBrainz integration`
4. Select: Public
5. Do NOT initialize with README (we already have one)
6. Click "Create repository"
7. Copy the commands shown, or run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/MusicOrganizer.git
git branch -M main
git push -u origin main
```

---

## Step 4: Create Development Branch

```bash
# Create and switch to develop branch
git checkout -b develop

# Push develop branch to GitHub
git push -u origin develop
```

---

## Step 5: Set Up Branch Protection (GitHub.com)

1. Go to your repo on GitHub
2. Click **Settings** → **Branches**
3. Click **Add branch protection rule**

### For `main` branch:
- Branch name pattern: `main`
- Check: ✅ Require a pull request before merging
- Check: ✅ Require approvals (set to 1)
- Check: ✅ Dismiss stale pull request approvals when new commits are pushed
- Check: ✅ Require status checks to pass before merging (optional)
- Click **Create**

### For `develop` branch:
- Branch name pattern: `develop`
- Check: ✅ Require a pull request before merging
- Click **Create**

---

## Step 6: Set Default Branch to `develop`

1. Go to **Settings** → **General**
2. Under "Default branch", click the swap icon
3. Select `develop`
4. Click **Update**

This ensures contributors branch from `develop` by default.

---

## Workflow for Future Changes

### Adding a new feature:

```bash
# Make sure you're on develop and up to date
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/add-spotify-integration

# Make changes...
# ...

# Commit changes
git add .
git commit -m "Add Spotify API integration for playlist metadata"

# Push feature branch
git push -u origin feature/add-spotify-integration

# Create pull request on GitHub (develop ← feature/add-spotify-integration)
gh pr create --base develop --title "Add Spotify integration" --body "Description here"
```

### Releasing to main:

```bash
# After features are tested in develop
git checkout main
git pull origin main
git merge develop
git push origin main

# Tag the release
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `git checkout develop` | Switch to develop branch |
| `git checkout -b feature/name` | Create new feature branch |
| `git push -u origin branch-name` | Push new branch to GitHub |
| `gh pr create` | Create pull request |
| `git tag -a v1.0.0 -m "msg"` | Create version tag |

---

## Repository Structure

```
MusicOrganizer/
├── .gitignore
├── README.md              # Project overview
├── CONTRIBUTING.md        # Contribution guidelines
├── GITHUB_SETUP.md        # This file
├── enrich_tags.py         # MusicBrainz enrichment
├── enrich_tags.md
├── resort_by_tags.py      # Tag-based sorting
├── resort_by_tags.md
├── organize_music.sh      # Artist/Album organization
├── organize_music.md
├── organize_by_genre.sh   # Genre mapping organization
├── organize_by_genre.md
└── genre_map_example.txt  # Sample genre mapping
```
