# River's Toy Room - Push to GitHub Pages Script
# Run this from the project folder on your local machine

$ErrorActionPreference = "Stop"

Write-Host "🚀 River's Toy Room → GitHub Pages Deploy Script" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git is not installed or not in your PATH." -ForegroundColor Red
    Write-Host "Please install Git for Windows: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Move to script directory
Set-Location $PSScriptRoot

# Initialize repository if needed
if (-not (Test-Path ".git")) {
    Write-Host "Initializing new git repository..." -ForegroundColor Yellow
    git init
}

# Stage all files
Write-Host "Staging files..." -ForegroundColor Yellow
git add .

# Commit changes if any
$changes = git status --porcelain
if ($changes) {
    Write-Host "Committing changes..." -ForegroundColor Yellow
    git commit -m "Deploy River's Toy Room to GitHub Pages"
} else {
    Write-Host "No new changes to commit." -ForegroundColor Green
}

# Configure remote
$remoteUrl = "https://github.com/MojoMikeTaylor/RiverToyRoom.git"
Write-Host "Setting remote origin to $remoteUrl" -ForegroundColor Yellow

# Remove existing remote if present (to avoid duplicates)
git remote remove origin 2>$null
git remote add origin $remoteUrl

# Ensure we're on main branch
git branch -M main

# Confirmation before push
Write-Host ""
Write-Host "Ready to push to GitHub." -ForegroundColor Cyan
Write-Host "Repository: $remoteUrl" -ForegroundColor White
$confirm = Read-Host "Do you want to continue with the push? (Y/N)"

if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "Push cancelled by user." -ForegroundColor Yellow
    exit 0
}

# Perform the push with robust error handling
Write-Host ""
Write-Host "Pushing to GitHub (this may ask for your GitHub credentials)..." -ForegroundColor Cyan

try {
    git push -u origin main 2>&1 | Tee-Object -Variable pushOutput

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Push successful!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps to enable GitHub Pages:" -ForegroundColor White
        Write-Host "1. Go to: https://github.com/MojoMikeTaylor/RiverToyRoom/settings/pages" -ForegroundColor White
        Write-Host "2. Under 'Build and deployment' → Source: Deploy from a branch" -ForegroundColor White
        Write-Host "3. Branch: main   |   Folder: / (root)" -ForegroundColor White
        Write-Host "4. Click Save" -ForegroundColor White
        Write-Host ""
        Write-Host "Your site will be live at:" -ForegroundColor Green
        Write-Host "https://MojoMikeTaylor.github.io/RiverToyRoom/" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "After Pages is enabled, open the live site and verify the social sharing images work." -ForegroundColor Yellow
    } else {
        throw "Push command failed with exit code $LASTEXITCODE"
    }

} catch {
    Write-Host ""
    Write-Host "❌ Push failed!" -ForegroundColor Red
    Write-Host ""

    $errorText = $_.Exception.Message + " " + $pushOutput

    if ($errorText -match "repository not found" -or $errorText -match "does not exist") {
        Write-Host "Common cause: The repository 'RiverToyRoom' does not exist on GitHub yet." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Please do this first:" -ForegroundColor White
        Write-Host "1. Go to https://github.com/new" -ForegroundColor White
        Write-Host "2. Create a new repository named exactly: RiverToyRoom" -ForegroundColor White
        Write-Host "3. Do NOT initialize it with a README, .gitignore, or license" -ForegroundColor White
        Write-Host "4. Run this script again after creating the repo." -ForegroundColor White
    }
    elseif ($errorText -match "Authentication failed" -or $errorText -match "could not read Username" -or $errorText -match "403") {
        Write-Host "Authentication failed." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Solutions:" -ForegroundColor White
        Write-Host "A) Use a Personal Access Token (recommended):" -ForegroundColor White
        Write-Host "   - Go to: https://github.com/settings/tokens" -ForegroundColor White
        Write-Host "   - Generate new token (classic) with 'repo' scope" -ForegroundColor White
        Write-Host "   - When prompted for password, paste the token instead of your GitHub password" -ForegroundColor White
        Write-Host ""
        Write-Host "B) Or install GitHub CLI (easiest long-term):" -ForegroundColor White
        Write-Host "   winget install --id GitHub.cli" -ForegroundColor White
        Write-Host "   Then run: gh auth login" -ForegroundColor White
    }
    else {
        Write-Host "Error details:" -ForegroundColor Yellow
        Write-Host $errorText -ForegroundColor Red
        Write-Host ""
        Write-Host "If you're stuck, copy the error above and send it here." -ForegroundColor White
    }

    exit 1
}
