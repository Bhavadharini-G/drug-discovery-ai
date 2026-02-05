from crewai import Agent, Task, Crew
from langchain.tools import Tool
from tools.pubmed import pubmed_search
from tools.pubchem import fetch_compound_data

# Define LangChain-compatible tools
pubmed_search_tool = Tool.from_function(
    func=pubmed_search,
    name="PubMed Search",
    description="Search PubMed for studies related to a compound."
)

pubchem_fetch_tool = Tool.from_function(
    func=fetch_compound_data,
    name="PubChem Fetch",
    description="Fetch compound data from PubChem."
)

def create_drug_discovery_crew():
    researcher = Agent(
        role="Biomedical Researcher",
        goal="Find relevant drug studies",
        backstory="Expert in literature analysis",
        tools=[pubmed_search_tool],
        verbose=True
    )

    chemist = Agent(
        role="Medicinal Chemist",
        goal="Analyze compound properties",
        backstory="Computational chemistry specialist",
        tools=[pubchem_fetch_tool],
        verbose=True
    )


    literature_review = Task(
        description="Find studies on {compound} as a potential Alzheimer's drug candidate.",
        agent=researcher
    )

    compound_analysis = Task(
        description="Analyze chemical properties of {compound} and assess its drug potential.",
        agent=chemist,
        context=[literature_review],
        expected_output="A summary of chemical properties for each candidate."
    )

    return Crew(agents=[researcher, chemist], tasks=[literature_review, compound_analysis])
