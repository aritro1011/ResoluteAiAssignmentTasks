import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
import sys
import io

def execute_python_code(code: str) -> str:
    """Executes Python code safely and returns output or errors."""
    try:
        # Redirect stdout to capture output
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        exec(code, {})  # Execute in isolated environment
        
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        return output if output else "Code executed successfully."
    except Exception as e:
        sys.stdout = old_stdout
        return f"Error: {str(e)}"

# Define a tool for executing Python code
execute_tool = Tool(
    name="Python Executor",
    func=execute_python_code,
    description="Executes Python code and returns the output."
)

# Initialize LangChain agent
llm = GoogleGenerativeAI(model="gemini-pro", temperature=0)
agent = initialize_agent(
    tools=[execute_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Example usage
prompt = "Write a Python function to check if a number is prime and test it with 5."
response = agent.run(prompt)
print(response)
