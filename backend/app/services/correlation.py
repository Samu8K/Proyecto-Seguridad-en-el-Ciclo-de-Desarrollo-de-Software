import hashlib

class CorrelationService:
    @staticmethod
    def generate_group(finding_data: dict) -> str:
        key = f"{finding_data.get('cwe_id', '')}_{finding_data.get('file_path', '')}"
        return hashlib.sha256(key.encode()).hexdigest()
