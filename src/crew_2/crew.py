from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, WebsiteSearchTool


web_scraper_tool = ScrapeWebsiteTool()
website_search_tool = WebsiteSearchTool()
@CrewBase
class Crew2Crew():
	"""Crew2 crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[web_scraper_tool, website_search_tool], 
			verbose=True
		)
	
	@task
	def analyze_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_task'],
			agent=self.researcher()
		)

	@task
	def update_database_task(self) -> Task:
		return Task(
			config=self.tasks_config['update_database_task'],
			agent=self.researcher(),
			# output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Crew2 crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
	
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