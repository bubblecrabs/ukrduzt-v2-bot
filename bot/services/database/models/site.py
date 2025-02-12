from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from bot.services.database.models.base import Base


class WebsiteSettings(Base):
    """Represents the site settings in the database."""
    __tablename__ = "website_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, default=81)
    semester: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
