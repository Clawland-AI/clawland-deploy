# 🍇 Clawland Deploy — Infrastructure Automation

**clawland-deploy** provides Ansible playbooks and Docker Compose configurations for deploying the Clawland edge AI agent network (MicroClaw, NanoClaw, PicoClaw, MoltClaw).

## Features

- ✅ **Ansible playbooks** — automated deployment for all agent layers
- ✅ **Architecture-aware** — supports ARM, RISC-V, x86_64
- ✅ **Systemd integration** — auto-start services on boot
- ✅ **Firewall configuration** — UFW rules for secure edge deployments
- ✅ **Health checks** — verify deployment success
- ✅ **Docker Compose** — optional containerized deployment

## Quick Start

### Prerequisites

**On your control machine:**

```bash
# Install Ansible
pip install ansible

# Clone this repository
git clone https://github.com/Clawland-AI/clawland-deploy.git
cd clawland-deploy
```

**On target nodes:**

- SSH access with sudo privileges
- Supported OS: Ubuntu 22.04+, Raspberry Pi OS, Debian 11+
- Supported architectures: ARM (aarch64, armv7l), RISC-V (riscv64), x86_64

### Deploy PicoClaw (L1 Agent)

#### 1. Configure Inventory

Edit `inventory/hosts.yml` and add your target node:

```yaml
picoclaw_nodes:
  hosts:
    picoclaw-01:
      ansible_host: 192.168.1.100  # Your Raspberry Pi IP
      ansible_user: pi
      ansible_become: yes
      picoclaw_port: 8080
      moltclaw_url: "https://moltclaw.clawland.ai"
```

#### 2. Run Playbook

```bash
ansible-playbook -i inventory/hosts.yml playbooks/deploy-picoclaw.yml
```

#### 3. Verify Deployment

```bash
# SSH to your node
ssh pi@192.168.1.100

# Check service status
sudo systemctl status picoclaw

# View logs
sudo journalctl -u picoclaw -f

# Test health endpoint
curl http://localhost:8080/healthz
```

## Playbooks

### deploy-picoclaw.yml

Deploy PicoClaw (L1 mid-weight agent) on Raspberry Pi 5, StarFive VisionFive 2, or similar SBC.

**What it does:**

- ✅ Installs Go runtime (or uses pre-built binary)
- ✅ Creates system user and directories
- ✅ Deploys PicoClaw binary and configuration
- ✅ Sets up systemd service with auto-restart
- ✅ Configures UFW firewall
- ✅ Runs health check verification

**Variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `picoclaw_version` | `0.1.0` | PicoClaw release version |
| `picoclaw_port` | `8080` | HTTP server port |
| `moltclaw_url` | `https://moltclaw.clawland.ai` | L3 cloud coordinator endpoint |
| `nanoclaw_enabled` | `false` | Connect to local L2 gateway |
| `nanoclaw_url` | `` | L2 NanoClaw gateway URL |

**Usage:**

```bash
# Deploy to all picoclaw_nodes in inventory
ansible-playbook -i inventory/hosts.yml playbooks/deploy-picoclaw.yml

# Deploy to specific host
ansible-playbook -i inventory/hosts.yml playbooks/deploy-picoclaw.yml --limit picoclaw-01

# Dry run (check mode)
ansible-playbook -i inventory/hosts.yml playbooks/deploy-picoclaw.yml --check
```

### deploy-nanoclaw.yml (TODO)

Deploy NanoClaw (L2 regional gateway) on Raspberry Pi 4/5.

### deploy-microclaw.yml (TODO)

Flash MicroClaw (L0 sensor agent) firmware to ESP32.

### deploy-moltclaw.yml (TODO)

Deploy MoltClaw (L3 cloud coordinator) on cloud VPS or Kubernetes.

## Configuration Templates

### picoclaw-config.yml.j2

Jinja2 template for PicoClaw configuration. Deployed to `/etc/picoclaw/config.yml`.

**Key settings:**

- **Server:** Host and port binding
- **MoltClaw:** L3 cloud coordinator URL and API key
- **NanoClaw:** Optional L2 gateway connection
- **MicroClaw:** MQTT broker for L0 sensor nodes
- **Logging:** Level and file paths
- **Features:** Inference, decision engine, LoRa gateway

