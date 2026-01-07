import requests

class AzureDevOpsClient:
    def __init__(self, organization: str, project: str, token: str):
        self.base_url = f"https://dev.azure.com/{organization}/{project}"
        self.auth = ("", token)
        self.headers = {"Content-Type": "application/json"}

    def fetch_done_items_with_effort(
        self,
        user_email: str,
        start_date: str,
        end_date: str,
    ) -> list[dict]:
        wiql_query = f"""
        SELECT [System.Id]
        FROM workitems
        WHERE [System.WorkItemType] = 'Product Backlog Item'
        AND [System.State] = 'Done'
        AND [System.AssignedTo] CONTAINS '{user_email}'
        AND [Microsoft.VSTS.Common.ClosedDate] >= '{start_date}'
        AND [Microsoft.VSTS.Common.ClosedDate] <= '{end_date}'
        AND [Microsoft.VSTS.Scheduling.Effort] > 0
        """

        response = requests.post(
            f"{self.base_url}/_apis/wit/wiql?api-version=7.0",
            auth=self.auth,
            headers=self.headers,
            json={"query": wiql_query},
        )

        ids = [str(i["id"]) for i in response.json().get("workItems", [])]

        if not ids:
            return []

        items_response = requests.get(
            f"{self.base_url}/_apis/wit/workitems"
            f"?ids={','.join(ids)}"
            f"&fields=System.Title,Microsoft.VSTS.Scheduling.Effort,Microsoft.VSTS.Common.BusinessValue"
            f"&api-version=7.0",
            auth=self.auth,
        )

        return items_response.json().get("value", [])
