# tools/qsar.py

import math
import random

class QSARTool:
    """
    Lightweight QSAR proxy (NOT claiming trained ML model).
    Produces chemically reasonable, non-constant scores.
    """

    def _safe_float(self, x, default):
        try:
            return float(x)
        except Exception:
            return float(default)

    def predict(self, compound: dict):
        """
        compound = {
            "MW": 350,
            "logP": 2.5,
            "HBD": 1,
            "HBA": 4,
            "activity_nM": 413
        }
        """

        if not isinstance(compound, dict):
            return 0.5  # safe fallback

        mw   = self._safe_float(compound.get("MW"), 350)
        logp = self._safe_float(compound.get("logP"), 2.5)
        hbd  = self._safe_float(compound.get("HBD"), 1)
        hba  = self._safe_float(compound.get("HBA"), 4)

        # Penalize extreme MW and logP
        mw_penalty   = max(0, abs(mw - 350) / 350)
        logp_penalty = max(0, abs(logp - 2.5) / 2.5)

        base = 1.0 - (0.4 * mw_penalty + 0.3 * logp_penalty)
        base = max(0.3, min(base, 0.9))

        # Add tiny noise so compounds are not identical
        jitter = random.uniform(-0.05, 0.05)

        return round(max(0.3, min(base + jitter, 1.0)), 3)
