import requests
import pandas as pd
from parser import parse_jsonstat  # changed from .parser to parser

class SSBClient:
    def __init__(self, base_url="https://data.ssb.no/api/v0/en/table/"):
        self.base_url = base_url

    def query(self, table_id, query):
        url = f"{self.base_url}{table_id}"
        response = requests.post(url, json=query)
        response.raise_for_status()
        df = parse_jsonstat(response.text)
        return df

# Example usage:
# client = SSBClient()
# df = client.query("05327", q1)
# df = client.query("05327", q1)
