DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'master') THEN
        CREATE USER master WITH PASSWORD 'HgAXVS5uWph3' SUPERUSER;
    END IF;
END
$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'query_user') THEN
        CREATE USER query_user WITH PASSWORD 'J5jY6vUttdF7';
        GRANT USAGE ON SCHEMA public TO query_user;
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO query_user;
    END IF;
END
$$;

