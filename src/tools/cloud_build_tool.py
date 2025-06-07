from google.adk.tools import FunctionTool

class CloudBuildTool(FunctionTool):
    name = "cloud_build_tool"
    description = "placeholder"
    async def _run(self, *args, **kwargs):
        return "ok"
