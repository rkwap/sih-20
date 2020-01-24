--
-- PostgreSQL database dump
--

-- Dumped from database version 12.1
-- Dumped by pg_dump version 12.1

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: twitter; Type: TABLE; Schema: public; Owner: rkwap
--

CREATE TABLE public.twitter (
    t_id text NOT NULL,
    tweet text NOT NULL,
    polarity character varying(150),
    subjectivity character varying(150)
);


ALTER TABLE public.twitter OWNER TO rkwap;

--
-- Name: youtube; Type: TABLE; Schema: public; Owner: rkwap
--

CREATE TABLE public.youtube (
    id character varying(200) NOT NULL,
    c_id text NOT NULL,
    text text NOT NULL,
    polarity character varying(150),
    subjectivity character varying(150)
);


ALTER TABLE public.youtube OWNER TO rkwap;

--
-- Data for Name: twitter; Type: TABLE DATA; Schema: public; Owner: rkwap
--



--
-- Data for Name: youtube; Type: TABLE DATA; Schema: public; Owner: rkwap
--



--
-- Name: twitter twitter_pkey; Type: CONSTRAINT; Schema: public; Owner: rkwap
--

ALTER TABLE ONLY public.twitter
    ADD CONSTRAINT twitter_pkey PRIMARY KEY (t_id);


--
-- Name: youtube youtube_pkey; Type: CONSTRAINT; Schema: public; Owner: rkwap
--

ALTER TABLE ONLY public.youtube
    ADD CONSTRAINT youtube_pkey PRIMARY KEY (c_id);


--
-- PostgreSQL database dump complete
--

