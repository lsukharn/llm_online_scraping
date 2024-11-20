import os
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools.tools import get_profile_url_tavily


load_dotenv()

# get_profile_url_tavily("Test Name")

def lookup(name: str):
    llm = ChatOllama(temperature=0.1, 
                     model="mistral")
    
    template = """given the full name {name_of_person} of a person I want you to get it me a link to their LinkedIn profile page.
                    Your answer should contain only a URL. Only one URL.""" # an output indicator
    
    prompt_template = PromptTemplate(input_variables=["name_of_person"], template=template)

    tools_for_agent = [ 
        Tool(
            name="Crawl Google for LinkedIn profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the LinkedIn page URL" # how the llm is going to determine to use this tool or not
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)  # the recipe
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True)  # the entity that invokes functions in the recipe

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )
    return result['output'][1:-2]

if __name__ == "__main__":
    linkedin_url = lookup(name = "Eden Marco")
    print(linkedin_url)
