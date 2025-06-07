from google.adk.tools import FunctionTool

class GitHubTool(FunctionTool):
    name = "github_tool"
    description = "placeholder"
    async def _run(self, *args, **kwargs):
        return "ok"
