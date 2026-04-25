class RiskScoringService:
    @staticmethod
    def calculate(severity: str, exposure: str = "internal") -> float:
        base = {
            "CRITICAL": 9.0,
            "HIGH": 7.0,
            "MEDIUM": 5.0,
            "LOW": 3.0
        }.get(severity.upper(), 1.0)
        multiplier = 1.5 if exposure == "public" else 1.0
        return round(base * multiplier, 2)
