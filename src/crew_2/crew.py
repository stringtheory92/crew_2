from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, WebsiteSearchTool
from .tools.custom_tool import GetArticleLinkTool
from langchain_anthropic import ChatAnthropic

# from .tools.custom_tool import GetUnanalyzedArticleLinksTool

# https://github.com/alejandro-ao/exa-crewai/blob/master/src/newsletter_gen/config/tasks.yaml
web_scraper_tool = ScrapeWebsiteTool()
website_search_tool = WebsiteSearchTool()
# get_unanalyzed_article_links_tool = GetUnanalyzedArticleLinksTool()
get_article_link_tool = GetArticleLinkTool()

haiku = "claude-3-haiku-20240307"
Consistent = ChatAnthropic(
    temperature=0.0,
    model=haiku
)
url = 'https://news.google.com/articles/CBMiWWh0dHBzOi8vd3d3LnZveC5jb20vZnV0dXJlLXBlcmZlY3QvMzYxNzQ5L3VuaXZlcnNhbC1iYXNpYy1pbmNvbWUtc2FtLWFsdG1hbi1vcGVuLWFpLXN0dWR50gEA?hl=en-US&gl=US&ceid=US%3Aen'

database_query_specialist = Agent(
    role="Database Query Specialist",
    goal="Use the get_article_link_tool to Pull the article link from the database. Only use the tool.",
    backstory="Your only task is to execute the 'get_article_link_tool' you have access to. Do not perform any other actions, or generate any other text. Simply use the tool.",
    verbose=True,
    allow_delegations=False,
    tools=[get_article_link_tool],
    llm=Consistent
)

scraper_agent = Agent(
    role="Article Scraper",
    goal="Access the web page at the URL provided to you and use the provided 'web_scraper_tool' to fetch the text from that page.",
    backstory="Your only tasks are to follow the URL provided, read and return all text from the page at that URL. Do not return partial text. Do not return anything but the article text.",
    verbose=True,
    allow_delegations=False,
    tools=[web_scraper_tool],
    llm=Consistent
)
# scraper_agent = Agent(
#     role="Article Scraper",
#     goal="Access the web page at the URL provided to you and use the provided web_scraper_tool to fetch the text from that page. Only use the tool.",
#     backstory="Your only tasks are to follow the URL provided and execute the 'web_scraper_tool' you have access to on the web page at that URL. Do not perform any other actions, or generate any other text. Simply use the tool.",
#     verbose=True,
#     allow_delegations=False,
#     tools=[web_scraper_tool],
#     llm=Consistent
# )

query_task = Task(
    description="""Use the provided get_article_link_tool to find the article link from the database.
    ONLY OUTPUT THE URL RETURNED FROM THE TOOL. DO NOT GENERATE ANY OTHER TEXT. 
    DO NOT ADD ANY FORMATTING. SIMPLY OUTPUT THE URL RETURNED FROM THE TOOL.""",
    expected_output='A valid article URL.',
    agent=database_query_specialist,
)
scrape_article_task = Task(
    description="""A URL will be provided to you by the database_query_specialist. Access the website at the URL provided to you. Read the website and fetch the text from the given URL and return ALL TEXT.
    DO NOT DELEGATE THIS TASK TO ANYONE. ONLY OUTPUT THE TEXT RETURNED FROM THE TOOL. DO NOT GENERATE ANY OTHER TEXT. 
    DO NOT ADD ANY FORMATTING. DO NOT RETURN PARTIAL TEXT FROM THE TOOL. SIMPLY OUTPUT ALL THE TEXT RETURNED FROM THE TOOL.""",
    expected_output='The FULL PAGE text.',
    agent=scraper_agent,
    context=[query_task],  # Ensure the context includes the first task to get the URL
)
# scrape_article_task = Task(
#     description="""A URL will be provided to you by the database_query_specialist. Access the website at the URL provided to you. Use the provided web_scraper_tool to fetch the scraped text from the given URL and return ALL SCRAPED TEXT.
#     DO NOT DELEGATE THIS TASK TO ANYONE. ONLY OUTPUT THE TEXT RETURNED FROM THE TOOL. DO NOT GENERATE ANY OTHER TEXT. 
#     DO NOT ADD ANY FORMATTING. DO NOT RETURN PARTIAL TEXT FROM THE TOOL. SIMPLY OUTPUT ALL THE TEXT RETURNED FROM THE TOOL.""",
#     expected_output='The FULL PAGE text.',
#     agent=scraper_agent,
#     context=[query_task],  # Ensure the context includes the first task to get the URL
# )

crew = Crew(
    agents=[database_query_specialist, scraper_agent],
    tasks=[query_task, scrape_article_task],
    verbose=True
)
	
