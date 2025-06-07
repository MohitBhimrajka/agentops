from google.adk.tools import FunctionTool

class SlackTool(FunctionTool):
    name = "slack_tool"
    description = "placeholder"
    async def _run(self, *args, **kwargs):
        return "ok"
