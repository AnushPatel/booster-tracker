--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.10
-- Dumped by pg_dump version 9.6.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
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
-- Name: _auth_group; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._auth_group (
    id character varying(1) DEFAULT NULL::character varying,
    name character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE public._auth_group OWNER TO rebasedata;

--
-- Name: _auth_group_permissions; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._auth_group_permissions (
    id character varying(1) DEFAULT NULL::character varying,
    group_id character varying(1) DEFAULT NULL::character varying,
    permission_id character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE public._auth_group_permissions OWNER TO rebasedata;

--
-- Name: _auth_permission; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._auth_permission (
    id smallint,
    content_type_id smallint,
    codename character varying(25) DEFAULT NULL::character varying,
    name character varying(31) DEFAULT NULL::character varying
);


ALTER TABLE public._auth_permission OWNER TO rebasedata;

--
-- Name: _auth_user; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._auth_user (
    id smallint,
    password character varying(88) DEFAULT NULL::character varying,
    last_login character varying(10) DEFAULT NULL::character varying,
    is_superuser smallint,
    username character varying(5) DEFAULT NULL::character varying,
    last_name character varying(1) DEFAULT NULL::character varying,
    email character varying(25) DEFAULT NULL::character varying,
    is_staff smallint,
    is_active smallint,
    date_joined character varying(10) DEFAULT NULL::character varying,
    first_name character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE public._auth_user OWNER TO rebasedata;

--
-- Name: _auth_user_groups; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._auth_user_groups (
    id character varying(1) DEFAULT NULL::character varying,
    user_id character varying(1) DEFAULT NULL::character varying,
    group_id character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE public._auth_user_groups OWNER TO rebasedata;

--
-- Name: _auth_user_user_permissions; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._auth_user_user_permissions (
    id character varying(1) DEFAULT NULL::character varying,
    user_id character varying(1) DEFAULT NULL::character varying,
    permission_id character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE public._auth_user_user_permissions OWNER TO rebasedata;

--
-- Name: _booster_tracker_boat; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._booster_tracker_boat (
    id smallint,
    name character varying(19) DEFAULT NULL::character varying,
    type character varying(19) DEFAULT NULL::character varying,
    status character varying(7) DEFAULT NULL::character varying
);


ALTER TABLE public._booster_tracker_boat OWNER TO rebasedata;

--
-- Name: _booster_tracker_fairingrecovery; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._booster_tracker_fairingrecovery (
    id smallint,
    catch smallint,
    recovery character varying(7) DEFAULT NULL::character varying,
    launch_id smallint,
    latitude character varying(7) DEFAULT NULL::character varying,
    longitude character varying(9) DEFAULT NULL::character varying,
    flights character varying(7) DEFAULT NULL::character varying,
    boat_id smallint
);


ALTER TABLE public._booster_tracker_fairingrecovery OWNER TO rebasedata;

--
-- Name: _booster_tracker_landingzone; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._booster_tracker_landingzone (
    id smallint,
    name character varying(30) DEFAULT NULL::character varying,
    nickname character varying(6) DEFAULT NULL::character varying,
    serial_number character varying(10) DEFAULT NULL::character varying,
    status character varying(7) DEFAULT NULL::character varying,
    image character varying(31) DEFAULT NULL::character varying
);


ALTER TABLE public._booster_tracker_landingzone OWNER TO rebasedata;

--
-- Name: _booster_tracker_launch; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._booster_tracker_launch (
    id smallint,
    "time" character varying(1) DEFAULT NULL::character varying,
    name character varying(66) DEFAULT NULL::character varying,
    customer character varying(47) DEFAULT NULL::character varying,
    launch_outcome character varying(15) DEFAULT NULL::character varying,
    rocket_id smallint,
    mass character varying(45) DEFAULT NULL::character varying,
    pad_id smallint,
    orbit_id smallint
);


ALTER TABLE public._booster_tracker_launch OWNER TO rebasedata;

--
-- Name: _booster_tracker_operator; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._booster_tracker_operator (
    id smallint,
    name character varying(6) DEFAULT NULL::character varying
);


ALTER TABLE public._booster_tracker_operator OWNER TO rebasedata;

--
-- Name: _booster_tracker_orbit; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._booster_tracker_orbit (
    id smallint,
    name character varying(34) DEFAULT NULL::character varying
);


ALTER TABLE public._booster_tracker_orbit OWNER TO rebasedata;

--
-- Name: _booster_tracker_pad; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._booster_tracker_pad (
    id smallint,
    name character varying(27) DEFAULT NULL::character varying,
    nickname character varying(13) DEFAULT NULL::character varying,
    location character varying(60) DEFAULT NULL::character varying,
    status character varying(7) DEFAULT NULL::character varying,
    image character varying(29) DEFAULT NULL::character varying
);


ALTER TABLE public._booster_tracker_pad OWNER TO rebasedata;

--
-- Name: _booster_tracker_padused; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._booster_tracker_padused (
    id smallint,
    pad_id smallint,
    rocket_id smallint,
    image character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE public._booster_tracker_padused OWNER TO rebasedata;

--
-- Name: _booster_tracker_rocket; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._booster_tracker_rocket (
    id smallint,
    name character varying(12) DEFAULT NULL::character varying,
    status character varying(7) DEFAULT NULL::character varying,
    family_id smallint
);


ALTER TABLE public._booster_tracker_rocket OWNER TO rebasedata;

--
-- Name: _booster_tracker_rocketfamily; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._booster_tracker_rocketfamily (
    id smallint,
    name character varying(8) DEFAULT NULL::character varying,
    provider_id smallint
);


ALTER TABLE public._booster_tracker_rocketfamily OWNER TO rebasedata;

--
-- Name: _booster_tracker_spacecraft; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._booster_tracker_spacecraft (
    id smallint,
    name character varying(4) DEFAULT NULL::character varying,
    nickname character varying(10) DEFAULT NULL::character varying,
    version character varying(2) DEFAULT NULL::character varying,
    type character varying(5) DEFAULT NULL::character varying,
    family_id smallint,
    status character varying(7) DEFAULT NULL::character varying,
    image character varying(36) DEFAULT NULL::character varying
);


ALTER TABLE public._booster_tracker_spacecraft OWNER TO rebasedata;

--
-- Name: _booster_tracker_spacecraftfamily; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._booster_tracker_spacecraftfamily (
    id smallint,
    status character varying(6) DEFAULT NULL::character varying,
    provider_id smallint,
    name character varying(6) DEFAULT NULL::character varying
);


ALTER TABLE public._booster_tracker_spacecraftfamily OWNER TO rebasedata;

--
-- Name: _booster_tracker_spacecraftonlaunch; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._booster_tracker_spacecraftonlaunch (
    id smallint,
    splashdown_time character varying(1) DEFAULT NULL::character varying,
    launch_id smallint,
    spacecraft_id smallint,
    recovery_boat_id character varying(3) DEFAULT NULL::character varying
);


ALTER TABLE public._booster_tracker_spacecraftonlaunch OWNER TO rebasedata;

--
-- Name: _booster_tracker_stage; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._booster_tracker_stage (
    id smallint,
    version character varying(9) DEFAULT NULL::character varying,
    type character varying(12) DEFAULT NULL::character varying,
    rocket_id smallint,
    name character varying(5) DEFAULT NULL::character varying,
    status character varying(8) DEFAULT NULL::character varying,
    image character varying(32) DEFAULT NULL::character varying
);


ALTER TABLE public._booster_tracker_stage OWNER TO rebasedata;

--
-- Name: _booster_tracker_stageandrecovery; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._booster_tracker_stageandrecovery (
    method character varying(13) DEFAULT NULL::character varying,
    recovery_success smallint,
    latitude character varying(10) DEFAULT NULL::character varying,
    longitude character varying(12) DEFAULT NULL::character varying,
    landing_zone_id character varying(2) DEFAULT NULL::character varying,
    launch_id smallint,
    stage_id character varying(3) DEFAULT NULL::character varying,
    method_success character varying(9) DEFAULT NULL::character varying,
    stage_position character varying(11) DEFAULT NULL::character varying,
    id smallint
);


ALTER TABLE public._booster_tracker_stageandrecovery OWNER TO rebasedata;

--
-- Name: _booster_tracker_supportonlaunch; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._booster_tracker_supportonlaunch (
    id smallint,
    boat_id smallint,
    launch_id smallint
);


ALTER TABLE public._booster_tracker_supportonlaunch OWNER TO rebasedata;

--
-- Name: _booster_tracker_tugonlaunch; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._booster_tracker_tugonlaunch (
    id smallint,
    boat_id smallint,
    launch_id smallint
);


ALTER TABLE public._booster_tracker_tugonlaunch OWNER TO rebasedata;

--
-- Name: _django_admin_log; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._django_admin_log (
    id smallint,
    object_id smallint,
    object_repr character varying(41) DEFAULT NULL::character varying,
    action_flag smallint,
    change_message character varying(398) DEFAULT NULL::character varying,
    content_type_id smallint,
    user_id smallint,
    action_time character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE public._django_admin_log OWNER TO rebasedata;

--
-- Name: _django_content_type; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._django_content_type (
    id smallint,
    app_label character varying(15) DEFAULT NULL::character varying,
    model character varying(18) DEFAULT NULL::character varying
);


ALTER TABLE public._django_content_type OWNER TO rebasedata;

--
-- Name: _django_migrations; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._django_migrations (
    id smallint,
    app character varying(15) DEFAULT NULL::character varying,
    name character varying(66) DEFAULT NULL::character varying,
    applied character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE public._django_migrations OWNER TO rebasedata;

--
-- Name: _django_session; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._django_session (
    session_key character varying(32) DEFAULT NULL::character varying,
    session_data character varying(226) DEFAULT NULL::character varying,
    expire_date character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE public._django_session OWNER TO rebasedata;

--
-- Name: _sqlite_sequence; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._sqlite_sequence (
    name character varying(34) DEFAULT NULL::character varying,
    seq smallint
);


ALTER TABLE public._sqlite_sequence OWNER TO rebasedata;

--
-- Data for Name: _auth_group; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: _auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: _auth_permission; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._auth_permission (id, content_type_id, codename, name) FROM stdin;
1	1	add_rocket	Can add rocket
2	1	change_rocket	Can change rocket
3	1	delete_rocket	Can delete rocket
4	1	view_rocket	Can view rocket
5	2	add_stage	Can add stage
6	2	change_stage	Can change stage
7	2	delete_stage	Can delete stage
8	2	view_stage	Can view stage
9	3	add_boat	Can add boat
10	3	change_boat	Can change boat
11	3	delete_boat	Can delete boat
12	3	view_boat	Can view boat
13	4	add_orbit	Can add orbit
14	4	change_orbit	Can change orbit
15	4	delete_orbit	Can delete orbit
16	4	view_orbit	Can view orbit
17	5	add_pad	Can add pad
18	5	change_pad	Can change pad
19	5	delete_pad	Can delete pad
20	5	view_pad	Can view pad
21	6	add_launch	Can add launch
22	6	change_launch	Can change launch
23	6	delete_launch	Can delete launch
24	6	view_launch	Can view launch
25	7	add_landingzone	Can add landing zone
26	7	change_landingzone	Can change landing zone
27	7	delete_landingzone	Can delete landing zone
28	7	view_landingzone	Can view landing zone
29	8	add_stageandrecovery	Can add stage and recovery
30	8	change_stageandrecovery	Can change stage and recovery
31	8	delete_stageandrecovery	Can delete stage and recovery
32	8	view_stageandrecovery	Can view stage and recovery
33	9	add_fairingrecovery	Can add fairing recovery
34	9	change_fairingrecovery	Can change fairing recovery
35	9	delete_fairingrecovery	Can delete fairing recovery
36	9	view_fairingrecovery	Can view fairing recovery
37	10	add_tugandsupport	Can add tug and support
38	10	change_tugandsupport	Can change tug and support
39	10	delete_tugandsupport	Can delete tug and support
40	10	view_tugandsupport	Can view tug and support
41	11	add_logentry	Can add log entry
42	11	change_logentry	Can change log entry
43	11	delete_logentry	Can delete log entry
44	11	view_logentry	Can view log entry
45	12	add_permission	Can add permission
46	12	change_permission	Can change permission
47	12	delete_permission	Can delete permission
48	12	view_permission	Can view permission
49	13	add_group	Can add group
50	13	change_group	Can change group
51	13	delete_group	Can delete group
52	13	view_group	Can view group
53	14	add_user	Can add user
54	14	change_user	Can change user
55	14	delete_user	Can delete user
56	14	view_user	Can view user
57	15	add_contenttype	Can add content type
58	15	change_contenttype	Can change content type
59	15	delete_contenttype	Can delete content type
60	15	view_contenttype	Can view content type
61	16	add_session	Can add session
62	16	change_session	Can change session
63	16	delete_session	Can delete session
64	16	view_session	Can view session
65	17	add_boatsupport	Can add boat support
66	17	change_boatsupport	Can change boat support
67	17	delete_boatsupport	Can delete boat support
68	17	view_boatsupport	Can view boat support
69	18	add_tugonlaunch	Can add tug on launch
70	18	change_tugonlaunch	Can change tug on launch
71	18	delete_tugonlaunch	Can delete tug on launch
72	18	view_tugonlaunch	Can view tug on launch
73	19	add_supportonlaunch	Can add support on launch
74	19	change_supportonlaunch	Can change support on launch
75	19	delete_supportonlaunch	Can delete support on launch
76	19	view_supportonlaunch	Can view support on launch
77	20	add_dragononlaunch	Can add dragon on launch
78	20	change_dragononlaunch	Can change dragon on launch
79	20	delete_dragononlaunch	Can delete dragon on launch
80	20	view_dragononlaunch	Can view dragon on launch
81	21	add_dragon	Can add dragon
82	21	change_dragon	Can change dragon
83	21	delete_dragon	Can delete dragon
84	21	view_dragon	Can view dragon
85	22	add_operator	Can add operator
86	22	change_operator	Can change operator
87	22	delete_operator	Can delete operator
88	22	view_operator	Can view operator
89	23	add_spacecraft	Can add spacecraft
90	23	change_spacecraft	Can change spacecraft
91	23	delete_spacecraft	Can delete spacecraft
92	23	view_spacecraft	Can view spacecraft
93	24	add_spacecraftonlaunch	Can add spacecraft on launch
94	24	change_spacecraftonlaunch	Can change spacecraft on launch
95	24	delete_spacecraftonlaunch	Can delete spacecraft on launch
96	24	view_spacecraftonlaunch	Can view spacecraft on launch
97	25	add_padused	Can add pad used
98	25	change_padused	Can change pad used
99	25	delete_padused	Can delete pad used
100	25	view_padused	Can view pad used
101	26	add_spacecraftfamily	Can add spacecraft family
102	26	change_spacecraftfamily	Can change spacecraft family
103	26	delete_spacecraftfamily	Can delete spacecraft family
104	26	view_spacecraftfamily	Can view spacecraft family
105	27	add_rocketfamily	Can add rocket family
106	27	change_rocketfamily	Can change rocket family
107	27	delete_rocketfamily	Can delete rocket family
108	27	view_rocketfamily	Can view rocket family
\.


--
-- Data for Name: _auth_user; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._auth_user (id, password, last_login, is_superuser, username, last_name, email, is_staff, is_active, date_joined, first_name) FROM stdin;
1	pbkdf2_sha256$720000$PV3xSxmpo0MizrgkUTeASR$/0rcSUGsWLRbtIAJ3PZ9IvpLLMZosiDY0+j/errMyzw=	2024-06-03	1	admin		trevor.monkey@outlook.com	1	1	2024-04-02
\.


--
-- Data for Name: _auth_user_groups; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: _auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: _booster_tracker_boat; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._booster_tracker_boat (id, name, type, status) FROM stdin;
234	GO Quest	SUPPORT	RETIRED
235	Elsbeth III	TUG	RETIRED
236	NRC Quest	SUPPORT	RETIRED
237	Int. Freedom	TUG	RETIRED
238	GO Searcher	FAIRING_RECOVERY	RETIRED
239	Pacific Warrior	TUG	RETIRED
240	Kelly C	TUG	RETIRED
241	Betty R Gambarella	TUG	RETIRED
242	Hawk	TUG	RETIRED
243	Mr. Steven	FAIRING_RECOVERY	RETIRED
244	GO Pursuit	FAIRING_RECOVERY	RETIRED
245	Rachel	TUG	RETIRED
246	Freedom	TUG	RETIRED
247	John Henry	SUPPORT	RETIRED
248	Signet Warhorse III	TUG	ACTIVE
249	Hollywood	TUG	RETIRED
250	GO Navigator	FAIRING_RECOVERY	RETIRED
251	GO Ms. Tree	FAIRING_RECOVERY	RETIRED
252	GO Ms. Chief	FAIRING_RECOVERY	RETIRED
253	Finn Falgout	TUG	RETIRED
254	Lauren Floss	TUG	RETIRED
255	NRC Quest	FAIRING_RECOVERY	RETIRED
256	GO Searcher	SUPPORT	RETIRED
257	Shelia Bordelon	FAIRING_RECOVERY	RETIRED
258	Mr. Jonah	TUG	RETIRED
259	Hos Briarwood	FAIRING_RECOVERY	RETIRED
260	Adele Elise	SUPPORT	RETIRED
261	Scorpius	TUG	ACTIVE
262	Doug	SUPPORT	ACTIVE
263	Doug	TUG	ACTIVE
264	Bob	FAIRING_RECOVERY	ACTIVE
265	Bob	SUPPORT	ACTIVE
266	Doug	FAIRING_RECOVERY	ACTIVE
267	Zion M Falgout	TUG	RETIRED
268	Bob	TUG	ACTIVE
269	Debra C	TUG	RETIRED
270	Kurt J Crosby	TUG	RETIRED
271	Crosby Skipper	TUG	RETIRED
272	Crosby Endeavor	TUG	RETIRED
273	GO Beyond	SUPPORT	ACTIVE
274	Nicole Foss	TUG	RETIRED
275	GO Beyond	FAIRING_RECOVERY	ACTIVE
276	Signet Titan	TUG	ACTIVE
277	Kimberly C	TUG	ACTIVE
278	Signet Titan III	TUG	ACTIVE
279	Lindsay C	TUG	ACTIVE
280	Crosby Courage	TUG	ACTIVE
281	Signet Warhorse I	TUG	ACTIVE
282	Megan	SPACECRAFT_RECOVERY	ACTIVE
283	Shannon	SPACECRAFT_RECOVERY	ACTIVE
284	Champion	SPACECRAFT_RECOVERY	RETIRED
285	Islander	SPACECRAFT_RECOVERY	RETIRED
286	GO Quest	SPACECRAFT_RECOVERY	RETIRED
287	N/A	SPACECRAFT_RECOVERY	RETIRED
\.


--
-- Data for Name: _booster_tracker_fairingrecovery; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._booster_tracker_fairingrecovery (id, catch, recovery, launch_id, latitude, longitude, flights, boat_id) FROM stdin;
4941	0	No	4057			1	238
4942	0	No	4057			1	238
4943	0	No	4058			1	238
4944	0	No	4058			1	238
4945	0	No	4060			1	238
4946	0	No	4060			1	238
4947	0	No	4065			1	238
4948	0	No	4065			1	238
4949	0	No	4069	28.188	-72.5471	1	238
4950	0	No	4069	28.188	-72.5471	1	238
4951	0	Unknown	4071	27.8327	-71.4227	1	238
4952	0	Unknown	4071	27.8327	-71.4227	1	238
4953	0	No	4076	28.3337	-72.7872	1	238
4954	0	No	4076	28.3337	-72.7872	1	238
4955	0	No	4077	27.9454	-72.5367	1	243
4956	0	No	4077	27.9454	-72.5367	1	243
4957	0	No	4079	28.7734	-120.608	1	243
4958	0	No	4079	28.7734	-120.608	1	243
4959	0	No	4081	28.023	-72.448	1	238
4960	0	No	4081	28.023	-72.448	1	238
4961	0	Yes	4083	30.3469	-121.5926	1	243
4962	0	No	4083	30.3469	-121.5926	1	243
4963	0	Yes	4085	28.6844	-120.5613	1	243
4964	0	No	4085	28.6844	-120.5613	1	243
4965	0	No	4087	29.1268	-74.6131	1	244
4966	0	No	4087	29.1268	-74.6131	1	244
4967	0	No	4088	28.1716	-72.6994	1	244
4968	0	No	4088	28.1716	-72.6994	1	244
4969	0	Yes	4089	26.6617	-120.542	1	243
4970	0	Yes	4089	26.6617	-120.542	1	243
4971	0	Yes	4090	28.5915	-71.089	1	244
4972	0	No	4090	28.5915	-71.089	1	244
4973	0	No	4092	28.2624	-72.6927	1	244
4974	0	No	4092	28.2624	-72.6927	1	244
4975	0	Yes	4093	29.3728	-119.9917	1	243
4976	0	No	4093	29.3728	-119.9917	1	243
4977	0	Yes	4098	31.5812	-121.1726	1	243
4978	0	Yes	4098	31.5812	-121.1726	1	243
4979	0	No	4100			1	244
4980	0	No	4100			1	244
4981	0	No	4102			1	243
4982	0	No	4102			1	243
4983	0	Yes	4104	28.5697	-70.0745	1	238
4984	0	Yes	4104	28.5697	-70.0745	1	250
4985	0	Yes	4106	33.3677	-75.4648	1	238
4986	0	Yes	4106	33.3677	-75.4648	1	250
4987	1	Yes	4108	27.7854	-66.9092	1	251
4988	0	No	4108	27.7854	-66.9092	1	250
4989	0	Yes	4110	28.4536	-71.1429	1	250
4990	1	Yes	4110	28.4536	-71.1429	1	251
4991	0	Yes	4113	28.2755	-72.5105	1	251
4992	0	Yes	4113	28.2755	-72.5105	1	252
4993	0	Yes	4114	33.1057	-74.9103	1	250
4994	0	No	4114	33.1057	-74.9103	1	251
4995	1	Yes	4116	33.1182	-74.8355	1	251
4996	0	Yes	4116	33.1182	-74.8355	1	252
4997	0	No	4117	32.9148	-75.0544	1	251
4998	0	No	4117	32.9148	-75.0544	1	252
4999	0	Yes	4119	32.9153	-75.2082	2	251
5000	0	No	4119	32.9153	-75.2082	2	252
5001	0	Yes	4120	32.8687	-75.0624	2	251
5002	0	Yes	4120	32.8687	-75.0624	2	252
5003	0	No	4122	32.9617	-75.3934	1	251
5004	0	Yes	4122	32.9617	-75.3934	1	252
5005	0	Yes	4123	32.9377	-75.4719	2	251
5006	0	Yes	4123	32.9377	-75.4719	2	252
5007	0	Yes	4124	33.709	-75.4523	1	251
5008	0	Yes	4124	33.709	-75.4523	1	252
5009	1	Yes	4125	28.2239	-72.5504	1	252
5010	1	Yes	4125	28.2239	-72.5504	1	251
5011	0	Yes	4126	33.1017	-75.2575	1	251
5012	0	Yes	4126	33.1017	-75.2575	1	252
5013	1	Yes	4127	33.0546	-75.3524	2	251
5014	0	Yes	4127	33.0546	-75.3524	2	252
5015	0	Yes	4128	23.9197	-79.3656	1	252
5016	0	Yes	4128	23.9197	-79.3656	1	252
5017	0	No	4129	32.9513	-75.4305	1	251
5018	0	No	4129	32.9513	-75.4305	1	252
5019	1	Yes	4130	33.0897	-75.0922	3	251
5020	0	Yes	4130	33.0897	-75.0922	1	252
5021	1	Yes	4131	33.0232	-75.2861	3	251
5022	1	Yes	4131	33.0232	-75.2861	3	252
5023	0	Yes	4132	32.8867	-75.4927	1	252
5024	0	Yes	4132	32.8867	-75.4927	1	252
5025	0	Yes	4133	33.6533	-75.2923	1	252
5026	0	Yes	4133	33.6533	-75.2923	1	252
5027	0	Yes	4135	31.1766	-118.4649	1	255
5028	0	Yes	4135	31.1766	-118.4649	1	255
5029	0	Yes	4136	32.8131	-75.3236	3	252
5030	0	Yes	4136	32.8131	-75.3236	2	238
5031	0	Yes	4138	28.2805	-72.4669	1	251
5032	0	Yes	4138	28.2805	-72.4669	2	238
5033	0	Yes	4139	30.6557	-78.2368	1	251
5034	0	Yes	4139	30.6557	-78.2368	1	238
5035	0	No	4140	28.1033	-71.9681	2	251
5036	0	Yes	4140	28.1033	-71.9681	2	252
5037	0	No	4141	32.8067	-75.0928	3	251
5038	0	No	4141	32.8067	-75.0928	2	252
5039	0	Yes	4142	23.2352	-78.9927	1	251
5040	0	Yes	4142	23.2352	-78.9927	1	252
5041	0	Yes	4143	32.6623	-75.2623	2	251
5042	0	Yes	4143	32.6623	-75.2623	2	252
5043	0	Yes	4144	33.065	-75.3517	1	252
5044	0	No	4144	33.065	-75.3517	1	251
5045	0	Yes	4145	32.6804	-75.5142	4	250
5046	0	Yes	4145	32.6804	-75.5142	3	238
5047	0	Yes	4146	32.7836	-75.5665	2	250
5048	0	Yes	4146	32.7836	-75.5665	3	238
5049	0	Yes	4147	32.6549	-75.2794	2	250
5050	0	Yes	4147	32.6549	-75.2794	2	238
5051	0	Yes	4148	32.9883	-75.49	2	257
5052	0	Yes	4148	32.9883	-75.49	2	257
5053	0	Yes	4149	32.6767	-75.4683	4	257
5054	0	No	4149	32.6767	-75.4683	2	257
5055	0	Yes	4151	32.855	-75.49	1	257
5056	0	Yes	4151	32.855	-75.49	1	257
5057	0	No	4152	32.8033	-75.4317	3	257
5058	0	Yes	4152	32.8033	-75.4317	1	257
5059	0	Yes	4153	32.6933	-75.515	2	257
5060	0	Yes	4153	32.6933	-75.515	2	257
5061	0	Yes	4154	32.7783	-75.3917	2	257
5062	0	No	4154	32.7783	-75.3917	2	257
5063	0	Yes	4155	32.7643	-75.6101	5	250
5064	0	Yes	4155	32.7643	-75.6101	3	238
5065	0	Yes	4157	28.3309	-72.7926	1	250
5066	0	Yes	4157	28.3309	-72.7926	1	238
5067	0	Yes	4158	33.6533	-74.915	1	259
5068	0	Yes	4158	33.6533	-74.915	1	259
5069	0	Yes	4159	23.38	-79.26	3	259
5070	0	Yes	4159	23.38	-79.26	3	259
5071	0	Yes	4161	29.0383	-117.7153	2	255
5072	0	Yes	4161	29.0383	-117.7153	3	255
5073	0	Yes	4164	32.7395	-75.5675	3	264
5074	0	Yes	4164	32.7395	-75.5675	2	264
5075	0	Yes	4165	28.1139	-119.0738	1	255
5076	0	Yes	4165	28.1139	-119.0738	1	255
5077	0	Yes	4166	32.9	-75.1539	1	264
5078	0	Yes	4166	32.9	-75.1539	1	264
5079	0	Yes	4167	28.0884	-71.8599	1	264
5080	0	Yes	4167	28.0884	-71.8599	1	264
5081	0	Yes	4168	29.7984	-116.8156	3	255
5082	0	Yes	4168	29.7984	-116.8156	4	255
5083	0	Yes	4169	28.1826	-72.5141	2	264
5084	0	Yes	4169	28.1826	-72.5141	2	264
5085	0	Yes	4171	25.7448	-74.9456	5	266
5086	0	Yes	4171	25.7448	-74.9456	4	266
5087	0	Yes	4172	23.2205	-79.1353	1	264
5088	0	Yes	4172	23.2205	-79.1353	1	264
5089	0	Yes	4173	25.7262	-74.933	2	266
5090	0	Yes	4173	25.7262	-74.933	2	266
5091	0	Yes	4174	23.163	-79.2897	4	264
5092	0	Yes	4174	23.163	-79.2897	4	264
5093	0	Yes	4175	31.2444	-121.6432	1	255
5094	0	Yes	4175	31.2444	-121.6432	1	255
5095	0	Yes	4176	25.647	-75.0376	6	266
5096	0	Yes	4176	25.647	-75.0376	4	266
5097	0	Yes	4177	25.5609	-74.9925	3	266
5098	0	Yes	4177	25.5609	-74.9925	3	266
5099	0	Unknown	4178	29.8483	-116.5799	3	255
5100	0	Unknown	4178	29.8483	-116.5799	3	255
5101	0	Yes	4179	25.5917	-75.155	3	264
5102	0	Yes	4179	25.5917	-75.155	4	264
5103	0	Yes	4180	25.8469	-75.1245	1	266
5104	0	Yes	4180	25.8469	-75.1245	1	266
5105	0	Yes	4181	32.6183	-75.7217	4	266
5106	0	Yes	4181	32.6183	-75.7217	2	266
5107	0	Yes	4182	23.4233	-79.1983	1	264
5108	0	Yes	4182	23.4233	-79.1983	1	264
5109	0	Unknown	4184	30.5154	-117.8615	1	255
5110	0	Unknown	4184	30.5154	-117.8615	1	255
5111	0	Yes	4185	32.62	-75.8567	2	264
5112	0	Yes	4185	32.62	-75.8567	2	264
5113	0	Yes	4187	32.43	-75.77	2	264
5114	0	Yes	4187	32.43	-75.77	2	264
5115	0	Yes	4188	32.6551	-75.8073	6	266
5116	0	Yes	4188	32.6551	-75.8073	3	266
5117	0	Unknown	4189	29.9526	-116.7061	4	255
5118	0	Unknown	4189	29.9526	-116.7061	5	255
5119	0	Yes	4190	32.4917	-76.0117	2	264
5120	0	Yes	4190	32.4917	-76.0117	2	264
5121	0	Yes	4191	32.475	-75.91	3	266
5122	0	Yes	4191	32.475	-75.91	3	266
5123	0	Yes	4192	23.29	-79.29	2	264
5124	0	Yes	4192	23.29	-79.29	2	264
5125	0	Yes	4193	27.6483	-72.6317	1	264
5126	0	Yes	4193	27.6483	-72.6317	1	264
5127	0	Yes	4194	32.5443	-75.7992	3	264
5128	0	Yes	4194	32.5443	-75.7992	3	266
5129	0	Yes	4195	30.9401	-121.4278	1	255
5130	0	Yes	4195	30.9401	-121.4278	1	255
5131	0	Yes	4196	32.98	-75.5767	4	264
5132	0	Yes	4196	32.98	-75.5767	4	264
5133	0	Yes	4197	27.7867	-72.8517	2	266
5134	0	Yes	4197	27.7867	-72.8517	2	266
5135	0	Yes	4198	32.7935	-75.7535	3	264
5136	0	No	4198	32.7935	-75.7535	3	264
5137	0	Yes	4199	28.9371	-121.7677	2	255
5138	0	Yes	4199	28.9371	-121.7677	2	255
5139	0	Yes	4201	32.71	-75.765	3	264
5140	0	Yes	4201	32.71	-75.765	3	264
5141	0	Unknown	4202	29.1579	-121.8218	3	255
5142	0	Unknown	4202	29.1579	-121.8218	5	255
5143	0	Yes	4204	29.3167	-73.2633	4	264
5144	0	Yes	4204	29.3167	-73.2633	4	264
5145	0	Yes	4205	32.5833	-75.895	3	266
5146	0	Yes	4205	32.5833	-75.895	3	266
5147	0	Unknown	4206	28.9547	-121.8598	4	255
5148	0	Unknown	4206	28.9547	-121.8598	4	255
5149	0	Yes	4207	32.815	-75.6	5	266
5150	0	Yes	4207	32.815	-75.6	6	266
5151	0	Yes	4208	32.8567	-75.7597	3	266
5152	0	Yes	4208	32.8567	-75.7597	3	266
5153	0	Yes	4209	29.0609	-121.9397	3	255
5154	0	Yes	4209	29.0609	-121.9397	3	255
5155	0	Yes	4210	33.0083	-75.395	5	266
5156	0	Yes	4210	33.0083	-75.395	4	266
5157	0	Yes	4211	32.6667	-75.68	4	264
5158	0	Yes	4211	32.6667	-75.68	5	264
5159	0	Yes	4212	32.6883	-75.805	4	266
5160	0	Yes	4212	32.6883	-75.805	3	266
5161	0	Yes	4213	32.5844	-75.8125	4	264
5162	0	Yes	4213	32.5844	-75.8125	5	264
5163	0	Unknown	4215	29.9837	-116.8908	4	255
5164	0	Unknown	4215	29.9837	-116.8908	4	255
5165	0	Yes	4216	28.1847	-72.5487	5	264
5166	0	Yes	4216	28.1847	-72.5487	5	264
5167	0	Yes	4217	28.395	-72.525	4	266
5168	0	Yes	4217	28.395	-72.525	4	266
5169	0	Yes	4218	32.7427	-75.6856	4	264
5170	0	No	4218	32.7427	-75.6856	4	264
5171	0	Unknown	4219	29.7735	-116.6322	5	255
5172	0	Unknown	4219	29.7735	-116.6322	5	255
5173	0	Yes	4220	25.8483	-65.8	1	266
5174	0	Yes	4220	25.8483	-65.8	1	266
5175	0	Yes	4221	28.38	-72.4383	6	264
5176	0	Yes	4221	28.38	-72.4383	4	264
5177	0	Yes	4222	27.9417	-70.8167	5	264
5178	0	Yes	4222	27.9417	-70.8167	5	264
5179	0	Yes	4223	27.7821	-70.4676	5	266
5180	0	Yes	4223	27.7821	-70.4676	6	266
5181	0	Yes	4225	23.2483	-79.3233	5	266
5182	0	Yes	4225	23.2483	-79.3233	6	266
5183	0	Yes	4226	28.725	-75.18	4	264
5184	0	Yes	4226	28.725	-75.18	5	264
5185	0	Unknown	4227	30.5903	-123.2746	1	255
5186	0	Unknown	4227	30.5903	-123.2746	1	255
5187	0	Yes	4228	28.245	-72.2917	4	264
5188	0	No	4228	28.245	-72.2917	5	264
5189	0	Yes	4229	32.7417	-75.43	Unknown	266
5190	0	Yes	4229	32.7417	-75.43	Unknown	266
5191	0	Yes	4230	25.7217	-74.9867	Unknown	266
5192	0	Yes	4230	25.7217	-74.9867	Unknown	266
5193	0	Unknown	4231	32.9973	-124.5873	Unknown	255
5194	0	Unknown	4231	32.9973	-124.5873	Unknown	255
5195	0	Yes	4232	23.235	-79.3333	Unknown	264
5196	0	Yes	4232	23.235	-79.3333	Unknown	264
5197	0	Yes	4233	23.3033	-79.1733	6	266
5198	0	Yes	4233	23.3033	-79.1733	7	266
5199	0	Yes	4234	27.6672	-65.3964	1	264
5200	0	Yes	4234	27.6672	-65.3964	1	264
5201	0	Yes	4235	33.5977	-75.0749	1	266
5202	0	Yes	4235	33.5977	-75.0749	1	266
5203	0	Unknown	4236	29.2206	-117.691	Unknown	255
5204	0	Unknown	4236	29.2206	-117.691	Unknown	255
5205	0	Yes	4237	25.6097	-74.7964	5	264
5206	0	Yes	4237	25.6097	-74.7964	6	264
5207	0	Unknown	4238	29.3429	-117.7734	3	255
5208	0	Unknown	4238	29.3429	-117.7734	5	255
5209	0	Yes	4239	25.6504	-74.8476	6	264
5210	0	Yes	4239	25.6504	-74.8476	7	264
5211	0	Yes	4240	28.0533	-72.6643	5	264
5212	0	Yes	4240	28.0533	-72.6643	6	264
5213	0	Yes	4241	25.705	-74.8917	5	266
5214	0	Yes	4241	25.705	-74.8917	8	266
5215	0	Unknown	4242	29.2035	-117.7054	5	255
5216	0	Unknown	4242	29.2035	-117.7054	6	255
5217	0	Yes	4243	28.8612	-72.4411	Unknown	264
5218	0	Yes	4243	28.8612	-72.4411	Unknown	264
5219	0	Yes	4244	25.3617	-74.55	2	266
5220	0	Yes	4244	25.3617	-74.55	2	266
5221	0	Unknown	4246	29.2444	-117.7299	2	255
5222	0	Unknown	4246	29.2444	-117.7299	5	255
5223	0	Yes	4247	23.3033	-79.1733	6	264
5224	0	Yes	4247	23.3033	-79.1733	6	264
5225	0	Unknown	4249	29.2514	-117.725	5	255
5226	0	Unknown	4249	29.2514	-117.725	5	255
5227	0	Yes	4250	28.083	-72.551	3	264
5228	0	Yes	4250	28.083	-72.551	7	264
5229	0	Yes	4251	25.71	-75.1617	6	266
5230	0	Yes	4251	25.71	-75.1617	7	266
5231	0	Yes	4252	25.6293	-74.9146	7	264
5232	0	Yes	4252	25.6293	-74.9146	7	264
5233	0	Unknown	4253	30.279	-119.838	4	255
5234	0	Unknown	4253	30.279	-119.838	6	255
5235	0	Yes	4254	28.235	-73.2083	2	266
5236	0	Yes	4254	28.235	-73.2083	8	266
5237	0	Unknown	4255	29.7501	-121.5628	2	255
5238	0	Unknown	4255	29.7501	-121.5628	5	255
5239	0	Yes	4256	25.3617	-74.55	Unknown	264
5240	0	Yes	4256	25.3617	-74.55	Unknown	264
5241	0	Unknown	4258	29.0268	-121.8539	6	255
5242	0	Unknown	4258	29.0268	-121.8539	7	255
5243	0	Yes	4259	28.1967	-72.23	3	264
5244	0	Yes	4259	28.1967	-72.23	4	264
5245	0	Yes	4260	28.15	-60.6367	2	266
5246	0	Yes	4260	28.15	-60.6367	2	266
5247	0	Yes	4261	25.7267	-74.8967	8	264
5248	0	Yes	4261	25.7267	-74.8967	9	264
5249	0	Yes	4262	29.2376	-117.652	2	275
5250	0	Yes	4262	29.2376	-117.652	2	275
5251	0	Yes	4263	25.71	-75.1	7	264
5252	0	Yes	4263	25.71	-75.1	8	264
5253	0	Yes	4264	25.47	-74.6483	8	266
5254	0	Yes	4264	25.47	-74.6483	8	266
5255	0	Unknown	4265	27.8798	-120.2465	3	275
5256	0	Unknown	4265	27.8798	-120.2465	6	275
5257	0	Yes	4267	28.4114	-73.6072	8	264
5258	0	Yes	4267	28.4114	-73.6072	9	264
5259	0	Yes	4268	29.2783	-117.5983	5	275
5260	0	Yes	4268	29.2783	-117.5983	7	275
5261	0	Yes	4269	25.395	-74.5791	6	264
5262	0	Yes	4269	25.395	-74.5791	9	264
5263	0	Yes	4271	25.8367	-75.185	4	264
5264	0	Yes	4271	25.8367	-75.185	5	264
5265	0	Unknown	4272	29.7795	-121.4606	Unknown	275
5266	0	Unknown	4272	29.7795	-121.4606	Unknown	275
5267	0	Yes	4273	28.1983	-72.3033	7	266
5268	0	Yes	4273	28.1983	-72.3033	9	266
5269	0	Yes	4274	29.932	-116.7865	3	275
5270	0	Yes	4274	29.932	-116.7865	3	275
5271	0	Yes	4275	25.68	-75.0967	7	264
5272	0	Yes	4275	25.68	-75.0967	10	264
5273	0	Yes	4276	25.3775	-73.1608	1	266
5274	0	Yes	4276	25.3775	-73.1608	1	266
5275	0	Unknown	4277	29.932	-116.7865	4	275
5276	0	Unknown	4277	29.932	-116.7865	7	275
5277	0	Yes	4278	25.4683	-74.5583	9	264
5278	0	Yes	4278	25.4683	-74.5583	9	264
5279	0	Yes	4279	25.6697	-75.0772	9	266
5280	0	Yes	4279	25.6697	-75.0772	10	266
5281	0	Unknown	4280	28.9413	-119.0678	6	275
5282	0	Unknown	4280	28.9413	-119.0678	6	275
5283	0	Yes	4281	25.43	-74.7283	7	264
5284	0	Yes	4281	25.43	-74.7283	8	264
5285	0	Yes	4282	25.4233	-74.7433	2	264
5286	0	Yes	4282	25.4233	-74.7433	2	264
5287	0	Yes	4283	27.6461	-65.0813	5	266
5288	0	Yes	4283	27.6461	-65.0813	6	266
5289	0	Yes	4284	27.9105	-72.5549	8	264
5290	0	Yes	4284	27.9105	-72.5549	10	264
5291	0	Yes	4285	25.4617	-74.7667	8	266
5292	0	Yes	4285	25.4617	-74.7667	10	266
5293	0	Yes	4286	29.1467	-119.2133	6	275
5294	0	Yes	4286	29.1467	-119.2133	6	275
5295	0	Yes	4287	25.605	-75.0134	10	266
5296	0	Yes	4287	25.605	-75.0134	11	266
5297	0	Yes	4288	25.4667	-74.7633	10	266
5298	0	Yes	4288	25.4667	-74.7633	11	266
5299	0	Unknown	4289	29.7083	-116.5267	Unknown	275
5300	0	Unknown	4289	29.7083	-116.5267	Unknown	275
5301	0	Yes	4291	25.4517	-74.785	Unknown	266
5302	0	Yes	4291	25.4517	-74.785	Unknown	266
5303	0	Yes	4292	25.4267	-74.7167	6	266
5304	0	Yes	4292	25.4267	-74.7167	7	266
5305	0	Unknown	4293	30.0557	-119.5591	5	275
5306	0	Unknown	4293	30.0557	-119.5591	8	275
5307	0	Yes	4294	25.5717	-74.9033	Unknown	266
5308	0	Yes	4294	25.5717	-74.9033	Unknown	266
5309	0	Yes	4295	25.4983	-74.69	Unknown	266
5310	0	Yes	4295	25.4983	-74.69	Unknown	266
5311	0	Yes	4296	29.6409	-116.4845	Unknown	275
5312	0	Yes	4296	29.6409	-116.4845	Unknown	275
5313	0	Yes	4297	25.4483	-74.6767	Unknown	264
5314	0	Yes	4297	25.4483	-74.6767	Unknown	264
5315	0	Yes	4298	25.495	-74.7167	Unknown	266
5316	0	Yes	4298	25.495	-74.7167	Unknown	266
5317	0	Yes	4299	25.5417	-74.7	Unknown	264
5318	0	No	4299	25.5417	-74.7	Unknown	264
5319	0	Unknown	4300	29.6883	-116.36	Unknown	275
5320	0	Unknown	4300	29.6883	-116.36	Unknown	275
5321	0	Yes	4301	25.4817	-74.7017	3	266
5322	0	Yes	4301	25.4817	-74.7017	Unknown	266
5323	0	Yes	4302	25.5017	-74.72	Unknown	266
5324	0	Yes	4302	25.5017	-74.72	Unknown	266
5325	0	Yes	4303	29.6504	-116.4804	Unknown	275
5326	0	Yes	4303	29.6504	-116.4804	Unknown	275
5327	0	Yes	4304	25.295	-65.49	1	264
5328	0	Yes	4304	25.295	-65.49	1	264
5329	0	Yes	4305	25.4183	-74.595	Unknown	266
5330	0	Yes	4305	25.4183	-74.595	Unknown	266
5331	0	Yes	4306	25.665	-74.655	Unknown	264
5332	0	Yes	4306	25.665	-74.655	Unknown	264
5333	0	Yes	4307	29.6036	-116.4108	Unknown	275
5334	0	Yes	4307	29.6036	-116.4108	Unknown	275
5335	0	Yes	4308	25.4467	-74.66	Unknown	266
5336	0	Yes	4308	25.4467	-74.66	Unknown	266
5337	0	Yes	4309	29.5417	-116.3783	Unknown	275
5338	0	Yes	4309	29.5417	-116.3783	Unknown	275
5339	0	Yes	4310	25.515	-74.6417	Unknown	264
5340	0	Yes	4310	25.515	-74.6417	Unknown	264
5341	0	Yes	4311	25.4467	-74.66	13	266
5342	0	Yes	4311	25.4467	-74.66	13	266
5343	0	Yes	4312	25.4217	-74.6933	Unknown	264
5344	0	Yes	4312	25.4217	-74.6933	Unknown	264
5345	0	Unknown	4314	29.8683	-121.5983	Unknown	275
5346	0	Unknown	4314	29.8683	-121.5983	Unknown	275
5347	0	Yes	4315	28.1883	-72.3583	8	264
5348	0	Yes	4315	28.1883	-72.3583	9	264
5349	0	Yes	4316	25.608	-74.6808	Unknown	264
5350	0	Yes	4316	25.608	-74.6808	Unknown	264
5351	0	Unknown	4318	29.4983	-116.395	Unknown	275
5352	0	Unknown	4318	29.4983	-116.395	Unknown	275
5353	0	Yes	4319	25.49	-74.675	Unknown	264
5354	0	No	4319	25.49	-74.675	Unknown	264
5355	0	Yes	4320	25.3817	-74.595	Unknown	264
5356	0	Yes	4320	25.3817	-74.595	Unknown	264
5357	0	Unknown	4321	31.3509	-121.9057	Unknown	275
5358	0	Unknown	4321	31.3509	-121.9057	Unknown	275
5359	0	Yes	4322	25.71	-74.89	Unknown	266
5360	0	Yes	4322	25.71	-74.89	Unknown	266
5361	0	Yes	4323	25.3817	-74.5083	Unknown	264
5362	0	Yes	4323	25.3817	-74.5083	Unknown	264
5363	0	Unknown	4324	29.5417	-116.3783	Unknown	275
5364	0	Unknown	4324	29.5417	-116.3783	Unknown	275
5365	0	Yes	4325	25.4978	-74.5686	Unknown	264
5366	0	Yes	4325	25.4978	-74.5686	Unknown	264
5367	0	Yes	4326	25.385	-74.6633	Unknown	264
5368	0	Yes	4326	25.385	-74.6633	Unknown	264
5369	0	Unknown	4327	30.499	-120.6573	Unknown	275
5370	0	Unknown	4327	30.499	-120.6573	Unknown	275
5371	0	Yes	4328	37.8633	-68.99	1	266
5372	0	Yes	4328	37.8633	-68.99	1	266
5373	0	Yes	4329	25.64	-74.4867	Unknown	264
5374	0	Yes	4329	25.64	-74.4867	Unknown	264
5375	0	Unknown	4330	29.5417	-116.3783	Unknown	275
5376	0	Unknown	4330	29.5417	-116.3783	Unknown	275
5377	0	Yes	4331	28.835	-75.2083	Unknown	264
5378	0	Yes	4331	28.835	-75.2083	Unknown	264
5379	0	Yes	4332	25.49	-74.5617	Unknown	266
5380	0	Yes	4332	25.49	-74.5617	Unknown	266
5381	0	Unknown	4333	29.5417	-116.3783	Unknown	275
5382	0	Unknown	4333	29.5417	-116.3783	Unknown	275
5383	0	Yes	4334	25.526	-74.5548	Unknown	266
5384	0	Yes	4334	25.526	-74.5548	Unknown	266
5385	0	Unknown	4336	29.5417	-116.3783	Unknown	275
5386	0	Unknown	4336	29.5417	-116.3783	Unknown	275
5387	0	Yes	4337	25.49	-74.5617	15	264
5388	0	Yes	4337	25.49	-74.5617	Unknown	264
5389	0	Unknown	4338	29.625	-116.5117	Unknown	275
5390	0	Unknown	4338	29.625	-116.5117	Unknown	275
5391	0	Yes	4339	31.4817	-76.9083	1	266
5392	0	Yes	4339	31.4817	-76.9083	1	266
5393	0	Yes	4340	24.2283	-79.68	1	264
5394	0	Yes	4340	24.2283	-79.68	1	264
5395	0	Unknown	4341	29.5417	-116.3783	Unknown	275
5396	0	Unknown	4341	29.5417	-116.3783	Unknown	275
5397	0	Yes	4342	30.425	-75.94	Unknown	266
5398	0	Yes	4342	30.425	-75.94	Unknown	266
5399	0	Yes	4343	28.6047	-75.1815	Unknown	264
5400	0	Yes	4343	28.6047	-75.1815	Unknown	264
5401	0	Unknown	4344	29.5417	-116.3783	Unknown	275
5402	0	Unknown	4344	29.5417	-116.3783	Unknown	275
5403	0	Yes	4345	28.4095	-72.3226	Unknown	264
5404	0	No	4345	28.4095	-72.3226	Unknown	264
5405	0	Unknown	4346	29.5379	-116.4573	Unknown	275
5406	0	Unknown	4346	29.5379	-116.4573	Unknown	275
5407	0	Yes	4347	25.2617	-74.3983	Unknown	266
5408	0	Yes	4347	25.2617	-74.3983	Unknown	266
5409	0	Yes	4348	25.43	-74.8583	Unknown	264
5410	0	Yes	4348	25.43	-74.8583	Unknown	264
5411	0	Unknown	4350	29.8546	-121.636	Unknown	275
5412	0	Unknown	4350	29.8546	-121.636	Unknown	275
5413	0	Yes	4351	25.5816	-74.8283	Unknown	266
5414	0	Yes	4351	25.5816	-74.8283	Unknown	266
5415	0	Yes	4352			Unknown	264
5416	0	Yes	4352			Unknown	264
5417	0	Unknown	4353			Unknown	275
5418	0	Unknown	4353			Unknown	275
5419	0	Attempt	4355			Unknown	266
5420	0	Attempt	4355			Unknown	266
5421	0	Unknown	4356			Unknown	275
5422	0	Unknown	4356			Unknown	275
5423	0	TBD	4358			Unknown	264
5424	0	TBD	4359			Unknown	266
5425	0	TBD	4360			Unknown	264
5426	0	TBD	4361			Unknown	266
5427	0	TBD	4362			Unknown	275
5428	0	TBD	4363				266
5429	0	TBD	4364			Unknown	275
5430	0	TBD	4365			Unknown	266
5431	0	TBD	4365			Unknown	266
5434	0	TBD	4367			Unknown	264
5435	0	TBD	4367			Unknown	264
5436	0	TBD	4368			Unknown	275
5437	0	TBD	4368			Unknown	275
5438	0	TBD	4364			Unknown	275
5439	0	TBD	4369			Unknown	266
5440	0	TBD	4369			Unknown	266
5441	0	TBD	4370			Unknown	264
5442	0	TBD	4370			Unknown	264
5443	0	TBD	4371			Unknown	266
5444	0	TBD	4371			Unknown	266
5445	0	TBD	4372			Unknown	264
5446	0	TBD	4372			Unknown	264
5447	0	TBD	4373			16	275
5448	0	TBD	4373			13	275
5449	0	TBD	4375			Unknown	264
5450	0	TBD	4375			Unknown	264
5451	0	TBD	4376			Unknown	266
5452	0	TBD	4376			Unknown	266
5453	0	TBD	4377			Unknown	266
5454	0	TBD	4377			Unknown	266
5455	0	TBD	4378			Unknown	264
5456	0	TBD	4378			Unknown	264
5457	0	TBD	4379			Unknown	266
5458	0	TBD	4379			Unknown	266
5459	0	TBD	4380			Unknown	275
5460	0	TBD	4380			Unknown	275
5461	0	TBD	4381			Unknown	266
5462	0	TBD	4381			Unknown	266
5463	0	Unknown	4382			Unknown	275
5464	0	Unknown	4382			Unknown	275
5465	0	TBD	4383			Unknown	266
5466	0	TBD	4383			Unknown	266
5467	0	Unknown	4384			Unknown	275
5468	0	Unknown	4384			Unknown	275
5469	0	Unknown	4385			Unknown	266
5470	0	Unknown	4385			Unknown	266
5471	0	TBD	4386			Unknown	264
5472	0	TBD	4386			Unknown	264
5473	0	TBD	4387			Unknown	266
5474	0	TBD	4387			Unknown	266
5475	0	Unknown	4388			Unknown	275
5476	0	Unknown	4388			Unknown	275
5477	0	TBD	4390			Unknown	266
5478	0	TBD	4390			Unknown	266
\.


--
-- Data for Name: _booster_tracker_landingzone; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._booster_tracker_landingzone (id, name, nickname, serial_number, status, image) FROM stdin;
14	Just Read the Instructions (2)	JRtI	MARMAC 303	ACTIVE	landing_zone_photos/jrti_2.jpeg
15	Of Course I Still Love You	OCISLY	MARMAC 304	ACTIVE	landing_zone_photos/ocisly.jpeg
16	Landing Zone 1	LZ-1		ACTIVE	landing_zone_photos/LZ1.jpeg
17	Landing Zone 2	LZ-2		ACTIVE	landing_zone_photos/LZ2.jpg
18	Landing Zone 4	LZ-4		ACTIVE	landing_zone_photos/LZ4.jpeg
19	A Shortfall of Gravitas	ASoG	MARMAC 302	ACTIVE	landing_zone_photos/asog.jpeg
20	Just Read the Instructions (1)	JRtI	MARMAC 300	RETIRED	landing_zone_photos/jrti_1.jpeg
\.


--
-- Data for Name: _booster_tracker_launch; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._booster_tracker_launch (id, "time", name, customer, launch_outcome, rocket_id, mass, pad_id, orbit_id) FROM stdin;
4028		FalconSAT-2	DARPA	FAILURE	8	19.5 kg	61	16
4029		DemoSat	DARPA	FAILURE	8	Unknown	61	16
4030		Trailblazer PRESat NanoSail-D Explorers	ORS/NASA	FAILURE	8	4 kg	61	16
4031		RatSat	SpaceX	SUCCESS	8	165 kg	61	16
4032		RazakSAT	ATSB	SUCCESS	8	180 kg	61	16
4033		Dragon Spacecraft Qualification Unit	SpaceX	SUCCESS	5	No payload (excl. Dragon Mass)	62	16
4034		SpaceX COTS Demo Flight 1	NASA (COTS), various others	SUCCESS	5	Unknown (excl. Dragon Mass)	62	16
4035		SpaceX COTS Demo Flight 2	NASA (COTS)	SUCCESS	5	525 kg (1,157 lb) (excl. Dragon mass)	62	16
4036		SpaceX CRS-1, Orbcomm-OG2	NASA (CRS), Orbcomm	PARTIAL FAILURE	5	4,700 kg (10,400 lb) (excl. Dragon mass)	62	16
4037		SpaceX CRS-2	NASA (CRS)	SUCCESS	5	4,877 kg (10,752 lb) (excl. Dragon mass)	62	16
4038		CASSIOPE	MDA	SUCCESS	5	500 kg (1,100 lb)	63	17
4039		SES-8	SES	SUCCESS	5	3,170 kg (6,990 lb)	62	18
4040		Thaicom 6	Thaicom	SUCCESS	5	3,325 kg (7,330 lb)	62	18
4041		SpaceX CRS-3	NASA (CRS)	SUCCESS	5	2,296 kg (5,062 lb) (excl. Dragon mass)	62	16
4042		Orbcomm-OG2-1(6 satellites)	Orbcomm	SUCCESS	5	1,316 kg (2,901 lb)	62	16
4043		AsiaSat 8	AsiaSat	SUCCESS	5	4,535 kg (9,998 lb)	62	18
4044		AsiaSat 6	AsiaSat	SUCCESS	5	4,428 kg (9,762 lb)	62	18
4045		SpaceX CRS-4	NASA (CRS)	SUCCESS	5	2,216 kg (4,885 lb) (excl. Dragon mass)	62	16
4046		SpaceX CRS-5	NASA (CRS)	SUCCESS	5	2,395 kg (5,280 lb) (excl. Dragon mass)	62	16
4047		DSCOVR	USAF, NASA, NOAA	SUCCESS	5	570 kg (1,260 lb)	62	19
4048		ABS-3A, Eutelsat 115 West B	ABS, Eutelsat	SUCCESS	5	4,159 kg (9,169 lb)	62	18
4049		SpaceX CRS-6	NASA (CRS)	SUCCESS	5	1,898 kg (4,184 lb) (excl. Dragon mass)	62	16
4050		TürkmenÄlem 52°E (MonacoSAT)	Turkmenistan NationalSpace Agency	SUCCESS	5	4,707 kg (10,377 lb)	62	18
4051		SpaceX CRS-7	NASA (CRS)	FAILURE	5	1,952 kg (4,303 lb) (excl. Dragon mass)	62	16
4052		Orbcomm-OG2-2(11 satellites)	Orbcomm	SUCCESS	5	2,034 kg (4,484 lb)	62	16
4053		Jason-3	NASA (LSP), NOAA, CNES	SUCCESS	5	553 kg (1,219 lb)	63	16
4054		SES-9	SES	SUCCESS	5	5,271 kg (11,621 lb)	62	18
4055		SpaceX CRS-8	NASA (CRS)	SUCCESS	5	3,136 kg (6,914 lb) (excl. Dragon mass)	62	16
4056		JCSAT-14	SKY Perfect JSAT Group	SUCCESS	5	4,696 kg (10,353 lb)	62	18
4057		Thaicom 8	Thaicom	SUCCESS	5	3,100 kg (6,800 lb)	62	18
4058		ABS-2A (Eutelsat 117 West B)	ABS, Eutelsat	SUCCESS	5	3,600 kg (7,900 lb)	62	18
4059		SpaceX CRS-9	NASA (CRS)	SUCCESS	5	2,257 kg (4,976 lb) (excl. Dragon mass)	62	16
4060		JCSAT-16	SKY Perfect JSAT Group	SUCCESS	5	4,600 kg (10,100 lb)	62	18
4061		AMOS-6	Spacecom	FAILURE	5	5,500 kg (12,100 lb)	62	18
4062		Iridium NEXT-1(10 satellites)	Iridium Communications	SUCCESS	5	9,600 kg (21,200 lb)	63	17
4063		SpaceX CRS-10	NASA (CRS)	SUCCESS	5	2,490 kg (5,490 lb) (excl. Dragon mass)	64	16
4064		EchoStar 23	EchoStar	SUCCESS	5	5,600 kg (12,300 lb)	64	18
4065		SES-10	SES	SUCCESS	5	5,300 kg (11,700 lb)	64	18
4066		NROL-76	NRO	SUCCESS	5	Classified	64	16
4067		Inmarsat-5 F4	Inmarsat	SUCCESS	5	6,070 kg (13,380 lb)	64	18
4068		SpaceX CRS-11	NASA (CRS)	SUCCESS	5	2,708 kg (5,970 lb) (excl. Dragon mass)	64	16
4069		BulgariaSat-1	Bulsatcom	SUCCESS	5	3,669 kg (8,089 lb)	64	18
4070		Iridium NEXT-2(10 satellites)	Iridium Communications	SUCCESS	5	9,600 kg (21,200 lb)	63	16
4071		Intelsat 35e	Intelsat	SUCCESS	5	6,761 kg (14,905 lb)	64	18
4072		SpaceX CRS-12	NASA (CRS)	SUCCESS	5	3,310 kg (7,300 lb) (excl. Dragon mass)	64	16
4073		Formosat-5	NSPO	SUCCESS	5	475 kg (1,047 lb)	63	20
4074		Boeing X-37B OTV-5	USAF	SUCCESS	5	4,990 kg (11,000 lb)+ OTV payload	64	16
4075		Iridium NEXT-3(10 satellites)	Iridium Communications	SUCCESS	5	9,600 kg (21,200 lb)	63	17
4076		SES-11 (EchoStar 105)	SES S.A., EchoStar	SUCCESS	5	5,400 kg (11,900 lb)	64	18
4077		Koreasat 5A	KT Corporation	SUCCESS	5	3,500 kg (7,700 lb)	64	18
4078		SpaceX CRS-13	NASA (CRS)	SUCCESS	5	2,205 kg (4,861 lb) (excl. Dragon mass)	62	16
4079		Iridium NEXT-4(10 satellites)	Iridium Communications	SUCCESS	5	9,600 kg (21,200 lb)	63	17
4080		Zuma	Northrop Grumman	SUCCESS	5	Classified	62	16
4081		GovSat-1 (SES-16)	SES	SUCCESS	5	4,230 kg (9,330 lb)	62	18
4082		Elon Musk's Tesla Roadster	SpaceX	SUCCESS	6	1,250 kg (2,760 lb)	64	21
4083		Paz, Tintin A and Tintin B	Hisdesat, exactEarth, SpaceX	SUCCESS	5	2,150 kg (4,740 lb)	63	20
4084		Hispasat 30W-6, PODSat	Hispasat, NovaWurks	SUCCESS	5	6,092 kg (13,431 lb)	62	18
4085		Iridium NEXT-5(10 satellites)	Iridium Communications	SUCCESS	5	9,600 kg (21,200 lb)	63	17
4086		SpaceX CRS-14	NASA (CRS)	SUCCESS	5	2,647 kg (5,836 lb) (excl. Dragon mass)	62	16
4087		Transiting Exoplanet Survey Satellite (TESS)	NASA (LSP)	SUCCESS	5	362 kg (798 lb)	62	22
4088		Bangabandhu-1	Thales-Alenia / BTRC	SUCCESS	5	3,600 kg (7,900 lb)	64	18
4089		Iridium NEXT-6(5 satellites), GRACE-FO (2 satellites)	Iridium Communications, GFZ, NASA	SUCCESS	5	6,460 kg (14,240 lb)	63	17
4090		SES-12	SES	SUCCESS	5	5,384 kg (11,870 lb)	62	18
4091		SpaceX CRS-15	NASA (CRS)	SUCCESS	5	2,697 kg (5,946 lb) (excl. Dragon mass)	62	16
4092		Telstar 19V	Telesat	SUCCESS	5	7,075 kg (15,598 lb)	62	18
4093		Iridium NEXT-7(10 satellites)	Iridium Communications	SUCCESS	5	9,600 kg (21,200 lb)	63	17
4094		Merah Putih (formerly Telkom-4)	Telkom Indonesia	SUCCESS	5	5,800 kg (12,800 lb)	62	18
4095		Telstar 18V (Apstar-5C)	Telesat	SUCCESS	5	7,060 kg (15,560 lb)	62	18
4096		SAOCOM 1A	CONAE	SUCCESS	5	3,000 kg (6,600 lb)	63	20
4097		Es'hail 2	Es'hailSat	SUCCESS	5	5,300 kg (11,700 lb)	64	18
4098		Sun-Synchronous Orbit-A (SmallSat Express)	Spaceflight Industries	SUCCESS	5	~4,000 kg (8,800 lb)	63	20
4099		SpaceX CRS-16	NASA (CRS)	SUCCESS	5	2,500 kg (5,500 lb) (excl. Dragon mass)	62	16
4100		GPS III SV01 (Vespucci)	USAF	SUCCESS	5	4,400 kg (9,700 lb)	62	23
4101		Iridium NEXT-8(10 satellites)	Iridium Communications	SUCCESS	5	9,600 kg (21,200 lb)	63	17
4102		Nusantara Satu (PSN-6), Beresheet Moon lander	PSN, SpaceIL / IAI, Air Force Research	SUCCESS	5	4,850 kg (10,690 lb)	62	18
4103		Crew Dragon Demo-1	NASA (CCD)	SUCCESS	5	12,055 kg (26,577 lb)	64	16
4104		Arabsat-6A	Arabsat	SUCCESS	6	6,465 (14,253 lb)	64	18
4105		SpaceX CRS-17	NASA (CRS)	SUCCESS	5	2,495 kg (5,501 lb) (excl. Dragon mass)	62	16
4106		Starlink v0.9 (60 satellites)	SpaceX	SUCCESS	5	13,620 kg (30,030 lb)	62	16
4107		RADARSAT Constellation(3 satellites)	Canadian Space Agency (CSA)	SUCCESS	5	4,200 kg (9,300 lb)	63	20
4108		Space Test Program Flight 2 (STP-2)	USAF	SUCCESS	6	3,700 kg (8,200 lb)	64	24
4109		SpaceX CRS-18	NASA (CRS)	SUCCESS	5	2,268 kg (5,000 lb) (excl. Dragon mass)	62	16
4110		AMOS-17	Spacecom	SUCCESS	5	6,500 kg (14,300 lb)	62	18
4111		Starlink 1 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	62	16
4112		SpaceX CRS-19	NASA (CRS)	SUCCESS	5	2,617 kg (5,769 lb) (excl. Dragon mass)	62	16
4113		JCSat-18 (Kacific 1)	Sky Perfect JSATKacific 1	SUCCESS	5	6,956 kg (15,335 lb)	62	18
4114		Starlink 2 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	62	16
4115		Crew Dragon in-flight abort test	NASA (CTS)	SUCCESS	5	12,050 kg (26,570 lb)	64	25
4116		Starlink 3 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	62	16
4117		Starlink 4 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	62	16
4118		SpaceX CRS-20	NASA (CRS)	SUCCESS	5	1,977 kg (4,359 lb) (excl. Dragon mass)	62	16
4119		Starlink 5 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	64	16
4120		Starlink 6 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	64	16
4121		Crew Dragon Demo-2	NASA (CCDev)	SUCCESS	5	12,530 kg (27,620 lb)	64	16
4122		Starlink 7 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	62	16
4123		Starlink 8 v1.0 (58 satellites),SkySats-16, -17, -18	SpaceXPlanet Labs	SUCCESS	5	15,410 kg (33,970 lb)	62	16
4124		GPS III SV03 (Matthew Henson)	U.S. Space Force	SUCCESS	5	4,311 kg (9,504 lb)	62	23
4125		ANASIS-II	Republic of Korea Army	SUCCESS	5	5,000–6,000 kg (11,000–13,000 lb)	62	18
4126		Starlink 9 v1.0 (57 Satellites),SXRS-1 (BlackSky Global 7 and 8)	SpaceXSpaceflight Industries (BlackSky)	SUCCESS	5	14,932 kg (32,919 lb)	64	16
4127		Starlink 10 v1.0 (58 satellites)SkySat-19, -20, -21	SpaceXPlanet Labs	SUCCESS	5	~15,440 kg (34,040 lb)	62	16
4128		SAOCOM 1B	CONAEPlanetIQTyvak	SUCCESS	5	3,130 kg (6,900 lb)	62	20
4129		Starlink 11 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	64	16
4130		Starlink 12 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	64	16
4131		Starlink 13 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	64	16
4132		Starlink 14 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	62	16
4133		GPS III SV04 (Sacagawea)	USSF	SUCCESS	5	4,311 kg (9,504 lb)	62	23
4134		Crew-1	NASA (CCP)	SUCCESS	5	~13,000 kg (29,000 lb)	64	16
4135		Sentinel-6 Michael Freilich (Jason-CS A)	NASA / NOAA / ESA / EUMETSAT	SUCCESS	5	1,192 kg (2,628 lb)	63	16
4136		Starlink 15 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	62	16
4137		SpaceX CRS-21	NASA (CRS)	SUCCESS	5	2,972 kg (6,552 lb) (excl. Dragon mass)	64	16
4138		SXM-7	Sirius XM	SUCCESS	5	7,000 kg (15,000 lb)	62	18
4139		NROL-108	NRO	SUCCESS	5	Classified	64	16
4140		Türksat 5A	Türksat	SUCCESS	5	3,500 kg (7,700 lb)	62	18
4141		Starlink 16 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	64	16
4142		Transporter-1: (143 smallsat rideshare)	Various	SUCCESS	5	~5,000 kg (11,000 lb)	62	20
4143		Starlink 18 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	62	16
4144		Starlink 19 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	62	16
4145		Starlink 17 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	64	16
4146		Starlink 20 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	62	16
4147		Starlink 21 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	64	16
4148		Starlink 22 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	62	16
4149		Starlink 23 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	62	16
4150		Crew-2	NASA (CTS)	SUCCESS	5	~12,500 kg (27,600 lb)	64	16
4151		Starlink 24 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	62	16
4152		Starlink 25 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	64	16
4153		Starlink 27 v1.0 (60 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	62	16
4154		Starlink 26 v1.0 (52 Satellites) Capella-6 &Tyvak-0130	SpaceX Capella Space and Tyvak	SUCCESS	5	~14,000 kg (31,000 lb)	64	16
4155		Starlink 28 v1.0 (60 Satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	62	16
4156		SpaceX CRS-22	NASA (CRS)	SUCCESS	5	3,328 kg (7,337 lb) (excl. Dragon mass)	64	16
4157		SXM-8	Sirius XM	SUCCESS	5	7,000 kg (15,000 lb)	62	18
4158		GPS III SV05 (Neil Armstrong)	USSF	SUCCESS	5	4,331 kg (9,548 lb)	62	23
4159		Transporter-2: (88 payloads Smallsat Rideshare)	Various	SUCCESS	5	Unknown	62	20
4160		SpaceX CRS-23	NASA (CRS)	SUCCESS	5	~2,200 kg (4,900 lb) (excl. Dragon mass)	64	16
4161		Starlink Group 2-1 (v1.5 L1, 51 satellites)	SpaceX	SUCCESS	5	~13,260 kg (29,230 lb)	63	16
4162		Inspiration4	Jared Isaacman	SUCCESS	5	~12,519 kg (27,600 lb)	64	16
4163		Crew-3	NASA (CTS)	SUCCESS	5	~13,000 kg (29,000 lb)	64	16
4164		Starlink Group 4-1 (53 satellites)	SpaceX	SUCCESS	5	~15,635 kg (34,469 lb)	62	16
4165		Double Asteroid Redirection Test (DART)	NASA (LSP)	SUCCESS	5	624 kg (1,376 lb)	63	21
4166		Starlink Group 4-3 (48 satellites)SXRS-2: BlackSky Global (2 sats)	SpaceXSpaceflight, Inc. (BlackSky Global)	SUCCESS	5	~14,500 kg (32,000 lb)	62	16
4167		Imaging X-ray Polarimetry Explorer (IXPE)	NASA (LSP)	SUCCESS	5	325 kg (717 lb)	64	16
4168		Starlink Group 4-4(52 satellites)	SpaceX	SUCCESS	5	15,600 kg (34,400 lb)	63	16
4169		Türksat 5B	Türksat	SUCCESS	5	4,500 kg (9,900 lb)	62	18
4170		SpaceX CRS-24	NASA (CRS)	SUCCESS	5	2,989 kg (6,590 lb) (excl. Dragon mass)	64	16
4171		Starlink Group 4-5(49 satellites)	SpaceX	SUCCESS	5	~14,500 kg (32,000 lb)	64	16
4172		Transporter-3: (105 payloads Smallsat Rideshare)	Various	SUCCESS	5	Unknown	62	20
4173		Starlink Group 4-6(49 satellites)	SpaceX	SUCCESS	5	~14,500 kg (32,000 lb)	64	16
4174		CSG-2	ASI	SUCCESS	5	2,205 kg (4,861 lb)	62	20
4175		NROL-87	NRO	SUCCESS	5	Classified	63	20
4176		Starlink Group 4-7(49 satellites)	SpaceX	SUCCESS	5	~14,500 kg (32,000 lb)	64	16
4177		Starlink Group 4-8 (46 satellites)	SpaceX	SUCCESS	5	~13,600 kg (30,000 lb)	62	16
4178		Starlink Group 4-11 (50 satellites)	SpaceX	SUCCESS	5	~14,750 kg (32,520 lb)	63	16
4179		Starlink Group 4-9 (47 satellites)	SpaceX	SUCCESS	5	~13,900 kg (30,600 lb)	64	16
4180		Starlink Group 4-10(48 satellites)	SpaceX	SUCCESS	5	~14,160 kg (31,220 lb)	62	16
4181		Starlink Group 4-12 (53 satellites)	SpaceX	SUCCESS	5	~16,250 kg (35,830 lb)	62	16
4182		Transporter-4: (40 payloads Smallsat Rideshare)	Various	SUCCESS	5	Unknown	62	20
4183		Axiom-1	Axiom Space	SUCCESS	5	~13,000 kg (29,000 lb)	64	16
4184		NROL-85 (Intruder 13A (NOSS-3 9A) and Intruder 13B (NOSS-3 9B))	NRO	SUCCESS	5	Classified	63	16
4185		Starlink Group 4-14 (53 satellites)	SpaceX	SUCCESS	5	~16,250 kg (35,830 lb)	62	16
4186		Crew-4	NASA (CTS)	SUCCESS	5	~13,000 kg (29,000 lb)	64	16
4187		Starlink Group 4-16 (53 satellites)	SpaceX	SUCCESS	5	~16,250 kg (35,830 lb)	62	16
4188		Starlink Group 4-17 (53 satellites)	SpaceX	SUCCESS	5	~16,250 kg (35,830 lb)	64	16
4189		Starlink Group 4-13 (53 satellites)	SpaceX	SUCCESS	5	~16,250 kg (35,830 lb)	63	16
4190		Starlink Group 4-15 (53 satellites)	SpaceX	SUCCESS	5	~16,250 kg (35,830 lb)	62	16
4191		Starlink Group 4-18 (53 satellites)	SpaceX	SUCCESS	5	~16,250 kg (35,830 lb)	64	16
4192		Transporter-5: (59 payloads Smallsat Rideshare)	Various	SUCCESS	5	Unknown	62	20
4193		Nilesat-301	Nilesat	SUCCESS	5	~4,100 kg (9,000 lb)	62	18
4194		Starlink Group 4-19 (53 satellites)	SpaceX	SUCCESS	5	~16,250 kg (35,830 lb)	64	16
4195		SARah 1	German Intelligence Service	SUCCESS	5	~4,000 kg (8,800 lb)	63	20
4196		Globalstar-2 M087 (FM15)	GlobalstarUnknown US Government Agency	SUCCESS	5	~700 kg (1,500 lb)(excluding secret payloads)	62	16
4197		SES-22	SES	SUCCESS	5	~3,500 kg (7,700 lb)	62	18
4198		Starlink Group 4-21 (53 satellites)	SpaceX	SUCCESS	5	~16,250 kg (35,830 lb)	62	16
4199		Starlink Group 3-1 (46 satellites)	SpaceX	SUCCESS	5	~14,100 kg (31,100 lb)	63	20
4200		SpaceX CRS-25	NASA (CRS)	SUCCESS	5	2,668 kg (5,881 lb)(excl. Dragon mass)	64	16
4201		Starlink Group 4-22 (53 satellites)	SpaceX	SUCCESS	5	~16,250 kg (35,830 lb)	62	16
4202		Starlink Group 3-2 (46 satellites)	SpaceX	SUCCESS	5	~14,100 kg (31,100 lb)	63	20
4203		Starlink Group 4-25 (53 satellites)	SpaceX	SUCCESS	5	~16,250 kg (35,830 lb)	64	16
4204		Danuri (Korea Pathfinder Lunar Orbiter)	KARI	SUCCESS	5	~679 kg (1,497 lb)	62	26
4205		Starlink Group 4-26 (52 satellites)	SpaceX	SUCCESS	5	~16,000 kg (35,000 lb)	64	16
4206		Starlink Group 3-3 (46 satellites)	SpaceX	SUCCESS	5	~14,100 kg (31,100 lb)	63	20
4207		Starlink Group 4-27 (53 satellites)	SpaceX	SUCCESS	5	~16,250 kg (35,830 lb)	62	16
4208		Starlink Group 4-23	SpaceX	SUCCESS	5	~16,700 kg (36,800 lb)	62	16
4209		Starlink Group 3-4 (46 satellites)	SpaceX	SUCCESS	5	~14,200 kg (31,300 lb)	63	20
4210		Starlink Group 4-20 (51 satellites) Sherpa-LTC2	SpaceXSpaceflight Industries	SUCCESS	5	~16,000 kg (35,000 lb)	62	16
4211		Starlink Group 4-2 (34 satellites)BlueWalker-3	SpaceXAST SpaceMobile	SUCCESS	5	~11,938 kg (26,319 lb)	64	16
4212		Starlink Group 4-34 (54 satellites)	SpaceX	SUCCESS	5	~16,700 kg (36,800 lb)	62	16
4213		Starlink Group 4-35 (52 satellites)	SpaceX	SUCCESS	5	~16,100 kg (35,500 lb)	62	16
4214		Crew-5	NASA (CTS)	SUCCESS	5	~13,000 kg (29,000 lb)	64	16
4215		Starlink Group 4-29 (52 satellites)	SpaceX	SUCCESS	5	~16,100 kg (35,500 lb)	63	16
4216		Galaxy 33 and Galaxy 34 (2 satellites)	Intelsat	SUCCESS	5	7,350 kg (16,200 lb)	62	18
4217		Hotbird 13F	Eutelsat	SUCCESS	5	~4,501 kg (9,923 lb)	62	18
4218		Starlink Group 4-36 (54 satellites)	SpaceX	SUCCESS	5	~16,700 kg (36,800 lb)	62	16
4219		Starlink Group 4-31 (53 satellites)	SpaceX	SUCCESS	5	~16,400 kg (36,200 lb)	63	16
4220		USSF-44	USSF, Millennium Space Systems, Lockheed martin	SUCCESS	6	~3,750 kg (8,270 lb)	64	27
4221		Hotbird 13G	Eutelsat	SUCCESS	5	~4,500 kg (9,900 lb)	62	18
4222		Galaxy 31 and Galaxy 32 (2 satellites)	Intelsat	SUCCESS	5	~6,600 kg (14,600 lb)	62	18
4223		Eutelsat 10B	Eutelsat	SUCCESS	5	5,500 kg (12,100 lb)	62	18
4224		SpaceX CRS-26	NASA (CRS)	SUCCESS	5	3,528 kg (7,778 lb)	64	16
4225		OneWeb Flight #15	OneWeb	SUCCESS	5	6,000 kg (13,000 lb)	64	17
4226		Hakuto-R Mission 1	ispace MBRSC  JAXA NASA	SUCCESS	5	~1,000 kg (2,200 lb)	62	26
4227		Surface Water and Ocean Topography (SWOT)	NASA/CNES	SUCCESS	5	~2,200 kg (4,900 lb)	63	16
4228		O3b mPOWER 1 & 2	SES	SUCCESS	5	~4,100 kg (9,000 lb)	62	23
4229		Starlink Group 4-37 (54 satellites)	SpaceX	SUCCESS	5	~16,700 kg (36,800 lb)	64	16
4230		Starlink Group 5-1 (54 satellites)	SpaceX	SUCCESS	5	~16,700 kg (36,800 lb)	62	16
4231		EROS-C3	ImageSat International	SUCCESS	5	~400 kg (880 lb)	63	16
4232		Transporter-6: (114 payloads Smallsat Rideshare)	Various	SUCCESS	5	Unknown	62	20
4233		OneWeb Flight #16	OneWeb	SUCCESS	5	6,000 kg (13,000 lb)	62	17
4234		USSF-67	USSF	SUCCESS	6	~3,750 kg (8,270 lb)	64	27
4235		GPS III SV06 (Amelia Earhart)	USSF	SUCCESS	5	4,352 kg (9,670 lb)	62	23
4236		Starlink Group 2-4 (51 satellites)	SpaceX	SUCCESS	5	~15,650 kg (~34,700 lb)	63	16
4237		Starlink Group 5-2 (56 satellites)	SpaceX	SUCCESS	5	~17,200 kg (~38,000 lb)	62	16
4238		Starlink Group 2-6 (49 satellites) & ION SCV009	SpaceX, D-Orbit	SUCCESS	5	~15,000 kg (~33,000 lb)	63	16
4239		Starlink Group 5-3 (53 satellites)	SpaceX	SUCCESS	5	~16,300 kg (~36,000 lb)	64	16
4240		Amazonas Nexus	Hispasat	SUCCESS	5	~4,500 kg (~9,900 lb)	62	18
4241		Starlink Group 5-4	SpaceX	SUCCESS	5	~16,900 kg (~37,200 lb)	62	16
4242		Starlink Group 2-5	SpaceX	SUCCESS	5	~15,600 kg (~34,300 lb)	63	16
4243		Inmarsat I-6 F2	Inmarsat	SUCCESS	5	5,470 kg (12,060 lb)	62	18
4244		Starlink Group 6-1	SpaceX	SUCCESS	5	~16,000 kg (35,000 lb)	62	16
4245		Crew-6	NASA	SUCCESS	5	~13,000 kg (29,000 lb)	64	16
4246		Starlink Group 2-7	SpaceX	SUCCESS	5	~15,600 kg (~34,300 lb)	63	16
4247		OneWeb Flight #17	OneWeb	SUCCESS	5	~6,000 kg (~13,000 lbs)	62	17
4248		SpaceX CRS-27	NASA (CRS)	SUCCESS	5	2,852 kg (6,288 lb)	64	16
4249		Starlink Group 2-8	SpaceX	SUCCESS	5	~16,000 kg (35,000 lb)	63	16
4250		SES 18&19	SES	SUCCESS	5	~7,000 kg (15,400 lb)	62	18
4251		Starlink Group 5-5	SpaceX	SUCCESS	5	~17,200 kg (~38,000 lb)	62	16
4252		Starlink Group 5-10	SpaceX	SUCCESS	5	~17,200 kg (~38,000 lb)	62	16
4253		SDA T&T Tranche 0A	SDA	SUCCESS	5	~5,000 kg (~11,000 lb)	63	16
4254		Intelsat 40e TEMPO	Intelsat/NASA	SUCCESS	5	6,161 kg (13,600 lb)	62	18
4255		Transporter-7 (51 payloads)	Numerous	SUCCESS	5	~5,000 kg (~11,000 lb)	63	20
4256		Starlink Group 6-2 (21 satellites)	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4257		Starship Flight 1	SpaceX	PARTIAL FAILURE	7	0 kg	65	25
4258		Starlink Group 3-5 (46 satellites)	SpaceX	SUCCESS	5	~14,100 kg (31,100 lb)	63	16
4259		O3b mPOWER 3 & 4	SES	SUCCESS	5	~4,100 kg (9,000 lb)	62	23
4260		Viasat-3 Americas & others	Astranis Space Technologies and ViaSat	SUCCESS	6	~6,722 kg (14,800 lb)	64	27
4261		Starlink Group 5-6 (56 satellites)	SpaceX	SUCCESS	5	~17,200 kg (~38,000 lb)	62	16
4262		Starlink Group 2-9 (51 satellites)	SpaceX	SUCCESS	5	~15,600 kg (~34,300 lb)	63	16
4263		Starlink Group 5-9 (56 satellites)	SpaceX	SUCCESS	5	~17,200 kg (~38,000 lb)	62	16
4264		Starlink Group 6-3 (22 satellites)	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4265		Iridium 9 and OneWeb 19	SpaceX	SUCCESS	5	~7,000 kg (~15,500 lb)	63	17
4266		Axiom-2	Axiom Space	SUCCESS	5	~13,000 kg (29,000 lb)	64	16
4267		Arabsat 7B (Badr-8)	Arabsat	SUCCESS	5	4,500 kg (9,900 lb)	62	18
4268		Starlink Group 2-10 (52 satellites)	SpaceX	SUCCESS	5	~16,000 kg (35,000 lb)	63	16
4269		Starlink Group 6-4 (22 satellites)	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4270		SpaceX CRS-28	NASA (CRS)	SUCCESS	5	~3,150+ kg (~7,000+ lb)	64	16
4271		Starlink Group 5-11	SpaceX	SUCCESS	5	~16,000 kg (~35,000 lb)	62	16
4272		Transporter-8 (72 payloads)	Numerous	SUCCESS	5	Unknown	63	20
4273		Satria	PT Pasifik Satelit Nusantara	SUCCESS	5	~4,700 kg (~10,400 lb)	62	18
4274		Starlink Group 5-7	SpaceX	SUCCESS	5	~14,500 kg (~32,000 lb)	63	16
4275		Starlink Group 5-12	SpaceX	SUCCESS	5	~17,200 kg (~38,000 lb)	62	16
4276		Euclid Telescope	ESA	SUCCESS	5	~2,100 kg (~4,600 lb)	62	28
4277		Starlink Group 5-13	SpaceX	SUCCESS	5	~14,700 kg (~32,400 lb)	63	16
4278		Starlink Group 6-5	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4279		Starlink Group 5-15	SpaceX	SUCCESS	5	~16,600 kg (~36,600 lb)	62	16
4280		Starlink Group 6-15	SpaceX	SUCCESS	5	~12,000 kg (~26,500 lb)	63	16
4281		Starlink Group 6-6	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4282		Starlink Group 6-7	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4283		EchoStar 24 (Jupiter 3)	EchoStar	SUCCESS	6	9,200 kg (20,300 lb)	64	18
4284		Galaxy 37	Intelsat	SUCCESS	5	~3,500 kg (~7,700)	62	18
4285		Starlink Group 6-8	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4286		Starlink Group 6-20	SpaceX	SUCCESS	5	~12,000 kg (~26,500 lb)	63	16
4287		Starlink Group 6-9	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4288		Starlink Group 6-10	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4289		Starlink Group 7-1	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	63	16
4290		Crew-7	NASA (CTS)	SUCCESS	5	~13,000 kg (29,000 lb)	64	16
4291		Starlink Group 6-11	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4292		Starlink Group 6-13	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4293		SDA T&T Tranche 0B	SDA	SUCCESS	5	~5,000 kg (~11,000 lb)	63	16
4294		Starlink Group 6-12	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	64	16
4295		Starlink Group 6-14	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4296		Starlink Group 7-2	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	63	16
4297		Starlink Group 6-16	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4298		Starlink Group 6-17	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4299		Starlink Group 6-18	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4300		Starlink Group 7-3	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	63	16
4301		Starlink Group 6-19	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4302		Starlink Group 6-21	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4303		Starlink Group 7-4	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	63	16
4304		Psyche	SpaceX	SUCCESS	6	2,600 kg	64	21
4305		Starlink Group 6-22	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4306		Starlink Group 6-23	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	62	16
4307		Starlink Group 7-5	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	63	16
4308		Starlink Group 6-24	SpaceX	SUCCESS	5	~18,400 kg (~40,500 lb)	62	16
4309		Starlink Group 7-6	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	63	16
4310		Starlink Group 6-25	SpaceX	SUCCESS	5	~18,400 kg (~40,500 lb)	62	16
4311		Starlink Group 6-26	SpaceX	SUCCESS	5	~18,400 kg (~40,500 lb)	62	16
4312		Starlink Group 6-27	SpaceX	SUCCESS	5	~18,400 kg (~40,500 lb)	62	16
4313		SpaceX CRS-29	NASA (CRS)	SUCCESS	5	~3,000 kg (6,500 lb)	64	16
4314		Transporter-9	Numerous	SUCCESS	5	Unknown	63	20
4315		O3b mPOWER 5 & 6	SES S.A.	SUCCESS	5	3,400 kg (~7,500 lb)	62	23
4316		Starlink Group 6-28	SpaceX	SUCCESS	5	~18,400 kg (~40,500 lb)	62	16
4317		Starship Flight 2	SpaceX	PARTIAL FAILURE	7	0 kg	65	25
4318		Starlink Group 7-7	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	63	16
4319		Starlink Group 6-29	SpaceX	SUCCESS	5	~18,400 kg (~40,500 lb)	62	16
4320		Starlink Group 6-30	SpaceX	SUCCESS	5	~18,400 kg (~40,500 lb)	62	16
4321		425 Project Flight 1 & others	South Korean DAPA & others	SUCCESS	5	~1,000 kg (~2,400 lb)	63	20
4322		Starlink Group 6-31	SpaceX	SUCCESS	5	~18,400 kg (~40,500 lb)	62	16
4323		Starlink Group 6-33	SpaceX	SUCCESS	5	~18,400 kg (~40,500 lb)	62	16
4324		Starlink Group 7-8	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	63	16
4325		Starlink Group 6-34	SpaceX	SUCCESS	5	~18,400 kg (~40,500 lb)	62	16
4326		Starlink Group 6-32	SpaceX	SUCCESS	5	~18,400 kg (~40,500 lb)	62	16
4327		SARah-2 and SARah-3	Bundeswehr	SUCCESS	5	3,800 kg (~8,400 lb)	63	17
4328		USSF-52	USSF	SUCCESS	6	~5,000 kg (~11,000 lb)	64	29
4329		Starlink Group 6-36	SpaceX	SUCCESS	5	~18,400 kg (~40,500 lb)	62	16
4330		Starlink Group 7-9	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	63	16
4331		Ovzon-3	SpaceX	SUCCESS	5	1,800 kg	62	18
4332		Starlink Group 6-35	SpaceX	SUCCESS	5	~18,400 kg (~40,500 lb)	62	16
4333		Starlink Group 7-10	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	63	16
4334		Starlink Group 6-37	SpaceX	SUCCESS	5	~18,400 kg (~40,500 lb)	62	16
4335		Axiom-3	Axiom Space	SUCCESS	5	~13,000 kg (29,000 lb)	64	16
4336		Starlink Group 7-11	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	63	16
4337		Starlink Group 6-38	SpaceX	SUCCESS	5	~18,400 kg (~40,500 lb)	64	16
4338		Starlink Group 7-12	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	63	16
4339		NG-20	NASA/Northrop Grumman	SUCCESS	5	3,726 kg (8,214 lb)	62	16
4340		PACE	NASA	SUCCESS	5	1,964 kg (4,329 lb)	62	20
4341		Starlink Group 7-13	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	63	16
4342		USSF-124	USSF/SDA	SUCCESS	5	Unknown	62	16
4343		Nova C (IM-1)	Intuitive Machines / NASA	SUCCESS	5	1,931 kg (4,250 lb)	64	30
4344		Starlink Group 7-14	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	63	16
4345		Merah Putih 2	Telkomsat	SUCCESS	5	~4,000 kg (8,800 lb)	62	18
4346		Starlink Group 7-15	SpaceX	SUCCESS	5	~17,600 kg (~37,000 lb)	63	16
4347		Starlink Group 6-39	SpaceX	SUCCESS	5	~17,500 kg (~35,800 lb)	62	16
4348		Starlink Group 6-40	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4349		Crew-8	NASA (CTS)	SUCCESS	5	~13,000 kg (29,000 lb)	64	16
4350		Transporter-10	Various	SUCCESS	5	~5,000 kg (~11,000 lb)	63	20
4351		Starlink Group 6-41	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4352		Starlink Group 6-43	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4353		Starlink Group 7-17	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	63	16
4354		Starship Flight 3	SpaceX	SUCCESS	7	None	65	25
4355		Starlink Group 6-44	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	64	16
4356		Starlink Group 7-16, USA-350, and USA-351	SpaceX	SUCCESS	5	~16,100 kg (~35,500 lb)	63	16
4357		SpaceX CRS-30	NASA	SUCCESS	5	2,841 kg (6,263 lb) (excl. Dragon mass)	62	16
4358		Starlink Group 6-42	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	64	16
4359		Starlink Group 6-46	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4360		Eutelsat 36D	Eutelsat	SUCCESS	5	5,000 kg (11,000 lb)	64	18
4361		Starlink Group 6-45	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4362		Starlink Group 7-18	SpaceX	SUCCESS	5	~16,100 kg (~35,500 lb)	63	16
4363		Starlink Group 6-47	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4364		Starlink Group 8-1	SpaceX	SUCCESS	5	~15,300 kg (~33,700 lb)	63	16
4365		Bandwagon-1	South Korean DAPA & others	SUCCESS	5	~1,300 kg (2,870 lb)	64	16
4367		Starlink Group 6-48	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4368		USSF-62 (WSF-M 1)	USSF	SUCCESS	5	1,200 kg (2,650 lb)	63	20
4369		Starlink Group 6-49	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4370		Starlink Group 6-51	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	64	16
4371		Starlink Group 6-52	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4372		Starlink Group 6-53	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4373		WorldView Legion 1 & 2	DigitalGlobe	SUCCESS	5	1,500 kg	63	20
4375		Galileo FOC FM25 & FM27	ESA	SUCCESS	5	1,603 kg	64	23
4376		Starlink Group 6-54	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4377		Starlink Group 6-55	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4378		Starlink Group 6-57	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4379		Starlink Group 6-56	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	64	16
4380		Starlink Group 8-2	SpaceX	SUCCESS	5	~16,000 kg (~35,000 lb)	63	16
4381		Starlink Group 6-58	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4382		Starlink Group 8-7	SpaceX	SUCCESS	5	~16,000 kg (~35,000 lb)	63	16
4383		Starlink Group 6-59	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4384		NROL-146	NROL	SUCCESS	5	Unknown	63	17
4385		Starlink Group 6-62	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4386		Starlink Group 6-63	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	64	16
4387		Starlink Group 6-60	SpaceX	SUCCESS	5	~16,800 kg (~37,000 lb)	62	16
4388		EarthCARE	ESA/JAXA/NICT	SUCCESS	5	2,350 kg	63	20
4390		Starlink Group 6-64	SpaceX		5	~16,800 kg (~37,000 lb)	62	16
\.


--
-- Data for Name: _booster_tracker_operator; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._booster_tracker_operator (id, name) FROM stdin;
1	SpaceX
\.


--
-- Data for Name: _booster_tracker_orbit; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._booster_tracker_orbit (id, name) FROM stdin;
26	Ballistic lunar transfer
30	Ballistic lunar transfer (BLT)
27	Geostationary Earth Orbit
18	Geostationary Transfer Orbit
21	Heliocentric
22	High-Earth Orbit
16	Low-Earth Orbit
24	Low-Earth Orbit/Medium-Earth Orbit
23	Medium-Earth Orbit
29	Molniya
17	Polar Low-Earth Orbit
25	Sub-orbital
28	Sun-Earth L2
20	Sun-Synchronous Orbit
19	Sun–Earth L1
\.


--
-- Data for Name: _booster_tracker_pad; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._booster_tracker_pad (id, name, nickname, location, status, image) FROM stdin;
61	Omelek Island	Omelek Island	Omelek Island, Kwajalein Atoll, Republic of Marshall Islands	RETIRED	pad_photos/omelek.jpeg
62	Space Launch Complex 40	SLC-40	Cape Canaveral Space Force Station, Florida	ACTIVE	pad_photos/slc_40.jpeg
63	Space Launch Complex 4 East	SLC-4E	Vandenberg Space Force Base, California	ACTIVE	pad_photos/slc_4e.jpeg
64	Launch Complex 39A	LC-39A	Kennedy Space Center, Florida	ACTIVE	pad_photos/lc39a.jpeg
65	Orbital Launch Pad A	OLP-A	Starbase, Texas	ACTIVE	pad_photos/olp_a_FdpzRIp.jpeg
\.


--
-- Data for Name: _booster_tracker_padused; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._booster_tracker_padused (id, pad_id, rocket_id, image) FROM stdin;
1	61	8	rocket_pad_photos/Falcon_1_launches_photo.jpg
2	65	7	rocket_pad_photos/Starship_OLPA_launches_photo.jpg
3	64	6	rocket_pad_photos/Falcon_Heavy_launches_photo.jpg
4	62	5	rocket_pad_photos/Falcon_SLC40_launches_photo.jpg
5	64	5	rocket_pad_photos/Falcon_LC39A_launches_photo.jpg
6	63	5	rocket_pad_photos/Falcon_SLC4E_launches_photo.jpg
\.


--
-- Data for Name: _booster_tracker_rocket; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._booster_tracker_rocket (id, name, status, family_id) FROM stdin;
5	Falcon 9	ACTIVE	1
6	Falcon Heavy	ACTIVE	1
7	Starship	ACTIVE	2
8	Falcon 1	RETIRED	1
\.


--
-- Data for Name: _booster_tracker_rocketfamily; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._booster_tracker_rocketfamily (id, name, provider_id) FROM stdin;
1	Falcon	1
2	Starship	1
\.


--
-- Data for Name: _booster_tracker_spacecraft; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._booster_tracker_spacecraft (id, name, nickname, version, type, family_id, status, image) FROM stdin;
1	C101		v1	CARGO	1	RETIRED	spacecraft_photos/default_dragon.jpg
2	C102		v1	CARGO	1	RETIRED	spacecraft_photos/default_dragon.jpg
3	C103		v1	CARGO	1	RETIRED	spacecraft_photos/default_dragon.jpg
4	C104		v1	CARGO	1	RETIRED	spacecraft_photos/default_dragon.jpg
5	C105		v1	CARGO	1	RETIRED	spacecraft_photos/default_dragon.jpg
6	C106		v1	CARGO	1	RETIRED	spacecraft_photos/default_dragon.jpg
7	C107		v1	CARGO	1	RETIRED	spacecraft_photos/default_dragon.jpg
8	C108		v1	CARGO	1	RETIRED	spacecraft_photos/default_dragon.jpg
9	C109		v1	CARGO	1	LOST	spacecraft_photos/default_dragon.jpg
10	C110		v1	CARGO	1	RETIRED	spacecraft_photos/default_dragon.jpg
11	C111		v1	CARGO	1	RETIRED	spacecraft_photos/default_dragon.jpg
12	C112		v1	CARGO	1	RETIRED	spacecraft_photos/default_dragon.jpg
13	C113		v1	CARGO	1	RETIRED	spacecraft_photos/default_dragon.jpg
14	C204		v2	CREW	1	LOST	spacecraft_photos/default_dragon.jpg
15	C205		v2	CREW	1	RETIRED	spacecraft_photos/default_dragon.jpg
16	C206	Endeavour	v2	CREW	1	ACTIVE	spacecraft_photos/default_dragon.jpg
17	C207	Resilience	v2	CREW	1	ACTIVE	spacecraft_photos/default_dragon.jpg
18	C208		v2	CARGO	1	ACTIVE	spacecraft_photos/default_dragon.jpg
19	C209		v2	CARGO	1	ACTIVE	spacecraft_photos/default_dragon.jpg
20	C210	Endurance	v2	CREW	1	ACTIVE	spacecraft_photos/default_dragon.jpg
21	C211		v2	CARGO	1	ACTIVE	spacecraft_photos/default_dragon.jpg
22	C212	Freedom	v2	CREW	1	ACTIVE	spacecraft_photos/default_dragon.jpg
\.


--
-- Data for Name: _booster_tracker_spacecraftfamily; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._booster_tracker_spacecraftfamily (id, status, provider_id, name) FROM stdin;
1	ACTIVE	1	Dragon
\.


--
-- Data for Name: _booster_tracker_spacecraftonlaunch; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._booster_tracker_spacecraftonlaunch (id, splashdown_time, launch_id, spacecraft_id, recovery_boat_id) FROM stdin;
1		4034	1	284
2		4035	2	284
3		4036	3	285
4		4037	4	285
5		4041	5	285
6		4045	6	285
7		4068	6	286
8		4112	6	286
9		4046	7	286
10		4049	8	286
11		4078	8	286
12		4109	8	286
13		4051	9	287
14		4055	10	286
15		4086	10	286
16		4059	11	286
17		4091	11	286
18		4063	12	286
19		4099	12	286
20		4118	12	286
21		4072	13	286
22		4105	13	286
23		4137	18	283
24		4160	18	282
25		4200	18	282
26		4270	18	283
27		4156	19	283
28		4170	19	283
29		4248	19	283
30		4357	19	283
31		4224	11	282
32		4313	21	283
33		4103	14	283
34		4115	15	283
35		4121	16	283
36		4150	16	283
37		4183	16	282
38		4245	16	282
39		4349	16
40		4134	17	283
41		4162	17	282
42		4163	20	283
43		4214	20	283
44		4290	20	282
45		4186	22	282
46		4266	22	282
47		4335	22	283
\.


--
-- Data for Name: _booster_tracker_stage; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._booster_tracker_stage (id, version, type, rocket_id, name, status, image) FROM stdin;
271	v1.0	BOOSTER	5	B0003	LOST	stage_photos/default_booster.jpg
272	v1.0	BOOSTER	5	B0004	LOST	stage_photos/default_booster.jpg
273	v1.0	BOOSTER	5	B0005	EXPENDED	stage_photos/default_booster.jpg
274	v1.0	BOOSTER	5	B0006	EXPENDED	stage_photos/default_booster.jpg
275	v1.0	BOOSTER	5	B0007	EXPENDED	stage_photos/default_booster.jpg
276	v1.1 B1	BOOSTER	5	B1003	EXPENDED	stage_photos/default_booster.jpg
277	v1.1 B1	BOOSTER	5	B1004	EXPENDED	stage_photos/default_booster.jpg
278	v1.1 B1	BOOSTER	5	B1005	EXPENDED	stage_photos/default_booster.jpg
279	v1.1 B1	BOOSTER	5	B1006	EXPENDED	stage_photos/default_booster.jpg
280	v1.1 B1	BOOSTER	5	B1007	EXPENDED	stage_photos/default_booster.jpg
281	v1.1 B1	BOOSTER	5	B1008	EXPENDED	stage_photos/default_booster.jpg
282	v1.1 B2	BOOSTER	5	B1011	EXPENDED	stage_photos/default_booster.jpg
283	v1.1 B1	BOOSTER	5	B1010	EXPENDED	stage_photos/default_booster.jpg
284	v1.1 B2	BOOSTER	5	B1012	LOST	stage_photos/default_booster.jpg
285	v1.1 B2	BOOSTER	5	B1013	EXPENDED	stage_photos/default_booster.jpg
286	v1.1 B2	BOOSTER	5	B1014	EXPENDED	stage_photos/default_booster.jpg
287	v1.1 B2	BOOSTER	5	B1015	LOST	stage_photos/default_booster.jpg
288	v1.1 B2	BOOSTER	5	B1016	EXPENDED	stage_photos/default_booster.jpg
289	v1.1 B2	BOOSTER	5	B1018	LOST	stage_photos/default_booster.jpg
290	v1.2 B1	BOOSTER	5	B1019	RETIRED	stage_photos/default_booster.jpg
291	v1.1 B2	BOOSTER	5	B1017	LOST	stage_photos/default_booster.jpg
292	v1.2 B1	BOOSTER	5	B1020	LOST	stage_photos/default_booster.jpg
293	v1.2 B2	BOOSTER	5	B1021	RETIRED	stage_photos/default_booster.jpg
294	v1.2 B2	BOOSTER	5	B1022	RETIRED	stage_photos/default_booster.jpg
295	v1.2 B2	BOOSTER	5	B1023	RETIRED	stage_photos/default_booster.jpg
296	v1.2 B2	BOOSTER	5	B1024	LOST	stage_photos/default_booster.jpg
297	v1.2 B2	BOOSTER	5	B1025	RETIRED	stage_photos/default_booster.jpg
298	v1.2 B2	BOOSTER	5	B1026	RETIRED	stage_photos/default_booster.jpg
299	v1.2 B3	BOOSTER	5	B1028	LOST	stage_photos/default_booster.jpg
300	v1.2 B3	BOOSTER	5	B1029	RETIRED	stage_photos/default_booster.jpg
301	v1.2 B3	BOOSTER	5	B1031	RETIRED	stage_photos/default_booster.jpg
302	v1.2 B3	BOOSTER	5	B1030	EXPENDED	stage_photos/default_booster.jpg
303	v1.2 B3	BOOSTER	5	B1032	EXPENDED	stage_photos/default_booster.jpg
304	v1.2 B3	BOOSTER	5	B1034	EXPENDED	stage_photos/default_booster.jpg
305	v1.2 B3	BOOSTER	5	B1035	RETIRED	stage_photos/default_booster.jpg
306	v1.2 B3	BOOSTER	5	B1036	EXPENDED	stage_photos/default_booster.jpg
307	v1.2 B3	BOOSTER	5	B1037	EXPENDED	stage_photos/default_booster.jpg
308	v1.2 B4	BOOSTER	5	B1039	EXPENDED	stage_photos/default_booster.jpg
309	v1.2 B3	BOOSTER	5	B1038	EXPENDED	stage_photos/default_booster.jpg
310	v1.2 B4	BOOSTER	5	B1040	EXPENDED	stage_photos/default_booster.jpg
311	v1.2 B4	BOOSTER	5	B1041	EXPENDED	stage_photos/default_booster.jpg
312	v1.2 B4	BOOSTER	5	B1042	RETIRED	stage_photos/default_booster.jpg
313	v1.2 B4	BOOSTER	5	B1043	EXPENDED	stage_photos/default_booster.jpg
314	v1.2 B3	BOOSTER	6	B1033	LOST	stage_photos/default_booster.jpg
315	v1.2 B4	BOOSTER	5	B1044	EXPENDED	stage_photos/default_booster.jpg
316	v1.2 B4	BOOSTER	5	B1045	EXPENDED	stage_photos/default_booster.jpg
317	v1.2 B5.0	BOOSTER	5	B1046	EXPENDED	stage_photos/default_booster.jpg
318	v1.2 B5.0	BOOSTER	5	B1047	EXPENDED	stage_photos/default_booster.jpg
319	v1.2 B5.0	BOOSTER	5	B1048	LOST	stage_photos/default_booster.jpg
320	v1.2 B5.0	BOOSTER	5	B1049	EXPENDED	stage_photos/default_booster.jpg
321	v1.2 B5.0	BOOSTER	5	B1050	LOST	stage_photos/default_booster.jpg
322	v1.2 B5.2	BOOSTER	5	B1054	EXPENDED	stage_photos/default_booster.jpg
323	v1.2 B5.1	BOOSTER	5	B1051	EXPENDED	stage_photos/default_booster.jpg
324	v1.2 B5.2	BOOSTER	6	B1055	LOST	stage_photos/default_booster.jpg
325	v1.2 B5.1	BOOSTER	5	B1052	EXPENDED	stage_photos/default_booster.jpg
326	v1.2 B5.1	BOOSTER	5	B1053	EXPENDED	stage_photos/default_booster.jpg
327	v1.2 B5.3	BOOSTER	5	B1056	LOST	stage_photos/default_booster.jpg
328	v1.2 B5.3	BOOSTER	6	B1057	LOST	stage_photos/default_booster.jpg
329	v1.2 B5.3	BOOSTER	5	B1059	LOST	stage_photos/default_booster.jpg
330	v1.2 B5.3	BOOSTER	5	B1058	LOST	stage_photos/default_booster.jpg
331	v1.2 B5.4	BOOSTER	5	B1060	EXPENDED	stage_photos/default_booster.jpg
332	v1.2 B5.4	BOOSTER	5	B1062	ACTIVE	stage_photos/default_booster.jpg
333	v1.2 B5.4	BOOSTER	5	B1061	ACTIVE	stage_photos/default_booster.jpg
334	v1.2 B5.4	BOOSTER	5	B1063	ACTIVE	stage_photos/default_booster.jpg
335	v1.2 B5.4	BOOSTER	5	B1067	ACTIVE	stage_photos/default_booster.jpg
336	v1.2 B5.4	BOOSTER	5	B1069	ACTIVE	stage_photos/default_booster.jpg
337	v1.2 B5.4	BOOSTER	5	B1071	ACTIVE	stage_photos/default_booster.jpg
338	v1.2 B5.4	BOOSTER	5	B1073	ACTIVE	stage_photos/default_booster.jpg
339	v1.2 B5.4	BOOSTER	5	B1077	ACTIVE	stage_photos/default_booster.jpg
340	v1.2 B5.4	BOOSTER	6	B1066	EXPENDED	stage_photos/default_booster.jpg
341	v1.2 B5.4	BOOSTER	5	B1064	ACTIVE	stage_photos/default_booster.jpg
342	v1.2 B5.4	BOOSTER	5	B1065	ACTIVE	stage_photos/default_booster.jpg
343	v1.2 B5.4	BOOSTER	5	B1076	ACTIVE	stage_photos/default_booster.jpg
344	v1.2 B5.4	BOOSTER	6	B1070	EXPENDED	stage_photos/default_booster.jpg
345	v1.2 B5.4	BOOSTER	5	B1075	ACTIVE	stage_photos/default_booster.jpg
346	v1.2 B5.4	BOOSTER	5	B1078	ACTIVE	stage_photos/default_booster.jpg
347	SH v1.0	BOOSTER	7	B7	EXPENDED	stage_photos/default_booster.jpg
348	v1.2 B5.4	BOOSTER	6	B1068	EXPENDED	stage_photos/default_booster.jpg
349	v1.2 B5.5	BOOSTER	5	B1080	ACTIVE	stage_photos/default_booster.jpg
350	v1.2 B5.4	BOOSTER	6	B1074	EXPENDED	stage_photos/default_booster.jpg
351	v1.2 B5.5	BOOSTER	5	B1081	ACTIVE	stage_photos/default_booster.jpg
352	v1.2 B5.4	BOOSTER	6	B1079	EXPENDED	stage_photos/default_booster.jpg
353	SH v1.0	BOOSTER	7	B9	EXPENDED	stage_photos/default_booster.jpg
354	v1.2 B5.5	BOOSTER	6	B1084	EXPENDED	stage_photos/default_booster.jpg
355	v1.2 B5.5	BOOSTER	5	B1082	ACTIVE	stage_photos/default_booster.jpg
356	v1.2 B5.5	BOOSTER	5	B1083	ACTIVE	stage_photos/default_booster.jpg
357	SH v1.0	BOOSTER	7	B10	EXPENDED	stage_photos/default_booster.jpg
358	SS v1.0	SECOND_STAGE	7	S24	EXPENDED	stage_photos/default_booster.jpg
359	SS v1.0	SECOND_STAGE	7	S25	EXPENDED	stage_photos/default_booster.jpg
360	SS v1.0	SECOND_STAGE	7	S28	EXPENDED	stage_photos/default_booster.jpg
361	v1.2 B5.4	BOOSTER	6	B1072	ACTIVE	stage_photos/default_booster.jpg
\.


--
-- Data for Name: _booster_tracker_stageandrecovery; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._booster_tracker_stageandrecovery (method, recovery_success, latitude, longitude, landing_zone_id, launch_id, stage_id, method_success, stage_position, id) FROM stdin;
PARACHUTE	0				4033	271	FAILURE	SINGLE_CORE	4196
PARACHUTE	0				4034	272	FAILURE	SINGLE_CORE	4197
EXPENDED	0				4035	273	SUCCESS	SINGLE_CORE	4198
EXPENDED	0				4036	274	SUCCESS	SINGLE_CORE	4199
EXPENDED	0				4037	275	SUCCESS	SINGLE_CORE	4200
OCEAN_SURFACE	0				4038	276	FAILURE	SINGLE_CORE	4201
EXPENDED	0				4039	277	SUCCESS	SINGLE_CORE	4202
EXPENDED	0				4040	278	SUCCESS	SINGLE_CORE	4203
OCEAN_SURFACE	0				4041	279	SUCCESS	SINGLE_CORE	4204
OCEAN_SURFACE	0				4042	280	SUCCESS	SINGLE_CORE	4205
EXPENDED	0				4043	281	SUCCESS	SINGLE_CORE	4206
EXPENDED	0				4044	282	SUCCESS	SINGLE_CORE	4207
OCEAN_SURFACE	0				4045	283	FAILURE	SINGLE_CORE	4208
DRONE_SHIP	0	30.8316667	-78.1080556	20	4046	284	FAILURE	SINGLE_CORE	4209
OCEAN_SURFACE	0				4047	285	SUCCESS	SINGLE_CORE	4210
EXPENDED	0				4048	286	SUCCESS	SINGLE_CORE	4211
DRONE_SHIP	0	30.8316646	-78.1080554	20	4049	287	FAILURE	SINGLE_CORE	4212
EXPENDED	0				4050	288	SUCCESS	SINGLE_CORE	4213
DRONE_SHIP	0	30.8316646	-78.1080527	15	4051	289	PRECLUDED	SINGLE_CORE	4214
GROUND_PAD	1			16	4052	290	SUCCESS	SINGLE_CORE	4215
DRONE_SHIP	0	32.1288868	-120.7786127	14	4053	291	FAILURE	SINGLE_CORE	4216
DRONE_SHIP	0	28.2722222	-73.8180556	15	4054	292	FAILURE	SINGLE_CORE	4217
DRONE_SHIP	1	30.5	-78.5	15	4055	293	SUCCESS	SINGLE_CORE	4218
DRONE_SHIP	1	28.19166	-73.83749	15	4056	294	SUCCESS	SINGLE_CORE	4219
DRONE_SHIP	1	28.1147222	-73.6422222	15	4057	295	SUCCESS	SINGLE_CORE	4220
DRONE_SHIP	0	28.1147222	-73.6422222	15	4058	296	FAILURE	SINGLE_CORE	4221
GROUND_PAD	1			16	4059	297	SUCCESS	SINGLE_CORE	4222
DRONE_SHIP	1	28.1030556	-74.5666667	15	4060	298	SUCCESS	SINGLE_CORE	4223
DRONE_SHIP	0	28.1477778	-73.83	15	4061	299	PRECLUDED	SINGLE_CORE	4224
DRONE_SHIP	1	31.2958333	-120.5127778	14	4062	300	SUCCESS	SINGLE_CORE	4225
GROUND_PAD	1			16	4063	301	SUCCESS	SINGLE_CORE	4226
EXPENDED	0				4064	302	SUCCESS	SINGLE_CORE	4227
DRONE_SHIP	1	28.2552778	-74.0216667	15	4065	293	SUCCESS	SINGLE_CORE	4228
GROUND_PAD	1			16	4066	303	SUCCESS	SINGLE_CORE	4229
EXPENDED	0				4067	304	SUCCESS	SINGLE_CORE	4230
GROUND_PAD	1			16	4068	305	SUCCESS	SINGLE_CORE	4231
DRONE_SHIP	1	28.23	-73.6808333	15	4069	300	SUCCESS	SINGLE_CORE	4232
DRONE_SHIP	1	31.7522	-119.9613	14	4070	306	SUCCESS	SINGLE_CORE	4233
EXPENDED	0				4071	307	SUCCESS	SINGLE_CORE	4234
GROUND_PAD	1			16	4072	308	SUCCESS	SINGLE_CORE	4235
DRONE_SHIP	1	31.6661111	-121.6619444	14	4073	309	SUCCESS	SINGLE_CORE	4236
GROUND_PAD	1			16	4074	310	SUCCESS	SINGLE_CORE	4237
DRONE_SHIP	1	32.4852778	-120.0647222	14	4075	311	SUCCESS	SINGLE_CORE	4238
DRONE_SHIP	1	28.5067	-73.9561	15	4076	301	SUCCESS	SINGLE_CORE	4239
DRONE_SHIP	1	28.0113889	-74.2605556	15	4077	312	SUCCESS	SINGLE_CORE	4240
GROUND_PAD	1			16	4078	305	SUCCESS	SINGLE_CORE	4241
OCEAN_SURFACE	0				4079	306	SUCCESS	SINGLE_CORE	4242
GROUND_PAD	1			16	4080	313	SUCCESS	SINGLE_CORE	4243
OCEAN_SURFACE	0				4081	303	SUCCESS	SINGLE_CORE	4244
DRONE_SHIP	0	29.0195	-75.444	15	4082	314	FAILURE	CENTER	4245
GROUND_PAD	1	29.0195	-75.444	16	4082	295	SUCCESS	PY	4246
GROUND_PAD	1	29.0195	-75.444	17	4082	297	SUCCESS	MY	4247
EXPENDED	0				4083	309	SUCCESS	SINGLE_CORE	4248
OCEAN_SURFACE	0				4084	315	SUCCESS	SINGLE_CORE	4249
OCEAN_SURFACE	0				4085	311	SUCCESS	SINGLE_CORE	4250
EXPENDED	0				4086	308	SUCCESS	SINGLE_CORE	4251
DRONE_SHIP	1	28.8741667	-77.5063889	15	4087	316	SUCCESS	SINGLE_CORE	4252
DRONE_SHIP	1	28.298	-74.1366	15	4088	317	SUCCESS	SINGLE_CORE	4253
EXPENDED	0				4089	313	SUCCESS	SINGLE_CORE	4254
EXPENDED	0				4090	310	SUCCESS	SINGLE_CORE	4255
EXPENDED	0				4091	316	SUCCESS	SINGLE_CORE	4256
DRONE_SHIP	1	28.3748	-74.157	15	4092	318	SUCCESS	SINGLE_CORE	4257
DRONE_SHIP	1	32.4853	-120.0647	14	4093	319	SUCCESS	SINGLE_CORE	4258
DRONE_SHIP	1	28.3342	-73.8794	15	4094	317	SUCCESS	SINGLE_CORE	4259
DRONE_SHIP	1	28.4222	-73.9813	15	4095	320	SUCCESS	SINGLE_CORE	4260
GROUND_PAD	1			18	4096	319	SUCCESS	SINGLE_CORE	4261
DRONE_SHIP	1	28.3525	-73.8825	15	4097	318	SUCCESS	SINGLE_CORE	4262
DRONE_SHIP	1	34.548	-121.129	14	4098	317	SUCCESS	SINGLE_CORE	4263
GROUND_PAD	0			16	4099	321	FAILURE	SINGLE_CORE	4264
EXPENDED	0				4100	322	SUCCESS	SINGLE_CORE	4265
DRONE_SHIP	1	32.4853	-120.0647	14	4101	320	SUCCESS	SINGLE_CORE	4266
DRONE_SHIP	1	28.284	-73.6966	15	4102	319	SUCCESS	SINGLE_CORE	4267
DRONE_SHIP	1	31.7231	-76.9797	15	4103	323	SUCCESS	SINGLE_CORE	4268
DRONE_SHIP	1	28.5492	-70.71	15	4104	324	SUCCESS	CENTER	4269
GROUND_PAD	1	28.5492	-70.71	16	4104	325	SUCCESS	MY	4270
GROUND_PAD	1	28.5492	-70.71	17	4104	326	SUCCESS	PY	4271
DRONE_SHIP	1	28.4428	-80.3217	15	4105	327	SUCCESS	SINGLE_CORE	4272
DRONE_SHIP	1	32.8158	-76.3825	15	4106	320	SUCCESS	SINGLE_CORE	4273
GROUND_PAD	1			18	4107	323	SUCCESS	SINGLE_CORE	4274
DRONE_SHIP	0	27.9478	-68.0153	15	4108	328	FAILURE	CENTER	4275
GROUND_PAD	1	27.9478	-68.0153	16	4108	325	SUCCESS	MY	4276
GROUND_PAD	1	27.9478	-68.0153	17	4108	326	SUCCESS	PY	4277
GROUND_PAD	1			16	4109	327	SUCCESS	SINGLE_CORE	4278
EXPENDED	0				4110	318	SUCCESS	SINGLE_CORE	4279
DRONE_SHIP	1	32.5472	-75.9231	15	4111	319	SUCCESS	SINGLE_CORE	4280
DRONE_SHIP	1	30.9483	-78.3022	15	4112	329	SUCCESS	SINGLE_CORE	4281
DRONE_SHIP	1	28.3228	-73.9297	15	4113	327	SUCCESS	SINGLE_CORE	4282
DRONE_SHIP	1	32.5472	-75.9231	15	4114	320	SUCCESS	SINGLE_CORE	4283
EXPENDED	0				4115	317	SUCCESS	SINGLE_CORE	4284
DRONE_SHIP	1	32.5472	-75.9231	15	4116	323	SUCCESS	SINGLE_CORE	4285
DRONE_SHIP	0	32.5472	-75.9231	15	4117	327	FAILURE	SINGLE_CORE	4286
GROUND_PAD	1			16	4118	329	SUCCESS	SINGLE_CORE	4287
DRONE_SHIP	0	32.5472	-75.9231	15	4119	319	FAILURE	SINGLE_CORE	4288
DRONE_SHIP	1	32.5472	-75.9231	15	4120	323	SUCCESS	SINGLE_CORE	4289
DRONE_SHIP	1	31.9474	-76.9842	15	4121	330	SUCCESS	SINGLE_CORE	4290
DRONE_SHIP	1	32.5472	-75.9231	14	4122	320	SUCCESS	SINGLE_CORE	4291
DRONE_SHIP	1	32.5472	-75.9231	15	4123	329	SUCCESS	SINGLE_CORE	4292
DRONE_SHIP	1	32.9353	-76.3331	14	4124	331	SUCCESS	SINGLE_CORE	4293
DRONE_SHIP	1	28.282	-73.9341	14	4125	330	SUCCESS	SINGLE_CORE	4294
DRONE_SHIP	1	32.5803	-75.8806	15	4126	323	SUCCESS	SINGLE_CORE	4295
DRONE_SHIP	1	32.5803	-75.8806	15	4127	320	SUCCESS	SINGLE_CORE	4296
GROUND_PAD	1			16	4128	329	SUCCESS	SINGLE_CORE	4297
DRONE_SHIP	1	32.5803	-75.8806	15	4129	331	SUCCESS	SINGLE_CORE	4298
DRONE_SHIP	1	32.5803	-75.8806	15	4130	330	SUCCESS	SINGLE_CORE	4299
DRONE_SHIP	1	32.5803	-75.8806	15	4131	323	SUCCESS	SINGLE_CORE	4300
DRONE_SHIP	1	32.412	-76.0751	14	4132	331	SUCCESS	SINGLE_CORE	4301
DRONE_SHIP	1	32.75	-76.075	15	4133	332	SUCCESS	SINGLE_CORE	4302
DRONE_SHIP	1	32.3377	-76.6915	14	4134	333	SUCCESS	SINGLE_CORE	4303
GROUND_PAD	1			18	4135	334	SUCCESS	SINGLE_CORE	4304
DRONE_SHIP	1	32.5803	-75.8806	15	4136	320	SUCCESS	SINGLE_CORE	4305
DRONE_SHIP	1	32.5928	-76.0392	15	4137	330	SUCCESS	SINGLE_CORE	4306
DRONE_SHIP	1	28.35	-74.005	14	4138	323	SUCCESS	SINGLE_CORE	4307
GROUND_PAD	1			16	4139	329	SUCCESS	SINGLE_CORE	4308
DRONE_SHIP	1	28.2919	-73.7064	14	4140	331	SUCCESS	SINGLE_CORE	4309
DRONE_SHIP	1	32.5803	-75.8806	14	4141	323	SUCCESS	SINGLE_CORE	4310
DRONE_SHIP	1	23.5982	-79.1433	15	4142	330	SUCCESS	SINGLE_CORE	4311
DRONE_SHIP	1	32.5803	-75.8806	15	4143	331	SUCCESS	SINGLE_CORE	4312
DRONE_SHIP	0	32.5803	-75.8806	15	4144	329	FAILURE	SINGLE_CORE	4313
DRONE_SHIP	1	32.3583	-76.0567	15	4145	320	SUCCESS	SINGLE_CORE	4314
DRONE_SHIP	1	32.4409	-76.0132	14	4146	330	SUCCESS	SINGLE_CORE	4315
DRONE_SHIP	1	32.489	-76.0483	15	4147	323	SUCCESS	SINGLE_CORE	4316
DRONE_SHIP	1	32.4588	-76.0532	15	4148	331	SUCCESS	SINGLE_CORE	4317
DRONE_SHIP	1	32.5656	-75.9078	15	4149	330	SUCCESS	SINGLE_CORE	4318
DRONE_SHIP	1	32.1581	-76.7414	15	4150	333	SUCCESS	SINGLE_CORE	4319
DRONE_SHIP	1	32.5373	-75.9415	14	4151	331	SUCCESS	SINGLE_CORE	4320
DRONE_SHIP	1	32.5767	-75.8817	15	4152	320	SUCCESS	SINGLE_CORE	4321
DRONE_SHIP	1	32.5282	-76.0067	14	4153	323	SUCCESS	SINGLE_CORE	4322
DRONE_SHIP	1	32.4133	-76.0722	15	4154	330	SUCCESS	SINGLE_CORE	4323
DRONE_SHIP	1	32.5203	-75.9596	14	4155	334	SUCCESS	SINGLE_CORE	4324
DRONE_SHIP	1	30.5356	-78.3928	15	4156	335	SUCCESS	SINGLE_CORE	4325
DRONE_SHIP	1	28.3985	-73.8842	14	4157	333	SUCCESS	SINGLE_CORE	4326
DRONE_SHIP	1	32.695	-76.1483	14	4158	332	SUCCESS	SINGLE_CORE	4327
GROUND_PAD	1			16	4159	331	SUCCESS	SINGLE_CORE	4328
DRONE_SHIP	1	30.5464	-78.4486	19	4160	333	SUCCESS	SINGLE_CORE	4329
DRONE_SHIP	1	29.3725	-117.8551	15	4161	320	SUCCESS	SINGLE_CORE	4330
DRONE_SHIP	1	32.2143	-76.6468	14	4162	332	SUCCESS	SINGLE_CORE	4331
DRONE_SHIP	1	32.2176	-76.6772	19	4163	335	SUCCESS	SINGLE_CORE	4332
DRONE_SHIP	1	32.5891	-75.8816	14	4164	330	SUCCESS	SINGLE_CORE	4333
DRONE_SHIP	1	28.9572	-119.4121	15	4165	334	SUCCESS	SINGLE_CORE	4334
DRONE_SHIP	1	32.5134	-75.9688	19	4166	331	SUCCESS	SINGLE_CORE	4335
DRONE_SHIP	1	28.2188	-73.9759	14	4167	333	SUCCESS	SINGLE_CORE	4336
DRONE_SHIP	1	29.9036	-116.7626	15	4168	323	SUCCESS	SINGLE_CORE	4337
DRONE_SHIP	1	28.2533	-73.88	19	4169	335	SUCCESS	SINGLE_CORE	4338
DRONE_SHIP	1	32.5782	-76.1416	14	4170	336	SUCCESS	SINGLE_CORE	4339
DRONE_SHIP	1	25.6617	-75.075	19	4171	332	SUCCESS	SINGLE_CORE	4340
GROUND_PAD	1			16	4172	330	SUCCESS	SINGLE_CORE	4341
DRONE_SHIP	1	25.6526	-75.0576	19	4173	331	SUCCESS	SINGLE_CORE	4342
GROUND_PAD	1			16	4174	325	SUCCESS	SINGLE_CORE	4343
GROUND_PAD	1			18	4175	337	SUCCESS	SINGLE_CORE	4344
DRONE_SHIP	1	25.6304	-75.1038	19	4176	333	SUCCESS	SINGLE_CORE	4345
DRONE_SHIP	1	25.6381	-75.0021	19	4177	330	SUCCESS	SINGLE_CORE	4346
DRONE_SHIP	1	32.6948	-162.1404	15	4178	334	SUCCESS	SINGLE_CORE	4347
DRONE_SHIP	1	25.6277	-75.0091	14	4179	331	SUCCESS	SINGLE_CORE	4348
DRONE_SHIP	1	25.721	-75.045	19	4180	325	SUCCESS	SINGLE_CORE	4349
DRONE_SHIP	1	32.56	-75.9367	14	4181	323	SUCCESS	SINGLE_CORE	4350
DRONE_SHIP	1	24.0267	-79.235	14	4182	333	SUCCESS	SINGLE_CORE	4351
DRONE_SHIP	1	32.1217	-76.75	19	4183	332	SUCCESS	SINGLE_CORE	4352
GROUND_PAD	1			18	4184	337	SUCCESS	SINGLE_CORE	4353
DRONE_SHIP	1	32.5541	-75.9219	14	4185	331	SUCCESS	SINGLE_CORE	4354
DRONE_SHIP	1	32.1933	-76.7	19	4186	335	SUCCESS	SINGLE_CORE	4355
DRONE_SHIP	1	32.48	-75.9633	14	4187	332	SUCCESS	SINGLE_CORE	4356
DRONE_SHIP	1	32.5862	-75.8798	19	4188	330	SUCCESS	SINGLE_CORE	4357
DRONE_SHIP	1	29.8667	-116.7287	15	4189	334	SUCCESS	SINGLE_CORE	4358
DRONE_SHIP	1	32.441	-76.0762	14	4190	338	SUCCESS	SINGLE_CORE	4359
DRONE_SHIP	1	32.5367	-75.9454	19	4191	325	SUCCESS	SINGLE_CORE	4360
GROUND_PAD	1			16	4192	333	SUCCESS	SINGLE_CORE	4361
DRONE_SHIP	1	27.7869	-73.8051	14	4193	332	SUCCESS	SINGLE_CORE	4362
DRONE_SHIP	1	32.7008	-75.7345	19	4194	331	SUCCESS	SINGLE_CORE	4363
GROUND_PAD	1			18	4195	337	SUCCESS	SINGLE_CORE	4364
DRONE_SHIP	1	32.8383	-75.9917	14	4196	333	SUCCESS	SINGLE_CORE	4365
DRONE_SHIP	1	27.9048	-74.1788	19	4197	338	SUCCESS	SINGLE_CORE	4366
DRONE_SHIP	1	32.6703	-75.7781	14	4198	330	SUCCESS	SINGLE_CORE	4367
DRONE_SHIP	1	28.9481	-121.8378	15	4199	334	SUCCESS	SINGLE_CORE	4368
DRONE_SHIP	1	30.5464	-78.4486	19	4200	335	SUCCESS	SINGLE_CORE	4369
DRONE_SHIP	1	32.6921	-75.7478	14	4201	323	SUCCESS	SINGLE_CORE	4370
DRONE_SHIP	1	29.0691	-121.8182	15	4202	337	SUCCESS	SINGLE_CORE	4371
DRONE_SHIP	1	32.7364	-75.6867	19	4203	332	SUCCESS	SINGLE_CORE	4372
DRONE_SHIP	1	29.2126	-74.0594	14	4204	325	SUCCESS	SINGLE_CORE	4373
DRONE_SHIP	1	32.6124	-75.8466	19	4205	338	SUCCESS	SINGLE_CORE	4374
DRONE_SHIP	1	28.9849	-121.8298	15	4206	333	SUCCESS	SINGLE_CORE	4375
DRONE_SHIP	1	32.7862	-75.6286	19	4207	332	SUCCESS	SINGLE_CORE	4376
DRONE_SHIP	1	32.7178	-75.7161	19	4208	336	SUCCESS	SINGLE_CORE	4377
DRONE_SHIP	1	28.9831	-121.8626	15	4209	334	SUCCESS	SINGLE_CORE	4378
DRONE_SHIP	1	32.4967	-75.9442	14	4210	325	SUCCESS	SINGLE_CORE	4379
DRONE_SHIP	1	32.6608	-75.7841	19	4211	330	SUCCESS	SINGLE_CORE	4380
DRONE_SHIP	1	32.7725	-75.64	14	4212	335	SUCCESS	SINGLE_CORE	4381
DRONE_SHIP	1	32.4752	-75.8547	19	4213	338	SUCCESS	SINGLE_CORE	4382
DRONE_SHIP	1	32.1975	-76.7175	14	4214	339	SUCCESS	SINGLE_CORE	4383
DRONE_SHIP	1	29.9376	-116.794	15	4215	337	SUCCESS	SINGLE_CORE	4384
DRONE_SHIP	1	28.2479	-73.7535	19	4216	331	SUCCESS	SINGLE_CORE	4385
DRONE_SHIP	1	28.4473	-73.858	14	4217	336	SUCCESS	SINGLE_CORE	4386
DRONE_SHIP	1	32.7455	-75.6819	19	4218	332	SUCCESS	SINGLE_CORE	4387
DRONE_SHIP	1	29.6883	-116.6809	15	4219	334	SUCCESS	SINGLE_CORE	4388
EXPENDED	0				4220	340	SUCCESS	CENTER	4389
GROUND_PAD	1			16	4220	341	SUCCESS	MY	4390
GROUND_PAD	1			17	4220	342	SUCCESS	PY	4391
DRONE_SHIP	1	28.4451	-73.7968	14	4221	335	SUCCESS	SINGLE_CORE	4392
EXPENDED	0				4222	323	SUCCESS	SINGLE_CORE	4393
EXPENDED	0				4223	320	SUCCESS	SINGLE_CORE	4394
DRONE_SHIP	1	30.5464	-78.4486	14	4224	343	SUCCESS	SINGLE_CORE	4395
GROUND_PAD	1			16	4225	336	SUCCESS	SINGLE_CORE	4396
GROUND_PAD	1			17	4226	338	SUCCESS	SINGLE_CORE	4397
GROUND_PAD	1			18	4227	337	SUCCESS	SINGLE_CORE	4398
DRONE_SHIP	1	28.2948	-73.609	19	4228	335	SUCCESS	SINGLE_CORE	4399
DRONE_SHIP	1	32.7518	-75.6664	14	4229	330	SUCCESS	SINGLE_CORE	4400
DRONE_SHIP	1	25.681	-74.9355	19	4230	332	SUCCESS	SINGLE_CORE	4401
GROUND_PAD	1			18	4231	333	SUCCESS	SINGLE_CORE	4402
GROUND_PAD	1			16	4232	331	SUCCESS	SINGLE_CORE	4403
GROUND_PAD	1			16	4233	343	SUCCESS	SINGLE_CORE	4404
EXPENDED	0				4234	344	SUCCESS	CENTER	4405
GROUND_PAD	1			16	4234	341	SUCCESS	MY	4406
GROUND_PAD	1			17	4234	342	SUCCESS	PY	4407
DRONE_SHIP	1	32.7658	-76.0603	19	4235	339	SUCCESS	SINGLE_CORE	4408
DRONE_SHIP	1	29.1933	-117.7644	15	4236	345	SUCCESS	SINGLE_CORE	4409
DRONE_SHIP	1	25.6097	-74.7964	14	4237	335	SUCCESS	SINGLE_CORE	4410
DRONE_SHIP	1	29.3194	-117.8264	15	4238	337	SUCCESS	SINGLE_CORE	4411
DRONE_SHIP	1	25.6097	-74.7964	19	4239	336	SUCCESS	SINGLE_CORE	4412
DRONE_SHIP	1	28.1564	-74.2564	14	4240	338	SUCCESS	SINGLE_CORE	4413
DRONE_SHIP	1	25.5968	-74.8928	19	4241	332	SUCCESS	SINGLE_CORE	4414
DRONE_SHIP	1	29.18	-117.7583	15	4242	334	SUCCESS	SINGLE_CORE	4415
DRONE_SHIP	1	28.9136	-73.78	14	4243	339	SUCCESS	SINGLE_CORE	4416
DRONE_SHIP	1	25.733	-75.1432	19	4244	343	SUCCESS	SINGLE_CORE	4417
DRONE_SHIP	1	32.18	-76.6583	14	4245	346	SUCCESS	SINGLE_CORE	4418
DRONE_SHIP	1	29.1863	-117.7693	15	4246	333	SUCCESS	SINGLE_CORE	4419
GROUND_PAD	1			16	4247	332	SUCCESS	SINGLE_CORE	4420
DRONE_SHIP	1	30.5464	-78.4486	19	4248	338	SUCCESS	SINGLE_CORE	4421
DRONE_SHIP	1	29.1933	-117.7644	15	4249	337	SUCCESS	SINGLE_CORE	4422
DRONE_SHIP	1	28.2217	-73.7292	14	4250	336	SUCCESS	SINGLE_CORE	4423
DRONE_SHIP	1	25.6904	-75.0434	19	4251	335	SUCCESS	SINGLE_CORE	4424
DRONE_SHIP	1	25.6097	-74.7964	14	4252	339	SUCCESS	SINGLE_CORE	4425
GROUND_PAD	1			18	4253	345	SUCCESS	SINGLE_CORE	4426
DRONE_SHIP	1	28.3166	-73.9334	19	4254	343	SUCCESS	SINGLE_CORE	4427
GROUND_PAD	1			18	4255	334	SUCCESS	SINGLE_CORE	4428
DRONE_SHIP	1	25.6678	-75.0339	19	4256	338	SUCCESS	SINGLE_CORE	4429
EXPENDED	0				4257	347	SUCCESS	SINGLE_CORE	4430
EXPENDED	0				4257	358	SUCCESS	SINGLE_CORE	4431
DRONE_SHIP	1	28.9666	-121.8887	15	4258	333	SUCCESS	SINGLE_CORE	4432
DRONE_SHIP	1	28.2133	-73.655	14	4259	346	SUCCESS	SINGLE_CORE	4433
EXPENDED	0				4260	348	SUCCESS	CENTER	4434
EXPENDED	0				4260	325	SUCCESS	MY	4435
EXPENDED	0				4260	326	SUCCESS	PY	4436
DRONE_SHIP	1	25.6626	-75.0109	19	4261	336	SUCCESS	SINGLE_CORE	4437
DRONE_SHIP	1	29.2139	-117.7756	15	4262	345	SUCCESS	SINGLE_CORE	4438
DRONE_SHIP	1	25.6031	-74.8854	14	4263	335	SUCCESS	SINGLE_CORE	4439
DRONE_SHIP	1	25.6678	-75.0339	19	4264	343	SUCCESS	SINGLE_CORE	4440
DRONE_SHIP	1	28.7528	-120.2539	15	4265	334	SUCCESS	SINGLE_CORE	4441
GROUND_PAD	1			16	4266	349	SUCCESS	SINGLE_CORE	4442
DRONE_SHIP	1	28.4089	-72.2948	14	4267	332	SUCCESS	SINGLE_CORE	4443
DRONE_SHIP	1	29.2139	-117.7756	15	4268	333	SUCCESS	SINGLE_CORE	4444
DRONE_SHIP	1	25.6383	-74.985	14	4269	346	SUCCESS	SINGLE_CORE	4445
DRONE_SHIP	1	32.9778	-75.8242	19	4270	339	SUCCESS	SINGLE_CORE	4446
DRONE_SHIP	1	25.813	-75.0812	14	4271	338	SUCCESS	SINGLE_CORE	4447
GROUND_PAD	1			18	4272	337	SUCCESS	SINGLE_CORE	4448
DRONE_SHIP	1	28.192	-73.5847	19	4273	335	SUCCESS	SINGLE_CORE	4449
DRONE_SHIP	1	29.6075	-116.7281	15	4274	345	SUCCESS	SINGLE_CORE	4450
DRONE_SHIP	1	25.6539	-75.0039	14	4275	336	SUCCESS	SINGLE_CORE	4451
DRONE_SHIP	1	25.8881	-74.2658	19	4276	349	SUCCESS	SINGLE_CORE	4452
DRONE_SHIP	1	29.6075	-116.7281	15	4277	334	SUCCESS	SINGLE_CORE	4453
DRONE_SHIP	1	25.6383	-74.985	14	4278	330	SUCCESS	SINGLE_CORE	4454
DRONE_SHIP	1	25.6436	-74.9844	19	4279	331	SUCCESS	SINGLE_CORE	4455
DRONE_SHIP	1	28.8517	-119.0603	15	4280	337	SUCCESS	SINGLE_CORE	4456
DRONE_SHIP	1	25.6383	-74.985	14	4281	343	SUCCESS	SINGLE_CORE	4457
DRONE_SHIP	1	25.6867	-75.2317	19	4282	332	SUCCESS	SINGLE_CORE	4458
EXPENDED	0				4283	350	SUCCESS	CENTER	4459
GROUND_PAD	1			16	4283	341	SUCCESS	MY	4460
GROUND_PAD	1			17	4283	342	SUCCESS	PY	4461
DRONE_SHIP	1	28.0567	-73.8524	14	4284	339	SUCCESS	SINGLE_CORE	4462
DRONE_SHIP	1	25.7527	-75.1741	19	4285	346	SUCCESS	SINGLE_CORE	4463
DRONE_SHIP	1	28.8517	-119.0603	15	4286	345	SUCCESS	SINGLE_CORE	4464
DRONE_SHIP	1	25.7633	-75.1833	14	4287	336	SUCCESS	SINGLE_CORE	4465
DRONE_SHIP	1	25.7539	-75.1912	19	4288	335	SUCCESS	SINGLE_CORE	4466
DRONE_SHIP	1	29.8806	-116.7508	15	4289	333	SUCCESS	SINGLE_CORE	4467
GROUND_PAD	1			16	4290	351	SUCCESS	SINGLE_CORE	4468
DRONE_SHIP	1	25.7539	-75.1912	14	4291	349	SUCCESS	SINGLE_CORE	4469
DRONE_SHIP	1	25.7539	-75.1912	19	4292	339	SUCCESS	SINGLE_CORE	4470
GROUND_PAD	1			18	4293	334	SUCCESS	SINGLE_CORE	4471
DRONE_SHIP	1	25.9417	-75.4317	14	4294	338	SUCCESS	SINGLE_CORE	4472
DRONE_SHIP	1	25.7539	-75.1912	19	4295	343	SUCCESS	SINGLE_CORE	4473
DRONE_SHIP	1	30.01	-116.7767	15	4296	337	SUCCESS	SINGLE_CORE	4474
DRONE_SHIP	1	25.7539	-75.1912	14	4297	346	SUCCESS	SINGLE_CORE	4475
DRONE_SHIP	1	25.7832	-75.2183	19	4298	330	SUCCESS	SINGLE_CORE	4476
DRONE_SHIP	1	25.768	-75.2351	14	4299	331	SUCCESS	SINGLE_CORE	4477
DRONE_SHIP	1	29.9902	-116.7623	15	4300	345	SUCCESS	SINGLE_CORE	4478
DRONE_SHIP	1	25.8016	-75.2446	19	4301	336	SUCCESS	SINGLE_CORE	4479
DRONE_SHIP	1	25.7888	-75.225	14	4302	343	SUCCESS	SINGLE_CORE	4480
DRONE_SHIP	1	30.0405	-116.8907	15	4303	334	SUCCESS	SINGLE_CORE	4481
EXPENDED	0				4304	352	SUCCESS	CENTER	4482
GROUND_PAD	1			16	4304	341	SUCCESS	MY	4483
GROUND_PAD	1			17	4304	342	SUCCESS	PY	4484
DRONE_SHIP	1	25.7827	-75.2237	19	4305	335	SUCCESS	SINGLE_CORE	4485
DRONE_SHIP	1	25.8433	-75.3533	14	4306	332	SUCCESS	SINGLE_CORE	4486
DRONE_SHIP	1	29.9902	-116.7623	15	4307	333	SUCCESS	SINGLE_CORE	4487
DRONE_SHIP	1	25.7924	-75.2334	19	4308	349	SUCCESS	SINGLE_CORE	4488
DRONE_SHIP	1	29.9902	-116.7623	15	4309	345	SUCCESS	SINGLE_CORE	4489
DRONE_SHIP	1	25.7924	-75.2334	14	4310	339	SUCCESS	SINGLE_CORE	4490
DRONE_SHIP	1	25.7924	-75.2334	19	4311	330	SUCCESS	SINGLE_CORE	4491
DRONE_SHIP	1	25.815	-75.35	14	4312	338	SUCCESS	SINGLE_CORE	4492
GROUND_PAD	1			16	4313	351	SUCCESS	SINGLE_CORE	4493
GROUND_PAD	1			18	4314	337	SUCCESS	SINGLE_CORE	4494
DRONE_SHIP	1	28.2697	-73.585	19	4315	343	SUCCESS	SINGLE_CORE	4495
DRONE_SHIP	1	25.815	-75.35	14	4316	336	SUCCESS	SINGLE_CORE	4496
EXPENDED	0				4317	353	SUCCESS	SINGLE_CORE	4497
EXPENDED	0				4317	359	SUCCESS	SINGLE_CORE	4498
DRONE_SHIP	1	29.8806	-116.7508	15	4318	334	SUCCESS	SINGLE_CORE	4499
DRONE_SHIP	1	25.7644	-75.1885	19	4319	335	SUCCESS	SINGLE_CORE	4500
DRONE_SHIP	1	25.7178	-75.1039	14	4320	332	SUCCESS	SINGLE_CORE	4501
GROUND_PAD	1			18	4321	333	SUCCESS	SINGLE_CORE	4502
DRONE_SHIP	1	25.7178	-75.1039	19	4322	346	SUCCESS	SINGLE_CORE	4503
DRONE_SHIP	1	25.7178	-75.1039	14	4323	339	SUCCESS	SINGLE_CORE	4504
DRONE_SHIP	1	29.8806	-116.7508	15	4324	337	SUCCESS	SINGLE_CORE	4505
DRONE_SHIP	1	25.7178	-75.1039	19	4325	351	SUCCESS	SINGLE_CORE	4506
DRONE_SHIP	1	25.7178	-75.1039	14	4326	330	SUCCESS	SINGLE_CORE	4507
GROUND_PAD	1			18	4327	345	SUCCESS	SINGLE_CORE	4508
EXPENDED	0				4328	354	SUCCESS	CENTER	4509
GROUND_PAD	1			16	4328	341	SUCCESS	MY	4510
GROUND_PAD	1			17	4328	342	SUCCESS	PY	4511
DRONE_SHIP	1	25.7178	-75.1039	19	4329	336	SUCCESS	SINGLE_CORE	4512
DRONE_SHIP	1	29.8806	-116.7508	15	4330	355	SUCCESS	SINGLE_CORE	4513
GROUND_PAD	1			16	4331	343	SUCCESS	SINGLE_CORE	4514
DRONE_SHIP	1	25.6936	-75.095	19	4332	335	SUCCESS	SINGLE_CORE	4515
DRONE_SHIP	1	29.8806	-116.7508	15	4333	333	SUCCESS	SINGLE_CORE	4516
DRONE_SHIP	1	25.6936	-75.095	19	4334	338	SUCCESS	SINGLE_CORE	4517
GROUND_PAD	1			16	4335	349	SUCCESS	SINGLE_CORE	4518
DRONE_SHIP	1	29.8806	-116.7508	15	4336	334	SUCCESS	SINGLE_CORE	4519
DRONE_SHIP	1	25.6936	-75.095	19	4337	332	SUCCESS	SINGLE_CORE	4520
DRONE_SHIP	1	29.8806	-116.7508	15	4338	345	SUCCESS	SINGLE_CORE	4521
GROUND_PAD	1			16	4339	339	SUCCESS	SINGLE_CORE	4522
GROUND_PAD	1			16	4340	351	SUCCESS	SINGLE_CORE	4523
DRONE_SHIP	1	29.8806	-116.7508	15	4341	337	SUCCESS	SINGLE_CORE	4524
GROUND_PAD	1			17	4342	346	SUCCESS	SINGLE_CORE	4525
GROUND_PAD	1			16	4343	331	SUCCESS	SINGLE_CORE	4526
DRONE_SHIP	1	29.8806	-116.7508	15	4344	355	SUCCESS	SINGLE_CORE	4527
DRONE_SHIP	1	28.4575	-73.9808	14	4345	335	SUCCESS	SINGLE_CORE	4528
DRONE_SHIP	1	30.1249	-116.9509	15	4346	333	SUCCESS	SINGLE_CORE	4529
DRONE_SHIP	1	25.6259	-74.9857	19	4347	336	SUCCESS	SINGLE_CORE	4530
DRONE_SHIP	1	25.6936	-75.095	14	4348	343	SUCCESS	SINGLE_CORE	4531
GROUND_PAD	1			16	4349	356	SUCCESS	SINGLE_CORE	4532
GROUND_PAD	1			18	4350	351	SUCCESS	SINGLE_CORE	4533
DRONE_SHIP	1	25.8495	-75.329	19	4351	338	SUCCESS	SINGLE_CORE	4534
DRONE_SHIP	1			14	4352	339	SUCCESS	SINGLE_CORE	4535
DRONE_SHIP	1			15	4353	334	SUCCESS	SINGLE_CORE	4536
OCEAN_SURFACE	0				4354	357	FAILURE	SINGLE_CORE	4537
OCEAN_SURFACE	0				4354	360	FAILURE	SINGLE_CORE	4538
DRONE_SHIP	1			19	4355	332	SUCCESS	SINGLE_CORE	4539
DRONE_SHIP	1			15	4356	345	SUCCESS	SINGLE_CORE	4540
GROUND_PAD	1			16	4357	349	SUCCESS	SINGLE_CORE	4541
DRONE_SHIP	1			14	4358	331	SUCCESS	SINGLE_CORE	4542
DRONE_SHIP	1			19	4359	346	SUCCESS	SINGLE_CORE	4543
DRONE_SHIP	1			14	4360	343	SUCCESS	SINGLE_CORE	4544
DRONE_SHIP	1			19	4361	335	SUCCESS	SINGLE_CORE	4545
DRONE_SHIP	1			15	4362	337	SUCCESS	SINGLE_CORE	4546
DRONE_SHIP	1			19	4363	336	SUCCESS	SINGLE_CORE	4547
DRONE_SHIP	1			15	4364	351	SUCCESS	SINGLE_CORE	4548
GROUND_PAD	1			16	4365	338	SUCCESS	SINGLE_CORE	4549
DRONE_SHIP	1			14	4367	356	SUCCESS	SINGLE_CORE	4551
GROUND_PAD	1			18	4368	355	SUCCESS	SINGLE_CORE	4552
DRONE_SHIP	1			19	4369	332	SUCCESS	SINGLE_CORE	4553
DRONE_SHIP	1			14	4370	339	SUCCESS	SINGLE_CORE	4554
DRONE_SHIP	1			19	4371	349	SUCCESS	SINGLE_CORE	4555
DRONE_SHIP	1			14	4372	346	SUCCESS	SINGLE_CORE	4556
GROUND_PAD	1			18	4373	333	SUCCESS	SINGLE_CORE	4557
EXPENDED	0				4375	331	SUCCESS	SINGLE_CORE	4561
DRONE_SHIP	1			14	4376	343	SUCCESS	SINGLE_CORE	4562
DRONE_SHIP	1			19	4377	335	SUCCESS	SINGLE_CORE	4563
DRONE_SHIP	1			14	4378	336	SUCCESS	SINGLE_CORE	4564
DRONE_SHIP	1			19	4379	356	SUCCESS	SINGLE_CORE	4565
DRONE_SHIP	1			15	4380	355	SUCCESS	SINGLE_CORE	4566
DRONE_SHIP	1			19	4381	338	SUCCESS	SINGLE_CORE	4567
DRONE_SHIP	1			15	4382	334	SUCCESS	SINGLE_CORE	4568
DRONE_SHIP	1			19	4383	332	SUCCESS	SINGLE_CORE	4569
DRONE_SHIP	1			15	4384	337	SUCCESS	SINGLE_CORE	4570
DRONE_SHIP	1			19	4385	349	SUCCESS	SINGLE_CORE	4571
DRONE_SHIP	1			14	4386	339	SUCCESS	SINGLE_CORE	4572
DRONE_SHIP	1			19	4387	346	SUCCESS	SINGLE_CORE	4573
GROUND_PAD	1			18	4388	351	SUCCESS	SINGLE_CORE	4574
DRONE_SHIP	0			19	4390			SINGLE_CORE	4576
\.


--
-- Data for Name: _booster_tracker_supportonlaunch; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._booster_tracker_supportonlaunch (id, boat_id, launch_id) FROM stdin;
1674	234	4046
1675	234	4049
1676	234	4051
1677	236	4053
1678	234	4054
1679	234	4055
1680	234	4056
1681	234	4057
1682	234	4058
1683	234	4060
1684	234	4061
1685	236	4062
1686	234	4065
1687	234	4069
1688	236	4070
1689	236	4073
1690	236	4075
1691	234	4076
1692	234	4077
1693	234	4082
1694	234	4087
1695	234	4088
1696	234	4092
1697	236	4093
1698	234	4094
1699	234	4095
1700	234	4097
1701	236	4098
1702	236	4101
1703	247	4101
1704	234	4102
1705	234	4103
1706	234	4104
1707	234	4105
1708	234	4106
1709	234	4108
1710	234	4111
1711	234	4112
1712	234	4113
1713	234	4114
1714	234	4116
1715	234	4117
1716	234	4119
1717	234	4120
1718	234	4121
1719	234	4122
1720	234	4123
1721	234	4124
1722	234	4125
1723	234	4126
1724	234	4127
1725	234	4129
1726	234	4130
1727	234	4131
1728	234	4132
1729	234	4133
1730	234	4134
1731	234	4136
1732	234	4137
1733	234	4138
1734	234	4140
1735	234	4141
1736	256	4142
1737	234	4143
1738	234	4144
1739	234	4145
1740	234	4146
1741	234	4147
1742	234	4148
1743	234	4149
1744	234	4150
1745	234	4151
1746	234	4152
1747	234	4153
1748	234	4154
1749	234	4155
1750	234	4156
1751	234	4157
1752	234	4158
1753	234	4160
1754	260	4161
1755	234	4162
1756	262	4163
1757	265	4164
1758	234	4165
1759	265	4166
1760	262	4167
1761	234	4168
1762	265	4169
1763	262	4170
1764	262	4171
1765	262	4173
1766	262	4176
1767	262	4177
1768	234	4178
1769	265	4179
1770	262	4180
1771	265	4181
1772	265	4182
1773	262	4183
1774	265	4185
1775	262	4186
1776	265	4187
1777	262	4188
1778	234	4189
1779	265	4190
1780	262	4191
1781	265	4193
1782	262	4194
1783	265	4196
1784	262	4197
1785	265	4198
1786	234	4199
1787	262	4200
1788	265	4201
1789	234	4202
1790	262	4203
1791	265	4204
1792	262	4205
1793	234	4206
1794	262	4207
1795	262	4208
1796	234	4209
1797	262	4210
1798	265	4211
1799	262	4212
1800	265	4213
1801	262	4214
1802	234	4215
1803	265	4216
1804	262	4217
1805	265	4218
1806	234	4219
1807	265	4221
1808	265	4224
1809	265	4228
1810	262	4229
1811	262	4230
1812	262	4235
1813	234	4236
1814	265	4237
1815	234	4238
1816	265	4239
1817	265	4240
1818	262	4241
1819	234	4242
1820	265	4243
1821	262	4244
1822	265	4245
1823	234	4246
1824	262	4248
1825	234	4249
1826	265	4250
1827	262	4251
1828	265	4252
1829	262	4254
1830	265	4256
1831	273	4258
1832	265	4259
1833	265	4261
1834	273	4262
1835	265	4263
1836	262	4264
1837	273	4265
1838	265	4267
1839	273	4268
1840	265	4269
1841	262	4270
1842	265	4271
1843	262	4273
1844	273	4274
1845	265	4275
1846	262	4276
1847	273	4277
1848	265	4278
1849	262	4279
1850	273	4280
1851	265	4281
1852	265	4282
1853	265	4284
1854	262	4285
1855	273	4286
1856	262	4287
1857	262	4288
1858	273	4289
1859	262	4291
1860	262	4292
1861	262	4294
1862	262	4295
1863	273	4296
1864	265	4297
1865	262	4298
1866	265	4299
1867	273	4300
1868	262	4301
1869	262	4302
1870	273	4303
1871	262	4305
1872	265	4306
1873	273	4307
1874	262	4308
1875	273	4309
1876	265	4310
1877	262	4311
1878	265	4312
1879	265	4315
1880	265	4316
1881	273	4318
1882	265	4319
1883	265	4320
1884	262	4322
1885	265	4323
1886	273	4324
1887	265	4325
1888	265	4326
1889	265	4329
1890	273	4330
1891	262	4332
1892	273	4333
1893	262	4334
1894	273	4336
1895	265	4337
1896	273	4338
1897	273	4341
1898	273	4344
1899	265	4345
1900	273	4346
1901	262	4347
1902	265	4348
1903	262	4351
1904	265	4352
1905	273	4353
1906	262	4355
1907	273	4356
1908	265	4358
1909	262	4359
1910	265	4360
1911	262	4361
1912	273	4362
1913	262	4363
1914	273	4364
1916	265	4367
1917	262	4369
1918	265	4370
1919	262	4371
1920	265	4372
1921	262	4376
1922	262	4377
1923	265	4378
1924	262	4379
1925	273	4380
1926	262	4381
1927	273	4382
1928	262	4383
1929	273	4384
1930	262	4385
1931	265	4386
1932	262	4387
1933	262	4390
\.


--
-- Data for Name: _booster_tracker_tugonlaunch; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._booster_tracker_tugonlaunch (id, boat_id, launch_id) FROM stdin;
1695	235	4046
1696	235	4049
1697	235	4051
1698	237	4053
1699	235	4054
1700	235	4055
1701	235	4056
1702	235	4057
1703	235	4058
1704	235	4060
1705	235	4061
1706	239	4062
1707	235	4065
1708	235	4069
1709	240	4070
1710	241	4073
1711	241	4075
1712	242	4076
1713	242	4077
1714	242	4082
1715	242	4087
1716	245	4088
1717	242	4092
1718	246	4093
1719	242	4094
1720	242	4095
1721	242	4097
1722	246	4098
1723	246	4101
1724	248	4102
1725	249	4103
1726	249	4104
1727	249	4105
1728	249	4106
1729	249	4108
1730	242	4111
1731	242	4112
1732	242	4113
1733	242	4114
1734	242	4116
1735	242	4117
1736	242	4119
1737	253	4120
1738	242	4121
1739	253	4122
1740	253	4123
1741	254	4124
1742	254	4125
1743	253	4126
1744	253	4127
1745	253	4129
1746	253	4130
1747	253	4131
1748	254	4132
1749	253	4133
1750	253	4134
1751	242	4136
1752	242	4137
1753	253	4138
1754	253	4140
1755	242	4141
1756	253	4142
1757	254	4143
1758	242	4144
1759	242	4145
1760	253	4146
1761	242	4147
1762	253	4148
1763	253	4149
1764	253	4150
1765	253	4151
1766	258	4152
1767	253	4153
1768	258	4154
1769	253	4155
1770	258	4156
1771	253	4157
1772	253	4158
1773	253	4160
1774	261	4161
1775	253	4162
1776	263	4163
1777	253	4164
1778	261	4165
1779	253	4166
1780	263	4167
1781	261	4168
1782	253	4169
1783	263	4170
1784	267	4171
1785	267	4173
1786	267	4176
1787	267	4177
1788	261	4178
1790	267	4179
1789	268	4179
1791	267	4180
1792	267	4181
1793	253	4182
1794	263	4183
1795	253	4185
1796	263	4186
1797	268	4187
1798	263	4188
1799	269	4189
1800	253	4190
1801	263	4191
1802	253	4193
1803	263	4194
1804	253	4196
1805	263	4197
1806	270	4198
1807	261	4199
1808	263	4200
1809	270	4201
1810	261	4202
1811	263	4203
1812	270	4204
1813	270	4205
1814	271	4205
1815	261	4206
1816	271	4207
1817	270	4208
1818	261	4209
1819	263	4210
1820	268	4211
1821	270	4212
1822	268	4213
1823	263	4214
1824	261	4215
1825	270	4216
1826	263	4217
1827	268	4218
1828	261	4219
1829	271	4221
1830	271	4224
1831	271	4228
1832	263	4229
1833	271	4230
1834	271	4235
1835	261	4236
1836	271	4237
1837	261	4238
1838	272	4239
1839	271	4240
1840	263	4241
1841	261	4242
1842	268	4243
1843	263	4244
1844	268	4245
1845	261	4246
1846	263	4248
1847	261	4249
1848	271	4250
1849	263	4251
1850	268	4252
1851	263	4254
1852	271	4256
1853	261	4258
1854	274	4259
1855	271	4261
1856	261	4262
1857	271	4263
1858	263	4264
1859	271	4264
1860	261	4265
1861	268	4267
1862	261	4268
1863	271	4269
1864	263	4270
1865	271	4271
1866	263	4273
1867	261	4274
1868	268	4275
1869	263	4276
1870	261	4277
1871	271	4278
1872	263	4279
1873	261	4280
1874	271	4281
1875	276	4282
1876	271	4284
1877	263	4285
1878	261	4286
1879	271	4287
1880	263	4288
1881	261	4289
1882	276	4291
1883	271	4292
1884	276	4294
1885	271	4295
1886	261	4296
1887	271	4297
1888	263	4298
1889	268	4299
1890	261	4300
1891	263	4301
1892	263	4302
1893	277	4303
1894	271	4305
1895	276	4306
1896	277	4307
1897	271	4308
1898	277	4309
1899	276	4310
1900	271	4311
1901	276	4312
1902	271	4315
1903	276	4316
1904	269	4318
1905	271	4319
1906	271	4320
1907	276	4322
1908	271	4323
1909	269	4324
1911	248	4325
1910	276	4325
1912	270	4326
1913	248	4329
1914	269	4330
1915	278	4332
1916	261	4333
1917	248	4334
1918	277	4336
1919	248	4337
1920	269	4338
1921	269	4341
1922	269	4344
1923	248	4345
1924	269	4346
1925	270	4347
1926	248	4348
1927	263	4351
1928	248	4352
1929	279	4353
1930	263	4355
1931	279	4356
1932	268	4358
1933	248	4359
1934	280	4360
1935	248	4361
1936	279	4362
1937	248	4363
1938	279	4364
1940	268	4367
1941	278	4369
1942	268	4370
1943	248	4371
1945	263	4371
1944	248	4372
1947	263	4376
1949	276	4376
1948	248	4377
1950	268	4378
1956	281	4378
1951	248	4379
1952	279	4380
1953	248	4381
1954	279	4382
1955	281	4383
1957	277	4384
1958	281	4385
1959	268	4386
1960	281	4387
1961	281	4390
\.


--
-- Data for Name: _django_admin_log; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) FROM stdin;
1	5		3		5	1	2024-04-02
2	4		3		5	1	2024-04-02
3	3		3		5	1	2024-04-02
4	2		3		5	1	2024-04-02
5	1		3		5	1	2024-04-02
6	10	OLP-A	3		5	1	2024-04-02
7	9	LC-39A	3		5	1	2024-04-02
8	8	SLC-4E	3		5	1	2024-04-02
9	7	SLC-40	3		5	1	2024-04-02
10	6	Omelek Island	3		5	1	2024-04-02
11	92	Crosby Courage	3		3	1	2024-04-02
12	91	Lindsay C	3		3	1	2024-04-02
13	90	Signet Titan III	3		3	1	2024-04-02
14	89	Kimberly C	3		3	1	2024-04-02
15	88	Signet Titan	3		3	1	2024-04-02
16	87	Nicole Foss	3		3	1	2024-04-02
17	86	Crosby Endeavor	3		3	1	2024-04-02
18	85	Crosby Skipper	3		3	1	2024-04-02
19	84	Kurt J Crosby	3		3	1	2024-04-02
20	83	Debra C	3		3	1	2024-04-02
21	82	Bob	3		3	1	2024-04-02
22	81	Zion M Falgout	3		3	1	2024-04-02
23	80	Doug	3		3	1	2024-04-02
24	79	Scorpius	3		3	1	2024-04-02
25	78	Mr. Jonah	3		3	1	2024-04-02
26	77	Lauren Floss	3		3	1	2024-04-02
27	76	Finn Falgout	3		3	1	2024-04-02
28	75	Hollywood	3		3	1	2024-04-02
29	74	Signet Warhorse III	3		3	1	2024-04-02
30	73	Freedom	3		3	1	2024-04-02
31	72	Rachel	3		3	1	2024-04-02
32	71	Hawk	3		3	1	2024-04-02
33	70	Betty R Gambarella	3		3	1	2024-04-02
34	69	Kelly C	3		3	1	2024-04-02
35	68	Pacific Warrior	3		3	1	2024-04-02
36	67	Int. Freedom	3		3	1	2024-04-02
37	66	Elsbeth III	3		3	1	2024-04-02
38	65	T	3		3	1	2024-04-02
39	64	GO Beyond	3		3	1	2024-04-02
40	63	v	3		3	1	2024-04-02
41	62	Z	3		3	1	2024-04-02
42	61	Bob	3		3	1	2024-04-02
43	60	D	3		3	1	2024-04-02
44	59	Doug	3		3	1	2024-04-02
45	58	p	3		3	1	2024-04-02
46	57	Adele Elise	3		3	1	2024-04-02
47	56	J	3		3	1	2024-04-02
48	55	M	3		3	1	2024-04-02
49	54	GO Searcher	3		3	1	2024-04-02
50	53	L	3		3	1	2024-04-02
51	52	u	3		3	1	2024-04-02
52	51	g	3		3	1	2024-04-02
53	50	S	3		3	1	2024-04-02
54	49	John Henry	3		3	1	2024-04-02
55	48	k	3		3	1	2024-04-02
56	47	w	3		3	1	2024-04-02
57	46	H	3		3	1	2024-04-02
58	45	G	3		3	1	2024-04-02
59	44	R	3		3	1	2024-04-02
60	43	B	3		3	1	2024-04-02
61	42	C	3		3	1	2024-04-02
62	41	y	3		3	1	2024-04-02
63	40	K	3		3	1	2024-04-02
64	39	W	3		3	1	2024-04-02
65	38	f	3		3	1	2024-04-02
66	37	i	3		3	1	2024-04-02
67	36	c	3		3	1	2024-04-02
68	35	a	3		3	1	2024-04-02
69	34	P	3		3	1	2024-04-02
70	33	m	3		3	1	2024-04-02
71	32	o	3		3	1	2024-04-02
72	31	d	3		3	1	2024-04-02
73	30	r	3		3	1	2024-04-02
74	29	F	3		3	1	2024-04-02
75	28	.	3		3	1	2024-04-02
76	27	n	3		3	1	2024-04-02
77	26	NRC Quest	3		3	1	2024-04-02
78	25	I	3		3	1	2024-04-02
79	24	 	3		3	1	2024-04-02
80	23	h	3		3	1	2024-04-02
81	22	t	3		3	1	2024-04-02
82	21	e	3		3	1	2024-04-02
83	20	b	3		3	1	2024-04-02
84	19	s	3		3	1	2024-04-02
85	18	l	3		3	1	2024-04-02
86	17	E	3		3	1	2024-04-02
87	16	GO Quest	3		3	1	2024-04-02
88	15	A	3		3	1	2024-04-02
89	14	/	3		3	1	2024-04-02
90	13	N	3		3	1	2024-04-02
91	12	GO Beyond	3		3	1	2024-04-02
92	11	Doug	3		3	1	2024-04-02
93	10	Bob	3		3	1	2024-04-02
94	9	Hos Briarwood	3		3	1	2024-04-02
95	8	Shelia Bordelon	3		3	1	2024-04-02
96	7	NRC Quest	3		3	1	2024-04-02
97	6	GO Ms. Chief	3		3	1	2024-04-02
98	5	GO Ms. Tree	3		3	1	2024-04-02
99	4	GO Navigator	3		3	1	2024-04-02
100	3	GO Pursuit	3		3	1	2024-04-02
101	2	Mr. Steven	3		3	1	2024-04-02
102	1	GO Searcher	3		3	1	2024-04-02
103	15	OLP-A	3		5	1	2024-04-02
104	14	LC-39A	3		5	1	2024-04-02
105	13	SLC-4E	3		5	1	2024-04-02
106	12	SLC-40	3		5	1	2024-04-02
107	11	Omelek Island	3		5	1	2024-04-02
108	1346	Starlink Group 7-18	3		6	1	2024-04-02
109	1345	Starlink Group 6-45	3		6	1	2024-04-02
110	1344	Eutelsat 36D	3		6	1	2024-04-02
111	1343	Starlink Group 6-46	3		6	1	2024-04-02
112	1342	Starlink Group 6-42	3		6	1	2024-04-02
113	1341	CRS-30	3		6	1	2024-04-02
114	1340	Starlink Group 7-16, USA-350, and USA-351	3		6	1	2024-04-02
115	1339	Starlink Group 6-44	3		6	1	2024-04-02
116	1338	Starship Flight 3	3		6	1	2024-04-02
117	1337	Starlink Group 7-17	3		6	1	2024-04-02
118	1336	Starlink Group 6-43	3		6	1	2024-04-02
119	1335	Starlink Group 6-41	3		6	1	2024-04-02
120	1334	Transporter-10	3		6	1	2024-04-02
121	1333	Crew-8 (Crew Dragon C206-5 Endeavour)	3		6	1	2024-04-02
122	1332	Starlink Group 6-40	3		6	1	2024-04-02
123	1331	Starlink Group 6-39	3		6	1	2024-04-02
124	1330	Starlink Group 7-15	3		6	1	2024-04-02
125	1329	Merah Putih 2	3		6	1	2024-04-02
126	1328	Starlink Group 7-14	3		6	1	2024-04-02
127	1327	Nova C (IM-1)	3		6	1	2024-04-02
128	1326	USSF-124	3		6	1	2024-04-02
129	1325	Starlink Group 7-13	3		6	1	2024-04-02
130	1324	PACE	3		6	1	2024-04-02
131	1323	NG-20	3		6	1	2024-04-02
132	1322	Starlink Group 7-12	3		6	1	2024-04-02
133	1321	Starlink Group 6-38	3		6	1	2024-04-02
134	1320	Starlink Group 7-11	3		6	1	2024-04-02
135	1319	Axiom-3	3		6	1	2024-04-02
136	1318	Starlink Group 6-37	3		6	1	2024-04-02
137	1317	Starlink Group 7-10	3		6	1	2024-04-02
138	1316	Starlink Group 6-35	3		6	1	2024-04-02
139	1315	Ovzon-3	3		6	1	2024-04-02
140	1314	Starlink Group 7-9	3		6	1	2024-04-02
141	1313	Starlink Group 6-36	3		6	1	2024-04-02
142	1312	USSF-52	3		6	1	2024-04-02
143	1311	SARah-2 and SARah-3	3		6	1	2024-04-02
144	1310	Starlink Group 6-32	3		6	1	2024-04-02
145	1309	Starlink Group 6-34	3		6	1	2024-04-02
146	1308	Starlink Group 7-8	3		6	1	2024-04-02
147	1307	Starlink Group 6-33	3		6	1	2024-04-02
148	1306	Starlink Group 6-31	3		6	1	2024-04-02
149	1305	425 Project Flight 1 & others	3		6	1	2024-04-02
150	1304	Starlink Group 6-30	3		6	1	2024-04-02
151	1303	Starlink Group 6-29	3		6	1	2024-04-02
152	1302	Starlink Group 7-7	3		6	1	2024-04-02
153	1301	Starship Flight 2	3		6	1	2024-04-02
154	1300	Starlink Group 6-28	3		6	1	2024-04-02
155	1299	O3b mPOWER 5 & 6	3		6	1	2024-04-02
156	1298	Transporter-9	3		6	1	2024-04-02
157	1297	SpaceX CRS-29 (Dragon C211-2)	3		6	1	2024-04-02
158	1296	Starlink Group 6-27	3		6	1	2024-04-02
159	1295	Starlink Group 6-26	3		6	1	2024-04-02
160	1294	Starlink Group 6-25	3		6	1	2024-04-02
161	1293	Starlink Group 7-6	3		6	1	2024-04-02
162	1292	Starlink Group 6-24	3		6	1	2024-04-02
163	1291	Starlink Group 7-5	3		6	1	2024-04-02
164	1290	Starlink Group 6-23	3		6	1	2024-04-02
165	1289	Starlink Group 6-22	3		6	1	2024-04-02
166	1288	Psyche	3		6	1	2024-04-02
167	1287	Starlink Group 7-4	3		6	1	2024-04-02
168	1286	Starlink Group 6-21	3		6	1	2024-04-02
169	1285	Starlink Group 6-19	3		6	1	2024-04-02
170	1284	Starlink Group 7-3	3		6	1	2024-04-02
171	1283	Starlink Group 6-18	3		6	1	2024-04-02
172	1282	Starlink Group 6-17	3		6	1	2024-04-02
173	1281	Starlink Group 6-16	3		6	1	2024-04-02
174	1280	Starlink Group 7-2	3		6	1	2024-04-02
175	1279	Starlink Group 6-14	3		6	1	2024-04-02
176	1278	Starlink Group 6-12	3		6	1	2024-04-02
177	1277	SDA T&T Tranche 0B	3		6	1	2024-04-02
178	1276	Starlink Group 6-13	3		6	1	2024-04-02
179	1275	Starlink Group 6-11	3		6	1	2024-04-02
180	1274	Crew-7 (Crew Dragon C210-3 Endurance)	3		6	1	2024-04-02
181	1273	Starlink Group 7-1	3		6	1	2024-04-02
182	1272	Starlink Group 6-10	3		6	1	2024-04-02
183	1271	Starlink Group 6-9	3		6	1	2024-04-02
184	1270	Starlink Group 6-20	3		6	1	2024-04-02
185	1269	Starlink Group 6-8	3		6	1	2024-04-02
186	1268	Galaxy 37	3		6	1	2024-04-02
187	1267	EchoStar 24 / Jupiter 3	3		6	1	2024-04-02
188	1266	Starlink Group 6-7	3		6	1	2024-04-02
189	1265	Starlink Group 6-6	3		6	1	2024-04-02
190	1264	Starlink Group 6-15	3		6	1	2024-04-02
191	1263	Starlink Group 5-15	3		6	1	2024-04-02
192	1262	Starlink Group 6-5	3		6	1	2024-04-02
193	1261	Starlink Group 5-13	3		6	1	2024-04-02
194	1260	Euclid Telescope	3		6	1	2024-04-02
195	1259	Starlink Group 5-12	3		6	1	2024-04-02
196	1258	Starlink Group 5-7	3		6	1	2024-04-02
197	1257	Satria	3		6	1	2024-04-02
198	1256	Transporter-8 (72 payloads)	3		6	1	2024-04-02
199	1255	Starlink Group 5-11	3		6	1	2024-04-02
200	1254	SpaceX CRS-28 (Dragon C208-4)	3		6	1	2024-04-02
201	1253	Starlink Group 6-4 (22 satellites)	3		6	1	2024-04-02
202	1252	Starlink Group 2-10 (52 satellites)	3		6	1	2024-04-02
203	1251	Arabsat 7B (Badr-8)	3		6	1	2024-04-02
204	1250	Axiom-2 (Crew Dragon C212-2 Freedom)	3		6	1	2024-04-02
205	1249	Iridium 9 and OneWeb 19	3		6	1	2024-04-02
206	1248	Starlink Group 6-3 (22 satellites)	3		6	1	2024-04-02
207	1247	Starlink Group 5-9 (56 satellites)	3		6	1	2024-04-02
208	20	OLP-A	3		5	1	2024-04-02
209	19	LC-39A	3		5	1	2024-04-02
210	18	SLC-4E	3		5	1	2024-04-02
211	17	SLC-40	3		5	1	2024-04-02
212	16	Omelek Island	3		5	1	2024-04-02
213	7	None	1	[{"added": {}}]	7	1	2024-04-02
214	1673	Starship Flight 3	2	[{"changed": {"name": "stage and recovery", "object": "StageAndRecovery object (1732)", "fields": ["Landing zone", "Method"]}}]	6	1	2024-04-02
215	25	OLP-A	3		5	1	2024-04-02
216	24	LC-39A	3		5	1	2024-04-02
217	23	SLC-4E	3		5	1	2024-04-02
218	22	SLC-40	3		5	1	2024-04-02
219	21	Omelek Island	3		5	1	2024-04-02
220	139	Crosby Courage	3		3	1	2024-04-02
221	138	Lindsay C	3		3	1	2024-04-02
222	137	Signet Titan III	3		3	1	2024-04-02
223	136	Kimberly C	3		3	1	2024-04-02
224	135	Signet Titan	3		3	1	2024-04-02
225	134	GO Beyond	3		3	1	2024-04-02
226	133	Nicole Foss	3		3	1	2024-04-02
227	132	GO Beyond	3		3	1	2024-04-02
228	131	Crosby Endeavor	3		3	1	2024-04-02
229	130	Crosby Skipper	3		3	1	2024-04-02
230	129	Kurt J Crosby	3		3	1	2024-04-02
231	128	Debra C	3		3	1	2024-04-02
232	127	Bob	3		3	1	2024-04-02
233	126	Zion M Falgout	3		3	1	2024-04-02
234	125	Doug	3		3	1	2024-04-02
235	124	Bob	3		3	1	2024-04-02
236	123	Bob	3		3	1	2024-04-02
237	122	Doug	3		3	1	2024-04-02
238	121	Doug	3		3	1	2024-04-02
239	120	Scorpius	3		3	1	2024-04-02
240	119	Adele Elise	3		3	1	2024-04-02
241	118	Hos Briarwood	3		3	1	2024-04-02
242	117	Mr. Jonah	3		3	1	2024-04-02
243	116	Shelia Bordelon	3		3	1	2024-04-02
244	115	GO Searcher	3		3	1	2024-04-02
245	114	NRC Quest	3		3	1	2024-04-02
246	113	Lauren Floss	3		3	1	2024-04-02
247	112	Finn Falgout	3		3	1	2024-04-02
248	111	GO Ms. Chief	3		3	1	2024-04-02
249	110	GO Ms. Tree	3		3	1	2024-04-02
250	109	GO Navigator	3		3	1	2024-04-02
251	108	Hollywood	3		3	1	2024-04-02
252	107	Signet Warhorse III	3		3	1	2024-04-02
253	106	John Henry	3		3	1	2024-04-02
254	105	Freedom	3		3	1	2024-04-02
255	104	Rachel	3		3	1	2024-04-02
256	103	GO Pursuit	3		3	1	2024-04-02
257	102	Mr. Steven	3		3	1	2024-04-02
258	101	Hawk	3		3	1	2024-04-02
259	100	Betty R Gambarella	3		3	1	2024-04-02
260	99	Kelly C	3		3	1	2024-04-02
261	98	Pacific Warrior	3		3	1	2024-04-02
262	97	GO Searcher	3		3	1	2024-04-02
263	96	Int. Freedom	3		3	1	2024-04-02
264	95	NRC Quest	3		3	1	2024-04-02
265	94	Elsbeth III	3		3	1	2024-04-02
266	93	GO Quest	3		3	1	2024-04-02
267	7	None	3		7	1	2024-04-02
268	6	A Shortfall of Gravitas	3		7	1	2024-04-02
269	5	Landing Zone 4	3		7	1	2024-04-02
270	4	Landing Zone 2	3		7	1	2024-04-02
271	3	Landing Zone 1	3		7	1	2024-04-02
272	2	Of Course I Still Love You	3		7	1	2024-04-02
273	1	Just Read the Instructions	3		7	1	2024-04-02
274	15	Ballistic lunar transfer (BLT)	3		4	1	2024-04-02
275	14	Molniya	3		4	1	2024-04-02
276	13	Sun-Earth L2	3		4	1	2024-04-02
277	12	Geostationary Earth Orbit	3		4	1	2024-04-02
278	11	Ballistic lunar transfer	3		4	1	2024-04-02
279	10	Sub-orbital	3		4	1	2024-04-02
280	9	Low-Earth Orbit/Medium-Earth Orbit	3		4	1	2024-04-02
281	8	Medium-Earth Orbit	3		4	1	2024-04-02
282	7	High-Earth Orbit	3		4	1	2024-04-02
283	6	Heliocentric	3		4	1	2024-04-02
284	5	Sun-Synchronous Orbit	3		4	1	2024-04-02
285	4	Sun–Earth L1	3		4	1	2024-04-02
286	3	Geostationary Transfer Orbit	3		4	1	2024-04-02
287	2	Polar Low-Earth Orbit	3		4	1	2024-04-02
288	1	Low-Earth Orbit	3		4	1	2024-04-02
289	90	28	3		2	1	2024-04-02
290	89	25	3		2	1	2024-04-02
291	88	24	3		2	1	2024-04-02
292	87	10	3		2	1	2024-04-02
293	86	1083	3		2	1	2024-04-02
294	85	1082	3		2	1	2024-04-02
295	84	1084	3		2	1	2024-04-02
296	83	9	3		2	1	2024-04-02
297	82	1079	3		2	1	2024-04-02
298	81	1081	3		2	1	2024-04-02
299	80	1074	3		2	1	2024-04-02
300	79	1080	3		2	1	2024-04-02
301	78	1068	3		2	1	2024-04-02
302	77	7	3		2	1	2024-04-02
303	76	1078	3		2	1	2024-04-02
304	75	1075	3		2	1	2024-04-02
305	74	1070	3		2	1	2024-04-02
306	73	1076	3		2	1	2024-04-02
307	72	1065	3		2	1	2024-04-02
308	71	1064	3		2	1	2024-04-02
309	70	1066	3		2	1	2024-04-02
310	69	1077	3		2	1	2024-04-02
311	68	1073	3		2	1	2024-04-02
312	67	1071	3		2	1	2024-04-02
313	66	1069	3		2	1	2024-04-02
314	65	1067	3		2	1	2024-04-02
315	64	1063	3		2	1	2024-04-02
316	63	1061	3		2	1	2024-04-02
317	62	1062	3		2	1	2024-04-02
318	61	1060	3		2	1	2024-04-02
319	60	1058	3		2	1	2024-04-02
320	59	1059	3		2	1	2024-04-02
321	58	1057	3		2	1	2024-04-02
322	57	1056	3		2	1	2024-04-02
323	56	1053	3		2	1	2024-04-02
324	55	1052	3		2	1	2024-04-02
325	54	1055	3		2	1	2024-04-02
326	53	1051	3		2	1	2024-04-02
327	52	1054	3		2	1	2024-04-02
328	51	1050	3		2	1	2024-04-02
329	50	1049	3		2	1	2024-04-02
330	49	1048	3		2	1	2024-04-02
331	48	1047	3		2	1	2024-04-02
332	47	1046	3		2	1	2024-04-02
333	46	1045	3		2	1	2024-04-02
334	45	1044	3		2	1	2024-04-02
335	44	1033	3		2	1	2024-04-02
336	43	1043	3		2	1	2024-04-02
337	42	1042	3		2	1	2024-04-02
338	41	1041	3		2	1	2024-04-02
339	40	1040	3		2	1	2024-04-02
340	39	1038	3		2	1	2024-04-02
341	38	1039	3		2	1	2024-04-02
342	37	1037	3		2	1	2024-04-02
343	36	1036	3		2	1	2024-04-02
344	35	1035	3		2	1	2024-04-02
345	34	1034	3		2	1	2024-04-02
346	33	1032	3		2	1	2024-04-02
347	32	1030	3		2	1	2024-04-02
348	31	1031	3		2	1	2024-04-02
349	30	1029	3		2	1	2024-04-02
350	29	1028	3		2	1	2024-04-02
351	28	1026	3		2	1	2024-04-02
352	27	1025	3		2	1	2024-04-02
353	26	1024	3		2	1	2024-04-02
354	25	1023	3		2	1	2024-04-02
355	24	1022	3		2	1	2024-04-02
356	23	1021	3		2	1	2024-04-02
357	22	1020	3		2	1	2024-04-02
358	21	1017	3		2	1	2024-04-02
359	20	1019	3		2	1	2024-04-02
360	19	1018	3		2	1	2024-04-02
361	18	1016	3		2	1	2024-04-02
362	17	1015	3		2	1	2024-04-02
363	16	1014	3		2	1	2024-04-02
364	15	1013	3		2	1	2024-04-02
365	14	1012	3		2	1	2024-04-02
366	13	1010	3		2	1	2024-04-02
367	12	1011	3		2	1	2024-04-02
368	11	1008	3		2	1	2024-04-02
369	10	1007	3		2	1	2024-04-02
370	9	1006	3		2	1	2024-04-02
371	8	1005	3		2	1	2024-04-02
372	7	1004	3		2	1	2024-04-02
373	6	1003	3		2	1	2024-04-02
374	5	0007	3		2	1	2024-04-02
375	4	0006	3		2	1	2024-04-02
376	3	0005	3		2	1	2024-04-02
377	2	0004	3		2	1	2024-04-02
378	1	0003	3		2	1	2024-04-02
379	4	Falcon 1	3		1	1	2024-04-02
380	3	Starship	3		1	1	2024-04-02
381	2	Falcon Heavy	3		1	1	2024-04-02
382	1	Falcon 9	3		1	1	2024-04-02
383	30	OLP-A	3		5	1	2024-04-02
384	29	LC-39A	3		5	1	2024-04-02
385	28	SLC-4E	3		5	1	2024-04-02
386	27	SLC-40	3		5	1	2024-04-02
387	26	Omelek Island	3		5	1	2024-04-02
388	35	OLP-A	3		5	1	2024-04-02
389	34	LC-39A	3		5	1	2024-04-02
390	33	SLC-4E	3		5	1	2024-04-02
391	32	SLC-40	3		5	1	2024-04-02
392	31	Omelek Island	3		5	1	2024-04-02
393	40	OLP-A	3		5	1	2024-04-02
394	39	LC-39A	3		5	1	2024-04-02
395	38	SLC-4E	3		5	1	2024-04-02
396	37	SLC-40	3		5	1	2024-04-02
397	36	Omelek Island	3		5	1	2024-04-02
398	45	OLP-A	3		5	1	2024-04-02
399	44	LC-39A	3		5	1	2024-04-02
400	43	SLC-4E	3		5	1	2024-04-02
401	42	SLC-40	3		5	1	2024-04-02
402	41	Omelek Island	3		5	1	2024-04-02
403	50	OLP-A	3		5	1	2024-04-02
404	49	LC-39A	3		5	1	2024-04-02
405	48	SLC-4E	3		5	1	2024-04-02
406	47	SLC-40	3		5	1	2024-04-02
407	46	Omelek Island	3		5	1	2024-04-02
408	55	OLP-A	3		5	1	2024-04-02
409	54	LC-39A	3		5	1	2024-04-02
410	53	SLC-4E	3		5	1	2024-04-02
411	52	SLC-40	3		5	1	2024-04-02
412	51	Omelek Island	3		5	1	2024-04-02
413	180	S28	3		2	1	2024-04-02
414	179	S25	3		2	1	2024-04-02
415	178	S24	3		2	1	2024-04-02
416	173	B9	3		2	1	2024-04-02
417	167	B7	3		2	1	2024-04-02
418	174	B1084	3		2	1	2024-04-02
419	176	B1083	3		2	1	2024-04-02
420	175	B1082	3		2	1	2024-04-02
421	171	B1081	3		2	1	2024-04-02
422	169	B1080	3		2	1	2024-04-02
423	172	B1079	3		2	1	2024-04-02
424	166	B1078	3		2	1	2024-04-02
425	159	B1077	3		2	1	2024-04-02
426	163	B1076	3		2	1	2024-04-02
427	165	B1075	3		2	1	2024-04-02
428	170	B1074	3		2	1	2024-04-02
429	158	B1073	3		2	1	2024-04-02
430	157	B1071	3		2	1	2024-04-02
431	164	B1070	3		2	1	2024-04-02
432	156	B1069	3		2	1	2024-04-02
433	168	B1068	3		2	1	2024-04-02
434	155	B1067	3		2	1	2024-04-02
435	160	B1066	3		2	1	2024-04-02
436	162	B1065	3		2	1	2024-04-02
437	161	B1064	3		2	1	2024-04-02
438	154	B1063	3		2	1	2024-04-02
439	152	B1062	3		2	1	2024-04-02
440	153	B1061	3		2	1	2024-04-02
441	151	B1060	3		2	1	2024-04-02
442	149	B1059	3		2	1	2024-04-02
443	150	B1058	3		2	1	2024-04-02
444	148	B1057	3		2	1	2024-04-02
445	147	B1056	3		2	1	2024-04-02
446	144	B1055	3		2	1	2024-04-02
447	142	B1054	3		2	1	2024-04-02
448	146	B1053	3		2	1	2024-04-02
449	145	B1052	3		2	1	2024-04-02
450	143	B1051	3		2	1	2024-04-02
451	141	B1050	3		2	1	2024-04-02
452	140	B1049	3		2	1	2024-04-02
453	139	B1048	3		2	1	2024-04-02
454	138	B1047	3		2	1	2024-04-02
455	137	B1046	3		2	1	2024-04-02
456	136	B1045	3		2	1	2024-04-02
457	135	B1044	3		2	1	2024-04-02
458	133	B1043	3		2	1	2024-04-02
459	132	B1042	3		2	1	2024-04-02
460	131	B1041	3		2	1	2024-04-02
461	130	B1040	3		2	1	2024-04-02
462	128	B1039	3		2	1	2024-04-02
463	129	B1038	3		2	1	2024-04-02
464	127	B1037	3		2	1	2024-04-02
465	126	B1036	3		2	1	2024-04-02
466	125	B1035	3		2	1	2024-04-02
467	124	B1034	3		2	1	2024-04-02
468	134	B1033	3		2	1	2024-04-02
469	123	B1032	3		2	1	2024-04-02
470	121	B1031	3		2	1	2024-04-02
471	122	B1030	3		2	1	2024-04-02
472	120	B1029	3		2	1	2024-04-02
473	119	B1028	3		2	1	2024-04-02
474	118	B1026	3		2	1	2024-04-02
475	117	B1025	3		2	1	2024-04-02
476	116	B1024	3		2	1	2024-04-02
477	115	B1023	3		2	1	2024-04-02
478	114	B1022	3		2	1	2024-04-02
479	113	B1021	3		2	1	2024-04-02
480	112	B1020	3		2	1	2024-04-02
481	110	B1019	3		2	1	2024-04-02
482	109	B1018	3		2	1	2024-04-02
483	111	B1017	3		2	1	2024-04-02
484	108	B1016	3		2	1	2024-04-02
485	107	B1015	3		2	1	2024-04-02
486	106	B1014	3		2	1	2024-04-02
487	105	B1013	3		2	1	2024-04-02
488	104	B1012	3		2	1	2024-04-02
489	102	B1011	3		2	1	2024-04-02
490	103	B1010	3		2	1	2024-04-02
491	101	B1008	3		2	1	2024-04-02
492	100	B1007	3		2	1	2024-04-02
493	99	B1006	3		2	1	2024-04-02
494	98	B1005	3		2	1	2024-04-02
495	97	B1004	3		2	1	2024-04-02
496	96	B1003	3		2	1	2024-04-02
497	177	B10	3		2	1	2024-04-02
498	95	B0007	3		2	1	2024-04-02
499	94	B0006	3		2	1	2024-04-02
500	93	B0005	3		2	1	2024-04-02
501	92	B0004	3		2	1	2024-04-02
502	91	B0003	3		2	1	2024-04-02
503	186	Crosby Courage	3		3	1	2024-04-02
504	185	Lindsay C	3		3	1	2024-04-02
505	184	Signet Titan III	3		3	1	2024-04-02
506	183	Kimberly C	3		3	1	2024-04-02
507	182	Signet Titan	3		3	1	2024-04-02
508	181	GO Beyond	3		3	1	2024-04-02
509	180	Nicole Foss	3		3	1	2024-04-02
510	179	GO Beyond	3		3	1	2024-04-02
511	178	Crosby Endeavor	3		3	1	2024-04-02
512	177	Crosby Skipper	3		3	1	2024-04-02
513	176	Kurt J Crosby	3		3	1	2024-04-02
514	175	Debra C	3		3	1	2024-04-02
515	174	Bob	3		3	1	2024-04-02
516	173	Zion M Falgout	3		3	1	2024-04-02
517	172	Doug	3		3	1	2024-04-02
518	171	Bob	3		3	1	2024-04-02
519	170	Bob	3		3	1	2024-04-02
520	169	Doug	3		3	1	2024-04-02
521	168	Doug	3		3	1	2024-04-02
522	167	Scorpius	3		3	1	2024-04-02
523	166	Adele Elise	3		3	1	2024-04-02
524	165	Hos Briarwood	3		3	1	2024-04-02
525	164	Mr. Jonah	3		3	1	2024-04-02
526	163	Shelia Bordelon	3		3	1	2024-04-02
527	162	GO Searcher	3		3	1	2024-04-02
528	161	NRC Quest	3		3	1	2024-04-02
529	160	Lauren Floss	3		3	1	2024-04-02
530	159	Finn Falgout	3		3	1	2024-04-02
531	158	GO Ms. Chief	3		3	1	2024-04-02
532	157	GO Ms. Tree	3		3	1	2024-04-02
533	156	GO Navigator	3		3	1	2024-04-02
534	155	Hollywood	3		3	1	2024-04-02
535	154	Signet Warhorse III	3		3	1	2024-04-02
536	153	John Henry	3		3	1	2024-04-02
537	152	Freedom	3		3	1	2024-04-02
538	151	Rachel	3		3	1	2024-04-02
539	150	GO Pursuit	3		3	1	2024-04-02
540	149	Mr. Steven	3		3	1	2024-04-02
541	148	Hawk	3		3	1	2024-04-02
542	147	Betty R Gambarella	3		3	1	2024-04-02
543	146	Kelly C	3		3	1	2024-04-02
544	145	Pacific Warrior	3		3	1	2024-04-02
545	144	GO Searcher	3		3	1	2024-04-02
546	143	Int. Freedom	3		3	1	2024-04-02
547	142	NRC Quest	3		3	1	2024-04-02
548	141	Elsbeth III	3		3	1	2024-04-02
549	140	GO Quest	3		3	1	2024-04-02
550	60	OLP-A	3		5	1	2024-04-07
551	59	LC-39A	3		5	1	2024-04-07
552	58	SLC-4E	3		5	1	2024-04-07
553	57	SLC-40	3		5	1	2024-04-07
554	56	Omelek Island	3		5	1	2024-04-07
555	270	S28	3		2	1	2024-04-07
556	269	S25	3		2	1	2024-04-07
557	268	S24	3		2	1	2024-04-07
558	267	B10	3		2	1	2024-04-07
559	266	B1083	3		2	1	2024-04-07
560	265	B1082	3		2	1	2024-04-07
561	264	B1084	3		2	1	2024-04-07
562	263	B9	3		2	1	2024-04-07
563	262	B1079	3		2	1	2024-04-07
564	261	B1081	3		2	1	2024-04-07
565	260	B1074	3		2	1	2024-04-07
566	259	B1080	3		2	1	2024-04-07
567	258	B1068	3		2	1	2024-04-07
568	257	B7	3		2	1	2024-04-07
569	256	B1078	3		2	1	2024-04-07
570	255	B1075	3		2	1	2024-04-07
571	254	B1070	3		2	1	2024-04-07
572	253	B1076	3		2	1	2024-04-07
573	252	B1065	3		2	1	2024-04-07
574	251	B1064	3		2	1	2024-04-07
575	250	B1066	3		2	1	2024-04-07
576	249	B1077	3		2	1	2024-04-07
577	248	B1073	3		2	1	2024-04-07
578	247	B1071	3		2	1	2024-04-07
579	246	B1069	3		2	1	2024-04-07
580	245	B1067	3		2	1	2024-04-07
581	244	B1063	3		2	1	2024-04-07
582	243	B1061	3		2	1	2024-04-07
583	242	B1062	3		2	1	2024-04-07
584	241	B1060	3		2	1	2024-04-07
585	240	B1058	3		2	1	2024-04-07
586	239	B1059	3		2	1	2024-04-07
587	238	B1057	3		2	1	2024-04-07
588	237	B1056	3		2	1	2024-04-07
589	236	B1053	3		2	1	2024-04-07
590	235	B1052	3		2	1	2024-04-07
591	234	B1055	3		2	1	2024-04-07
592	233	B1051	3		2	1	2024-04-07
593	232	B1054	3		2	1	2024-04-07
594	231	B1050	3		2	1	2024-04-07
595	230	B1049	3		2	1	2024-04-07
596	229	B1048	3		2	1	2024-04-07
597	228	B1047	3		2	1	2024-04-07
598	227	B1046	3		2	1	2024-04-07
599	226	B1045	3		2	1	2024-04-07
600	225	B1044	3		2	1	2024-04-07
601	224	B1033	3		2	1	2024-04-07
602	223	B1043	3		2	1	2024-04-07
603	222	B1042	3		2	1	2024-04-07
604	221	B1041	3		2	1	2024-04-07
605	220	B1040	3		2	1	2024-04-07
606	219	B1038	3		2	1	2024-04-07
607	218	B1039	3		2	1	2024-04-07
608	217	B1037	3		2	1	2024-04-07
609	216	B1036	3		2	1	2024-04-07
610	215	B1035	3		2	1	2024-04-07
611	214	B1034	3		2	1	2024-04-07
612	213	B1032	3		2	1	2024-04-07
613	212	B1030	3		2	1	2024-04-07
614	211	B1031	3		2	1	2024-04-07
615	210	B1029	3		2	1	2024-04-07
616	209	B1028	3		2	1	2024-04-07
617	208	B1026	3		2	1	2024-04-07
618	207	B1025	3		2	1	2024-04-07
619	206	B1024	3		2	1	2024-04-07
620	205	B1023	3		2	1	2024-04-07
621	204	B1022	3		2	1	2024-04-07
622	203	B1021	3		2	1	2024-04-07
623	202	B1020	3		2	1	2024-04-07
624	201	B1017	3		2	1	2024-04-07
625	200	B1019	3		2	1	2024-04-07
626	199	B1018	3		2	1	2024-04-07
627	198	B1016	3		2	1	2024-04-07
628	197	B1015	3		2	1	2024-04-07
629	196	B1014	3		2	1	2024-04-07
630	195	B1013	3		2	1	2024-04-07
631	194	B1012	3		2	1	2024-04-07
632	193	B1010	3		2	1	2024-04-07
633	192	B1011	3		2	1	2024-04-07
634	191	B1008	3		2	1	2024-04-07
635	190	B1007	3		2	1	2024-04-07
636	189	B1006	3		2	1	2024-04-07
637	188	B1005	3		2	1	2024-04-07
638	187	B1004	3		2	1	2024-04-07
639	186	B1003	3		2	1	2024-04-07
640	185	B0007	3		2	1	2024-04-07
641	184	B0006	3		2	1	2024-04-07
642	183	B0005	3		2	1	2024-04-07
643	182	B0004	3		2	1	2024-04-07
644	181	B0003	3		2	1	2024-04-07
645	13	A Shortfall of Gravitas	3		7	1	2024-04-07
646	12	Landing Zone 4	3		7	1	2024-04-07
647	11	Landing Zone 2	3		7	1	2024-04-07
648	10	Landing Zone 1	3		7	1	2024-04-07
649	9	Of Course I Still Love You	3		7	1	2024-04-07
650	8	Just Read the Instructions	3		7	1	2024-04-07
651	233	Crosby Courage	3		3	1	2024-04-07
652	232	Lindsay C	3		3	1	2024-04-07
653	231	Signet Titan III	3		3	1	2024-04-07
654	230	Kimberly C	3		3	1	2024-04-07
655	229	Signet Titan	3		3	1	2024-04-07
656	228	GO Beyond	3		3	1	2024-04-07
657	227	Nicole Foss	3		3	1	2024-04-07
658	226	GO Beyond	3		3	1	2024-04-07
659	225	Crosby Endeavor	3		3	1	2024-04-07
660	224	Crosby Skipper	3		3	1	2024-04-07
661	223	Kurt J Crosby	3		3	1	2024-04-07
662	222	Debra C	3		3	1	2024-04-07
663	221	Bob	3		3	1	2024-04-07
664	220	Zion M Falgout	3		3	1	2024-04-07
665	219	Doug	3		3	1	2024-04-07
666	218	Bob	3		3	1	2024-04-07
667	217	Bob	3		3	1	2024-04-07
668	216	Doug	3		3	1	2024-04-07
669	215	Doug	3		3	1	2024-04-07
670	214	Scorpius	3		3	1	2024-04-07
671	213	Adele Elise	3		3	1	2024-04-07
672	212	Hos Briarwood	3		3	1	2024-04-07
673	211	Mr. Jonah	3		3	1	2024-04-07
674	210	Shelia Bordelon	3		3	1	2024-04-07
675	209	GO Searcher	3		3	1	2024-04-07
676	208	NRC Quest	3		3	1	2024-04-07
677	207	Lauren Floss	3		3	1	2024-04-07
678	206	Finn Falgout	3		3	1	2024-04-07
679	205	GO Ms. Chief	3		3	1	2024-04-07
680	204	GO Ms. Tree	3		3	1	2024-04-07
681	203	GO Navigator	3		3	1	2024-04-07
682	202	Hollywood	3		3	1	2024-04-07
683	201	Signet Warhorse III	3		3	1	2024-04-07
684	200	John Henry	3		3	1	2024-04-07
685	199	Freedom	3		3	1	2024-04-07
686	198	Rachel	3		3	1	2024-04-07
687	197	GO Pursuit	3		3	1	2024-04-07
688	196	Mr. Steven	3		3	1	2024-04-07
689	195	Hawk	3		3	1	2024-04-07
690	194	Betty R Gambarella	3		3	1	2024-04-07
691	193	Kelly C	3		3	1	2024-04-07
692	192	Pacific Warrior	3		3	1	2024-04-07
693	191	GO Searcher	3		3	1	2024-04-07
694	190	Int. Freedom	3		3	1	2024-04-07
695	189	NRC Quest	3		3	1	2024-04-07
696	188	Elsbeth III	3		3	1	2024-04-07
697	187	GO Quest	3		3	1	2024-04-07
698	4050	TürkmenÄlem 52°E (MonacoSAT)	2	[{"changed": {"fields": ["Name"]}}]	6	1	2024-04-08
699	4283	EchoStar 24 (Jupiter 3)	2	[{"changed": {"fields": ["Name"]}}]	6	1	2024-04-08
700	4254	Intelsat 40e TEMPO	2	[{"changed": {"fields": ["Name"]}}]	6	1	2024-04-08
701	4247	OneWeb Flight #17	2	[{"changed": {"fields": ["Name"]}}]	6	1	2024-04-08
702	4233	OneWeb Flight #16	2	[{"changed": {"fields": ["Name"]}}]	6	1	2024-04-08
703	4225	OneWeb Flight #15	2	[{"changed": {"fields": ["Name"]}}]	6	1	2024-04-08
704	4113	JCSat-18 (Kacific 1)	2	[{"changed": {"fields": ["Name"]}}]	6	1	2024-04-08
705	4095	Telstar 18V (Apstar-5C)	2	[{"changed": {"fields": ["Name"]}}]	6	1	2024-04-08
706	4076	SES-11 (EchoStar 105)	2	[{"changed": {"fields": ["Name"]}}]	6	1	2024-04-08
707	4058	ABS-2A (Eutelsat 117 West B)	2	[{"changed": {"fields": ["Name"]}}]	6	1	2024-04-08
708	4051	SpaceX CRS-7 (Dragon C109)	2	[{"changed": {"name": "stage and recovery", "object": "B1018 recovery", "fields": ["Method success"]}}]	6	1	2024-04-08
709	4061	AMOS-6	2	[{"changed": {"name": "stage and recovery", "object": "B1028 recovery", "fields": ["Method success"]}}]	6	1	2024-04-08
710	4365	Bandwagon-1	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1073 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}]	6	1	2024-04-08
711	4365	Bandwagon-1	2	[{"changed": {"name": "fairing recovery", "object": "Fairing recovery with Doug", "fields": ["Recovery"]}}, {"changed": {"name": "fairing recovery", "object": "Fairing recovery with Doug", "fields": ["Recovery"]}}]	6	1	2024-04-08
712	4366	TEST LAUNCH	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1061 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with GO Navigator"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with GO Navigator"}}, {"added": {"name": "tug on launch", "object": "Pacific Warrior"}}, {"added": {"name": "support on launch", "object": "Adele Elise"}}]	6	1	2024-04-08
713	4366	TEST LAUNCH	3		6	1	2024-04-08
714	4367	Starlink Group 6-48	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1083 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Bob"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Bob"}}, {"added": {"name": "tug on launch", "object": "Bob"}}, {"added": {"name": "support on launch", "object": "Bob"}}]	6	1	2024-04-09
715	4367	Starlink Group 6-48	2	[{"changed": {"fields": ["Launch outcome"]}}]	6	1	2024-04-09
716	4367	Starlink Group 6-48	2	[{"changed": {"fields": ["Launch Time", "Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1083 recovery", "fields": ["Method success", "Recovery success"]}}]	6	1	2024-04-10
717	4367	Starlink Group 6-48	2	[{"changed": {"fields": ["Launch Time"]}}]	6	1	2024-04-10
718	4367	Starlink Group 6-48	2	[{"changed": {"fields": ["Launch Time"]}}]	6	1	2024-04-10
719	4368	USSF-62/WSF-M 1	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1082 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with GO Beyond"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with GO Beyond"}}]	6	1	2024-04-10
720	4368	USSF-62 (WSF-M 1)	2	[{"changed": {"fields": ["Name"]}}]	6	1	2024-04-11
721	4368	USSF-62 (WSF-M 1)	2	[{"changed": {"fields": ["Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1082 recovery", "fields": ["Method success", "Recovery success"]}}]	6	1	2024-04-11
722	4364	Starlink Group 8-1	2	[{"changed": {"fields": ["Launch Time"]}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with GO Beyond"}}, {"changed": {"name": "fairing recovery", "object": "Fairing recovery with GO Beyond", "fields": ["Flights"]}}]	6	1	2024-04-11
723	4369	Starlink Group 6-49	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1069 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "tug on launch", "object": "Signet Titan III"}}, {"added": {"name": "support on launch", "object": "Doug"}}]	6	1	2024-04-12
724	4369	Starlink Group 6-49	2	[{"changed": {"name": "stage and recovery", "object": "B1062 recovery", "fields": ["Stage"]}}]	6	1	2024-04-12
725	4369	Starlink Group 6-49	2	[]	6	1	2024-04-12
726	4369	Starlink Group 6-49	2	[{"changed": {"fields": ["Launch Time"]}}]	6	1	2024-04-13
727	4369	Starlink Group 6-49	2	[{"changed": {"fields": ["Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1062 recovery", "fields": ["Method success", "Recovery success"]}}]	6	1	2024-04-13
728	64	LC-39A	2	[{"changed": {"fields": ["Name"]}}]	5	1	2024-04-16
729	65	OLP-A	2	[{"changed": {"fields": ["Name"]}}]	5	1	2024-04-16
730	4370	Starlink Group 6-51	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1077 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Bob"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Bob"}}, {"added": {"name": "tug on launch", "object": "Bob"}}, {"added": {"name": "support on launch", "object": "Bob"}}]	6	1	2024-04-18
731	4371	Starlink Group 6-52	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1080 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "tug on launch", "object": "Signet Warhorse III"}}, {"added": {"name": "support on launch", "object": "Doug"}}]	6	1	2024-04-18
732	4371	Starlink Group 6-52	2	[{"changed": {"fields": ["Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1080 recovery", "fields": ["Method success", "Recovery success"]}}]	6	1	2024-04-18
733	4372	Starlink Group 6-53	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1078 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Bob"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Bob"}}, {"added": {"name": "tug on launch", "object": "Signet Warhorse III"}}, {"added": {"name": "support on launch", "object": "Bob"}}]	6	1	2024-04-23
734	4373	WorldView Legion 1 & 2	1	[{"added": {}}]	6	1	2024-04-23
735	4371	Starlink Group 6-52	2	[{"added": {"name": "tug on launch", "object": "Doug"}}]	6	1	2024-04-23
736	4373	WorldView Legion 1 & 2	2	[{"added": {"name": "stage and recovery", "object": "Unknown recovery"}}]	6	1	2024-04-24
737	4373	WorldView Legion 1 & 2	2	[{"added": {"name": "fairing recovery", "object": "Fairing recovery with GO Beyond"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with GO Beyond"}}]	6	1	2024-04-24
738	4372	Starlink Group 6-53	2	[{"added": {"name": "tug on launch", "object": "Kelly C"}}]	6	1	2024-04-24
739	4372	Starlink Group 6-53	2	[{"deleted": {"name": "tug on launch", "object": "Kelly C"}}]	6	1	2024-04-24
740	4374	TEST LAUNCH	1	[{"added": {}}]	6	1	2024-04-24
741	4374	TEST LAUNCH	2	[{"changed": {"fields": ["Pad", "Rocket"]}}]	6	1	2024-04-24
742	4374	TEST LAUNCH	2	[{"changed": {"fields": ["Pad", "Rocket"]}}]	6	1	2024-04-24
743	4374	TEST LAUNCH	2	[{"changed": {"fields": ["Pad", "Rocket"]}}, {"added": {"name": "stage and recovery", "object": "B0004 recovery"}}, {"added": {"name": "stage and recovery", "object": "B0005 recovery"}}, {"added": {"name": "stage and recovery", "object": "B1034 recovery"}}]	6	1	2024-04-24
744	4374	TEST LAUNCH	3		6	1	2024-04-24
745	4373	WorldView Legion 1 & 2	2	[{"changed": {"fields": ["Launch Time"]}}]	6	1	2024-04-24
746	4373	WorldView Legion 1 & 2	2	[{"changed": {"fields": ["Launch Time"]}}]	6	1	2024-04-25
747	4375	Galileo FOC FM25 & FM27	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1060 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Bob"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Bob"}}]	6	1	2024-04-25
748	4373	WorldView Legion 1 & 2	2	[{"changed": {"fields": ["Launch Time"]}}]	6	1	2024-04-25
749	4375	Galileo FOC FM25 & FM27	2	[{"changed": {"fields": ["Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1060 recovery", "fields": ["Method success"]}}]	6	1	2024-04-28
750	4376	Starlink Group 6-54	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1076 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "tug on launch", "object": "Doug"}}, {"added": {"name": "support on launch", "object": "Doug"}}]	6	1	2024-04-28
751	4372	Starlink Group 6-53	2	[{"changed": {"name": "stage and recovery", "object": "B1078 recovery", "fields": ["Method success", "Recovery success"]}}]	6	1	2024-04-28
752	4372	Starlink Group 6-53	2	[{"changed": {"fields": ["Launch outcome"]}}]	6	1	2024-04-28
753	4051	SpaceX CRS-7 (Dragon C109)	2	[{"changed": {"name": "stage and recovery", "object": "B1018 recovery", "fields": ["Method success"]}}]	6	1	2024-04-28
754	4061	AMOS-6	2	[{"changed": {"name": "stage and recovery", "object": "B1028 recovery", "fields": ["Method success"]}}]	6	1	2024-04-28
755	4376	Starlink Group 6-54	2	[{"changed": {"fields": ["Launch Time"]}}, {"changed": {"name": "stage and recovery", "object": "B1076 recovery", "fields": ["Method success"]}}]	6	1	2024-04-28
756	4376	Starlink Group 6-54	2	[{"changed": {"name": "tug on launch", "object": "Signet Warhorse III", "fields": ["Boat"]}}]	6	1	2024-04-28
1025	4051	SpaceX CRS-7	2	[]	6	1	2024-05-27
757	4293	SDA T&T Tranche 0B	2	[{"changed": {"name": "stage and recovery", "object": "B1063 recovery", "fields": ["Landing zone"]}}]	6	1	2024-04-29
758	4376	Starlink Group 6-54	2	[{"changed": {"fields": ["Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1076 recovery", "fields": ["Method success", "Recovery success"]}}]	6	1	2024-04-29
759	4376	Starlink Group 6-54	2	[{"changed": {"name": "tug on launch", "object": "Doug", "fields": ["Boat"]}}]	6	1	2024-04-30
760	4373	WorldView Legion 1 & 2	2	[{"changed": {"fields": ["Launch Time"]}}, {"changed": {"name": "stage and recovery", "object": "B1061 recovery", "fields": ["Stage", "Method success"]}}]	6	1	2024-05-02
761	4377	Starlink Group 6-55	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1067 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "tug on launch", "object": "Signet Warhorse III"}}, {"added": {"name": "support on launch", "object": "Doug"}}]	6	1	2024-05-02
762	4376	Starlink Group 6-54	2	[{"added": {"name": "tug on launch", "object": "Signet Titan"}}]	6	1	2024-05-02
763	4373	WorldView Legion 1 & 2	2	[{"changed": {"name": "fairing recovery", "object": "Fairing recovery with GO Beyond", "fields": ["Flights"]}}, {"changed": {"name": "fairing recovery", "object": "Fairing recovery with GO Beyond", "fields": ["Flights"]}}]	6	1	2024-05-02
764	4373	WorldView Legion 1 & 2	2	[{"changed": {"fields": ["Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1061 recovery", "fields": ["Method success", "Recovery success"]}}]	6	1	2024-05-02
765	4377	Starlink Group 6-55	2	[{"changed": {"fields": ["Launch Time", "Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1067 recovery", "fields": ["Method success", "Recovery success"]}}]	6	1	2024-05-03
766	4378	Starlink Group 6-57	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1069 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Bob"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Bob"}}, {"added": {"name": "tug on launch", "object": "Signet Warhorse III"}}, {"added": {"name": "support on launch", "object": "Bob"}}]	6	1	2024-05-05
767	4378	Starlink Group 6-57	2	[{"changed": {"fields": ["Launch Time"]}}]	6	1	2024-05-06
768	4378	Starlink Group 6-57	2	[{"changed": {"fields": ["Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1069 recovery", "fields": ["Method success", "Recovery success"]}}, {"changed": {"name": "tug on launch", "object": "Bob", "fields": ["Boat"]}}]	6	1	2024-05-06
769	4379	Starlink Group 6-56	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1083 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "tug on launch", "object": "Signet Warhorse III"}}, {"added": {"name": "support on launch", "object": "Doug"}}]	6	1	2024-05-08
770	4380	Starlink Group 8-1	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1082 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with GO Beyond"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with GO Beyond"}}, {"added": {"name": "tug on launch", "object": "Lindsay C"}}, {"added": {"name": "support on launch", "object": "GO Beyond"}}]	6	1	2024-05-08
771	4380	Starlink Group 8-2	2	[{"changed": {"fields": ["Name"]}}]	6	1	2024-05-08
772	271	B0003	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-08
773	4379	Starlink Group 6-56	2	[{"changed": {"fields": ["Launch Time"]}}]	6	1	2024-05-08
774	4379	Starlink Group 6-56	2	[{"changed": {"fields": ["Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1083 recovery", "fields": ["Method success", "Recovery success"]}}]	6	1	2024-05-08
775	1	SpaceX	1	[{"added": {}}]	22	1	2024-05-09
776	8	Falcon 1	2	[{"changed": {"fields": ["Provider"]}}]	1	1	2024-05-09
777	7	Starship	2	[{"changed": {"fields": ["Provider"]}}]	1	1	2024-05-09
778	6	Falcon Heavy	2	[{"changed": {"fields": ["Provider"]}}]	1	1	2024-05-09
779	5	Falcon 9	2	[{"changed": {"fields": ["Provider"]}}]	1	1	2024-05-09
780	4380	Starlink Group 8-2	2	[{"changed": {"fields": ["Launch Time"]}}, {"changed": {"name": "stage and recovery", "object": "Unknown recovery", "fields": ["Stage"]}}]	6	1	2024-05-09
781	4380	Starlink Group 8-2	2	[{"changed": {"fields": ["Launch Time"]}}]	6	1	2024-05-09
782	355	B1082	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
783	4380	Starlink Group 8-2	2	[{"changed": {"name": "stage and recovery", "object": "B1082 recovery", "fields": ["Stage"]}}]	6	1	2024-05-09
784	4033	Dragon Spacecraft Qualification Unit	2	[{"changed": {"name": "stage and recovery", "object": "B0003 recovery", "fields": ["Method"]}}]	6	1	2024-05-09
785	271	B0003	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
786	4034	SpaceX COTS Demo Flight 1 (Dragon C101)	2	[{"changed": {"name": "stage and recovery", "object": "B0004 recovery", "fields": ["Method"]}}]	6	1	2024-05-09
787	272	B0004	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
788	274	B0006	2	[]	2	1	2024-05-09
789	276	B1003	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
790	276	B1003	2	[]	2	1	2024-05-09
791	279	B1006	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
792	280	B1007	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
793	283	B1010	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
794	285	B1013	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
795	290	B1019	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
796	293	B1021	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
797	294	B1022	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
798	295	B1023	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
799	297	B1025	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
800	298	B1026	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
801	300	B1029	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
802	301	B1031	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
803	303	B1032	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
804	305	B1035	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
805	306	B1036	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
806	311	B1041	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
807	312	B1042	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
808	315	B1044	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
809	324	B1055	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
810	330	B1058	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
811	360	S28	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
812	357	B10	2	[{"changed": {"fields": ["Status"]}}]	2	1	2024-05-09
813	4380	Starlink Group 8-2	2	[{"changed": {"fields": ["Launch Time"]}}]	6	1	2024-05-09
814	4379	Starlink Group 6-56	2	[]	6	1	2024-05-09
815	8	Falcon 1	2	[{"added": {"name": "pad used", "object": "Omelek Island"}}]	1	1	2024-05-09
816	7	Starship	2	[{"added": {"name": "pad used", "object": "Orbital Launch Pad A"}}]	1	1	2024-05-09
817	6	Falcon Heavy	2	[{"added": {"name": "pad used", "object": "Launch Complex 39A"}}]	1	1	2024-05-09
818	5	Falcon 9	2	[{"added": {"name": "pad used", "object": "Space Launch Complex 40"}}, {"added": {"name": "pad used", "object": "Launch Complex 39A"}}, {"added": {"name": "pad used", "object": "Space Launch Complex 4 East"}}]	1	1	2024-05-09
819	4380	Starlink Group 8-2	2	[{"changed": {"fields": ["Launch Time"]}}]	6	1	2024-05-09
820	4380	Starlink Group 8-2	2	[{"changed": {"fields": ["Launch Time"]}}]	6	1	2024-05-09
821	4380	Starlink Group 8-2	2	[{"changed": {"fields": ["Launch Time", "Mass", "Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1082 recovery", "fields": ["Method success", "Recovery success"]}}]	6	1	2024-05-12
822	4380	Starlink Group 8-2	2	[]	6	1	2024-05-12
823	4381	Starlink Group 6-58	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1073 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "tug on launch", "object": "Signet Warhorse III"}}, {"added": {"name": "support on launch", "object": "Doug"}}]	6	1	2024-05-12
824	4381	Starlink Group 6-58	2	[{"changed": {"fields": ["Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1073 recovery", "fields": ["Method success", "Recovery success"]}}]	6	1	2024-05-13
825	65	OLP-A	2	[{"changed": {"fields": ["Location", "Image"]}}]	5	1	2024-05-13
826	64	LC-39A	2	[{"changed": {"fields": ["Location", "Image"]}}]	5	1	2024-05-13
827	63	SLC-4E	2	[{"changed": {"fields": ["Location", "Image"]}}]	5	1	2024-05-13
828	62	SLC-40	2	[{"changed": {"fields": ["Location", "Image"]}}]	5	1	2024-05-13
829	61	Omelek Island	2	[{"changed": {"fields": ["Location"]}}]	5	1	2024-05-13
830	61	Omelek Island	2	[{"changed": {"fields": ["Image"]}}]	5	1	2024-05-13
831	66	test	1	[{"added": {}}]	5	1	2024-05-13
832	66	test	3		5	1	2024-05-13
833	67	test	1	[{"added": {}}]	5	1	2024-05-13
834	67	test	3		5	1	2024-05-13
835	19	A Shortfall of Gravitas	2	[{"changed": {"fields": ["Serial number"]}}]	7	1	2024-05-13
836	19	A Shortfall of Gravitas	2	[]	7	1	2024-05-13
837	14	Just Read the Instructions (2)	2	[{"changed": {"fields": ["Name", "Serial number"]}}]	7	1	2024-05-13
838	15	Of Course I Still Love You	2	[{"changed": {"fields": ["Serial number"]}}]	7	1	2024-05-13
839	20	Just Read the Instructions (1)	1	[{"added": {}}]	7	1	2024-05-13
840	4046	SpaceX CRS-5 (Dragon C107)	2	[{"changed": {"name": "stage and recovery", "object": "B1012 recovery", "fields": ["Landing zone"]}}]	6	1	2024-05-13
841	4049	SpaceX CRS-6 (Dragon C108-1)	2	[{"changed": {"name": "stage and recovery", "object": "B1015 recovery", "fields": ["Landing zone"]}}]	6	1	2024-05-13
842	20	Just Read the Instructions (1)	2	[{"changed": {"fields": ["Status"]}}]	7	1	2024-05-13
843	20	Just Read the Instructions (1)	2	[{"changed": {"fields": ["Image"]}}]	7	1	2024-05-13
844	19	A Shortfall of Gravitas	2	[{"changed": {"fields": ["Image"]}}]	7	1	2024-05-13
845	15	Of Course I Still Love You	2	[{"changed": {"fields": ["Image"]}}]	7	1	2024-05-13
846	14	Just Read the Instructions (2)	2	[{"changed": {"fields": ["Image"]}}]	7	1	2024-05-13
847	16	Landing Zone 1	2	[{"changed": {"fields": ["Image"]}}]	7	1	2024-05-13
848	17	Landing Zone 2	2	[{"changed": {"fields": ["Image"]}}]	7	1	2024-05-13
849	18	Landing Zone 4	2	[{"changed": {"fields": ["Image"]}}]	7	1	2024-05-13
850	61	Omelek Island	2	[{"changed": {"fields": ["Status"]}}]	5	1	2024-05-13
851	4382	Starlink Group 8-7	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "Unknown recovery"}}]	6	1	2024-05-13
852	4382	Starlink Group 8-7	2	[{"changed": {"fields": ["Launch Time"]}}, {"changed": {"name": "stage and recovery", "object": "B1063 recovery", "fields": ["Stage"]}}]	6	1	2024-05-14
853	361	B1090	1	[{"added": {}}]	2	1	2024-05-14
854	361	B1090	3		2	1	2024-05-14
855	4382	Starlink Group 8-7	2	[{"added": {"name": "fairing recovery", "object": "Fairing recovery with GO Beyond"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with GO Beyond"}}, {"added": {"name": "tug on launch", "object": "Lindsay C"}}, {"added": {"name": "support on launch", "object": "GO Quest"}}]	6	1	2024-05-14
856	4382	Starlink Group 8-7	2	[{"changed": {"name": "support on launch", "object": "GO Beyond", "fields": ["Boat"]}}]	6	1	2024-05-14
857	4382	Starlink Group 8-7	2	[{"changed": {"fields": ["Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1063 recovery", "fields": ["Method success", "Recovery success"]}}]	6	1	2024-05-14
858	4382	Starlink Group 8-7	2	[]	6	1	2024-05-17
859	281	Signet Warhorse I	1	[{"added": {}}]	3	1	2024-05-17
860	4383	Starlink Group 6-59	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1062 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "tug on launch", "object": "Signet Warhorse I"}}, {"added": {"name": "support on launch", "object": "Doug"}}]	6	1	2024-05-17
861	4378	Starlink Group 6-57	2	[{"added": {"name": "tug on launch", "object": "Signet Warhorse I"}}]	6	1	2024-05-17
862	4378	Starlink Group 6-57	2	[{"added": {"name": "tug on launch", "object": "Signet Warhorse I"}}]	6	1	2024-05-17
863	4383	Starlink Group 6-59	2	[{"changed": {"fields": ["Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1062 recovery", "fields": ["Method success", "Recovery success"]}}]	6	1	2024-05-18
864	1	Dragon	1	[{"added": {}}]	26	1	2024-05-20
865	238	GO Searcher	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
866	238	GO Searcher	2	[]	3	1	2024-05-20
867	243	Mr. Steven	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
868	244	GO Pursuit	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
869	250	GO Navigator	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
870	251	GO Ms. Tree	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
871	252	GO Ms. Chief	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
872	255	NRC Quest	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
873	257	Shelia Bordelon	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
874	259	Hos Briarwood	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
875	234	GO Quest	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
876	236	NRC Quest	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
877	247	John Henry	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
878	256	GO Searcher	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
879	260	Adele Elise	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
880	235	Elsbeth III	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
881	237	Int. Freedom	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
882	239	Pacific Warrior	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
883	240	Kelly C	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
884	241	Betty R Gambarella	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
885	242	Hawk	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
886	245	Rachel	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
887	246	Freedom	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
888	249	Hollywood	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
889	253	Finn Falgout	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
890	254	Lauren Floss	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
891	258	Mr. Jonah	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
892	267	Zion M Falgout	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
893	269	Debra C	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
894	271	Crosby Skipper	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
895	270	Kurt J Crosby	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
896	272	Crosby Endeavor	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
897	274	Nicole Foss	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-20
898	361	B1068	1	[{"added": {}}]	2	1	2024-05-20
899	361	B1068	3		2	1	2024-05-20
900	4383	Starlink Group 6-59	2	[{"added": {"name": "stage and recovery", "object": "B1061 recovery"}}]	6	1	2024-05-20
901	4383	Starlink Group 6-59	2	[{"changed": {"name": "stage and recovery", "object": "B1062 recovery", "fields": ["Stage"]}}]	6	1	2024-05-20
902	4383	Starlink Group 6-59	2	[]	6	1	2024-05-20
903	4383	Starlink Group 6-59	2	[{"changed": {"name": "stage and recovery", "object": "B1062 recovery", "fields": ["Method"]}}]	6	1	2024-05-20
904	4383	Starlink Group 6-59	2	[{"deleted": {"name": "stage and recovery", "object": "B1062 recovery"}}]	6	1	2024-05-20
905	4383	Starlink Group 6-59	2	[{"added": {"name": "tug on launch", "object": "Signet Warhorse I"}}]	6	1	2024-05-20
906	4383	Starlink Group 6-59	2	[{"added": {"name": "stage and recovery", "object": "B1062 recovery"}}]	6	1	2024-05-20
907	4383	Starlink Group 6-59	2	[{"deleted": {"name": "stage and recovery", "object": "B1062 recovery"}}]	6	1	2024-05-20
908	4378	Starlink Group 6-57	2	[{"deleted": {"name": "tug on launch", "object": "Signet Warhorse I"}}]	6	1	2024-05-20
909	4378	Starlink Group 6-57	2	[]	6	1	2024-05-20
910	4383	Starlink Group 6-59	2	[{"deleted": {"name": "tug on launch", "object": "Signet Warhorse I"}}]	6	1	2024-05-20
911	4383	Starlink Group 6-59	2	[]	6	1	2024-05-20
912	4082	Elon Musk's Tesla Roadster	2	[{"changed": {"name": "stage and recovery", "object": "B1033 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1023 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1025 recovery", "fields": ["Stage position"]}}]	6	1	2024-05-21
913	4104	Arabsat-6A	2	[{"changed": {"name": "stage and recovery", "object": "B1055 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1052 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1053 recovery", "fields": ["Stage position"]}}]	6	1	2024-05-21
914	4108	Space Test Program Flight 2 (STP-2)	2	[{"changed": {"name": "stage and recovery", "object": "B1057 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1052 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1053 recovery", "fields": ["Stage position"]}}]	6	1	2024-05-21
915	4220	USSF-44	2	[{"changed": {"name": "stage and recovery", "object": "B1066 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1064 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1065 recovery", "fields": ["Stage position"]}}]	6	1	2024-05-21
916	4234	USSF-67	2	[{"changed": {"name": "stage and recovery", "object": "B1070 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1064 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1065 recovery", "fields": ["Stage position"]}}]	6	1	2024-05-21
917	4260	Viasat-3 Americas & others	2	[{"changed": {"name": "stage and recovery", "object": "B1068 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1052 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1053 recovery", "fields": ["Stage position"]}}]	6	1	2024-05-21
918	4283	EchoStar 24 (Jupiter 3)	2	[{"changed": {"name": "stage and recovery", "object": "B1074 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1064 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1065 recovery", "fields": ["Stage position"]}}]	6	1	2024-05-21
975	4037	SpaceX CRS-2	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C104 on launch"}}]	6	1	2024-05-26
1026	65	OLP-A	2	[{"changed": {"fields": ["Image"]}}]	5	1	2024-05-28
919	4304	Psyche	2	[{"changed": {"name": "stage and recovery", "object": "B1079 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1064 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1065 recovery", "fields": ["Stage position"]}}]	6	1	2024-05-21
920	4328	USSF-52	2	[{"changed": {"name": "stage and recovery", "object": "B1084 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1064 recovery", "fields": ["Stage position"]}}, {"changed": {"name": "stage and recovery", "object": "B1065 recovery", "fields": ["Stage position"]}}]	6	1	2024-05-21
921	282	Megan	1	[{"added": {}}]	3	1	2024-05-21
922	283	Shannon	1	[{"added": {}}]	3	1	2024-05-21
923	283	Shannon	2	[{"changed": {"fields": ["Status"]}}]	3	1	2024-05-21
924	8	Falcon 1	2	[{"changed": {"fields": ["Status"]}}]	1	1	2024-05-21
925	4384	NROL-146	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1071 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with GO Beyond"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with GO Beyond"}}, {"added": {"name": "tug on launch", "object": "Kimberly C"}}, {"added": {"name": "support on launch", "object": "GO Beyond"}}]	6	1	2024-05-21
926	4384	NROL-146	2	[{"changed": {"fields": ["Orbit", "Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1071 recovery", "fields": ["Method success", "Recovery success"]}}]	6	1	2024-05-23
927	4385	Starlink Group 6-62	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1080 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Bob"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Bob"}}]	6	1	2024-05-23
928	4385	Starlink Group 6-62	2	[{"added": {"name": "tug on launch", "object": "Signet Warhorse I"}}, {"added": {"name": "support on launch", "object": "Bob"}}]	6	1	2024-05-23
929	4385	Starlink Group 6-62	2	[{"changed": {"fields": ["Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1080 recovery", "fields": ["Method success", "Recovery success"]}}]	6	1	2024-05-23
930	4386	Starlink Group 6-63	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1077 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}]	6	1	2024-05-23
931	4386	Starlink Group 6-63	2	[{"changed": {"fields": ["Launch Time"]}}]	6	1	2024-05-23
932	4386	Starlink Group 6-63	2	[{"changed": {"fields": ["Launch Time"]}}]	6	1	2024-05-23
933	65	OLP-A	2	[{"changed": {"fields": ["Image"]}}]	5	1	2024-05-23
934	4386	Starlink Group 6-63	2	[{"changed": {"fields": ["Launch Time"]}}]	6	1	2024-05-24
935	4386	Starlink Group 6-63	2	[{"added": {"name": "tug on launch", "object": "Signet Warhorse III"}}]	6	1	2024-05-24
936	4386	Starlink Group 6-63	2	[{"changed": {"name": "fairing recovery", "object": "Fairing recovery with Bob", "fields": ["Boat"]}}, {"changed": {"name": "fairing recovery", "object": "Fairing recovery with Bob", "fields": ["Boat"]}}]	6	1	2024-05-24
937	4386	Starlink Group 6-63	2	[{"changed": {"name": "tug on launch", "object": "Bob", "fields": ["Boat"]}}]	6	1	2024-05-24
938	4386	Starlink Group 6-63	2	[{"changed": {"fields": ["Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1077 recovery", "fields": ["Method success", "Recovery success"]}}]	6	1	2024-05-24
939	285	B1013	2	[{"changed": {"fields": ["Photo"]}}]	2	1	2024-05-24
940	332	B1062	2	[{"changed": {"fields": ["Image"]}}]	2	1	2024-05-24
941	361	test	1	[{"added": {}}]	2	1	2024-05-24
942	361	test	3		2	1	2024-05-24
943	4078	SpaceX CRS-13 (Dragon C108-2)	2	[{"changed": {"name": "stage and recovery", "object": "B1035 recovery", "fields": ["Stage"]}}]	6	1	2024-05-24
944	4385	Starlink Group 6-62	2	[{"changed": {"name": "support on launch", "object": "Doug", "fields": ["Boat"]}}]	6	1	2024-05-26
945	4386	Starlink Group 6-63	2	[{"added": {"name": "support on launch", "object": "Bob"}}]	6	1	2024-05-26
946	4385	Starlink Group 6-62	2	[{"changed": {"name": "fairing recovery", "object": "Fairing recovery with Doug", "fields": ["Boat"]}}, {"changed": {"name": "fairing recovery", "object": "Fairing recovery with Doug", "fields": ["Boat"]}}]	6	1	2024-05-26
947	4387	Starlink Group 6-60	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1078 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "tug on launch", "object": "Signet Warhorse I"}}, {"added": {"name": "support on launch", "object": "Doug"}}]	6	1	2024-05-26
948	1	C101	1	[{"added": {}}]	23	1	2024-05-26
949	2	C102	1	[{"added": {}}]	23	1	2024-05-26
950	3	C103	1	[{"added": {}}]	23	1	2024-05-26
951	4	C104	1	[{"added": {}}]	23	1	2024-05-26
952	5	C105	1	[{"added": {}}]	23	1	2024-05-26
953	6	C106	1	[{"added": {}}]	23	1	2024-05-26
954	7	C107	1	[{"added": {}}]	23	1	2024-05-26
955	8	C108	1	[{"added": {}}]	23	1	2024-05-26
956	9	C109	1	[{"added": {}}]	23	1	2024-05-26
957	10	C110	1	[{"added": {}}]	23	1	2024-05-26
958	11	C111	1	[{"added": {}}]	23	1	2024-05-26
959	12	C112	1	[{"added": {}}]	23	1	2024-05-26
960	13	C113	1	[{"added": {}}]	23	1	2024-05-26
961	14	C204	1	[{"added": {}}]	23	1	2024-05-26
962	15	C205	1	[{"added": {}}]	23	1	2024-05-26
963	16	C206	1	[{"added": {}}]	23	1	2024-05-26
964	17	C207	1	[{"added": {}}]	23	1	2024-05-26
965	18	C208	1	[{"added": {}}]	23	1	2024-05-26
966	19	C209	1	[{"added": {}}]	23	1	2024-05-26
967	20	C210	1	[{"added": {}}]	23	1	2024-05-26
968	21	C211	1	[{"added": {}}]	23	1	2024-05-26
969	22	C212	1	[{"added": {}}]	23	1	2024-05-26
970	284	Champion	1	[{"added": {}}]	3	1	2024-05-26
971	4034	SpaceX COTS Demo Flight 1	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C101 on launch"}}]	6	1	2024-05-26
972	4035	SpaceX COTS Demo Flight 2	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C102 on launch"}}]	6	1	2024-05-26
973	285	Islander	1	[{"added": {}}]	3	1	2024-05-26
974	4036	SpaceX CRS-1, Orbcomm-OG2	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C103 on launch"}}]	6	1	2024-05-26
976	4041	SpaceX CRS-3	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C105 on launch"}}]	6	1	2024-05-26
977	4045	SpaceX CRS-4	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C106 on launch"}}]	6	1	2024-05-26
978	286	GO Quest	1	[{"added": {}}]	3	1	2024-05-26
979	4068	SpaceX CRS-11	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C106 on launch"}}]	6	1	2024-05-26
980	4068	SpaceX CRS-11	2	[]	6	1	2024-05-26
981	4112	SpaceX CRS-19	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C106 on launch"}}]	6	1	2024-05-26
982	4046	SpaceX CRS-5	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C107 on launch"}}]	6	1	2024-05-26
983	4049	SpaceX CRS-6	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C108 on launch"}}]	6	1	2024-05-26
984	4078	SpaceX CRS-13	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C108 on launch"}}]	6	1	2024-05-26
985	4109	SpaceX CRS-18	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C108 on launch"}}]	6	1	2024-05-26
986	4051	SpaceX CRS-7	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C109 on launch"}}]	6	1	2024-05-26
987	4055	SpaceX CRS-8	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C110 on launch"}}]	6	1	2024-05-26
988	4086	SpaceX CRS-14	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C110 on launch"}}]	6	1	2024-05-26
989	4059	SpaceX CRS-9	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C111 on launch"}}]	6	1	2024-05-26
990	4091	SpaceX CRS-15	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C111 on launch"}}]	6	1	2024-05-26
991	4063	SpaceX CRS-10	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C112 on launch"}}]	6	1	2024-05-26
992	4099	SpaceX CRS-16	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C112 on launch"}}]	6	1	2024-05-26
993	4118	SpaceX CRS-20	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C112 on launch"}}]	6	1	2024-05-26
994	4072	SpaceX CRS-12	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C113 on launch"}}]	6	1	2024-05-26
995	4105	SpaceX CRS-17	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C113 on launch"}}]	6	1	2024-05-26
996	4137	SpaceX CRS-21	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C208 on launch"}}]	6	1	2024-05-26
997	4160	SpaceX CRS-23	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C208 on launch"}}]	6	1	2024-05-26
998	4200	SpaceX CRS-25	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C208 on launch"}}]	6	1	2024-05-26
999	4270	SpaceX CRS-28	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C208 on launch"}}]	6	1	2024-05-26
1000	4156	SpaceX CRS-22	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C209 on launch"}}]	6	1	2024-05-26
1001	4170	SpaceX CRS-24	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C209 on launch"}}]	6	1	2024-05-26
1002	4248	SpaceX CRS-27	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C209 on launch"}}]	6	1	2024-05-26
1003	4357	SpaceX CRS-30	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C209 on launch"}}]	6	1	2024-05-26
1004	4224	SpaceX CRS-26	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C111 on launch"}}]	6	1	2024-05-26
1005	4313	SpaceX CRS-29	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C211 on launch"}}]	6	1	2024-05-26
1006	4103	Crew Dragon Demo-1	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C204 on launch"}}]	6	1	2024-05-26
1007	4115	Crew Dragon in-flight abort test	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C205 on launch"}}]	6	1	2024-05-26
1008	4121	Crew Dragon Demo-2	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C206 on launch"}}]	6	1	2024-05-26
1009	4150	Crew-2	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C206 on launch"}}]	6	1	2024-05-26
1010	4183	Axiom-1	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C206 on launch"}}]	6	1	2024-05-26
1011	4245	Crew-6	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C206 on launch"}}]	6	1	2024-05-26
1012	4349	Crew-8	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C206 on launch"}}]	6	1	2024-05-26
1013	4134	Crew-1	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C207 on launch"}}]	6	1	2024-05-26
1014	4162	Inspiration4	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C207 on launch"}}]	6	1	2024-05-26
1015	4163	Crew-3	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C210 on launch"}}]	6	1	2024-05-26
1016	4214	Crew-5	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C210 on launch"}}]	6	1	2024-05-26
1017	4290	Crew-7	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C210 on launch"}}]	6	1	2024-05-26
1018	4186	Crew-4	2	[{"added": {"name": "spacecraft on launch", "object": "C212 on launch"}}]	6	1	2024-05-26
1019	4266	Axiom-2	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "spacecraft on launch", "object": "C212 on launch"}}]	6	1	2024-05-26
1020	4335	Axiom-3	2	[{"added": {"name": "spacecraft on launch", "object": "C212 on launch"}}]	6	1	2024-05-26
1021	361	B1072	1	[{"added": {}}]	2	1	2024-05-26
1022	287	None	1	[{"added": {}}]	3	1	2024-05-27
1023	4051	SpaceX CRS-7	2	[{"changed": {"name": "spacecraft on launch", "object": "C109 on launch", "fields": ["Splashdown Time", "Recovery boat"]}}]	6	1	2024-05-27
1024	287	N/A	2	[{"changed": {"fields": ["Name"]}}]	3	1	2024-05-27
1027	4387	Starlink Group 6-60	2	[{"changed": {"fields": ["Launch Time"]}}]	6	1	2024-05-28
1028	4387	Starlink Group 6-60	2	[{"changed": {"fields": ["Launch Time"]}}]	6	1	2024-05-28
1029	4387	Starlink Group 6-60	2	[{"changed": {"fields": ["Launch outcome"]}}, {"changed": {"name": "stage and recovery", "object": "B1078 recovery", "fields": ["Method success", "Recovery success"]}}]	6	1	2024-05-28
1030	4388	EarthCARE	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "B1081 recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with GO Beyond"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with GO Beyond"}}]	6	1	2024-05-28
1031	4389	test	1	[{"added": {}}]	6	1	2024-05-28
1032	4389	test	2	[{"added": {"name": "stage and recovery", "object": "B7 recovery"}}]	6	1	2024-05-28
1033	4389	test	3		6	1	2024-05-28
1034	1	Falcon	1	[{"added": {}}]	27	1	2024-05-29
1035	2	Starship	1	[{"added": {}}]	27	1	2024-05-29
1036	5	Falcon 9	2	[{"changed": {"fields": ["Family"]}}]	1	1	2024-05-29
1037	6	Falcon Heavy	2	[{"changed": {"fields": ["Family"]}}]	1	1	2024-05-29
1038	7	Starship	2	[{"changed": {"fields": ["Family"]}}]	1	1	2024-05-29
1039	8	Falcon 1	2	[{"changed": {"fields": ["Family"]}}]	1	1	2024-05-29
1040	4390	Starlink Group 6-64	1	[{"added": {}}, {"added": {"name": "stage and recovery", "object": "Unknown recovery"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "fairing recovery", "object": "Fairing recovery with Doug"}}, {"added": {"name": "tug on launch", "object": "Signet Warhorse I"}}, {"added": {"name": "support on launch", "object": "Doug"}}]	6	1	2024-05-31
1041	362	TEST STAGE	1	[{"added": {}}]	2	1	2024-06-03
1042	363	TEST STAGE 2	1	[{"added": {}}]	2	1	2024-06-03
1043	364	NE-N 3	1	[{"added": {}}]	2	1	2024-06-03
1044	364	NE-N 3	3		2	1	2024-06-03
1045	363	TEST STAGE 2	3		2	1	2024-06-03
1046	362	TEST STAGE	3		2	1	2024-06-03
\.


