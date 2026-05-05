#!/bin/bash

#═══════════════════════════════════════════════════════════════════════════════
#  🟠 ORANGE TEAM - Social Engineering Test Suite
#  Automated social engineering testing tools
#═══════════════════════════════════════════════════════════════════════════════

set -e

ORANGE='\033[0;33m'
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${SCRIPT_DIR}/../../logs/social_eng"
RESULTS_DIR="${SCRIPT_DIR}/../../metrics/data/social_eng"

mkdir -p "$LOG_DIR" "$RESULTS_DIR"

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warning() { echo -e "${ORANGE}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }

print_banner() {
    echo -e "${ORANGE}"
    cat << "EOF"
    ╔═══════════════════════════════════════════════════════════════╗
    ║     🟠 ORANGE TEAM - Social Engineering Test Suite            ║
    ║                                                               ║
    ║     Testing human security awareness through controlled       ║
    ║     social engineering simulations                            ║
    ╚═══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Vishing (Voice Phishing) Test Framework
vishing_test() {
    log_info "🎤 Vishing Test Framework"
    echo ""
    echo "Available vishing scenarios:"
    echo "  1. IT Support - Password reset request"
    echo "  2. HR Department - Benefits verification"
    echo "  3. Executive Assistant - Urgent request"
    echo "  4. Vendor Support - Account verification"
    echo ""
    
    read -p "Select scenario (1-4): " scenario
    read -p "Target phone number: " target_phone
    read -p "Caller ID to spoof (optional): " caller_id
    
    log_info "Preparing vishing test..."
    log_warning "Remember: All tests must be authorized and documented"
    
    # Log the test
    echo "$(date -Iseconds),vishing,$scenario,$target_phone,$caller_id" >> "$LOG_DIR/vishing_tests.csv"
    
    log_success "Vishing test logged. Execute manually and record results."
}

# Pretexting Test
pretexting_test() {
    log_info "🎭 Pretexting Test Framework"
    echo ""
    echo "Available pretexts:"
    echo "  1. New Employee - Needs system access"
    echo "  2. IT Audit - Compliance verification"
    echo "  3. Vendor - Delivery confirmation"
    echo "  4. Executive - Urgent project"
    echo ""
    
    read -p "Select pretext (1-4): " pretext
    read -p "Target department: " department
    read -p "Objective (info to obtain): " objective
    
    log_info "Preparing pretext scenario..."
    
    # Generate pretext script
    case $pretext in
        1) script="Hi, I'm [Name], just started in [Department]. I'm having trouble accessing [System]..." ;;
        2) script="Hello, I'm from IT Audit. We're conducting a compliance review and need to verify..." ;;
        3) script="Hi, this is [Name] from [Vendor]. I have a delivery but need to confirm..." ;;
        4) script="This is [Executive]'s assistant. They need urgent access to..." ;;
    esac
    
    echo ""
    echo -e "${BLUE}Suggested script:${NC}"
    echo "$script"
    echo ""
    
    echo "$(date -Iseconds),pretexting,$pretext,$department,$objective" >> "$LOG_DIR/pretexting_tests.csv"
    
    log_success "Pretext test logged."
}

# Tailgating/Physical Security Test
tailgating_test() {
    log_info "🚪 Physical Security Test Framework"
    echo ""
    echo "Test types:"
    echo "  1. Tailgating - Follow authorized person"
    echo "  2. Badge cloning - Test badge security"
    echo "  3. Dumpster diving - Document disposal"
    echo "  4. USB drop - Test device policy"
    echo ""
    
    read -p "Select test type (1-4): " test_type
    read -p "Location: " location
    read -p "Time of test: " test_time
    
    log_warning "Physical tests require explicit written authorization"
    read -p "Authorization reference number: " auth_ref
    
    echo "$(date -Iseconds),physical,$test_type,$location,$test_time,$auth_ref" >> "$LOG_DIR/physical_tests.csv"
    
    log_success "Physical security test logged."
}

# Generate Report
generate_report() {
    log_info "📊 Generating Social Engineering Test Report"
    
    report_file="$RESULTS_DIR/se_report_$(date +%Y%m%d).md"
    
    cat > "$report_file" << EOF
# 🟠 Social Engineering Test Report

**Generated:** $(date)

## Summary

### Vishing Tests
$(if [ -f "$LOG_DIR/vishing_tests.csv" ]; then wc -l < "$LOG_DIR/vishing_tests.csv"; else echo "0"; fi) tests conducted

### Pretexting Tests
$(if [ -f "$LOG_DIR/pretexting_tests.csv" ]; then wc -l < "$LOG_DIR/pretexting_tests.csv"; else echo "0"; fi) tests conducted

### Physical Security Tests
$(if [ -f "$LOG_DIR/physical_tests.csv" ]; then wc -l < "$LOG_DIR/physical_tests.csv"; else echo "0"; fi) tests conducted

## Recommendations

1. Continue regular social engineering awareness training
2. Implement verification procedures for sensitive requests
3. Conduct quarterly physical security assessments

---
*Report generated by Orange Team Social Engineering Test Suite*
EOF

    log_success "Report saved to: $report_file"
}

# Main menu
main_menu() {
    print_banner
    
    echo "Select test type:"
    echo "  1. Vishing (Voice Phishing)"
    echo "  2. Pretexting"
    echo "  3. Physical Security (Tailgating)"
    echo "  4. Generate Report"
    echo "  5. Exit"
    echo ""
    
    read -p "Choice: " choice
    
    case $choice in
        1) vishing_test ;;
        2) pretexting_test ;;
        3) tailgating_test ;;
        4) generate_report ;;
        5) exit 0 ;;
        *) log_error "Invalid choice"; main_menu ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
    main_menu
}

# Entry point
case "${1:-}" in
    --vishing) vishing_test ;;
    --pretext) pretexting_test ;;
    --physical) tailgating_test ;;
    --report) generate_report ;;
    *) main_menu ;;
esac
