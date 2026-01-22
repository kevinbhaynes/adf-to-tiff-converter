# Desktop Organizer Script
# This script organizes files on your Desktop into categorized folders

$DesktopPath = "$env:USERPROFILE\OneDrive - University of South Carolina\Desktop"

# Define folder categories
$folders = @{
    "Documents" = @("*.pdf", "*.doc", "*.docx", "*.txt", "*.rtf", "*.odt", "*.xls", "*.xlsx", "*.ppt", "*.pptx", "*.csv")
    "Images" = @("*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.svg", "*.ico", "*.tif", "*.tiff", "*.webp", "*.heic")
    "Videos" = @("*.mp4", "*.avi", "*.mkv", "*.mov", "*.wmv", "*.flv", "*.webm", "*.m4v")
    "Audio" = @("*.mp3", "*.wav", "*.flac", "*.aac", "*.ogg", "*.wma", "*.m4a")
    "Archives" = @("*.zip", "*.rar", "*.7z", "*.tar", "*.gz", "*.bz2", "*.iso")
    "Code" = @("*.py", "*.js", "*.html", "*.css", "*.java", "*.cpp", "*.c", "*.h", "*.cs", "*.php", "*.rb", "*.go", "*.rs", "*.sql", "*.json", "*.xml", "*.yaml", "*.yml")
    "Executables" = @("*.exe", "*.msi", "*.bat", "*.cmd", "*.ps1", "*.sh")
    "Shortcuts" = @("*.lnk", "*.url")
}

Write-Host "Desktop Organizer - Starting..." -ForegroundColor Cyan
Write-Host "Working on: $DesktopPath" -ForegroundColor Yellow
Write-Host ""

# Check if Desktop exists
if (-not (Test-Path $DesktopPath)) {
    Write-Host "Error: Desktop path not found: $DesktopPath" -ForegroundColor Red
    exit
}

# Create a backup timestamp
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Write-Host "Backup timestamp: $timestamp" -ForegroundColor Gray
Write-Host ""

# Get all files on Desktop (excluding folders)
$files = Get-ChildItem -Path $DesktopPath -File

if ($files.Count -eq 0) {
    Write-Host "Your Desktop is already clean - no files to organize!" -ForegroundColor Green
    exit
}

Write-Host "Found $($files.Count) files to organize..." -ForegroundColor Yellow
Write-Host ""

# Create category folders if they don't exist
foreach ($folder in $folders.Keys) {
    $folderPath = Join-Path $DesktopPath $folder
    if (-not (Test-Path $folderPath)) {
        New-Item -Path $folderPath -ItemType Directory | Out-Null
        Write-Host "Created folder: $folder" -ForegroundColor Green
    }
}

# Create "Other" folder for uncategorized files
$otherPath = Join-Path $DesktopPath "Other"
if (-not (Test-Path $otherPath)) {
    New-Item -Path $otherPath -ItemType Directory | Out-Null
    Write-Host "Created folder: Other" -ForegroundColor Green
}

Write-Host ""
Write-Host "Organizing files..." -ForegroundColor Cyan
Write-Host ""

# Move files to appropriate folders
$movedCount = 0
$skippedCount = 0

foreach ($file in $files) {
    # Skip this script itself
    if ($file.Name -eq "Organize-Desktop.ps1") {
        continue
    }

    $moved = $false

    # Check which category the file belongs to
    foreach ($category in $folders.Keys) {
        foreach ($extension in $folders[$category]) {
            if ($file.Name -like $extension) {
                $destinationPath = Join-Path $DesktopPath $category
                $destinationFile = Join-Path $destinationPath $file.Name

                # Handle duplicate filenames
                if (Test-Path $destinationFile) {
                    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
                    $ext = [System.IO.Path]::GetExtension($file.Name)
                    $counter = 1

                    while (Test-Path $destinationFile) {
                        $newName = "${baseName}_${counter}${ext}"
                        $destinationFile = Join-Path $destinationPath $newName
                        $counter++
                    }
                }

                try {
                    Move-Item -Path $file.FullName -Destination $destinationFile -ErrorAction Stop
                    Write-Host "  Moved: $($file.Name) -> $category" -ForegroundColor Gray
                    $movedCount++
                    $moved = $true
                    break
                } catch {
                    Write-Host "  ERROR moving $($file.Name): $_" -ForegroundColor Red
                    $skippedCount++
                }
            }
        }
        if ($moved) { break }
    }

    # If file doesn't match any category, move to "Other"
    if (-not $moved) {
        $destinationFile = Join-Path $otherPath $file.Name

        # Handle duplicate filenames
        if (Test-Path $destinationFile) {
            $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
            $ext = [System.IO.Path]::GetExtension($file.Name)
            $counter = 1

            while (Test-Path $destinationFile) {
                $newName = "${baseName}_${counter}${ext}"
                $destinationFile = Join-Path $otherPath $newName
                $counter++
            }
        }

        try {
            Move-Item -Path $file.FullName -Destination $destinationFile -ErrorAction Stop
            Write-Host "  Moved: $($file.Name) -> Other" -ForegroundColor Gray
            $movedCount++
        } catch {
            Write-Host "  ERROR moving $($file.Name): $_" -ForegroundColor Red
            $skippedCount++
        }
    }
}

Write-Host ""
Write-Host "Organization complete!" -ForegroundColor Green
Write-Host "Files moved: $movedCount" -ForegroundColor Yellow
if ($skippedCount -gt 0) {
    Write-Host "Files skipped (errors): $skippedCount" -ForegroundColor Red
}

# Remove empty folders
Write-Host ""
Write-Host "Cleaning up empty folders..." -ForegroundColor Cyan
$allFolders = @($folders.Keys) + @("Other")
foreach ($folderName in $allFolders) {
    $folderPath = Join-Path $DesktopPath $folderName
    if ((Test-Path $folderPath) -and ((Get-ChildItem $folderPath).Count -eq 0)) {
        Remove-Item $folderPath
        Write-Host "  Removed empty folder: $folderName" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Your Desktop has been organized! 🎉" -ForegroundColor Green