--
-- Data for Name: _django_content_type; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._django_content_type (id, app_label, model) FROM stdin;
11	admin	logentry
13	auth	group
12	auth	permission
14	auth	user
3	booster_tracker	boat
17	booster_tracker	boatsupport
21	booster_tracker	dragon
20	booster_tracker	dragononlaunch
9	booster_tracker	fairingrecovery
7	booster_tracker	landingzone
6	booster_tracker	launch
22	booster_tracker	operator
4	booster_tracker	orbit
5	booster_tracker	pad
25	booster_tracker	padused
1	booster_tracker	rocket
27	booster_tracker	rocketfamily
23	booster_tracker	spacecraft
26	booster_tracker	spacecraftfamily
24	booster_tracker	spacecraftonlaunch
2	booster_tracker	stage
8	booster_tracker	stageandrecovery
19	booster_tracker	supportonlaunch
10	booster_tracker	tugandsupport
18	booster_tracker	tugonlaunch
15	contenttypes	contenttype
16	sessions	session
\.


--
-- Data for Name: _django_migrations; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2024-03-30
2	auth	0001_initial	2024-03-30
3	admin	0001_initial	2024-03-30
4	admin	0002_logentry_remove_auto_add	2024-03-30
5	admin	0003_logentry_add_action_flag_choices	2024-03-30
6	contenttypes	0002_remove_content_type_name	2024-03-30
7	auth	0002_alter_permission_name_max_length	2024-03-30
8	auth	0003_alter_user_email_max_length	2024-03-30
9	auth	0004_alter_user_username_opts	2024-03-30
10	auth	0005_alter_user_last_login_null	2024-03-30
11	auth	0006_require_contenttypes_0002	2024-03-30
12	auth	0007_alter_validators_add_error_messages	2024-03-30
13	auth	0008_alter_user_username_max_length	2024-03-30
14	auth	0009_alter_user_last_name_max_length	2024-03-30
15	auth	0010_alter_group_name_max_length	2024-03-30
16	auth	0011_update_proxy_permissions	2024-03-30
17	auth	0012_alter_user_first_name_max_length	2024-03-30
18	sessions	0001_initial	2024-03-30
19	booster_tracker	0001_initial	2024-03-31
20	booster_tracker	0002_boat_remove_booster_rocket_alter_launch_options_and_more	2024-03-31
21	booster_tracker	0003_alter_launch_options_alter_launch_name	2024-03-31
22	booster_tracker	0004_remove_fairingrecovery_fairing_lat_and_more	2024-03-31
23	booster_tracker	0005_rename_serial_number_stage_name_alter_stage_type	2024-04-01
24	booster_tracker	0006_alter_stage_type	2024-04-01
25	booster_tracker	0007_launch_mass	2024-04-02
26	booster_tracker	0008_remove_launch_support_remove_launch_tug_and_more	2024-04-02
27	booster_tracker	0009_remove_stageandrecovery_support_and_more	2024-04-02
28	booster_tracker	0010_fairingrecovery_flights	2024-04-02
29	booster_tracker	0011_alter_fairingrecovery_recovery	2024-04-02
30	booster_tracker	0012_alter_fairingrecovery_options_and_more	2024-04-02
31	booster_tracker	0013_tugandsupport_launch	2024-04-02
32	booster_tracker	0014_launch_pad	2024-04-02
33	booster_tracker	0015_boatsupport_delete_tugandsupport	2024-04-02
34	booster_tracker	0016_supportonlaunch_tugonlaunch_delete_boatsupport	2024-04-02
35	booster_tracker	0017_alter_supportonlaunch_options_and_more	2024-04-02
36	booster_tracker	0018_alter_stageandrecovery_options	2024-04-02
37	booster_tracker	0019_dragon_dragononlaunch	2024-04-05
38	booster_tracker	0020_dragononlaunch_splashdown_time	2024-04-05
39	booster_tracker	0021_alter_stageandrecovery_launch	2024-04-05
40	booster_tracker	0022_alter_stageandrecovery_launch	2024-04-06
41	booster_tracker	0023_alter_stageandrecovery_landing_zone	2024-04-08
42	booster_tracker	0024_alter_launch_launch_outcome	2024-04-09
43	booster_tracker	0025_alter_stageandrecovery_stage	2024-04-24
44	booster_tracker	0026_alter_fairingrecovery_boat	2024-04-24
45	booster_tracker	0027_stageandrecovery_method_success_2	2024-04-28
46	booster_tracker	0028_alter_stageandrecovery_options_and_more	2024-04-28
47	booster_tracker	0029_rename_method_success_2_stageandrecovery_method_success	2024-04-28
48	booster_tracker	0030_operator_remove_dragononlaunch_dragon_and_more	2024-05-03
49	booster_tracker	0031_stage_photo	2024-05-08
50	booster_tracker	0032_alter_launch_name	2024-05-08
51	booster_tracker	0033_padused	2024-05-09
52	booster_tracker	0034_alter_padused_image_alter_stageandrecovery_method	2024-05-09
53	booster_tracker	0035_pad_image_pad_location	2024-05-13
54	booster_tracker	0036_alter_pad_image_alter_pad_nickname	2024-05-13
55	booster_tracker	0037_landingzone_serial_number	2024-05-13
56	booster_tracker	0038_landingzone_image_alter_pad_image	2024-05-13
57	booster_tracker	0039_alter_landingzone_serial_number	2024-05-13
58	booster_tracker	0040_landingzone_status	2024-05-13
59	booster_tracker	0041_pad_status	2024-05-13
60	booster_tracker	0042_remove_spacecraft_operator_boat_status_rocket_status_and_more	2024-05-20
61	booster_tracker	0043_alter_spacecraftfamily_options_alter_operator_name_and_more	2024-05-20
62	booster_tracker	0044_alter_landingzone_options_alter_padused_options_and_more	2024-05-20
63	booster_tracker	0045_alter_spacecraftonlaunch_options_and_more	2024-05-20
64	booster_tracker	0046_remove_stageandrecovery_unique_launch_stage	2024-05-20
65	booster_tracker	0047_stageandrecovery_unique_launch_stage	2024-05-20
66	booster_tracker	0048_stageandrecovery_stage_position	2024-05-21
67	booster_tracker	0049_spacecraft_status_spacecraftonlaunch_recovery_boat_and_more	2024-05-21
68	booster_tracker	0050_alter_launch_orbit	2024-05-21
69	booster_tracker	0051_alter_stageandrecovery_id	2024-05-22
70	booster_tracker	0052_alter_stage_photo	2024-05-24
71	booster_tracker	0053_alter_stage_photo	2024-05-24
72	booster_tracker	0054_alter_stage_photo	2024-05-24
73	booster_tracker	0055_alter_landingzone_image_alter_pad_image_and_more	2024-05-24
74	booster_tracker	0056_alter_stage_photo	2024-05-24
75	booster_tracker	0057_rename_photo_stage_image	2024-05-24
76	booster_tracker	0058_remove_stage_image	2024-05-24
77	booster_tracker	0059_stage_image	2024-05-24
78	booster_tracker	0060_alter_stage_image	2024-05-24
79	booster_tracker	0061_spacecraft_image	2024-05-26
80	booster_tracker	0062_alter_spacecraftonlaunch_splashdown_time	2024-05-26
81	booster_tracker	0063_remove_rocket_provider_alter_stageandrecovery_method_and_more	2024-05-29
82	booster_tracker	0064_alter_rocketfamily_options_alter_rocket_family_and_more	2024-05-30
\.


