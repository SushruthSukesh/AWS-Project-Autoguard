import unittest
import os
from agentcore.tools import cost_analyzer, nova_act_bridge

class TestCostAnalyzer(unittest.TestCase):
    def test_local_score(self):
        # This test expects no SageMaker endpoint; use local scoring via sagemaker/train.py model instead
        model_path = os.path.join(os.path.dirname(__file__), "../sagemaker/model_artifacts/anomaly_model.joblib")
        if not os.path.exists(model_path):
            self.skipTest("No local model; run sagemaker/train.py --train")
        from sagemaker.train import score_local
        res = score_local(model_path, [100.0, 110.0, 500.0])
        self.assertIn("anomalies", res)

class TestNovaActBridge(unittest.TestCase):
    def test_run_flow_not_configured(self):
        res = nova_act_bridge.run_flow({"flow_id":"x","inputs":{}})
        self.assertIn("status", res)

if __name__ == "__main__":
    unittest.main()
