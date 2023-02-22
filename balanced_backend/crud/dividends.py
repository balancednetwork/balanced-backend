from sqlalchemy.orm import Session
from sqlmodel import select

from balanced_backend.config import settings
from balanced_backend.crud.pools import get_pools


def init_dividends(session: 'Session'):
    """Init the dividends table """
