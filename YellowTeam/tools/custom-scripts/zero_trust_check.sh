#!/bin/bash

#═══════════════════════════════════════════════════════════════════════════════
#  🟡 YELLOW TEAM - Zero Trust Validation Script
#═══════════════════════════════════════════════════════════════════════════════
#  Validates architecture against Zero Trust principles
#═══════════════════════════════════════════════════════════════════════════════

# Colors
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Counters
PASS=0
FAIL=0
WARN=0
NA=0

# Banner
print_banner() {
    echo -e "${YELLOW}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🟡 YELLOW TEAM - ZERO TRUST VALIDATION                                      ║
║                                                                               ║
║   "Never Trust, Always Verify"                                                ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Logging functions
log_pass() {
    echo -e "${GREEN}[✓ PASS]${NC} $1"
    ((PASS++))
}

log_fail() {
    echo -e "${RED}[✗ FAIL]${NC} $1"
    ((FAIL++))
}

log_warn() {
    echo -e "${YELLOW}[! WARN]${NC} $1"
    ((WARN++))
}

log_na() {
    echo -e "${BLUE}[- N/A]${NC} $1"
    ((NA++))
}

log_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

log_section() {
    echo ""
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}  $1${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Check functions
check_identity() {
    log_section "🔐 IDENTITY VERIFICATION"

    echo "Checking identity controls..."
    echo ""

    # Check for MFA configuration files
    if [ -f "/etc/pam.d/common-auth" ]; then
        if grep -q "pam_google_authenticator\|pam_duo\|pam_yubico" /etc/pam.d/common-auth 2>/dev/null; then
            log_pass "MFA PAM module configured"
        else
            log_warn "MFA PAM module not detected in common-auth"
        fi
    else
        log_na "PAM configuration not found (may not be applicable)"
    fi

    # Check SSH configuration
    if [ -f "/etc/ssh/sshd_config" ]; then
        if grep -q "^PasswordAuthentication no" /etc/ssh/sshd_config 2>/dev/null; then
            log_pass "SSH password authentication disabled"
        else
            log_warn "SSH password authentication may be enabled"
        fi

        if grep -q "^PubkeyAuthentication yes" /etc/ssh/sshd_config 2>/dev/null; then
            log_pass "SSH public key authentication enabled"
        else
            log_warn "SSH public key authentication not explicitly enabled"
        fi
    else
        log_na "SSH configuration not found"
    fi

    # Check for identity provider configurations
    if [ -d "/etc/sssd" ] || [ -f "/etc/krb5.conf" ]; then
        log_pass "Centralized identity management detected"
    else
        log_warn "No centralized identity management detected"
    fi

    echo ""
    echo "Identity Verification Recommendations:"
    echo "  • Implement MFA for all user accounts"
    echo "  • Use centralized identity provider (LDAP/AD/OIDC)"
    echo "  • Disable password-based authentication where possible"
    echo "  • Implement risk-based authentication"
}

check_devices() {
    log_section "💻 DEVICE VERIFICATION"

    echo "Checking device controls..."
    echo ""

    # Check for endpoint protection
    if command -v clamd &> /dev/null || [ -d "/opt/CrowdStrike" ] || [ -d "/opt/carbonblack" ]; then
        log_pass "Endpoint protection detected"
    else
        log_warn "No endpoint protection detected"
    fi

    # Check for device compliance tools
    if command -v osquery &> /dev/null; then
        log_pass "OSQuery installed for device monitoring"
    else
        log_warn "OSQuery not installed"
    fi

    # Check for disk encryption
    if command -v cryptsetup &> /dev/null; then
        if lsblk -o NAME,TYPE,FSTYPE | grep -q "crypt"; then
            log_pass "Disk encryption detected"
        else
            log_warn "Disk encryption not detected on mounted volumes"
        fi
    else
        log_na "cryptsetup not available"
    fi

    # Check for host firewall
    if command -v ufw &> /dev/null; then
        if ufw status 2>/dev/null | grep -q "Status: active"; then
            log_pass "UFW firewall is active"
        else
            log_warn "UFW firewall is not active"
        fi
    elif command -v firewall-cmd &> /dev/null; then
        if firewall-cmd --state 2>/dev/null | grep -q "running"; then
            log_pass "Firewalld is running"
        else
            log_warn "Firewalld is not running"
        fi
    elif command -v iptables &> /dev/null; then
        if iptables -L -n 2>/dev/null | grep -q "Chain"; then
            log_pass "iptables rules configured"
        else
            log_warn "iptables may not have rules configured"
        fi
    else
        log_warn "No host firewall detected"
    fi

    echo ""
    echo "Device Verification Recommendations:"
    echo "  • Deploy endpoint detection and response (EDR)"
    echo "  • Enable full disk encryption"
    echo "  • Implement device health attestation"
    echo "  • Use host-based firewalls"
}

check_network() {
    log_section "🌐 NETWORK VERIFICATION"

    echo "Checking network controls..."
    echo ""

    # Check for network segmentation (basic check)
    if ip route show 2>/dev/null | grep -q "via"; then
        log_pass "Multiple network routes detected (potential segmentation)"
    else
        log_warn "Single network route - verify segmentation"
    fi

    # Check for TLS configuration
    if [ -d "/etc/ssl/certs" ] && [ "$(ls -A /etc/ssl/certs 2>/dev/null)" ]; then
        log_pass "SSL certificates directory exists and populated"
    else
        log_warn "SSL certificates directory empty or missing"
    fi

    # Check for VPN
    if command -v openvpn &> /dev/null || command -v wg &> /dev/null || [ -d "/etc/wireguard" ]; then
        log_pass "VPN software detected"
    else
        log_warn "No VPN software detected"
    fi

    # Check DNS configuration
    if [ -f "/etc/resolv.conf" ]; then
        if grep -q "nameserver" /etc/resolv.conf; then
            log_pass "DNS configured"
            # Check for DNS over HTTPS/TLS
            if grep -q "127.0.0.1\|::1" /etc/resolv.conf && (command -v dnscrypt-proxy &> /dev/null || command -v stubby &> /dev/null); then
                log_pass "Encrypted DNS detected"
            else
                log_warn "Encrypted DNS (DoH/DoT) not detected"
            fi
        else
            log_fail "DNS not configured"
        fi
    fi

    # Check for open ports
    echo ""
    log_info "Checking listening ports..."
    if command -v ss &> /dev/null; then
        LISTENING_PORTS=$(ss -tlnp 2>/dev/null | grep LISTEN | wc -l)
        log_info "Found $LISTENING_PORTS listening TCP ports"
        if [ "$LISTENING_PORTS" -gt 20 ]; then
            log_warn "High number of listening ports - review for unnecessary services"
        else
            log_pass "Reasonable number of listening ports"
        fi
    fi

    echo ""
    echo "Network Verification Recommendations:"
    echo "  • Implement micro-segmentation"
    echo "  • Use encrypted communications (TLS 1.3)"
    echo "  • Deploy network access control"
    echo "  • Minimize exposed services"
}

check_applications() {
    log_section "📱 APPLICATION VERIFICATION"

    echo "Checking application controls..."
    echo ""

    # Check for container runtime
    if command -v docker &> /dev/null; then
        log_pass "Docker installed"

        # Check Docker security
        if docker info 2>/dev/null | grep -q "userns"; then
            log_pass "Docker user namespaces enabled"
        else
            log_warn "Docker user namespaces not enabled"
        fi
    else
        log_na "Docker not installed"
    fi

    if command -v podman &> /dev/null; then
        log_pass "Podman installed (rootless containers)"
    fi

    # Check for Kubernetes
    if command -v kubectl &> /dev/null; then
        log_pass "Kubernetes CLI installed"
    fi

    # Check for secrets management
    if command -v vault &> /dev/null; then
        log_pass "HashiCorp Vault installed"
    else
        log_warn "No secrets management tool detected"
    fi

    # Check for application firewall
    if command -v modsecurity &> /dev/null || [ -f "/etc/nginx/modsecurity.conf" ] || [ -d "/etc/modsecurity" ]; then
        log_pass "ModSecurity WAF detected"
    else
        log_warn "No WAF detected"
    fi

    echo ""
    echo "Application Verification Recommendations:"
    echo "  • Use application-level authentication"
    echo "  • Implement API gateway with security controls"
    echo "  • Deploy secrets management solution"
    echo "  • Use container security scanning"
}

check_data() {
    log_section "📊 DATA VERIFICATION"

    echo "Checking data controls..."
    echo ""

    # Check for encryption tools
    if command -v gpg &> /dev/null; then
        log_pass "GPG encryption available"
    else
        log_warn "GPG not installed"
    fi

    if command -v openssl &> /dev/null; then
        log_pass "OpenSSL available"
        # Check OpenSSL version
        OPENSSL_VERSION=$(openssl version 2>/dev/null | awk '{print $2}')
        log_info "OpenSSL version: $OPENSSL_VERSION"
    fi

    # Check for database encryption
    if command -v mysql &> /dev/null || command -v psql &> /dev/null; then
        log_info "Database client detected - verify encryption at rest is enabled"
    fi

    # Check file permissions on sensitive directories
    if [ -d "/etc/ssl/private" ]; then
        PERMS=$(stat -c %a /etc/ssl/private 2>/dev/null)
        if [ "$PERMS" = "700" ] || [ "$PERMS" = "710" ]; then
            log_pass "SSL private directory has restrictive permissions"
        else
            log_warn "SSL private directory permissions may be too open: $PERMS"
        fi
    fi

    echo ""
    echo "Data Verification Recommendations:"
    echo "  • Implement data classification"
    echo "  • Enable encryption at rest for all data stores"
    echo "  • Use TLS 1.3 for data in transit"
    echo "  • Implement data loss prevention (DLP)"
}

check_visibility() {
    log_section "👁️ VISIBILITY & ANALYTICS"

    echo "Checking visibility controls..."
    echo ""

    # Check for logging
    if [ -d "/var/log" ]; then
        log_pass "System logging directory exists"

        # Check for audit logging
        if [ -f "/var/log/audit/audit.log" ] || command -v auditd &> /dev/null; then
            log_pass "Audit logging available"
        else
            log_warn "Audit logging not detected"
        fi

        # Check for centralized logging agents
        if command -v filebeat &> /dev/null || command -v fluentd &> /dev/null || command -v rsyslog &> /dev/null; then
            log_pass "Log shipping agent detected"
        else
            log_warn "No log shipping agent detected"
        fi
    fi

    # Check for monitoring tools
    if command -v prometheus &> /dev/null || [ -d "/etc/prometheus" ]; then
        log_pass "Prometheus monitoring detected"
    fi

    if command -v grafana-server &> /dev/null || [ -d "/etc/grafana" ]; then
        log_pass "Grafana dashboards detected"
    fi

    # Check for SIEM/security monitoring
    if [ -d "/opt/splunk" ] || [ -d "/opt/elastic" ] || command -v wazuh-agent &> /dev/null; then
        log_pass "Security monitoring solution detected"
    else
        log_warn "No SIEM/security monitoring detected"
    fi

    echo ""
    echo "Visibility Recommendations:"
    echo "  • Implement centralized logging (SIEM)"
    echo "  • Enable security event monitoring"
    echo "  • Deploy anomaly detection"
    echo "  • Create security dashboards"
}

generate_report() {
    log_section "📋 ZERO TRUST ASSESSMENT SUMMARY"

    TOTAL=$((PASS + FAIL + WARN + NA))

    echo -e "Results:"
    echo -e "  ${GREEN}✓ PASS:${NC} $PASS"
    echo -e "  ${RED}✗ FAIL:${NC} $FAIL"
    echo -e "  ${YELLOW}! WARN:${NC} $WARN"
    echo -e "  ${BLUE}- N/A:${NC}  $NA"
    echo ""

    # Calculate score
    if [ $((PASS + FAIL + WARN)) -gt 0 ]; then
        SCORE=$(( (PASS * 100) / (PASS + FAIL + WARN) ))
    else
        SCORE=0
    fi

    echo -e "Zero Trust Maturity Score: ${YELLOW}${SCORE}%${NC}"
    echo ""

    if [ $SCORE -ge 80 ]; then
        echo -e "${GREEN}Rating: OPTIMAL${NC}"
        echo "Your environment demonstrates strong Zero Trust implementation."
    elif [ $SCORE -ge 60 ]; then
        echo -e "${YELLOW}Rating: ADVANCED${NC}"
        echo "Good progress on Zero Trust, but improvements needed."
    elif [ $SCORE -ge 40 ]; then
        echo -e "${YELLOW}Rating: INITIAL${NC}"
        echo "Basic Zero Trust controls in place, significant work needed."
    else
        echo -e "${RED}Rating: TRADITIONAL${NC}"
        echo "Limited Zero Trust implementation. Recommend comprehensive review."
    fi

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Zero Trust Principles Reminder:"
    echo "  1. Verify explicitly - Always authenticate and authorize"
    echo "  2. Use least privilege - Limit access to minimum necessary"
    echo "  3. Assume breach - Minimize blast radius, segment access"
    echo ""
}

# Main
main() {
    print_banner

    echo "Starting Zero Trust validation..."
    echo "Date: $(date)"
    echo ""

    check_identity
    check_devices
    check_network
    check_applications
    check_data
    check_visibility

    generate_report
}

# Run
main "$@"
