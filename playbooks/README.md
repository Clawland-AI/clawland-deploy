# PicoClaw Ansible Deployment

Automated deployment of PicoClaw edge agent using Ansible.

## Requirements

- **Ansible**: 2.14 or later
- **Target Node**: Ubuntu 22.04+ / Debian 11+ on ARM64, RISC-V, or x86_64
- **SSH Access**: Passwordless sudo or become password configured

## Quick Start

### 1. Install Ansible

```bash
# Ubuntu/Debian
sudo apt-get install ansible

# macOS
brew install ansible

# Python pip
pip install ansible
```

### 2. Configure Inventory

Edit `inventory/picclaw.ini` and add your target nodes:

```ini
[picclaw_nodes]
raspberrypi.local ansible_user=pi

[picclaw_nodes:vars]
telegram_bot_token=YOUR_BOT_TOKEN
fleet_manager_url=https://fleet.clawland.ai
```

### 3. Deploy PicoClaw

```bash
cd clawland-deploy

# Run playbook
ansible-playbook -i inventory/picclaw.ini playbooks/deploy-picclaw.yml

# With password prompt
ansible-playbook -i inventory/picclaw.ini playbooks/deploy-picclaw.yml --ask-become-pass

# Dry run (check mode)
ansible-playbook -i inventory/picclaw.ini playbooks/deploy-picclaw.yml --check
```

### 4. Verify Deployment

```bash
# SSH into node
ssh pi@raspberrypi.local

# Check service status
sudo systemctl status picclaw

# View logs
sudo journalctl -u picclaw -f

# Test health check
curl http://localhost:8080/healthz
```

## Configuration

### Variables

Edit variables in `playbooks/deploy-picclaw.yml`:

| Variable | Default | Description |
|----------|---------|-------------|
| `picclaw_version` | `0.1.0` | PicoClaw release version |
| `picclaw_port` | `8080` | HTTP server port |
| `picclaw_enable_telegram` | `true` | Enable Telegram integration |
| `enable_firewall` | `true` | Configure UFW firewall |
| `fleet_manager_url` | `https://fleet.clawland.ai` | Fleet Manager URL |

### Override Variables

```bash
# Command-line override
ansible-playbook -i inventory/picclaw.ini playbooks/deploy-picclaw.yml \\
  -e "picclaw_port=9090" \\
  -e "enable_firewall=false"

# Inventory override
[picclaw_nodes:vars]
picclaw_port=9090
enable_firewall=false
```

## What Gets Deployed

### Directories

- `/opt/picclaw/` - Binary installation
- `/etc/picclaw/` - Configuration files
- `/var/lib/picclaw/` - Data and logs

### System User

- User: `picclaw` (system account, no login)
- Group: `picclaw`

### Systemd Service

- Service: `picclaw.service`
- Auto-start: Enabled
- Restart: On failure (10s delay)

### Firewall Rules (UFW)

- Allow: SSH (port 22)
- Allow: PicoClaw (port 8080)
- Default: Deny all incoming

### Security Hardening

- `NoNewPrivileges=true` - Prevent privilege escalation
- `PrivateTmp=true` - Isolated /tmp
- `ProtectSystem=strict` - Read-only system directories
- `ProtectHome=true` - No access to /home

## Advanced Usage

### Multi-Node Deployment

```bash
# Deploy to multiple nodes in parallel
ansible-playbook -i inventory/picclaw.ini playbooks/deploy-picclaw.yml -f 10

# Deploy to specific group
ansible-playbook -i inventory/picclaw.ini playbooks/deploy-picclaw.yml --limit raspberrypi.local
```

### Custom Binary URL

```bash
# Use locally built binary
ansible-playbook -i inventory/picclaw.ini playbooks/deploy-picclaw.yml \\
  -e "picclaw_binary_url=http://192.168.1.5:8000/picclaw-arm64"
```

### Disable Firewall

```bash
ansible-playbook -i inventory/picclaw.ini playbooks/deploy-picclaw.yml \\
  -e "enable_firewall=false"
```

## Troubleshooting

### Binary Download Fails

**Problem**: `get_url` task fails with 404

**Solution**:
```bash
# Check if release exists
curl -I https://github.com/Clawland-AI/picclaw/releases/download/v0.1.0/picclaw-aarch64

# Use local binary
ansible-playbook ... -e "picclaw_binary_url=file:///path/to/picclaw"
```

### Health Check Timeout

**Problem**: Task "Verify PicoClaw health check" times out

**Causes**:
- Binary not starting (check logs: `journalctl -u picclaw`)
- Firewall blocking localhost (disable UFW: `ufw disable`)
- Wrong port configured

**Solution**:
```bash
# Check service status
sudo systemctl status picclaw

# View logs
sudo journalctl -u picclaw -n 50

# Test manually
curl -v http://localhost:8080/healthz
```

### Permission Denied

**Problem**: Ansible cannot become root

**Solution**:
```bash
# Add user to sudo group
sudo usermod -aG sudo pi

# Or use password prompt
ansible-playbook ... --ask-become-pass
```

### SSH Connection Refused

**Problem**: Cannot connect to target node

**Solution**:
```bash
# Test SSH manually
ssh pi@raspberrypi.local

# Use IP address instead of hostname
ansible-playbook -i "192.168.1.100," playbooks/deploy-picclaw.yml

# Specify SSH key
ansible-playbook ... --private-key ~/.ssh/id_rsa
```

## Architecture Support

| Architecture | Binary Name | Example Hardware |
|--------------|-------------|------------------|
| `aarch64` | `picclaw-aarch64` | Raspberry Pi 4/5, ARM servers |
| `riscv64` | `picclaw-riscv64` | VisionFive 2, Milk-V Pioneer |
| `x86_64` | `picclaw-x86_64` | Intel/AMD servers, VPS |

Ansible automatically detects architecture via `{{ ansible_architecture }}`.

## Uninstallation

```bash
# Stop and disable service
sudo systemctl stop picclaw
sudo systemctl disable picclaw

# Remove files
sudo rm -rf /opt/picclaw /etc/picclaw /var/lib/picclaw
sudo rm /etc/systemd/system/picclaw.service

# Remove user
sudo userdel picclaw

# Reload systemd
sudo systemctl daemon-reload
```

## Next Steps

- Configure Telegram bot token in inventory
- Add multiple nodes to `inventory/picclaw.ini`
- Set up monitoring (Grafana + Prometheus)
- Enable auto-updates via cron + Ansible

---

**Built for Clawland Deploy Issue #1** 🚀
