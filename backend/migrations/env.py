"""Migration metadata and environment-owned URL (never embed credentials)."""
from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel
from skillmatch.core.config import DATABASE_URL
from skillmatch.features.employees import models as employees  # noqa: F401
from skillmatch.features.jobs import models as jobs  # noqa: F401
from skillmatch.features.recommendations import models as recommendations  # noqa: F401
from skillmatch.features.feedback import models as feedback  # noqa: F401

from skillmatch.features.skills import models as skills  # noqa: F401

metadata = SQLModel.metadata

if context.is_offline_mode():
    context.configure(url=DATABASE_URL, target_metadata=metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    engine = engine_from_config({'sqlalchemy.url': DATABASE_URL}, prefix='sqlalchemy.', poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=metadata)
        with context.begin_transaction():
            context.run_migrations()
