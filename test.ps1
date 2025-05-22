<#
.SYNOPSIS
    Performs a DNS lookup for a specified domain.

.DESCRIPTION
    This script uses the Resolve-DnsName cmdlet to query DNS records for a given domain.
    It will display information such as the IP addresses (A records), CNAMEs, etc.
    It's a basic tool for simulating network reconnaissance.

.NOTES
    Author: Gemini
    Date: May 22, 2025
    Version: 1.0

.EXAMPLE
    .\Lookup-Mandiant.ps1
    (Executes the script to lookup mandiant.com)
#>

# Ensure the script runs with necessary permissions if needed (though Resolve-DnsName typically doesn't require elevated rights)
# This check is more for general best practice in scripts that might do more sensitive operations.
# if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
#     Write-Warning "This script might require Administrator privileges for certain DNS operations. Please run as Administrator if issues occur."
# }

# Define the target domain for the DNS lookup
$TargetDomain = "mandiant.com"

Write-Host "`n"
Write-Host "----------------------------------------------------" -ForegroundColor Cyan
Write-Host "  Performing DNS Lookup for: $($TargetDomain)" -ForegroundColor Green
Write-Host "----------------------------------------------------" -ForegroundColor Cyan
Write-Host "`n"

# Perform the DNS lookup using Resolve-DnsName
# This cmdlet is available in PowerShell 3.0 and later.
# It provides detailed DNS record information.
try {
    $DnsRecords = Resolve-DnsName -Name $TargetDomain -DnsOnly -ErrorAction Stop

    # Display the results
    if ($DnsRecords) {
        Write-Host "DNS Records found for $($TargetDomain):" -ForegroundColor Yellow
        Write-Host "----------------------------------------------------" -ForegroundColor Yellow
        $DnsRecords | Format-Table -AutoSize

        # Extract and display A records (IPv4 addresses) specifically
        $ARecords = $DnsRecords | Where-Object {$_.Type -eq "A"}
        if ($ARecords.Count -gt 0) {
            Write-Host "`nIPv4 Addresses (A Records):" -ForegroundColor Green
            $ARecords | ForEach-Object { Write-Host "  - $($_.IPAddress)" }
        }

        # Extract and display AAAA records (IPv6 addresses) if any
        $AAAARecords = $DnsRecords | Where-Object {$_.Type -eq "AAAA"}
        if ($AAAARecords.Count -gt 0) {
            Write-Host "`nIPv6 Addresses (AAAA Records):" -ForegroundColor Green
            $AAAARecords | ForEach-Object { Write-Host "  - $($_.IPAddress)" }
        }

        # Extract and display CNAME records if any
        $CnameRecords = $DnsRecords | Where-Object {$_.Type -eq "CNAME"}
        if ($CnameRecords.Count -gt 0) {
            Write-Host "`nCanonical Name (CNAME) Records:" -ForegroundColor Green
            $CnameRecords | ForEach-Object { Write-Host "  - $($_.Name) -> $($_.NameHost)" }
        }

    } else {
        Write-Warning "No DNS records found for $($TargetDomain)."
    }
}
catch {
    Write-Error "An error occurred during DNS lookup for $($TargetDomain):"
    Write-Error $_.Exception.Message
    Write-Warning "Please ensure you have network connectivity and the domain name is correct."
}

Write-Host "`n"
Write-Host "----------------------------------------------------" -ForegroundColor Cyan
Write-Host "  DNS Lookup Complete." -ForegroundColor Green
Write-Host "----------------------------------------------------" -ForegroundColor Cyan
Write-Host "`n"

# Keep the console window open if running directly, useful for reviewing output
if ($Host.Name -eq "ConsoleHost") {
    Read-Host "Press Enter to exit..."
}
