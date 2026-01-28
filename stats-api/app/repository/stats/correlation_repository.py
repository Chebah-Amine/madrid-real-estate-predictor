from app.config.extensions import get_collection
from typing import Any, Dict, List, Optional
import pandas as pd
import numpy as np


class CorrelationRepository:
    def __init__(self):
        self.collection = get_collection()

    def get_buy_price_correlation_matrix(
        self, features: List[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Return a correlation matrix for buy_price and given numeric features.
        - Uses Pearson correlation.
        - Filters out rows with missing/non-numeric values.
        - Ensures JSON-safe output (no NaN).
        """
        target = "buy_price"
        cols = [target] + features

        # Fetch only needed fields from Mongo
        projection = {c: 1 for c in cols}
        projection["_id"] = 0

        docs = list(self.collection.find({}, projection))
        if not docs:
            return None

        # Build DataFrame
        df = pd.DataFrame(docs)

        # Coerce to numeric (strings -> numbers where possible, invalid -> NaN)
        for c in cols:
            df[c] = pd.to_numeric(df.get(c), errors="coerce")

        # Drop rows with missing values for these columns
        df = df.dropna(subset=cols)
        if df.empty or len(df) < 2:
            return None

        # Correlation matrix (Pearson by default)
        corr = df[cols].corr(method="pearson")

        # JSON-safe (replace NaN/inf with None)
        corr = corr.replace([np.inf, -np.inf], np.nan)

        return {
            "target": target,
            "features": features,
            "rows_used": int(len(df)),
            "method": "pearson",
            "matrix": corr.to_dict(),  # nested dict: matrix[row][col] = corr
        }
