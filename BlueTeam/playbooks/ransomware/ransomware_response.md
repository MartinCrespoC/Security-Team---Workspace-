# Ransomware Incident Response Playbook

## 🚨 Severity: CRITICAL

## Immediate Actions (First 15 Minutes)

### 1. Isolate Affected Systems
```bash
# Disable network interface
sudo ip link set eth0 down

# Or block all traffic except SSH
sudo iptables -F
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT
sudo iptables -A INPUT -j DROP
sudo iptables -A OUTPUT -j DROP
```

### 2. Identify Scope
- [ ] How many systems are affected?
- [ ] What data has been encrypted?
- [ ] Is the ransomware still spreading?
- [ ] What is the ransomware variant?

### 3. Preserve Evidence
```bash
# Collect forensic evidence
sudo ./tools/custom-scripts/forensic_collector.sh --collect-all --package
```

### 4. Document Everything
- Screenshot ransom notes
- Record file extensions of encrypted files
- Note any contact information provided

## Investigation Phase

### Identify Ransomware Variant
1. Check ransom note for identifiers
2. Upload sample to:
   - [ID Ransomware](https://id-ransomware.malwarehunterteam.com/)
   - [No More Ransom](https://www.nomoreransom.org/)
3. Search for decryption tools

### Determine Entry Point
Common vectors:
- [ ] Phishing email
- [ ] RDP brute force
- [ ] Vulnerable software
- [ ] Supply chain compromise

### Check for Data Exfiltration
Many ransomware groups exfiltrate data before encryption:
```bash
# Check for large outbound transfers
grep -E "scp|rsync|curl.*POST" /var/log/*.log
```

## Containment

### Network Level
```bash
# Block C2 domains/IPs
echo "127.0.0.1 ransomware-c2.com" | sudo tee -a /etc/hosts

# Block at firewall
sudo iptables -A OUTPUT -d <C2_IP> -j DROP
```

### Endpoint Level
```bash
# Kill ransomware process
sudo pkill -9 -f <ransomware_process>

# Disable persistence
sudo systemctl disable <malicious_service>
sudo rm /etc/cron.d/<malicious_cron>
```

## Eradication

### Remove Ransomware
1. Boot from clean media if possible
2. Remove malicious files
3. Clean registry/startup items
4. Verify removal with AV scan

### Patch Vulnerabilities
- [ ] Update all systems
- [ ] Patch exploited vulnerability
- [ ] Change all credentials

## Recovery

### Restore from Backups
1. Verify backups are clean
2. Test restore process
3. Restore critical systems first
4. Validate data integrity

### If No Backups Available
1. Check for decryption tools
2. Consider negotiation (last resort)
3. Accept data loss

## Post-Incident

### Lessons Learned
- [ ] How did the attack succeed?
- [ ] What could have prevented it?
- [ ] What detection gaps existed?

### Improvements
- [ ] Implement better backup strategy
- [ ] Deploy EDR solution
- [ ] Improve email security
- [ ] Segment network
- [ ] Train users

## Do NOT

- ❌ Pay ransom immediately
- ❌ Delete encrypted files
- ❌ Reboot systems unnecessarily
- ❌ Communicate with attacker without legal counsel
- ❌ Restore without verifying backup integrity

## Resources

- [CISA Ransomware Guide](https://www.cisa.gov/stopransomware)
- [No More Ransom Project](https://www.nomoreransom.org/)
- [ID Ransomware](https://id-ransomware.malwarehunterteam.com/)
