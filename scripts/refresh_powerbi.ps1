# refresh_powerbi.ps1

# Path to Power BI .pbix file
$pbixPath = "D:\CROWD-ANALYSIS-Project\powerBI\Crowd_Analysis_Dashboard.pbix"

# Power BI Desktop executable path
$powerBIPath = "C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe"

# Start Power BI with the report
Start-Process -FilePath $powerBIPath -ArgumentList "`"$pbixPath`""

# Wait 5 minutes for auto-refresh to complete
Start-Sleep -Seconds 300

# Close Power BI (optional)
Get-Process -Name PBIDesktop -ErrorAction SilentlyContinue | Stop-Process -Force
