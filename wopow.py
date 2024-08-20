from langchain_community.tools import E2BDataAnalysisTool

e2b_tool = E2BDataAnalysisTool()
result = e2b_tool.execute({"python_code": "print('Hello, World!')"})
print(result.stdout)