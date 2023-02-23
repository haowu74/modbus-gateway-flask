Install-Module -Name Posh-SSH

$username = "pi"
$password = ConvertTo-SecureString "raspberry" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential ($username, $password)
$session = New-SSHSession -ComputerName 192.168.0.200 -Credential $cred
$sftpSession = New-SFTPSession -ComputerName 192.168.0.200 -Credential $cred

Invoke-SSHCommand -Command "sudo apt-get install -y python3, python3-pip, libffi-dev, libssl-dev, nginx" -SSHSession $session
Invoke-SSHCommand -Command "sudo pip install virtualenv" -SSHSession $session
Invoke-SSHCommand -Command "mkdir temp" -SSHSession $session

Set-SFTPItem -SessionId $sftpSession.SessionId -Destination temp -Path static -Force
Set-SFTPItem -SessionId $sftpSession.SessionId -Destination temp -Path templates -Force
Set-SFTPItem -SessionId $sftpSession.SessionId -Destination temp -Path app.py -Force
Set-SFTPItem -SessionId $sftpSession.SessionId -Destination temp -Path gateway.py -Force
Set-SFTPItem -SessionId $sftpSession.SessionId -Destination temp -Path unit.py -Force
Set-SFTPItem -SessionId $sftpSession.SessionId -Destination temp -Path config.json -Force
Set-SFTPItem -SessionId $sftpSession.SessionId -Destination temp -Path users.json -Force
Set-SFTPItem -SessionId $sftpSession.SessionId -Destination temp -Path requirements.txt -Force
Set-SFTPItem -SessionId $sftpSession.SessionId -Destination temp -Path pyvenv.cfg -Force
Set-SFTPItem -SessionId $sftpSession.SessionId -Destination temp -Path flask.service -Force

Invoke-SSHCommand -Command "sudo mv temp/* /opt/modbus-gateway-flask" -SSHSession $session
Invoke-SSHCommand -Command "cd /opt/modbus-gateway-flask" -SSHSession $session
Invoke-SSHCommand -Command "sudo chmod 755 /opt/modbus-gateway-flask/*" -SSHSession $session
Invoke-SSHCommand -Command "sudo python3 -m venv /opt/modbus-gateway-flask/venv" -SSHSession $session
Invoke-SSHCommand -Command 'bash -c "source /opt/modbus-gateway-flask/venv/bin/activate"' -SSHSession $session
Invoke-SSHCommand -Command "sudo mv /opt/modbus-gateway-flask/pyvenv.cfg /opt/modbus-gateway-flask/venv/" -SSHSession $session
Invoke-SSHCommand -Command "sudo pip install -r /opt/modbus-gateway-flask/requirements.txt" -SSHSession $session
Invoke-SSHCommand -Command 'sudo echo "export FLASK_APP=app.py" >> /opt/modbus-gateway-flask/venv/bin/activate' -SSHSession $session
Invoke-SSHCommand -Command 'sudo echo "export FLASK_ENV=production" >> /opt/modbus-gateway-flask/venv/bin/activate' -SSHSession $session
Invoke-SSHCommand -Command 'sudo mv /opt/modbus-gateway-flask/flask.service /etc/systemd/system' -SSHSession $session
Invoke-SSHCommand -Command 'sudo raspi-config nonint do_serial 2' -SSHSession $session
Invoke-SSHCommand -Command 'sudo systemctl daemon-reload' -SSHSession $session
Invoke-SSHCommand -Command 'sudo systemctl enable flask' -SSHSession $session
Invoke-SSHCommand -Command 'sudo reboot' -SSHSession $session -TimeOut 60

Remove-SSHSession -SSHSession $session
Remove-SFTPSession -SFTPSession $sftpSession

