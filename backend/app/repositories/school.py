from app.models.school import School
from app.repositories.base import BaseRepository


class SchoolRepository(BaseRepository[School]):
    """学校仓储"""
    
    def __init__(self):
        super().__init__(School)
