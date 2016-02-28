#Sync from Active Directory to S3 Bucket Engine
Import-Module "C:\Program Files (x86)\AWS Tools\PowerShell\AWSPowerShell\AWSPowerShell.psd1"

$accesskey = "AWS Access Key"
$secretkey = "AWS Secret Key"
$bucket = "AWS Bucket Name"

Set-AWSCredentials -AccessKey $accesskey -SecretKey $secretkey

$Now = ((Get-Date).AddDays(-7)).Date

try
    {
        Import-Module ActiveDirectory
        $DomainName = Get-ADDomain | Select -ExpandProperty Name
        echo $env:temp\new_user_email\active_users
        New-Item $env:temp\new_user_email\active_users -type directory -force

        $count = (Get-ADUser -Filter {(Enabled -eq $true) -and (EmailAddress -like "*" ) -and (whenCreated -ge $Now)}).count
    }
        catch [Exception]
    {
        echo $_.Exception.GetType().FullName, $_.Exception.Message
    }

if ($count -gt 0) { 
    try
        {
            Get-ADUser -Filter {(Enabled -eq $true) -and (EmailAddress -like "*" ) -and (whenCreated -ge $Now)} -properties objectGUID, DisplayName, EmailAddress, whenCreated | select objectGUID, DisplayName, EmailAddress, whenCreated | ConvertTo-Json | New-Item $env:temp\new_user_email\active_users\$DomainName.json -type file -force

            echo "Writing to Amazon S3 Bucket"
            Write-S3Object -BucketName $bucket -Key "$DomainName.json" -File $env:temp\new_user_email\active_users\$DomainName.json
        }
            catch [Exception]
        {
            echo $_.Exception.GetType().FullName, $_.Exception.Message
        }
}

if ($count -eq 0) { 
    try
        {
            Remove-Item $env:temp\new_user_email\active_users\$DomainName.json
        }
            catch [Exception]
        {
            echo $_.Exception.GetType().FullName, $_.Exception.Message
        }
}