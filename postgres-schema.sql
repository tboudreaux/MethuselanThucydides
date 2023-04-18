--
-- PostgreSQL database dump
--

-- Dumped from database version 10.9 (Ubuntu 10.9-0ubuntu0.18.10.1)
-- Dumped by pg_dump version 10.9 (Ubuntu 10.9-0ubuntu0.18.10.1)

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

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
--

CREATE TABLE public.authors (
    uuid uuid NOT NULL,
    full_name text[] NOT NULL,
    first_name text
);



--
--

CREATE TABLE public.authors_papers (
    paper_uuid uuid NOT NULL,
    author_uuid uuid NOT NULL
);



--
--

CREATE TABLE public.papers (
    title character varying(200) NOT NULL,
    first_author character varying(100),
    url character varying(100) NOT NULL,
    abstract character varying(5000),
    comments character varying(5000),
    published_date date NOT NULL,
    added_date date DEFAULT CURRENT_DATE NOT NULL,
    last_used date,
    arxiv_id character varying(30),
    doi character varying(100),
    subjects character varying(200),
    hastex boolean,
    gpt_summary_short text,
    gpt_summary_long text,
    full_page_text text,
    num_authors integer,
    uuid uuid NOT NULL
);



--
--

CREATE TABLE public.queries (
    uuid uuid NOT NULL,
    query text NOT NULL,
    order_id integer NOT NULL,
    response text,
    paper_uuid uuid NOT NULL,
    created_at date NOT NULL,
    user_uuid uuid
);



--
--

CREATE TABLE public.users (
    username character varying(100) NOT NULL,
    password character varying(1000) NOT NULL,
    email character varying(100) NOT NULL,
    created_at date NOT NULL,
    last_login date,
    last_ip character varying(50),
    last_user_agent character varying(1000),
    last_country character varying(1000),
    last_city character varying(1000),
    last_timezone character varying(20),
    num_logins integer DEFAULT 0 NOT NULL,
    num_queries integer DEFAULT 0 NOT NULL,
    can_query boolean DEFAULT true NOT NULL,
    enabled boolean DEFAULT true NOT NULL,
    admin boolean DEFAULT false NOT NULL,
    salt character varying(100) NOT NULL,
    uuid uuid NOT NULL
);



--
--

ALTER TABLE ONLY public.papers
    ADD CONSTRAINT arxivsummary_pkey PRIMARY KEY (uuid);


--
--

ALTER TABLE ONLY public.authors_papers
    ADD CONSTRAINT authors_papers_pkey PRIMARY KEY (paper_uuid, author_uuid);


--
--

ALTER TABLE ONLY public.authors
    ADD CONSTRAINT authors_pkey PRIMARY KEY (uuid);


--
--

ALTER TABLE ONLY public.queries
    ADD CONSTRAINT queries_pkey PRIMARY KEY (uuid);


--
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (uuid);


--
--

ALTER TABLE ONLY public.authors_papers
    ADD CONSTRAINT author_uuid FOREIGN KEY (author_uuid) REFERENCES public.authors(uuid) NOT VALID;


--
--

ALTER TABLE ONLY public.authors_papers
    ADD CONSTRAINT paper_uuid FOREIGN KEY (paper_uuid) REFERENCES public.papers(uuid) NOT VALID;


--
-- PostgreSQL database dump complete
--

