BEGIN;
    ALTER TABLE card ADD COLUMN collected BOOLEAN DEFAULT false;
COMMIT;