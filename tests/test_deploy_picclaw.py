import pathlib
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLAYBOOK = ROOT / "playbooks" / "deploy-picclaw.yml"
SERVICE = ROOT / "templates" / "picclaw.service.j2"
CONFIG = ROOT / "templates" / "picclaw.config.json.j2"
README = ROOT / "README.md"


class PicClawDeployPlaybookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playbook_text = PLAYBOOK.read_text(encoding="utf-8")
        cls.playbook = yaml.safe_load(cls.playbook_text)[0]
        cls.tasks = cls.playbook["tasks"]
        cls.task_names = [task.get("name", "") for task in cls.tasks]
        cls.service_text = SERVICE.read_text(encoding="utf-8")
        cls.readme_text = README.read_text(encoding="utf-8")

    def test_playbook_is_single_node_edge_deploy(self):
        self.assertEqual(self.playbook["hosts"], "edge_nodes")
        self.assertIn("picclaw_version", self.playbook["vars"])
        self.assertIn("picclaw_edge_port", self.playbook["vars"])
        self.assertIn("picclaw_cloud_endpoint", self.playbook["vars"])
        self.assertIn("picclaw_arch_map", self.playbook["vars"])

    def test_binary_config_and_state_are_deployed(self):
        self.assertTrue(any("Download PicoClaw binary" in name for name in self.task_names))
        self.assertTrue(any("Deploy PicoClaw config" in name for name in self.task_names))
        self.assertTrue(any("Create PicoClaw state directory" in name for name in self.task_names))
        self.assertTrue(CONFIG.exists(), "config template should exist")

    def test_firewall_and_health_check_are_configured(self):
        self.assertIn("community.general.ufw", self.playbook_text)
        self.assertIn("ansible.builtin.uri", self.playbook_text)
        self.assertIn("/api/health", self.playbook_text)

    def test_systemd_runs_gateway_with_config_env(self):
        self.assertIn("ExecStart=/usr/local/bin/picclaw gateway", self.service_text)
        self.assertIn("Environment=PICOCLAW_CONFIG=", self.service_text)
        self.assertIn("Restart=always", self.service_text)

    def test_readme_has_single_node_deployment_command(self):
        self.assertIn("Single-node PicoClaw", self.readme_text)
        self.assertIn("ansible-playbook -i inventory/hosts.yml playbooks/deploy-picclaw.yml", self.readme_text)
        self.assertIn("picclaw_edge_port", self.readme_text)


if __name__ == "__main__":
    unittest.main()
