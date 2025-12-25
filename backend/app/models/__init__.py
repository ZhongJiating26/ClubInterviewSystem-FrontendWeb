from app.models.school import School  # noqa: F401
from app.models.user_account import UserAccount  # noqa: F401
from app.models.role import Role, Permission, RolePermission, UserRole  # noqa: F401
from app.models.major import Major  # noqa: F401
from app.models.club import Club, ClubMember  # noqa: F401
from app.models.department import Department  # noqa: F401
from app.models.position import Position  # noqa: F401
from app.models.recruitment import Recruitment, Application, Interview  # noqa: F401
from app.models.interview_session import (  # noqa: F401
    InterviewSession,
    InterviewerAssignment,
    InterviewCandidate,
    InterviewRecord,
    ScoreTemplate,
    ScoreItem,
    InterviewScore,
)
from app.models.notification import Notification  # noqa: F401
from app.models.ticket import Ticket, TicketReply  # noqa: F401
from app.models.faq import FAQ  # noqa: F401
