# River's Toy Room - Push to GitHub Pages Script
# Run this from the project folder on your local machine (where Git is installed)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Preparing River's Toy Room for GitHub Pages..." -ForegroundColor Cyan

# Change to the script directory
Set-Location $PSScriptRoot

# Initialize git if needed
if (-not (Test-Path ".git")) {
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
}

# Add all files
git add .

# Commit if there are changes
$status = git status --porcelain
if ($status) {
    Write-Host "Committing changes..." -ForegroundColor Yellow
    git commit -m "Deploy River's Toy Room to GitHub Pages"
} else {
    Write-Host "No new changes to commit." -ForegroundColor Green
}

# Set remote (idempotent)
$remote = "https://github.com/MojoMikeTaylor/RiverToyRoom.git"
git remote remove origin 2>$null
git remote add origin $remote

# Push to main
Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
git branch -M main
git push -u origin main

Write-Host ""
Write-Host "✅ Push complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "1. Go to https://github.com/MojoMikeTaylor/RiverToyRoom/settings/pages" -ForegroundColor White
Write-Host "2. Under 'Build and deployment', set Source to 'Deploy from a branch'" -ForegroundColor White
Write-Host "3. Select branch 'main' and folder '/ (root)'" -ForegroundColor White
Write-Host "4. Save" -ForegroundColor White
Write-Host ""
Write-Host "Your site will be live at: https://MojoMikeTaylor.github.io/RiverToyRoom/" -ForegroundColor Cyan
Write-Host ""
Write-Host "After enabling Pages, remember to verify the Open Graph URLs in index.html point correctly." -ForegroundColor Yellow
.\push-to-github.ps1
