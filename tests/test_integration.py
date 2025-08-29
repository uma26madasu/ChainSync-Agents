import unittest
from chainsync import config

from chainsync import domain_manager

class TestConfig(unittest.TestCase):
	def test_openai_api_key(self):
		self.assertTrue(hasattr(config.Config, 'OPENAI_API_KEY'))

	def test_validate(self):
		self.assertTrue(callable(getattr(config.Config, 'validate', None)))

	def test_default_values(self):
		self.assertIsInstance(config.Config.CHAINSYNC_API_URL, str)
		self.assertIsInstance(config.Config.PYTHON_AGENT_PORT, int)

class TestDomainManager(unittest.TestCase):
	def test_domain_manager_class_exists(self):
		self.assertTrue(hasattr(domain_manager, 'DomainManager'), "Class DomainManager should exist.")

if __name__ == "__main__":
	unittest.main()
