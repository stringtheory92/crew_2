from crewai_tools import BaseTool
from crew_2.db_sqlite import DBHandler


class GetAllArticleLinksTool(BaseTool):
    name: str = "Get All Article Links Tool"
    description: str = (
        "Fetches all article links from the database."
    )

    def _run(self) -> list:
        db = DBHandler()
        query = "SELECT DISTINCT link FROM articles LIMIT 5"
        links = db.fetch_all(query)
        db.close()
        return [link[0] for link in links]

if __name__ == "__main__":
    tool = GetAllArticleLinksTool()
    print(tool._run())