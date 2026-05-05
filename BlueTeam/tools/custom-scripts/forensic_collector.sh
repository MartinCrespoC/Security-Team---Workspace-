#!/bin/bash

#===============================================================================
# BlueTeam-Windsurf - Forensic Evidence Collector
# Automated forensic artifact collection for incident response
#===============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
HOSTNAME_VAR=$(hostname)
COLLECTION_DIR="$BASE_DIR/forensics/artifacts/${HOSTNAME_VAR}_${TIMESTAMP}"
LOG_FILE="$COLLECTION_DIR/collection.log"

# Banner
show_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║     🔬 BlueTeam Forensic Collector                           ║"
    echo "║        Evidence Collection & Preservation                    ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Initialize collection
init_collection() {
    mkdir -p "$COLLECTION_DIR"/{system,network,processes,users,logs,files,memory,timeline,hashes}
    
    # Start logging
    exec > >(tee -a "$LOG_FILE") 2>&1
    
    log "Forensic collection started"
    log "Collection directory: $COLLECTION_DIR"
    log "Hostname: $HOSTNAME_VAR"
    log "Date: $(date)"
    log "Collector: $(whoami)"
    echo ""
}

# Logging
log() { echo -e "${GREEN}[+]${NC} $(date '+%H:%M:%S') $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $(date '+%H:%M:%S') $1"; }
error() { echo -e "${RED}[✗]${NC} $(date '+%H:%M:%S') $1"; }
info() { echo -e "${BLUE}[i]${NC} $(date '+%H:%M:%S') $1"; }

# Calculate hash
hash_file() {
    local file=$1
    if [ -f "$file" ]; then
        sha256sum "$file" >> "$COLLECTION_DIR/hashes/file_hashes.txt" 2>/dev/null
    fi
}

#===============================================================================
# SYSTEM INFORMATION
#===============================================================================

