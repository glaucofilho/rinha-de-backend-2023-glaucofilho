SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;
COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';

SET default_tablespace = '';

SET default_table_access_method = heap;

CREATE TABLE public.pessoas (
    id uuid NOT NULL,
    apelido character varying(32) NOT NULL,
    nome character varying(100) NOT NULL,
    nascimento timestamp(6) without time zone,
    stack character varying,
    busca text GENERATED ALWAYS AS ((((((nome)::text || ' '::text) || (apelido)::text) || ' '::text) || (COALESCE(stack, ' '::character varying))::text)) STORED
);

ALTER TABLE ONLY public.pessoas
ADD CONSTRAINT pessoas_pkey PRIMARY KEY (id);

CREATE UNIQUE INDEX index_pessoas_on_apelido ON public.pessoas USING btree (apelido);

CREATE INDEX index_pessoas_on_busca ON public.pessoas USING gist (busca public.gist_trgm_ops);

SET search_path TO "$user", public;