from sqlalchemy import text

from app.database import engine


def migrate() -> None:
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                ALTER TABLE events
                ADD COLUMN IF NOT EXISTS external_event_id VARCHAR(255)
                """
            )
        )
        connection.execute(
            text(
                """
                UPDATE events
                SET external_event_id = 'legacy-' || id
                WHERE external_event_id IS NULL
                """
            )
        )
        connection.execute(
            text(
                """
                ALTER TABLE events
                ALTER COLUMN external_event_id SET NOT NULL
                """
            )
        )
        connection.execute(
            text(
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM pg_constraint
                        WHERE conname = 'uq_events_source_external_event_id'
                          AND conrelid = 'events'::regclass
                    ) THEN
                        ALTER TABLE events
                        ADD CONSTRAINT uq_events_source_external_event_id
                        UNIQUE (source, external_event_id);
                    END IF;
                END
                $$
                """
            )
        )

    print("external_event_id migration completed successfully.")


if __name__ == "__main__":
    migrate()
