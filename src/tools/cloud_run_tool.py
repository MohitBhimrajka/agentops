from google.adk.tools import FunctionTool

class CloudRunTool(FunctionTool):
    name = "cloud_run_tool"
    description = "placeholder"
    async def _run(self, *args, **kwargs):
        return "ok"
