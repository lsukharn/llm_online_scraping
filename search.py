from typing import Tuple
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from third_parties.linkedin import scrape_linkedin_profile  
from third_parties.twitter import scrape_user_tweets_mock

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from output_parsers import summary_parser, Summary


def agent_search(name: str) -> Tuple[Summary, str]:
    linkedin_url = ""
    # linkedin_url = linkedin_lookup_agent(name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=True)

    twitter_username = twitter_lookup_agent(name)
    print(f"twitter username: {twitter_username}")
    tweets = scrape_user_tweets_mock(twitter_username)

    summary_template = """
        given the LinkedIn information {information} about a person
        and twitter latest posts {twitter_posts} 
        I want you to create:
        1. a short summary
        2. two interesting facts about them

        use both information from Twitter and LinkedIn.
        \n{format_instructions} 
    """ 

    summary_template_prompt = PromptTemplate(input_variables=["information", "twitter_posts"], template=summary_template,
                                             partial_variables={"format_instructions": summary_parser.get_format_instructions()})

    # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    llm = ChatOllama(model="mistral")

    chain = summary_template_prompt | llm | summary_parser

    res: Summary = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})

    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    print("Scrape Online")
    agent_search(name="")
