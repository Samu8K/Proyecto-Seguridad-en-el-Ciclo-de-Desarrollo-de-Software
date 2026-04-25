import re

class FalsePositiveDetector:
    async def predict(self, finding: dict) -> bool:
        # Reglas simples para demostración
        file_path = finding.get("file_path", "").lower()
        if "test" in file_path or "mock" in file_path or "fixture" in file_path:
            return True
        if finding.get("severity", "").upper() == "INFO":
            return True
        return False