# researcher = Agent(
# 		role='AI Product Researcher',
# 		goal='Give a summary of the article located at the url https://news.google.com/articles/CBMiWWh0dHBzOi8vd3d3LnZveC5jb20vZnV0dXJlLXBlcmZlY3QvMzYxNzQ5L3VuaXZlcnNhbC1iYXNpYy1pbmNvbWUtc2FtLWFsdG1hbi1vcGVuLWFpLXN0dWR50gEA?hl=en-US&gl=US&ceid=US%3Aen.',
# 		backstory='The ResearcherAgent is an AI specialized in identifying, analyzing, and compiling information about features and products in the AI and machine learning domains, It has been trained on a vast dataset of AI and machine learning resources and is adept at discerning valuable insights from technical content, The agent is meticulous and thorough, ensuring that all relevant information is gathered and presented in a clear, concise manner.',
# 		tools=[web_scraper_tool],
#         max_iter=25
# 	)

# locate_article_url = Task(
#     description='Use the get_article_link_tool to Pull the article link from the database.',
#     expected_output='A valid article URL.',
#     agent=researcher
# )
# scrape_article_content = Task(
#     description='Follow the article URL (https://news.google.com/articles/CBMiWWh0dHBzOi8vd3d3LnZveC5jb20vZnV0dXJlLXBlcmZlY3QvMzYxNzQ5L3VuaXZlcnNhbC1iYXNpYy1pbmNvbWUtc2FtLWFsdG1hbi1vcGVuLWFpLXN0dWR50gEA?hl=en-US&gl=US&ceid=US%3Aen) and scrape the main article text.',
#     expected_output='The full article text or an error message if unable to scrape the content.',
#     # context=[locate_article_url],
#     agent=researcher
# )
# validate_scraped_content = Task(
#     description='Check if the scraped content is valid and contains the main article text.',
#     expected_output='Validation result of the scraped content (valid or invalid).',
#     context=[scrape_article_content],
#     agent=researcher
# )
# summarize_article = Task(
#     description='Summarize the valid article text.',
#     expected_output='A clear, complete summary of the article text.',
#     context=[validate_scraped_content],
#     agent=researcher
# )
# handle_errors = Task(
#     description='Handle any errors encountered during the process and log them appropriately.',
#     expected_output='An error message and logging details.',
#     context=[scrape_article_content, validate_scraped_content],
#     # context=[locate_article_url, scrape_article_content, validate_scraped_content],
#     agent=researcher
# )


# locate_and_scrape_article = Task(
# 		description='pull the article link from the db and follow it to the article page, locate the main article text and scrape the content. If unable to pull valid url from the db, terminate the process and inform what happened',
# 		expected_output='The articles full text',
# 		agent=researcher
# 	)


# summarize_article = Task(
# 		description='summarize the article text',
# 		expected_output='a clear, complete summary of the article text',
# 		context=[locate_and_scrape_article],
# 		agent=researcher
# 	)

# crew = Crew(
#     agents=[researcher],
#     tasks=[scrape_article_content, validate_scraped_content, summarize_article, handle_errors],
#     # tasks=[locate_article_url,scrape_article_content, validate_scraped_content, summarize_article, handle_errors],
#     verbose=True
# )
# @CrewBase
# class Crew2Crew():
# 	"""Crew2 crew"""
# 	agents_config = 'config/agents.yaml'
# 	tasks_config = 'config/tasks.yaml'
	

	# def researcher(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['researcher'],
	# 		tools=[web_scraper_tool, website_search_tool, get_unanalyzed_article_links_tool], 
	# 		verbose=True
	# 	)

	# @task
	# def analyze_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['analyze_task'],
	# 		agent=self.researcher()
	# 	)

	# @task
	# def update_database_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['update_database_task'],
	# 		agent=self.researcher(),
	# 		context=[self.tasks_config['analyze_task']]
	# 	)

	# @crew
	# def crew(self) -> Crew:
	# 	"""Creates the Crew2 crew"""
	# 	return Crew(
	# 		agents=self.agents, # Automatically created by the @agent decorator
	# 		tasks=self.tasks, # Automatically created by the @task decorator
	# 		process=Process.sequential,
	# 		verbose=2,
	# 		# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
	# 	)
	
# Original codes

# @CrewBase
# class Crew2Crew():
# 	"""Crew2 crew"""
# 	agents_config = 'config/agents.yaml'
# 	tasks_config = 'config/tasks.yaml'

# 	@agent
# 	def researcher(self) -> Agent:
# 		return Agent(
# 			config=self.agents_config['researcher'],
# 			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
# 			verbose=True
# 		)

# 	@agent
# 	def reporting_analyst(self) -> Agent:
# 		return Agent(
# 			config=self.agents_config['reporting_analyst'],
# 			verbose=True
# 		)

# 	@task
# 	def research_task(self) -> Task:
# 		return Task(
# 			config=self.tasks_config['research_task'],
# 			agent=self.researcher()
# 		)

# 	@task
# 	def reporting_task(self) -> Task:
# 		return Task(
# 			config=self.tasks_config['reporting_task'],
# 			agent=self.reporting_analyst(),
# 			output_file='report.md'
# 		)

# 	@crew
# 	def crew(self) -> Crew:
# 		"""Creates the Crew2 crew"""
# 		return Crew(
# 			agents=self.agents, # Automatically created by the @agent decorator
# 			tasks=self.tasks, # Automatically created by the @task decorator
# 			process=Process.sequential,
# 			verbose=2,
# 			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
# 		)