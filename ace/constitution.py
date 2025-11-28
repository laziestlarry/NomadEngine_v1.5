# ace/constitution.py
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Tuple


@dataclass
class Constitution:
    mission: str
    ethics: list[str]
    constraints: Dict[str, Any]

    def check_scores(self, scores: Dict[str, float]) -> Tuple[bool, Dict[str, Any]]:
        """
        Given scores like:
          {"roi_score": 0.7, "automation_score": 0.8, "risk_score": 0.3}
        return (allowed, details)
        """
        min_auto = float(self.constraints.get("min_automation_score", 0.0))
        max_risk = float(self.constraints.get("max_risk_score", 1.0))
        min_roi  = float(self.constraints.get("min_roi_score", 0.0))

        auto_ok = scores.get("automation_score", 0.0) >= min_auto
        risk_ok = scores.get("risk_score", 1.0) <= max_risk
        roi_ok  = scores.get("roi_score", 0.0) >= min_roi

        allowed = auto_ok and risk_ok and roi_ok

        return allowed, {
            "auto_ok": auto_ok,
            "risk_ok": risk_ok,
            "roi_ok": roi_ok,
            "thresholds": {
                "min_automation_score": min_auto,
                "max_risk_score": max_risk,
                "min_roi_score": min_roi,
            },
        }


def _load_constitution() -> Constitution:
    here = Path(__file__).resolve().parent
    cfg_path = here / "constitution.json"

    with cfg_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return Constitution(
        mission=data.get("mission", ""),
        ethics=data.get("ethics", []),
        constraints=data.get("constraints", {}),
    )


# singleton-style instance for easy import
constitution = _load_constitution()