**Override in inventory:**

```yaml
picoclaw-01:
  ansible_host: 192.168.1.100
  picoclaw_api_key: "your-secret-key"
  nanoclaw_enabled: true
  nanoclaw_url: "http://192.168.1.50:8000"
```

### picoclaw.service.j2

Systemd service unit file template. Includes:

- Auto-restart on failure
- Resource limits (file descriptors, processes)
- Security hardening (NoNewPrivileges, PrivateTmp, ProtectSystem)
- Journal logging

## Inventory

### hosts.yml

Sample inventory with all agent layers:

```yaml
all:
  children:
    picoclaw_nodes:
      hosts:
        picoclaw-01:
          ansible_host: 192.168.1.100
          ansible_user: pi
      vars:
        picoclaw_version: "0.1.0"
    
    nanoclaw_nodes:
      hosts:
        nanoclaw-01:
          ansible_host: 192.168.1.50
    
    microclaw_nodes:
      hosts:
        microclaw-01:
          ansible_host: 192.168.1.200
```

**Host variables:**

- `ansible_host` — IP address or hostname
- `ansible_user` — SSH user (e.g., `pi`, `ubuntu`)
- `ansible_become` — Use sudo (default: `yes`)

## Docker Compose (Alternative)

For quick local testing, use Docker Compose:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f picoclaw

# Stop all services
docker-compose down
```

**Services:**

- **PicoClaw:** http://localhost:8080
- **NanoClaw:** http://localhost:8000
- **MoltClaw:** http://localhost:3000

## Architecture

```
┌───────────────────────────────────────────┐
│  Clawland Edge AI Network                 │
├───────────────────────────────────────────┤
│  L0 MicroClaw (ESP32)                     │
│    └─ Ansible flash (future)             │
│           ↓ MQTT                          │
│  L1 PicoClaw (Raspberry Pi 5)             │
│    └─ Ansible deploy-picoclaw.yml        │
│           ↓ HTTP                          │
│  L2 NanoClaw (Raspberry Pi 4)             │
│    └─ Ansible deploy-nanoclaw.yml        │
│           ↓ HTTPS                         │
│  L3 MoltClaw (Cloud)                      │
│    └─ Ansible deploy-moltclaw.yml        │
└───────────────────────────────────────────┘
```

## Troubleshooting

### SSH Connection Failed

```bash
# Test SSH connection
ansible -i inventory/hosts.yml picoclaw-01 -m ping

# Check SSH config
ssh -vvv pi@192.168.1.100
```

### Playbook Fails on "Download Binary"

**Cause:** Pre-built binary not available for your architecture.

**Solution:** Playbook automatically falls back to building from source (requires Go runtime).

### Health Check Timeout

```bash
# SSH to target node
ssh pi@192.168.1.100

# Check if PicoClaw is running
sudo systemctl status picoclaw

# View logs
sudo journalctl -u picoclaw -n 50

# Test health endpoint locally
curl -v http://localhost:8080/healthz
```

### Firewall Blocks Access

```bash
# Check UFW status
sudo ufw status

# Allow PicoClaw port
sudo ufw allow 8080/tcp

# Reload UFW
sudo ufw reload
```

## Development

### Test Playbook Locally

```bash
# Install Vagrant
brew install vagrant  # macOS
sudo apt install vagrant  # Linux

# Create test VM
vagrant init ubuntu/jammy64
vagrant up

# Run playbook against VM
ansible-playbook -i "127.0.0.1:2222," playbooks/deploy-picoclaw.yml \
  --user vagrant \
  --private-key ~/.vagrant.d/insecure_private_key
```

### Lint Playbooks

```bash
# Install ansible-lint
pip install ansible-lint

# Lint all playbooks
ansible-lint playbooks/*.yml
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, coding standards, and PR guidelines.

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.

## Links

- **Clawland Docs:** https://docs.clawland.ai
- **Issues:** https://github.com/Clawland-AI/clawland-deploy/issues
- **Discussions:** https://github.com/Clawland-AI/clawland-deploy/discussions