--
-- Data for Name: _django_session; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._django_session (session_key, session_data, expire_date) FROM stdin;
xr11v9xxh41jjxbosuepncmxl5d9cine	.eJxVjEEOwiAQAP_C2RBgoYBH730DWViQqqFJaU_GvxuSHvQ6M5k3C3jsNRw9b2EhdmWSXX5ZxPTMbQh6YLuvPK1t35bIR8JP2_m8Un7dzvZvULHXsc0EwpDR3irn0ehYEAr45ETWxcVIZMGobEGSLEqCISXUZGgil2zS7PMF3KI3pg:1rrWVr:n3yqbdBemMWUS3OC64M-dDFJzlUte87MaEANfBcF7zA	2024-04-16
31xc9dho2gse5jkh4ailpsu7nst4ojc6	.eJxVjEEOwiAQAP_C2RBgoYBH730DWViQqqFJaU_GvxuSHvQ6M5k3C3jsNRw9b2EhdmWSXX5ZxPTMbQh6YLuvPK1t35bIR8JP2_m8Un7dzvZvULHXsc0EwpDR3irn0ehYEAr45ETWxcVIZMGobEGSLEqCISXUZGgil2zS7PMF3KI3pg:1rxJyN:1Qw2ngwBUzhxVY_4chYYSMJkscwGcnWaP7lCUuMyjKQ	2024-05-02
9wkafax89bu398hwczuezhmxc3hbn4e9	.eJxVjEEOwiAQAP_C2RBgoYBH730DWViQqqFJaU_GvxuSHvQ6M5k3C3jsNRw9b2EhdmWSXX5ZxPTMbQh6YLuvPK1t35bIR8JP2_m8Un7dzvZvULHXsc0EwpDR3irn0ehYEAr45ETWxcVIZMGobEGSLEqCISXUZGgil2zS7PMF3KI3pg:1s2Yde:plZzE6rX8sIgrblz0Hr9Kp1e66mDF8-3l3quOfpLi7o	2024-05-16
4dv0tfee6kw9m9ig9hxex2v983yz7xs0	.eJxVjEEOwiAQAP_C2RBgoYBH730DWViQqqFJaU_GvxuSHvQ6M5k3C3jsNRw9b2EhdmWSXX5ZxPTMbQh6YLuvPK1t35bIR8JP2_m8Un7dzvZvULHXsc0EwpDR3irn0ehYEAr45ETWxcVIZMGobEGSLEqCISXUZGgil2zS7PMF3KI3pg:1s7fSg:DqxdDdtQk8UbrvNgvj2FCWsbwvHCR7eCLoRJ8BLf-AM	2024-05-30
jl4wrhp99y0hpaj7t0m46vza97wkyypd	.eJxVjE0OwiAYBe_C2hCBWsCle89Avl-pmjYp7cp4d23ShW7fzLyXKbAutaxN5jKwORtnDr8bAj1k3ADfYbxNlqZxmQe0m2J32ux1YnledvfvoEKr31pRPWPyvqMUJKLz6jUkYSYXgRz2HNgBqOSUY8Agx95lytDFpEon8_4AETw4-w:1sDyBT:Eb3yXkTgo4BeO73N0D0Si5i7eluTwijs3SysrsO0p3U	2024-06-17
\.


--
-- Data for Name: _sqlite_sequence; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._sqlite_sequence (name, seq) FROM stdin;
django_migrations	82
django_admin_log	1046
django_content_type	27
auth_permission	108
auth_group	0
auth_user	1
booster_tracker_fairingrecovery	5478
booster_tracker_operator	1
booster_tracker_orbit	30
booster_tracker_spacecraftfamily	1
booster_tracker_boat	287
booster_tracker_spacecraftonlaunch	47
booster_tracker_supportonlaunch	1933
booster_tracker_tugonlaunch	1961
booster_tracker_launch	4390
booster_tracker_stageandrecovery	4576
booster_tracker_landingzone	20
booster_tracker_pad	65
booster_tracker_padused	6
booster_tracker_stage	364
booster_tracker_spacecraft	22
booster_tracker_rocket	8
booster_tracker_rocketfamily	2
\.


--
-- PostgreSQL database dump complete
--
