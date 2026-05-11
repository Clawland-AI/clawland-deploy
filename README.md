# clawland-deploy

One-click deployment tools for the Clawland edge AI ecosystem.

---

## Overview

`clawland-deploy` provides automated deployment recipes for all Claw family agents (picclaw, moltclaw, nanoclaw) across different environments — from a single $10 board to a fleet of hundreds.

## Deployment Methods

| Method | Target | Use Case |
|--------|--------|----------|
| **Docker Compose** | Any Linux host | Single-node or dev setup |
| **Ansible Playbook** | VPS / bare metal | Production multi-node fleet |
| **Pre-built Images** | SD card flash | Zero-config edge deployment |
| **systemd Units** | Linux boards | Lightweight daemon setup |

## Quick Start

### Docker Compose (Single Node)

```bash
git clone https://github.com/Clawland-AI/clawland-deploy.git
cd clawland-deploy/docker

# Deploy picclaw edge agent
docker compose -f picclaw.yml up -d

# Deploy moltclaw cloud gateway
docker compose -f moltclaw.yml up -d
```

### Single-node PicoClaw Ansible Deployment

```bash
# Install the UFW module collection once on the control host
ansible-galaxy collection install -r collections/requirements.yml

# Edit inventory with your edge node
vim inventory/hosts.yml

# Deploy PicoClaw to the edge node
ansible-playbook -i inventory/hosts.yml playbooks/deploy-picclaw.yml
```

Useful variables:

| Variable | Default | Purpose |
|----------|---------|---------|
| `picclaw_version` | `0.1.0` | Release tag to download |
| `picclaw_edge_port` | `9090` | Local Edge API port and UFW allow rule |
| `picclaw_cloud_endpoint` | `http://localhost:8080` | Upstream NanoClaw/Fleet endpoint |
| `picclaw_cloud_token` | empty | Optional bearer token for upstream reporting |
| `picclaw_heartbeat_seconds` | `30` | Edge reporter heartbeat interval |

The playbook creates the `picclaw` system user, downloads the release binary,
renders `/var/lib/picclaw/.picoclaw/config.json`, installs a hardened systemd
unit, opens the Edge API port with UFW, starts the service, and verifies
`GET /api/health`.

### Ansible (Fleet Deployment)

```bash
# Reuse the same playbook for every host in the edge_nodes group.
ansible-playbook -i inventory/hosts.yml playbooks/deploy-picclaw.yml
```

### Pre-built Image (SD Card)

1. Download the latest image from [Releases](https://github.com/Clawland-AI/clawland-deploy/releases)
2. Flash to SD card: `dd if=picclaw-licheerv.img of=/dev/sdX bs=4M`
3. Insert into board, power on — picclaw starts automatically

## Directory Structure

```
clawland-deploy/
├── docker/                  # Docker Compose files
│   ├── picclaw.yml          # Edge agent
│   ├── moltclaw.yml         # Cloud gateway
│   ├── nanoclaw.yml         # Mid-weight agent
│   └── fleet-stack.yml      # Full fleet stack
├── ansible/                 # Ansible playbooks
│   ├── inventory/
│   │   └── hosts.yml        # Node inventory template
│   ├── playbooks/
│   │   ├── picclaw.yml      # Deploy picclaw
│   │   ├── moltclaw.yml     # Deploy moltclaw
│   │   └── fleet.yml        # Deploy full fleet
│   └── roles/
│       ├── common/          # Base OS setup
│       ├── picclaw/         # picclaw role
│       └── moltclaw/        # moltclaw role
├── images/                  # Pre-built image configs
│   ├── licheerv-nano/       # LicheeRV-Nano image
│   ├── milkv-duo/           # Milk-V Duo image
│   └── raspberry-pi/        # Raspberry Pi image
├── systemd/                 # systemd service units
│   ├── picclaw.service
│   └── moltclaw.service
└── scripts/                 # Helper scripts
    ├── setup-edge.sh        # One-line edge setup
    └── setup-cloud.sh       # One-line cloud setup
```

## Supported Hardware

| Board | Agent | Image Available |
|-------|-------|-----------------|
| LicheeRV-Nano ($10) | picclaw | Planned |
| Milk-V Duo ($9) | picclaw | Planned |
| Raspberry Pi 4/5 | nanoclaw / picclaw | Planned |
| Any x86/ARM Linux | moltclaw | Docker |
| Cloud VM | moltclaw | Docker / Ansible |

## Related Repositories

- [picclaw](https://github.com/Clawland-AI/picclaw) — Edge AI Agent
- [moltclaw](https://github.com/Clawland-AI/moltclaw) — Cloud AI Gateway
- [clawland-fleet](https://github.com/Clawland-AI/clawland-fleet) — Fleet orchestration
- [clawland-kits](https://github.com/Clawland-AI/clawland-kits) — Hardware sensor kits

## Contributing

See [CONTRIBUTING.md](https://github.com/Clawland-AI/.github/blob/main/CONTRIBUTING.md) for guidelines. Deployment improvements earn contribution points toward the quarterly [Revenue Pool](https://github.com/Clawland-AI/.github/blob/main/CONTRIBUTOR-REVENUE-SHARE.md).

## License

Apache 2.0 — See [LICENSE](LICENSE)