collect_system_info() {
    log "Collecting system information..."
    local dir="$COLLECTION_DIR/system"
    
    # Basic system info
    {
        echo "=== SYSTEM INFORMATION ==="
        echo "Hostname: $(hostname)"
        echo "Date: $(date)"
        echo "Uptime: $(uptime)"
        echo "Kernel: $(uname -a)"
        echo ""
        echo "=== OS RELEASE ==="
        cat /etc/os-release 2>/dev/null || cat /etc/*release 2>/dev/null
        echo ""
        echo "=== CPU INFO ==="
        lscpu 2>/dev/null || cat /proc/cpuinfo
        echo ""
        echo "=== MEMORY INFO ==="
        free -h
        echo ""
        cat /proc/meminfo
        echo ""
        echo "=== DISK INFO ==="
        df -h
        echo ""
        lsblk
        echo ""
        echo "=== MOUNT POINTS ==="
        mount
        echo ""
        cat /etc/fstab
    } > "$dir/system_info.txt" 2>&1
    
    # Hardware info
    {
        echo "=== PCI DEVICES ==="
        lspci 2>/dev/null || echo "lspci not available"
        echo ""
        echo "=== USB DEVICES ==="
        lsusb 2>/dev/null || echo "lsusb not available"
        echo ""
        echo "=== DMI/BIOS ==="
        dmidecode 2>/dev/null || echo "dmidecode not available"
    } > "$dir/hardware_info.txt" 2>&1
    
    # Installed packages
    {
        echo "=== INSTALLED PACKAGES ==="
        if command -v dpkg &>/dev/null; then
            dpkg -l
        elif command -v rpm &>/dev/null; then
            rpm -qa
        elif command -v pacman &>/dev/null; then
            pacman -Q
        fi
    } > "$dir/installed_packages.txt" 2>&1
    
    # Kernel modules
    lsmod > "$dir/kernel_modules.txt" 2>&1
    
    # Environment variables
    env > "$dir/environment.txt" 2>&1
    
    # Timezone
    {
        echo "=== TIMEZONE ==="
        timedatectl 2>/dev/null || cat /etc/timezone 2>/dev/null
        echo ""
        date +%Z
    } > "$dir/timezone.txt" 2>&1
    
    log "System information collected"
}

#===============================================================================
# NETWORK INFORMATION
#===============================================================================

collect_network_info() {
    log "Collecting network information..."
    local dir="$COLLECTION_DIR/network"
    
    # Network interfaces
    {
        echo "=== NETWORK INTERFACES ==="
        ip addr
        echo ""
        echo "=== INTERFACE DETAILS ==="
        ip link
        echo ""
        ifconfig -a 2>/dev/null || echo "ifconfig not available"
    } > "$dir/interfaces.txt" 2>&1
    
    # Routing
    {
        echo "=== ROUTING TABLE ==="
        ip route
        echo ""
        route -n 2>/dev/null || echo "route not available"
        echo ""
        echo "=== ARP CACHE ==="
        ip neigh
        echo ""
        arp -a 2>/dev/null || echo "arp not available"
    } > "$dir/routing.txt" 2>&1
    
    # Active connections
    {
        echo "=== ACTIVE CONNECTIONS (ss) ==="
        ss -tunapl
        echo ""
        echo "=== ACTIVE CONNECTIONS (netstat) ==="
        netstat -tunapl 2>/dev/null || echo "netstat not available"
        echo ""
        echo "=== LISTENING PORTS ==="
        ss -tlnp
        echo ""
        echo "=== ESTABLISHED CONNECTIONS ==="
        ss -tnp state established
    } > "$dir/connections.txt" 2>&1
    
    # DNS
    {
        echo "=== DNS CONFIGURATION ==="
        cat /etc/resolv.conf
        echo ""
        echo "=== HOSTS FILE ==="
        cat /etc/hosts
        echo ""
        echo "=== NSSWITCH ==="
        cat /etc/nsswitch.conf 2>/dev/null
    } > "$dir/dns.txt" 2>&1
    
    # Firewall rules
    {
        echo "=== IPTABLES RULES ==="
        iptables -L -n -v 2>/dev/null || echo "iptables not available"
        echo ""
        echo "=== IPTABLES NAT ==="
        iptables -t nat -L -n -v 2>/dev/null
        echo ""
        echo "=== IP6TABLES ==="
        ip6tables -L -n -v 2>/dev/null || echo "ip6tables not available"
        echo ""
        echo "=== UFW STATUS ==="
        ufw status verbose 2>/dev/null || echo "ufw not available"
        echo ""
        echo "=== NFTABLES ==="
        nft list ruleset 2>/dev/null || echo "nftables not available"
    } > "$dir/firewall.txt" 2>&1
    
    # Network statistics
    {
        echo "=== NETWORK STATISTICS ==="
        netstat -s 2>/dev/null || ss -s
        echo ""
        echo "=== INTERFACE STATISTICS ==="
        ip -s link
    } > "$dir/network_stats.txt" 2>&1
    
    log "Network information collected"
}

#===============================================================================
# PROCESS INFORMATION
#===============================================================================

collect_process_info() {
    log "Collecting process information..."
    local dir="$COLLECTION_DIR/processes"
    
    # Process list
    {
        echo "=== PROCESS LIST (ps auxf) ==="
        ps auxf
        echo ""
        echo "=== PROCESS LIST (ps -ef) ==="
        ps -ef
        echo ""
        echo "=== PROCESS TREE ==="
        pstree -p 2>/dev/null || echo "pstree not available"
    } > "$dir/process_list.txt" 2>&1
    
    # Process details
    {
        echo "=== TOP PROCESSES BY CPU ==="
        ps aux --sort=-%cpu | head -20
        echo ""
        echo "=== TOP PROCESSES BY MEMORY ==="
        ps aux --sort=-%mem | head -20
    } > "$dir/top_processes.txt" 2>&1
    
    # Open files
    {
        echo "=== OPEN FILES (lsof) ==="
        lsof -n 2>/dev/null | head -1000 || echo "lsof not available"
    } > "$dir/open_files.txt" 2>&1
    
    # Process maps and file descriptors
    for pid in $(ps -eo pid --no-headers | head -50); do
        if [ -d "/proc/$pid" ]; then
            {
                echo "=== PID: $pid ==="
                echo "Command: $(cat /proc/$pid/cmdline 2>/dev/null | tr '\0' ' ')"
                echo "CWD: $(readlink /proc/$pid/cwd 2>/dev/null)"
                echo "EXE: $(readlink /proc/$pid/exe 2>/dev/null)"
                echo ""
            } >> "$dir/process_details.txt" 2>&1
        fi
    done
    
    # Deleted but running executables
    {
        echo "=== DELETED EXECUTABLES STILL RUNNING ==="
        ls -la /proc/*/exe 2>/dev/null | grep deleted
    } > "$dir/deleted_executables.txt" 2>&1
    
    log "Process information collected"
}

