import json
import re
from urllib.parse import quote
from urllib.request import Request, urlopen


def search(query: str) -> str:

    try:
        encoded_query = quote(query)

        url = (
            "https://en.wikipedia.org/w/api.php"
            f"?action=query"
            f"&list=search"
            f"&srsearch={encoded_query}"
            f"&format=json"
            f"&srlimit=3"
        )

        request = Request(
            url,
            headers={
                "User-Agent": "ReactAgentLearningProject/1.0"
            }
        )

        with urlopen(request, timeout=10) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

        results = data["query"]["search"]

        if not results:
            return "No results found."

        output = []

        for result in results:

            title = result["title"]

            snippet = re.sub(
                r"<[^>]+>",
                "",
                result["snippet"]
            )

            output.append(
                f"Title: {title}\n"
                f"Snippet: {snippet}"
            )

        return "\n\n".join(output)

    except Exception as e:

        return f"Search error: {str(e)}"