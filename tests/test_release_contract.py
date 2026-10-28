import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_release import check_rendered_yaml

class ReleasePolicyTests(unittest.TestCase):
 def test_live_path_is_not_repointed(self):
  content=(ROOT/'argocd-application.yaml').read_text()
  self.assertIn('path: kubernetes',content)
  self.assertIn('targetRevision: main',content)
 def test_restrict_dangerous_resource_omissions(self):
  policy=(ROOT/'releases/project/argocd-project.yaml').read_text()
  self.assertIn('cloud-app-controlled',policy)
  self.assertIn('namespaceResourceWhitelist',policy)
  self.assertNotIn('kind: "*"',policy)
 def test_envs_are_not_automatically_enabled(self):
  manifest=(ROOT/'argocd-application.yaml').read_text()
  self.assertNotIn('releases/overlays',manifest)
if __name__=='__main__': unittest.main()