#===============================================================================
# USER INFORMATION
#===============================================================================

collect_user_info() {
    log "Collecting user information..."
    local dir="$COLLECTION_DIR/users"
    
    # User accounts
    {
        echo "=== PASSWD FILE ==="
        cat /etc/passwd
        echo ""
        echo "=== GROUP FILE ==="
        cat /etc/group
        echo ""
        echo "=== SHADOW PERMISSIONS ==="
        ls -la /etc/shadow
        echo ""
        echo "=== SUDOERS ==="
        cat /etc/sudoers 2>/dev/null
        echo ""
        echo "=== SUDOERS.D ==="
        ls -la /etc/sudoers.d/ 2>/dev/null
        cat /etc/sudoers.d/* 2>/dev/null
    } > "$dir/accounts.txt" 2>&1
    
    # Logged in users
    {
        echo "=== CURRENTLY LOGGED IN ==="
        who -a
        echo ""
        w
        echo ""
        echo "=== LAST LOGINS ==="
        last -50
        echo ""
        echo "=== FAILED LOGINS ==="
        lastb 2>/dev/null | head -50 || echo "lastb not available"
        echo ""
        echo "=== LAST LOG ==="
        lastlog 2>/dev/null | grep -v "Never"
    } > "$dir/login_history.txt" 2>&1
    
    # User home directories
    {
        echo "=== HOME DIRECTORIES ==="
        ls -la /home/
        echo ""
        echo "=== ROOT HOME ==="
        ls -la /root/ 2>/dev/null
    } > "$dir/home_dirs.txt" 2>&1
    
    # SSH keys
    {
        echo "=== SSH AUTHORIZED KEYS ==="
        for user_home in /home/* /root; do
            if [ -f "$user_home/.ssh/authorized_keys" ]; then
                echo "--- $user_home/.ssh/authorized_keys ---"
                cat "$user_home/.ssh/authorized_keys"
                echo ""
            fi
        done
        echo ""
        echo "=== SSH KNOWN HOSTS ==="
        for user_home in /home/* /root; do
            if [ -f "$user_home/.ssh/known_hosts" ]; then
                echo "--- $user_home/.ssh/known_hosts ---"
                cat "$user_home/.ssh/known_hosts"
                echo ""
            fi
        done
    } > "$dir/ssh_keys.txt" 2>&1
    
    # Bash history
    {
        echo "=== BASH HISTORY ==="
        for user_home in /home/* /root; do
            if [ -f "$user_home/.bash_history" ]; then
                echo "--- $user_home/.bash_history ---"
                cat "$user_home/.bash_history" 2>/dev/null | tail -500
                echo ""
            fi
        done
    } > "$dir/bash_history.txt" 2>&1
    
    # Crontabs
    {
        echo "=== SYSTEM CRONTAB ==="
        cat /etc/crontab
        echo ""
        echo "=== CRON.D ==="
        ls -la /etc/cron.d/
        cat /etc/cron.d/* 2>/dev/null
        echo ""
        echo "=== USER CRONTABS ==="
        for crontab in /var/spool/cron/crontabs/*; do
            if [ -f "$crontab" ]; then
                echo "--- $crontab ---"
                cat "$crontab"
                echo ""
            fi
        done
    } > "$dir/crontabs.txt" 2>&1
    
    log "User information collected"
}

#===============================================================================
# LOG COLLECTION
#===============================================================================

collect_logs() {
    log "Collecting log files..."
    local dir="$COLLECTION_DIR/logs"
    
    # Copy important logs
    local log_files=(
        "/var/log/auth.log"
        "/var/log/secure"
        "/var/log/syslog"
        "/var/log/messages"
        "/var/log/kern.log"
        "/var/log/dmesg"
        "/var/log/boot.log"
        "/var/log/cron"
        "/var/log/maillog"
        "/var/log/audit/audit.log"
        "/var/log/faillog"
        "/var/log/lastlog"
        "/var/log/wtmp"
        "/var/log/btmp"
    )
    
    for logfile in "${log_files[@]}"; do
        if [ -f "$logfile" ]; then
            cp "$logfile" "$dir/" 2>/dev/null && log "Copied: $logfile"
            hash_file "$logfile"
        fi
    done
    
    # Web server logs
    for weblog in /var/log/apache2/*.log /var/log/nginx/*.log /var/log/httpd/*.log; do
        if [ -f "$weblog" ]; then
            cp "$weblog" "$dir/" 2>/dev/null
        fi
    done
    
    # Journal logs
    if command -v journalctl &>/dev/null; then
        journalctl --no-pager -n 10000 > "$dir/journal.txt" 2>&1
        journalctl --no-pager -u ssh -n 1000 > "$dir/journal_ssh.txt" 2>&1
        journalctl --no-pager -u sshd -n 1000 >> "$dir/journal_ssh.txt" 2>&1
    fi
    
    # Audit logs
    if command -v ausearch &>/dev/null; then
        ausearch -i > "$dir/audit_search.txt" 2>&1 || true
    fi
    
    log "Log files collected"
}

#===============================================================================
# FILE SYSTEM ARTIFACTS
#===============================================================================

collect_filesystem() {
    log "Collecting filesystem artifacts..."
    local dir="$COLLECTION_DIR/files"
    
    # Recently modified files
    {
        echo "=== FILES MODIFIED IN LAST 24 HOURS ==="
        find / -type f -mtime -1 2>/dev/null | grep -vE "^/(proc|sys|dev)" | head -500
    } > "$dir/recent_modified.txt" 2>&1
    
    # Recently accessed files
    {
        echo "=== FILES ACCESSED IN LAST 24 HOURS ==="
        find / -type f -atime -1 2>/dev/null | grep -vE "^/(proc|sys|dev)" | head -500
    } > "$dir/recent_accessed.txt" 2>&1
    
    # SUID/SGID files
    {
        echo "=== SUID FILES ==="
        find / -perm -4000 -type f 2>/dev/null
        echo ""
        echo "=== SGID FILES ==="
        find / -perm -2000 -type f 2>/dev/null
    } > "$dir/suid_sgid.txt" 2>&1
    
    # World-writable files
    {
        echo "=== WORLD-WRITABLE FILES ==="
        find / -perm -002 -type f 2>/dev/null | grep -vE "^/(proc|sys|dev)" | head -200
        echo ""
        echo "=== WORLD-WRITABLE DIRECTORIES ==="
        find / -perm -002 -type d 2>/dev/null | grep -vE "^/(proc|sys|dev)" | head -100
    } > "$dir/world_writable.txt" 2>&1
    
    # Hidden files
    {
        echo "=== HIDDEN FILES IN /tmp ==="
        find /tmp -name ".*" -type f 2>/dev/null
        echo ""
        echo "=== HIDDEN FILES IN /var/tmp ==="
        find /var/tmp -name ".*" -type f 2>/dev/null
        echo ""
        echo "=== HIDDEN FILES IN /dev/shm ==="
        find /dev/shm -name ".*" -type f 2>/dev/null
    } > "$dir/hidden_files.txt" 2>&1
    
    # Temp directories
    {
        echo "=== /tmp CONTENTS ==="
        ls -laR /tmp 2>/dev/null
        echo ""
        echo "=== /var/tmp CONTENTS ==="
        ls -laR /var/tmp 2>/dev/null
        echo ""
        echo "=== /dev/shm CONTENTS ==="
        ls -laR /dev/shm 2>/dev/null
    } > "$dir/temp_dirs.txt" 2>&1
    
    # Startup scripts
    {
        echo "=== INIT.D SCRIPTS ==="
        ls -la /etc/init.d/
        echo ""
        echo "=== RC.LOCAL ==="
        cat /etc/rc.local 2>/dev/null
        echo ""
        echo "=== SYSTEMD SERVICES ==="
        systemctl list-unit-files --type=service 2>/dev/null
    } > "$dir/startup.txt" 2>&1
    
    # Suspicious file types in temp
    {
        echo "=== EXECUTABLES IN TEMP ==="
        find /tmp /var/tmp /dev/shm -type f -executable 2>/dev/null
        echo ""
        echo "=== SCRIPTS IN TEMP ==="
        find /tmp /var/tmp /dev/shm -type f \( -name "*.sh" -o -name "*.py" -o -name "*.pl" -o -name "*.rb" \) 2>/dev/null
    } > "$dir/suspicious_temp.txt" 2>&1
    
    log "Filesystem artifacts collected"
}

#===============================================================================
# MEMORY DUMP
#===============================================================================

collect_memory() {
    log "Collecting memory information..."
    local dir="$COLLECTION_DIR/memory"
    
    # Memory info
    {
        echo "=== MEMORY INFO ==="
        free -h
        echo ""
        cat /proc/meminfo
        echo ""
        echo "=== SWAP INFO ==="
        swapon -s 2>/dev/null
    } > "$dir/memory_info.txt" 2>&1
    
    # Process memory maps
    {
        echo "=== PROCESS MEMORY MAPS ==="
        for pid in $(ps -eo pid --no-headers | head -20); do
            if [ -f "/proc/$pid/maps" ]; then
                echo "--- PID $pid ---"
                head -50 "/proc/$pid/maps" 2>/dev/null
                echo ""
            fi
        done
    } > "$dir/process_maps.txt" 2>&1
    
    # Full memory dump (if requested and tools available)
    if [ "$FULL_MEMORY" = "true" ]; then
        if command -v avml &>/dev/null; then
            log "Creating memory dump with AVML..."
            avml "$dir/memory.lime" 2>/dev/null || warn "AVML memory dump failed"
        elif command -v lime &>/dev/null; then
            log "Creating memory dump with LiME..."
            # LiME requires kernel module
            warn "LiME requires manual setup"
        elif [ -r /dev/mem ]; then
            log "Creating memory dump from /dev/mem..."
            dd if=/dev/mem of="$dir/memory.raw" bs=1M count=1024 2>/dev/null || warn "Memory dump failed"
        else
            warn "No memory dump tool available"
        fi
    fi
    
    log "Memory information collected"
}

#===============================================================================
# TIMELINE
#===============================================================================

create_timeline() {
    log "Creating filesystem timeline..."
    local dir="$COLLECTION_DIR/timeline"
    
    # MACtime timeline
    {
        echo "=== FILESYSTEM TIMELINE (last 7 days) ==="
        find / -type f -mtime -7 -printf "%T+ %p\n" 2>/dev/null | sort | tail -1000
    } > "$dir/timeline_mtime.txt" 2>&1
    
    # Access time timeline
    {
        echo "=== ACCESS TIMELINE (last 24 hours) ==="
        find / -type f -atime -1 -printf "%A+ %p\n" 2>/dev/null | sort | tail -500
    } > "$dir/timeline_atime.txt" 2>&1
    
    # Change time timeline
    {
        echo "=== CHANGE TIMELINE (last 7 days) ==="
        find / -type f -ctime -7 -printf "%C+ %p\n" 2>/dev/null | sort | tail -1000
    } > "$dir/timeline_ctime.txt" 2>&1
    
    # Combined timeline
    {
        echo "Timestamp,Type,Path"
        find / -type f \( -mtime -7 -o -atime -1 -o -ctime -7 \) -printf "%T+,M,%p\n" 2>/dev/null | head -2000
    } > "$dir/timeline_combined.csv" 2>&1
    
    log "Timeline created"
}

#===============================================================================
# HASH COLLECTION
#===============================================================================

collect_hashes() {
    log "Calculating file hashes..."
    local dir="$COLLECTION_DIR/hashes"
    
    # Hash critical system files
    {
        echo "=== SYSTEM BINARY HASHES ==="
        for bin in /bin/* /sbin/* /usr/bin/* /usr/sbin/*; do
            if [ -f "$bin" ]; then
                sha256sum "$bin" 2>/dev/null
            fi
        done
    } > "$dir/system_hashes.txt" 2>&1
    
    # Hash collected evidence
    {
        echo "=== EVIDENCE HASHES ==="
        find "$COLLECTION_DIR" -type f -exec sha256sum {} \; 2>/dev/null
    } > "$dir/evidence_hashes.txt" 2>&1
    
    log "Hashes calculated"
}

#===============================================================================
# PACKAGE AND VERIFY
#===============================================================================

package_evidence() {
    log "Packaging evidence..."
    
    local archive_name="${HOSTNAME_VAR}_forensics_${TIMESTAMP}.tar.gz"
    local archive_path="$BASE_DIR/forensics/$archive_name"
    
    # Create archive
    cd "$BASE_DIR/forensics/artifacts"
    tar -czf "$archive_path" "${HOSTNAME_VAR}_${TIMESTAMP}"
    
    # Calculate hash of archive
    sha256sum "$archive_path" > "${archive_path}.sha256"
    
    log "Evidence packaged: $archive_path"
    log "Archive hash: $(cat "${archive_path}.sha256")"
    
    # Create manifest
    {
        echo "=== FORENSIC COLLECTION MANIFEST ==="
        echo "Hostname: $HOSTNAME_VAR"
        echo "Collection Date: $(date)"
        echo "Collector: $(whoami)"
        echo "Archive: $archive_name"
        echo "SHA256: $(cat "${archive_path}.sha256" | awk '{print $1}')"
        echo ""
        echo "=== CONTENTS ==="
        tar -tzf "$archive_path"
    } > "${archive_path}.manifest"
    
    log "Manifest created: ${archive_path}.manifest"
}

#===============================================================================
# MAIN
#===============================================================================

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --collect-all     Collect all artifacts"
    echo "  --system          Collect system information"
    echo "  --network         Collect network information"
    echo "  --processes       Collect process information"
    echo "  --users           Collect user information"
    echo "  --logs            Collect log files"
    echo "  --filesystem      Collect filesystem artifacts"
    echo "  --memory          Collect memory information"
    echo "  --memory-dump     Create full memory dump (requires tools)"
    echo "  --timeline        Create filesystem timeline"
    echo "  --hashes          Calculate file hashes"
    echo "  --package         Package evidence for transport"
    echo "  -h, --help        Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 --collect-all"
    echo "  $0 --system --network --processes"
    echo "  $0 --collect-all --package"
}

main() {
    show_banner
    
    if [ $# -eq 0 ]; then
        # Default: collect all
        init_collection
        collect_system_info
        collect_network_info
        collect_process_info
        collect_user_info
        collect_logs
        collect_filesystem
        collect_memory
        create_timeline
        collect_hashes
        package_evidence
        exit 0
    fi
    
    local do_init=false
    local do_package=false
    
    # Parse arguments
    for arg in "$@"; do
        case "$arg" in
            --collect-all|--system|--network|--processes|--users|--logs|--filesystem|--memory|--memory-dump|--timeline|--hashes)
                do_init=true
                ;;
            --package)
                do_package=true
                ;;
        esac
    done
    
    if [ "$do_init" = true ]; then
        init_collection
    fi
    
    while [ $# -gt 0 ]; do
        case "$1" in
            --collect-all)
                collect_system_info
                collect_network_info
                collect_process_info
                collect_user_info
                collect_logs
                collect_filesystem
                collect_memory
                create_timeline
                collect_hashes
                ;;
            --system)
                collect_system_info
                ;;
            --network)
                collect_network_info
                ;;
            --processes)
                collect_process_info
                ;;
            --users)
                collect_user_info
                ;;
            --logs)
                collect_logs
                ;;
            --filesystem)
                collect_filesystem
                ;;
            --memory)
                collect_memory
                ;;
            --memory-dump)
                FULL_MEMORY=true
                collect_memory
                ;;
            --timeline)
                create_timeline
                ;;
            --hashes)
                collect_hashes
                ;;
            --package)
                # Will be handled after collection
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
        shift
    done
    
    if [ "$do_package" = true ]; then
        package_evidence
    fi
    
    echo ""
    log "Collection complete!"
    log "Evidence directory: $COLLECTION_DIR"
}

main "$@"
