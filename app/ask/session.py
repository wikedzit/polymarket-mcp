from dataclasses import dataclass, field
from time import time
from uuid import uuid4

from app.ask.schemas import AskCandidate


@dataclass
class AskSession:
    session_id: str
    original_query: str
    pending_candidates: list[AskCandidate] | None = None
    created_at: float = field(default_factory=time)
    last_access: float = field(default_factory=time)


class SessionStore:
    def __init__(self, ttl_seconds: int = 1800) -> None:
        self._ttl = ttl_seconds
        self._sessions: dict[str, AskSession] = {}

    def create(self, original_query: str) -> AskSession:
        self._purge_expired()
        session = AskSession(session_id=str(uuid4()), original_query=original_query)
        self._sessions[session.session_id] = session
        return session

    def get(self, session_id: str) -> AskSession | None:
        self._purge_expired()
        session = self._sessions.get(session_id)
        if session is None:
            return None
        session.last_access = time()
        return session

    def save(self, session: AskSession) -> None:
        session.last_access = time()
        self._sessions[session.session_id] = session

    def clear_pending(self, session: AskSession) -> None:
        session.pending_candidates = None
        self.save(session)

    def _purge_expired(self) -> None:
        cutoff = time() - self._ttl
        expired = [sid for sid, s in self._sessions.items() if s.last_access < cutoff]
        for sid in expired:
            del self._sessions[sid]
