from google.adk.tools import FunctionTool

class ContainerAnalysisTool(FunctionTool):
    name = "container_analysis_tool"
    description = "placeholder"
    async def _run(self, *args, **kwargs):
        return "ok"
