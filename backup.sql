--
-- PostgreSQL database dump
--

-- Dumped from database version 14.2
-- Dumped by pg_dump version 14.1

-- Started on 2023-11-11 22:51:51

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
-- TOC entry 209 (class 1259 OID 1087346)
-- Name: admins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admins (
    id integer NOT NULL
);


ALTER TABLE public.admins OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 1087349)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 1087352)
-- Name: conditions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.conditions (
    id integer NOT NULL,
    description text,
    formula json,
    type_task_id integer
);


ALTER TABLE public.conditions OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 1087357)
-- Name: conditions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.conditions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.conditions_id_seq OWNER TO postgres;

--
-- TOC entry 3555 (class 0 OID 0)
-- Dependencies: 212
-- Name: conditions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.conditions_id_seq OWNED BY public.conditions.id;


--
-- TOC entry 213 (class 1259 OID 1087358)
-- Name: employee_skill_links; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employee_skill_links (
    employe_id integer NOT NULL,
    skill_id integer NOT NULL
);


ALTER TABLE public.employee_skill_links OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 1087361)
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    id integer NOT NULL,
    grade_id integer,
    office_id integer
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 1087364)
-- Name: grades; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.grades (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    value integer
);


ALTER TABLE public.grades OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 1087367)
-- Name: grades_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.grades_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.grades_id_seq OWNER TO postgres;

--
-- TOC entry 3556 (class 0 OID 0)
-- Dependencies: 216
-- Name: grades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.grades_id_seq OWNED BY public.grades.id;


--
-- TOC entry 217 (class 1259 OID 1087368)
-- Name: history_tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.history_tasks (
    id integer NOT NULL,
    type json,
    type_id integer,
    point json,
    point_id integer,
    status_id integer,
    employee json,
    employee_id integer,
    date_begin timestamp without time zone,
    date_create timestamp without time zone,
    feedback_value integer,
    feedback_description text
);


ALTER TABLE public.history_tasks OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 1087373)
-- Name: history_tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.history_tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.history_tasks_id_seq OWNER TO postgres;

--
-- TOC entry 3557 (class 0 OID 0)
-- Dependencies: 218
-- Name: history_tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.history_tasks_id_seq OWNED BY public.history_tasks.id;


--
-- TOC entry 219 (class 1259 OID 1087374)
-- Name: managers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.managers (
    id integer NOT NULL
);


ALTER TABLE public.managers OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 1087637)
-- Name: notes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notes (
    id integer NOT NULL,
    user_id integer,
    message text,
    date_create timestamp without time zone
);


ALTER TABLE public.notes OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 1087636)
-- Name: notes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notes_id_seq OWNER TO postgres;

--
-- TOC entry 3558 (class 0 OID 0)
-- Dependencies: 248
-- Name: notes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notes_id_seq OWNED BY public.notes.id;


--
-- TOC entry 220 (class 1259 OID 1087377)
-- Name: office_durations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.office_durations (
    id integer NOT NULL,
    point_id integer,
    office_id integer,
    value integer
);


ALTER TABLE public.office_durations OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 1087380)
-- Name: office_durations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.office_durations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.office_durations_id_seq OWNER TO postgres;

--
-- TOC entry 3559 (class 0 OID 0)
-- Dependencies: 221
-- Name: office_durations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.office_durations_id_seq OWNED BY public.office_durations.id;


--
-- TOC entry 222 (class 1259 OID 1087381)
-- Name: offices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.offices (
    id integer NOT NULL,
    address character varying(255) NOT NULL,
    created_at timestamp without time zone,
    coordinate json,
    img text
);


ALTER TABLE public.offices OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 1087386)
-- Name: offices_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.offices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.offices_id_seq OWNER TO postgres;

--
-- TOC entry 3560 (class 0 OID 0)
-- Dependencies: 223
-- Name: offices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.offices_id_seq OWNED BY public.offices.id;


--
-- TOC entry 224 (class 1259 OID 1087387)
-- Name: point_durations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.point_durations (
    id integer NOT NULL,
    point_id1 integer,
    point_id2 integer,
    value integer
);


ALTER TABLE public.point_durations OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 1087390)
-- Name: point_durations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.point_durations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.point_durations_id_seq OWNER TO postgres;

--
-- TOC entry 3561 (class 0 OID 0)
-- Dependencies: 225
-- Name: point_durations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.point_durations_id_seq OWNED BY public.point_durations.id;


--
-- TOC entry 226 (class 1259 OID 1087391)
-- Name: points; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.points (
    id integer NOT NULL,
    address character varying(255) NOT NULL,
    created_at date,
    coordinate json,
    img text,
    is_delivered_card boolean,
    last_date_issue_card date,
    quantity_requests integer,
    quantity_card integer
);


ALTER TABLE public.points OWNER TO postgres;

--
-- TOC entry 3562 (class 0 OID 0)
-- Dependencies: 226
-- Name: COLUMN points.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.points.created_at IS 'Дата создания';


--
-- TOC entry 3563 (class 0 OID 0)
-- Dependencies: 226
-- Name: COLUMN points.is_delivered_card; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.points.is_delivered_card IS 'Карты были доставлены?';


--
-- TOC entry 3564 (class 0 OID 0)
-- Dependencies: 226
-- Name: COLUMN points.last_date_issue_card; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.points.last_date_issue_card IS 'Последняя дата выдачи карт';


--
-- TOC entry 3565 (class 0 OID 0)
-- Dependencies: 226
-- Name: COLUMN points.quantity_requests; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.points.quantity_requests IS 'Количество заявок';


--
-- TOC entry 3566 (class 0 OID 0)
-- Dependencies: 226
-- Name: COLUMN points.quantity_card; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.points.quantity_card IS 'Количество выданных карт';


--
-- TOC entry 227 (class 1259 OID 1087396)
-- Name: points_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.points_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.points_id_seq OWNER TO postgres;

--
-- TOC entry 3567 (class 0 OID 0)
-- Dependencies: 227
-- Name: points_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.points_id_seq OWNED BY public.points.id;


--
-- TOC entry 228 (class 1259 OID 1087397)
-- Name: priorities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.priorities (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    value integer NOT NULL
);


ALTER TABLE public.priorities OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 1087400)
-- Name: priorities_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.priorities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.priorities_id_seq OWNER TO postgres;

--
-- TOC entry 3568 (class 0 OID 0)
-- Dependencies: 229
-- Name: priorities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.priorities_id_seq OWNED BY public.priorities.id;


--
-- TOC entry 230 (class 1259 OID 1087401)
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    is_public boolean
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 1087404)
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roles_id_seq OWNER TO postgres;

--
-- TOC entry 3569 (class 0 OID 0)
-- Dependencies: 231
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- TOC entry 232 (class 1259 OID 1087405)
-- Name: skills; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skills (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.skills OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 1087408)
-- Name: skills_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.skills_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.skills_id_seq OWNER TO postgres;

--
-- TOC entry 3570 (class 0 OID 0)
-- Dependencies: 233
-- Name: skills_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.skills_id_seq OWNED BY public.skills.id;


--
-- TOC entry 234 (class 1259 OID 1087409)
-- Name: task_statusess; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_statusess (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    in_history boolean
);


ALTER TABLE public.task_statusess OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 1087412)
-- Name: task_statusess_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_statusess_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_statusess_id_seq OWNER TO postgres;

--
-- TOC entry 3571 (class 0 OID 0)
-- Dependencies: 235
-- Name: task_statusess_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.task_statusess_id_seq OWNED BY public.task_statusess.id;


--
-- TOC entry 236 (class 1259 OID 1087413)
-- Name: tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    type_id integer,
    point_id integer,
    status_id integer,
    date_begin timestamp without time zone,
    date_create timestamp without time zone,
    priority_id integer,
    employee_id integer
);


ALTER TABLE public.tasks OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 1087416)
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_id_seq OWNER TO postgres;

--
-- TOC entry 3572 (class 0 OID 0)
-- Dependencies: 237
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- TOC entry 238 (class 1259 OID 1087417)
-- Name: traffics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.traffics (
    id integer NOT NULL,
    hour integer,
    level integer
);


ALTER TABLE public.traffics OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 1087420)
-- Name: traffics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.traffics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.traffics_id_seq OWNER TO postgres;

--
-- TOC entry 3573 (class 0 OID 0)
-- Dependencies: 239
-- Name: traffics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.traffics_id_seq OWNED BY public.traffics.id;


--
-- TOC entry 240 (class 1259 OID 1087421)
-- Name: type_task_grade_links; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.type_task_grade_links (
    type_task_id integer NOT NULL,
    grade_id integer NOT NULL
);


ALTER TABLE public.type_task_grade_links OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 1087424)
-- Name: type_task_skill_links; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.type_task_skill_links (
    type_task_id integer NOT NULL,
    skill_id integer NOT NULL
);


ALTER TABLE public.type_task_skill_links OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 1087427)
-- Name: type_tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.type_tasks (
    id integer NOT NULL,
    name character varying(255),
    priority_id integer,
    duration double precision NOT NULL,
    details json,
    interval_block integer NOT NULL
);


ALTER TABLE public.type_tasks OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 1087432)
-- Name: type_tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.type_tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.type_tasks_id_seq OWNER TO postgres;

--
-- TOC entry 3574 (class 0 OID 0)
-- Dependencies: 243
-- Name: type_tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.type_tasks_id_seq OWNED BY public.type_tasks.id;


--
-- TOC entry 244 (class 1259 OID 1087433)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(320) NOT NULL,
    hashed_password character varying(1024) NOT NULL,
    firstname character varying(100),
    lastname character varying(100),
    patronymic character varying(100),
    img text,
    created_at timestamp without time zone,
    role_id integer,
    is_active boolean
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 1087438)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 3575 (class 0 OID 0)
-- Dependencies: 245
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 246 (class 1259 OID 1087439)
-- Name: vakt_policies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vakt_policies (
    id integer NOT NULL,
    resources json,
    actions json,
    subjects json,
    description text
);


ALTER TABLE public.vakt_policies OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 1087444)
-- Name: vakt_policies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.vakt_policies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.vakt_policies_id_seq OWNER TO postgres;

--
-- TOC entry 3576 (class 0 OID 0)
-- Dependencies: 247
-- Name: vakt_policies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.vakt_policies_id_seq OWNED BY public.vakt_policies.id;


--
-- TOC entry 3272 (class 2604 OID 1087445)
-- Name: conditions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conditions ALTER COLUMN id SET DEFAULT nextval('public.conditions_id_seq'::regclass);


--
-- TOC entry 3273 (class 2604 OID 1087446)
-- Name: grades id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades ALTER COLUMN id SET DEFAULT nextval('public.grades_id_seq'::regclass);


--
-- TOC entry 3274 (class 2604 OID 1087447)
-- Name: history_tasks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.history_tasks ALTER COLUMN id SET DEFAULT nextval('public.history_tasks_id_seq'::regclass);


--
-- TOC entry 3288 (class 2604 OID 1087640)
-- Name: notes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notes ALTER COLUMN id SET DEFAULT nextval('public.notes_id_seq'::regclass);


--
-- TOC entry 3275 (class 2604 OID 1087448)
-- Name: office_durations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.office_durations ALTER COLUMN id SET DEFAULT nextval('public.office_durations_id_seq'::regclass);


--
-- TOC entry 3276 (class 2604 OID 1087449)
-- Name: offices id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.offices ALTER COLUMN id SET DEFAULT nextval('public.offices_id_seq'::regclass);


--
-- TOC entry 3277 (class 2604 OID 1087450)
-- Name: point_durations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.point_durations ALTER COLUMN id SET DEFAULT nextval('public.point_durations_id_seq'::regclass);


--
-- TOC entry 3278 (class 2604 OID 1087451)
-- Name: points id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.points ALTER COLUMN id SET DEFAULT nextval('public.points_id_seq'::regclass);


--
-- TOC entry 3279 (class 2604 OID 1087452)
-- Name: priorities id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.priorities ALTER COLUMN id SET DEFAULT nextval('public.priorities_id_seq'::regclass);


--
-- TOC entry 3280 (class 2604 OID 1087453)
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- TOC entry 3281 (class 2604 OID 1087454)
-- Name: skills id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skills ALTER COLUMN id SET DEFAULT nextval('public.skills_id_seq'::regclass);


--
-- TOC entry 3282 (class 2604 OID 1087455)
-- Name: task_statusess id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_statusess ALTER COLUMN id SET DEFAULT nextval('public.task_statusess_id_seq'::regclass);


--
-- TOC entry 3283 (class 2604 OID 1087456)
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- TOC entry 3284 (class 2604 OID 1087457)
-- Name: traffics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.traffics ALTER COLUMN id SET DEFAULT nextval('public.traffics_id_seq'::regclass);


--
-- TOC entry 3285 (class 2604 OID 1087458)
-- Name: type_tasks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.type_tasks ALTER COLUMN id SET DEFAULT nextval('public.type_tasks_id_seq'::regclass);


--
-- TOC entry 3286 (class 2604 OID 1087459)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 3287 (class 2604 OID 1087460)
-- Name: vakt_policies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vakt_policies ALTER COLUMN id SET DEFAULT nextval('public.vakt_policies_id_seq'::regclass);


--
-- TOC entry 3509 (class 0 OID 1087346)
-- Dependencies: 209
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admins (id) FROM stdin;
1
\.


--
-- TOC entry 3510 (class 0 OID 1087349)
-- Dependencies: 210
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
c0864d8e2957
\.


--
-- TOC entry 3511 (class 0 OID 1087352)
-- Dependencies: 211
-- Data for Name: conditions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.conditions (id, description, formula, type_task_id) FROM stdin;
7	Карты и материалы не доставлялись	{"is_delivered_card": false}	3
8	Отношение кол-ва выданных карт к одобренным заявкам менее 50%, если выдано больше 0 карт	{"quantity_card": {"$\\u0431\\u043e\\u043b\\u044c\\u0448\\u0435": 0}, "$\\u0434\\u0435\\u043b\\u0435\\u043d\\u0438\\u0435": {"$\\u0430\\u0440\\u04331": "quantity_card", "$\\u0430\\u0440\\u04332": "quantity_requests", "$\\u043c\\u0435\\u043d\\u044c\\u0448\\u0435": 0.5}}	2
6	Точка подключена вчера	{"created_at": {"$ровно_n_дней_назад": 1}}	3
9	Дата выдачи последней карты более 7 дней назад, при этом есть одобренные заявки (разница между одобренными заявками и картами)	{"last_date_issue_card": {"$меньше_n_дней": 7}, "$вычитание": {"$арг1": "quantity_requests", "$арг2": "quantity_card", "$больше": 0}}	1
10	Дата выдачи последней карты более 14 дней назад	{"last_date_issue_card": {"$меньше_n_дней": 14}}	1
\.


--
-- TOC entry 3513 (class 0 OID 1087358)
-- Dependencies: 213
-- Data for Name: employee_skill_links; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employee_skill_links (employe_id, skill_id) FROM stdin;
15	1
15	4
15	6
16	9
16	10
16	12
17	13
17	7
17	3
19	3
19	9
20	11
20	8
21	6
21	1
22	8
22	11
23	8
23	3
\.


--
-- TOC entry 3514 (class 0 OID 1087361)
-- Dependencies: 214
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employees (id, grade_id, office_id) FROM stdin;
15	1	1
16	2	1
17	3	1
19	1	2
20	2	2
21	3	2
22	2	3
23	3	3
\.


--
-- TOC entry 3515 (class 0 OID 1087364)
-- Dependencies: 215
-- Data for Name: grades; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.grades (id, name, value) FROM stdin;
1	Синьор	3
2	Мидл	2
3	Джун	1
\.


--
-- TOC entry 3517 (class 0 OID 1087368)
-- Dependencies: 217
-- Data for Name: history_tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.history_tasks (id, type, type_id, point, point_id, status_id, employee, employee_id, date_begin, date_create, feedback_value, feedback_description) FROM stdin;
\.


--
-- TOC entry 3519 (class 0 OID 1087374)
-- Dependencies: 219
-- Data for Name: managers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.managers (id) FROM stdin;
18
\.


--
-- TOC entry 3549 (class 0 OID 1087637)
-- Dependencies: 249
-- Data for Name: notes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notes (id, user_id, message, date_create) FROM stdin;
30	16	Вам назначены новые задачи, зайдите в личный кабинет	2023-11-11 19:50:16.888318
31	23	Вам назначены новые задачи, зайдите в личный кабинет	2023-11-11 19:50:16.901719
32	15	Вам назначены новые задачи, зайдите в личный кабинет	2023-11-11 19:50:16.908919
33	19	Вам назначены новые задачи, зайдите в личный кабинет	2023-11-11 19:50:16.915895
34	22	Вам назначены новые задачи, зайдите в личный кабинет	2023-11-11 19:50:16.924773
35	17	Вам назначены новые задачи, зайдите в личный кабинет	2023-11-11 19:50:16.931325
36	21	Вам назначены новые задачи, зайдите в личный кабинет	2023-11-11 19:50:16.93734
37	20	Вам назначены новые задачи, зайдите в личный кабинет	2023-11-11 19:50:16.945385
\.


--
-- TOC entry 3520 (class 0 OID 1087377)
-- Dependencies: 220
-- Data for Name: office_durations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.office_durations (id, point_id, office_id, value) FROM stdin;
673	1	1	1183
674	4	1	225
675	6	1	1808
676	7	1	1846
677	8	1	393
678	9	1	1214
679	10	1	592
680	11	1	3095
681	13	1	1726
682	15	1	1639
683	19	1	1726
684	20	1	1398
685	22	1	1867
686	24	1	496
687	26	1	1563
688	27	1	1852
689	28	1	1601
690	29	1	1983
691	30	1	1602
692	34	1	1618
693	37	1	355
694	40	1	1063
695	41	1	268
696	43	1	333
697	12	1	507
698	5	1	2462
699	38	1	1147
700	25	1	638
701	21	1	471
702	16	1	1869
703	44	1	242
704	33	1	1396
705	31	1	296
706	2	1	638
707	3	1	616
708	39	1	503
709	32	1	253
710	36	1	1705
711	14	1	2754
712	35	1	1819
713	1	2	1178
714	4	2	1735
715	6	2	538
716	7	2	1742
717	8	2	1720
718	9	2	1033
719	10	2	2081
720	11	2	4193
721	13	2	574
722	15	2	1667
723	19	2	1898
724	20	2	1599
725	22	2	1749
726	24	2	1663
727	26	2	1721
728	27	2	595
729	28	2	1628
730	29	2	2112
731	30	2	1697
732	34	2	1749
733	37	2	1792
734	40	2	1690
735	41	2	1675
736	43	2	1614
737	12	2	1828
738	5	2	1777
739	38	2	2090
740	25	2	1646
741	21	2	1616
742	16	2	1877
743	44	2	1689
744	33	2	1454
745	31	2	1753
746	2	2	1363
747	3	2	2067
748	39	2	2063
749	32	2	1595
750	36	2	1853
751	14	2	2763
752	35	2	1672
753	1	3	751
754	4	3	516
755	6	3	1662
756	7	3	1614
757	8	3	563
758	9	3	918
759	10	3	882
760	11	3	2866
761	13	3	1584
762	15	3	1395
763	19	3	1593
764	20	3	1324
765	22	3	1551
766	24	3	472
767	26	3	1485
768	27	3	1630
769	28	3	1236
770	29	3	1704
771	30	3	1628
772	34	3	1483
773	37	3	512
774	40	3	1297
775	41	3	524
776	43	3	642
777	12	3	477
778	5	3	2268
779	38	3	1383
780	25	3	511
781	21	3	538
782	16	3	1824
783	44	3	384
784	33	3	1264
785	31	3	626
786	2	3	350
787	3	3	1030
788	39	3	884
789	32	3	424
790	36	3	1475
791	14	3	2555
792	35	3	1473
\.


--
-- TOC entry 3522 (class 0 OID 1087381)
-- Dependencies: 222
-- Data for Name: offices; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.offices (id, address, created_at, coordinate, img) FROM stdin;
1	Краснодар, Красная, д. 139	2023-11-05 19:02:07.570743	{"y": 38.977131, "x": 45.044942}	\N
2	Краснодар, В.Н. Мачуги, 41	2023-11-05 21:58:03.588725	{"y": 39.071919, "x": 45.012762}	\N
3	Краснодар, Красных Партизан, 321	2023-11-05 21:58:14.978678	{"y": 38.941967, "x": 45.053632}	\N
\.


--
-- TOC entry 3524 (class 0 OID 1087387)
-- Dependencies: 224
-- Data for Name: point_durations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.point_durations (id, point_id1, point_id2, value) FROM stdin;
5629	1	4	1105
5630	4	1	1109
5631	1	6	1144
5632	6	1	1591
5633	1	7	942
5634	7	1	875
5635	1	8	1096
5636	8	1	1185
5637	1	9	168
5638	9	1	67
5639	1	10	1068
5640	10	1	1221
5641	1	11	3485
5642	11	1	3483
5643	1	13	1247
5644	13	1	1527
5645	1	15	878
5646	15	1	998
5647	1	19	926
5648	19	1	803
5649	1	20	612
5650	20	1	488
5651	1	22	847
5652	22	1	1015
5653	1	24	1154
5654	24	1	1059
5655	1	26	906
5656	26	1	946
5657	1	27	1283
5658	27	1	1517
5659	1	28	696
5660	28	1	604
5661	1	29	1143
5662	29	1	1002
5663	1	30	871
5664	30	1	883
5665	1	34	973
5666	34	1	964
5667	1	37	1261
5668	37	1	1160
5669	1	40	697
5670	40	1	587
5671	1	41	1009
5672	41	1	1181
5673	1	43	1163
5674	43	1	1149
5675	1	12	1270
5676	12	1	1049
5677	1	5	1982
5678	5	1	1975
5679	1	38	1232
5680	38	1	1191
5681	1	25	1159
5682	25	1	1146
5683	1	21	1047
5684	21	1	1044
5685	1	16	1322
5686	16	1	1327
5687	1	44	1028
5688	44	1	1132
5689	1	33	665
5690	33	1	472
5691	1	31	1284
5692	31	1	1199
5693	1	2	653
5694	2	1	664
5695	1	3	943
5696	3	1	1154
5697	1	39	1117
5698	39	1	931
5699	1	32	1007
5700	32	1	1093
5701	1	36	915
5702	36	1	959
5703	1	14	1993
5704	14	1	1857
5705	1	35	1164
5706	35	1	1308
5707	4	6	1721
5708	6	4	2052
5709	4	7	1759
5710	7	4	1777
5711	4	8	327
5712	8	4	520
5713	4	9	1121
5714	9	4	1111
5715	4	10	560
5716	10	4	505
5717	4	11	3176
5718	11	4	3057
5719	4	13	1898
5720	13	4	1947
5721	4	15	1617
5722	15	4	1500
5723	4	19	1745
5724	19	4	1748
5725	4	20	1410
5726	20	4	1325
5727	4	22	1874
5728	22	4	1911
5729	4	24	462
5730	24	4	434
5731	4	26	1627
5732	26	4	1641
5733	4	27	1850
5734	27	4	2036
5735	4	28	1565
5736	28	4	1558
5737	4	29	1873
5738	29	4	1888
5739	4	30	1656
5740	30	4	1784
5741	4	34	1595
5742	34	4	1608
5743	4	37	353
5744	37	4	329
5745	4	40	1097
5746	40	4	1131
5747	4	41	193
5748	41	4	276
5749	4	43	173
5750	43	4	172
5751	4	12	517
5752	12	4	493
5753	4	5	2581
5754	5	4	2613
5755	4	38	976
5756	38	4	1084
5757	4	25	792
5758	25	4	767
5759	4	21	545
5760	21	4	474
5761	4	16	1923
5762	16	4	2023
5763	4	44	287
5764	44	4	291
5765	4	33	1520
5766	33	4	1355
5767	4	31	246
5768	31	4	247
5769	4	2	726
5770	2	4	747
5771	4	3	624
5772	3	4	558
5773	4	39	600
5774	39	4	641
5775	4	32	87
5776	32	4	226
5777	4	36	1625
5778	36	4	1766
5779	4	14	2919
5780	14	4	2737
5781	4	35	1688
5782	35	4	1768
5783	6	7	2144
5784	7	6	1872
5785	6	8	2061
5786	8	6	1876
5787	6	9	1409
5788	9	6	1243
5789	6	10	2271
5790	10	6	2137
5791	6	11	4493
5792	11	6	4276
5793	6	13	81
5794	13	6	292
5795	6	15	1967
5796	15	6	1647
5797	6	19	2163
5798	19	6	1973
5799	6	20	1995
5800	20	6	1631
5801	6	22	2233
5802	22	6	1930
5803	6	24	2080
5804	24	6	1898
5805	6	26	2104
5806	26	6	1872
5807	6	27	177
5808	27	6	143
5809	6	28	1991
5810	28	6	1788
5811	6	29	2466
5812	29	6	2002
5813	6	30	2155
5814	30	6	1826
5815	6	34	2136
5816	34	6	1957
5817	6	37	2030
5818	37	6	1826
5819	6	40	1957
5820	40	6	1720
5821	6	41	2049
5822	41	6	1722
5823	6	43	1984
5824	43	6	1899
5825	6	12	2228
5826	12	6	1845
5827	6	5	2042
5828	5	6	2560
5829	6	38	2379
5830	38	6	2224
5831	6	25	1914
5832	25	6	1658
5833	6	21	2175
5834	21	6	1826
5835	6	16	2436
5836	16	6	2177
5837	6	44	2017
5838	44	6	1694
5839	6	33	1938
5840	33	6	1699
5841	6	31	2114
5842	31	6	1984
5843	6	2	1731
5844	2	6	1445
5845	6	3	2297
5846	3	6	2143
5847	6	39	2376
5848	39	6	2103
5849	6	32	1959
5850	32	6	1768
5851	6	36	2078
5852	36	6	2009
5853	6	14	3301
5854	14	6	2873
5855	6	35	2093
5856	35	6	1900
5857	7	8	1700
5858	8	7	1713
5859	7	9	903
5860	9	7	813
5861	7	10	1622
5862	10	7	1457
5863	7	11	4213
5864	11	7	4264
5865	7	13	1982
5866	13	7	2290
5867	7	15	1675
5868	15	7	1589
5869	7	19	1181
5870	19	7	1332
5871	7	20	989
5872	20	7	988
5873	7	22	356
5874	22	7	439
5875	7	24	1778
5876	24	7	1781
5877	7	26	1181
5878	26	7	1365
5879	7	27	1942
5880	27	7	2162
5881	7	28	1176
5882	28	7	1120
5883	7	29	629
5884	29	7	712
5885	7	30	1247
5886	30	7	1282
5887	7	34	1279
5888	34	7	1306
5889	7	37	1858
5890	37	7	1778
5891	7	40	1013
5892	40	7	958
5893	7	41	1706
5894	41	7	1818
5895	7	43	1904
5896	43	7	1790
5897	7	12	1852
5898	12	7	1798
5899	7	5	2662
5900	5	7	2748
5901	7	38	1679
5902	38	7	1568
5903	7	25	1859
5904	25	7	1793
5905	7	21	1882
5906	21	7	1777
5907	7	16	2102
5908	16	7	2156
5909	7	44	1677
5910	44	7	1775
5911	7	33	884
5912	33	7	930
5913	7	31	1628
5914	31	7	1714
5915	7	2	1359
5916	2	7	1490
5917	7	3	1391
5918	3	7	1434
5919	7	39	1417
5920	39	7	1414
5921	7	32	1694
5922	32	7	1757
5923	7	36	1315
5924	36	7	1370
5925	7	14	1579
5926	14	7	1515
5927	7	35	1966
5928	35	7	1836
5929	8	9	1078
5930	9	8	1153
5931	8	10	723
5932	10	8	619
5933	8	11	3132
5934	11	8	3079
5935	8	13	1746
5936	13	8	2134
5937	8	15	1454
5938	15	8	1654
5939	8	19	1755
5940	19	8	1892
5941	8	20	1459
5942	20	8	1532
5943	8	22	1836
5944	22	8	1871
5945	8	24	288
5946	24	8	203
5947	8	26	1793
5948	26	8	1719
5949	8	27	1711
5950	27	8	1970
5951	8	28	1653
5952	28	8	1572
5953	8	29	1999
5954	29	8	1930
5955	8	30	1731
5956	30	8	1764
5957	8	34	1673
5958	34	8	1748
5959	8	37	443
5960	37	8	449
5961	8	40	1254
5962	40	8	1138
5963	8	41	394
5964	41	8	330
5965	8	43	467
5966	43	8	384
5967	8	12	213
5968	12	8	214
5969	8	5	2452
5970	5	8	2604
5971	8	38	1339
5972	38	8	1343
5973	8	25	719
5974	25	8	755
5975	8	21	311
5976	21	8	115
5977	8	16	1953
5978	16	8	2077
5979	8	44	361
5980	44	8	323
5981	8	33	1586
5982	33	8	1536
5983	8	31	679
5984	31	8	563
5985	8	2	738
5986	2	8	721
5987	8	3	898
5988	3	8	843
5989	8	39	773
5990	39	8	944
5991	8	32	448
5992	32	8	320
5993	8	36	1702
5994	36	8	1883
5995	8	14	2927
5996	14	8	2873
5997	8	35	1687
5998	35	8	1803
5999	9	10	1166
6000	10	9	1053
6001	9	11	3538
6002	11	9	3512
6003	9	13	1293
6004	13	9	1430
6005	9	15	986
6006	15	9	938
6007	9	19	902
6008	19	9	904
6009	9	20	699
6010	20	9	511
6011	9	22	876
6012	22	9	861
6013	9	24	1166
6014	24	9	978
6015	9	26	878
6016	26	9	901
6017	9	27	1368
6018	27	9	1615
6019	9	28	614
6020	28	9	571
6021	9	29	957
6022	29	9	960
6023	9	30	947
6024	30	9	730
6025	9	34	901
6026	34	9	878
6027	9	37	1190
6028	37	9	1047
6029	9	40	613
6030	40	9	620
6031	9	41	966
6032	41	9	983
6033	9	43	1189
6034	43	9	1124
6035	9	12	1258
6036	12	9	1273
6037	9	5	1969
6038	5	9	1981
6039	9	38	1191
6040	38	9	1083
6041	9	25	1082
6042	25	9	1019
6043	9	21	1194
6044	21	9	1104
6045	9	16	1388
6046	16	9	1486
6047	9	44	1193
6048	44	9	1134
6049	9	33	523
6050	33	9	573
6051	9	31	1137
6052	31	9	1298
6053	9	2	747
6054	2	9	679
6055	9	3	1034
6056	3	9	1017
6057	9	39	1025
6058	39	9	982
6059	9	32	992
6060	32	9	1117
6061	9	36	739
6062	36	9	777
6063	9	14	1980
6064	14	9	2030
6065	9	35	1329
6066	35	9	1238
6067	10	11	3497
6068	11	10	3543
6069	10	13	2102
6070	13	10	2327
6071	10	15	1764
6072	15	10	1859
6073	10	19	1357
6074	19	10	1407
6075	10	20	1085
6076	20	10	1126
6077	10	22	1682
6078	22	10	1665
6079	10	24	707
6080	24	10	771
6081	10	26	1287
6082	26	10	1310
6083	10	27	2159
6084	27	10	2463
6085	10	28	1213
6086	28	10	1056
6087	10	29	1709
6088	29	10	1780
6089	10	30	1287
6090	30	10	1323
6091	10	34	1437
6092	34	10	1437
6093	10	37	351
6094	37	10	402
6095	10	40	677
6096	40	10	646
6097	10	41	489
6098	41	10	572
6099	10	43	513
6100	43	10	523
6101	10	12	778
6102	12	10	860
6103	10	5	2910
6104	5	10	2780
6105	10	38	654
6106	38	10	781
6107	10	25	953
6108	25	10	1034
6109	10	21	699
6110	21	10	681
6111	10	16	2359
6112	16	10	2309
6113	10	44	428
6114	44	10	496
6115	10	33	1184
6116	33	10	1103
6117	10	31	278
6118	31	10	316
6119	10	2	970
6120	2	10	865
6121	10	3	253
6122	3	10	379
6123	10	39	222
6124	39	10	296
6125	10	32	636
6126	32	10	435
6127	10	36	1318
6128	36	10	1424
6129	10	14	2566
6130	14	10	2586
6131	10	35	2060
6132	35	10	1994
6133	11	13	4205
6134	13	11	4426
6135	11	15	3908
6136	15	11	3938
6137	11	19	4108
6138	19	11	4184
6139	11	20	3900
6140	20	11	3976
6141	11	22	4287
6142	22	11	4229
6143	11	24	3136
6144	24	11	3219
6145	11	26	4107
6146	26	11	4097
6147	11	27	4275
6148	27	11	4497
6149	11	28	4071
6150	28	11	3998
6151	11	29	4375
6152	29	11	4355
6153	11	30	4168
6154	30	11	4162
6155	11	34	4169
6156	34	11	4246
6157	11	37	3121
6158	37	11	3304
6159	11	40	3909
6160	40	11	3935
6161	11	41	3225
6162	41	11	3196
6163	11	43	3339
6164	43	11	3265
6165	11	12	3309
6166	12	11	3232
6167	11	5	4810
6168	5	11	4881
6169	11	38	3948
6170	38	11	4099
6171	11	25	2705
6172	25	11	2714
6173	11	21	3196
6174	21	11	3113
6175	11	16	4324
6176	16	11	4377
6177	11	44	3131
6178	44	11	3131
6179	11	33	3981
6180	33	11	4005
6181	11	31	3405
6182	31	11	3445
6183	11	2	3150
6184	2	11	3175
6185	11	3	3519
6186	3	11	3684
6187	11	39	3500
6188	39	11	3647
6189	11	32	3101
6190	32	11	3122
6191	11	36	4260
6192	36	11	4248
6193	11	14	5401
6194	14	11	5261
6195	11	35	4232
6196	35	11	4319
6197	13	15	1874
6198	15	13	1780
6199	13	19	2244
6200	19	13	1890
6201	13	20	1856
6202	20	13	1688
6203	13	22	2347
6204	22	13	1989
6205	13	24	1946
6206	24	13	1697
6207	13	26	2081
6208	26	13	1950
6209	13	27	235
6210	27	13	93
6211	13	28	1974
6212	28	13	1640
6213	13	29	2404
6214	29	13	2104
6215	13	30	2115
6216	30	13	1852
6217	13	34	2213
6218	34	13	1978
6219	13	37	2204
6220	37	13	1814
6221	13	40	1924
6222	40	13	1785
6223	13	41	2042
6224	41	13	1824
6225	13	43	2083
6226	43	13	1789
6227	13	12	2087
6228	12	13	1834
6229	13	5	2171
6230	5	13	2522
6231	13	38	2597
6232	38	13	2193
6233	13	25	2015
6234	25	13	1895
6235	13	21	2074
6236	21	13	1921
6237	13	16	2360
6238	16	13	2179
6239	13	44	2133
6240	44	13	1764
6241	13	33	1999
6242	33	13	1723
6243	13	31	2327
6244	31	13	2071
6245	13	2	1757
6246	2	13	1497
6247	13	3	2287
6248	3	13	2030
6249	13	39	2281
6250	39	13	2163
6251	13	32	2140
6252	32	13	1730
6253	13	36	2112
6254	36	13	1822
6255	13	14	3210
6256	14	13	2887
6257	13	35	2235
6258	35	13	1984
6259	15	19	1583
6260	19	15	1794
6261	15	20	1313
6262	20	15	1369
6263	15	22	1839
6264	22	15	1639
6265	15	24	1595
6266	24	15	1640
6267	15	26	1550
6268	26	15	1740
6269	15	27	1740
6270	27	15	1982
6271	15	28	1594
6272	28	15	1406
6273	15	29	1939
6274	29	15	1950
6275	15	30	1558
6276	30	15	1602
6277	15	34	1684
6278	34	15	1716
6279	15	37	1713
6280	37	15	1734
6281	15	40	1489
6282	40	15	1492
6283	15	41	1609
6284	41	15	1475
6285	15	43	1731
6286	43	15	1546
6287	15	12	1519
6288	12	15	1740
6289	15	5	2267
6290	5	15	2395
6291	15	38	2060
6292	38	15	2083
6293	15	25	1517
6294	25	15	1526
6295	15	21	1569
6296	21	15	1508
6297	15	16	688
6298	16	15	552
6299	15	44	1467
6300	44	15	1428
6301	15	33	1356
6302	33	15	1370
6303	15	31	1696
6304	31	15	1806
6305	15	2	1155
6306	2	15	1283
6307	15	3	1799
6308	3	15	1757
6309	15	39	1785
6310	39	15	1965
6311	15	32	1422
6312	32	15	1607
6313	15	36	1791
6314	36	15	1725
6315	15	14	2771
6316	14	15	2857
6317	15	35	321
6318	35	15	324
6319	19	20	568
6320	20	19	535
6321	19	22	1410
6322	22	19	1346
6323	19	24	1717
6324	24	19	1726
6325	19	26	483
6326	26	19	578
6327	19	27	1937
6328	27	19	2112
6329	19	28	475
6330	28	19	362
6331	19	29	1423
6332	29	19	1484
6333	19	30	612
6334	30	19	629
6335	19	34	488
6336	34	19	547
6337	19	37	1552
6338	37	19	1736
6339	19	40	877
6340	40	19	942
6341	19	41	1628
6342	41	19	1816
6343	19	43	1630
6344	43	19	1622
6345	19	12	1836
6346	12	19	1751
6347	19	5	2502
6348	5	19	2562
6349	19	38	1302
6350	38	19	1282
6351	19	25	1773
6352	25	19	1797
6353	19	21	1782
6354	21	19	1770
6355	19	16	2176
6356	16	19	2197
6357	19	44	1753
6358	44	19	1788
6359	19	33	485
6360	33	19	516
6361	19	31	1597
6362	31	19	1543
6363	19	2	1469
6364	2	19	1414
6365	19	3	1231
6366	3	19	1367
6367	19	39	1124
6368	39	19	1263
6369	19	32	1756
6370	32	19	1769
6371	19	36	459
6372	36	19	641
6373	19	14	2318
6374	14	19	2416
6375	19	35	1974
6376	35	19	1971
6377	20	22	1152
6378	22	20	1032
6379	20	24	1578
6380	24	20	1573
6381	20	26	441
6382	26	20	548
6383	20	27	1776
6384	27	20	1917
6385	20	28	269
6386	28	20	272
6387	20	29	1198
6388	29	20	1105
6389	20	30	499
6390	30	20	368
6391	20	34	583
6392	34	20	444
6393	20	37	1221
6394	37	20	1221
6395	20	40	628
6396	40	20	515
6397	20	41	1355
6398	41	20	1381
6399	20	43	1275
6400	43	20	1354
6401	20	12	1591
6402	12	20	1659
6403	20	5	2236
6404	5	20	2501
6405	20	38	951
6406	38	20	1176
6407	20	25	1602
6408	25	20	1532
6409	20	21	1501
6410	21	20	1528
6411	20	16	1916
6412	16	20	1733
6413	20	44	1401
6414	44	20	1435
6415	20	33	206
6416	33	20	218
6417	20	31	1157
6418	31	20	1276
6419	20	2	1134
6420	2	20	1281
6421	20	3	1053
6422	3	20	995
6423	20	39	917
6424	39	20	843
6425	20	32	1363
6426	32	20	1308
6427	20	36	404
6428	36	20	566
6429	20	14	2157
6430	14	20	2103
6431	20	35	1650
6432	35	20	1668
6433	22	24	1829
6434	24	22	1770
6435	22	26	1282
6436	26	22	1292
6437	22	27	1969
6438	27	22	2132
6439	22	28	1009
6440	28	22	992
6441	22	29	832
6442	29	22	870
6443	22	30	1341
6444	30	22	1235
6445	22	34	1396
6446	34	22	1240
6447	22	37	1884
6448	37	22	1898
6449	22	40	1191
6450	40	22	1102
6451	22	41	1692
6452	41	22	1850
6453	22	43	1756
6454	43	22	1759
6455	22	12	1874
6456	12	22	1954
6457	22	5	2582
6458	5	22	2812
6459	22	38	1681
6460	38	22	1710
6461	22	25	1711
6462	25	22	1829
6463	22	21	1956
6464	21	22	1979
6465	22	16	2036
6466	16	22	2196
6467	22	44	1853
6468	44	22	1757
6469	22	33	1119
6470	33	22	1101
6471	22	31	1665
6472	31	22	1794
6473	22	2	1543
6474	2	22	1534
6475	22	3	1616
6476	3	22	1485
6477	22	39	1414
6478	39	22	1479
6479	22	32	1701
6480	32	22	1847
6481	22	36	1301
6482	36	22	1254
6483	22	14	1212
6484	14	22	1108
6485	22	35	1989
6486	35	22	1920
6487	24	26	1808
6488	26	24	1808
6489	24	27	1799
6490	27	24	2070
6491	24	28	1601
6492	28	24	1552
6493	24	29	2001
6494	29	24	1887
6495	24	30	1790
6496	30	24	1699
6497	24	34	1697
6498	34	24	1817
6499	24	37	487
6500	37	24	438
6501	24	40	1346
6502	40	24	1198
6503	24	41	385
6504	41	24	269
6505	24	43	555
6506	43	24	486
6507	24	12	146
6508	12	24	147
6509	24	5	2462
6510	5	24	2582
6511	24	38	1156
6512	38	24	1355
6513	24	25	778
6514	25	24	736
6515	24	21	352
6516	21	24	200
6517	24	16	1937
6518	16	24	1894
6519	24	44	484
6520	44	24	329
6521	24	33	1349
6522	33	24	1512
6523	24	31	520
6524	31	24	541
6525	24	2	590
6526	2	24	689
6527	24	3	948
6528	3	24	852
6529	24	39	730
6530	39	24	871
6531	24	32	348
6532	32	24	334
6533	24	36	1755
6534	36	24	1778
6535	24	14	2801
6536	14	24	2937
6537	24	35	1666
6538	35	24	1719
6539	26	27	1893
6540	27	26	2135
6541	26	28	373
6542	28	26	312
6543	26	29	1395
6544	29	26	1359
6545	26	30	112
6546	30	26	167
6547	26	34	234
6548	34	26	124
6549	26	37	1487
6550	37	26	1668
6551	26	40	744
6552	40	26	911
6553	26	41	1664
6554	41	26	1613
6555	26	43	1679
6556	43	26	1489
6557	26	12	1787
6558	12	26	1769
6559	26	5	2548
6560	5	26	2525
6561	26	38	1271
6562	38	26	1449
6563	26	25	1765
6564	25	26	1770
6565	26	21	1762
6566	21	26	1791
6567	26	16	2128
6568	16	26	2146
6569	26	44	1743
6570	44	26	1787
6571	26	33	446
6572	33	26	545
6573	26	31	1425
6574	31	26	1532
6575	26	2	1451
6576	2	26	1491
6577	26	3	1293
6578	3	26	1199
6579	26	39	1210
6580	39	26	1245
6581	26	32	1724
6582	32	26	1747
6583	26	36	279
6584	36	26	157
6585	26	14	2263
6586	14	26	2336
6587	26	35	1919
6588	35	26	1813
6589	27	28	1901
6590	28	27	1735
6591	27	29	2290
6592	29	27	2153
6593	27	30	2133
6594	30	27	2015
6595	27	34	2196
6596	34	27	1884
6597	27	37	2190
6598	37	27	1919
6599	27	40	1868
6600	40	27	1807
6601	27	41	2053
6602	41	27	1732
6603	27	43	2181
6604	43	27	1948
6605	27	12	2137
6606	12	27	1900
6607	27	5	2132
6608	5	27	2575
6609	27	38	2379
6610	38	27	2321
6611	27	25	1975
6612	25	27	1880
6613	27	21	2044
6614	21	27	1828
6615	27	16	2344
6616	16	27	2123
6617	27	44	2122
6618	44	27	1682
6619	27	33	1961
6620	33	27	1673
6621	27	31	2167
6622	31	27	2010
6623	27	2	1784
6624	2	27	1482
6625	27	3	2372
6626	3	27	2114
6627	27	39	2460
6628	39	27	2135
6629	27	32	1921
6630	32	27	1685
6631	27	36	2174
6632	36	27	1867
6633	27	14	3258
6634	14	27	3026
6635	27	35	2215
6636	35	27	1849
6637	28	29	1150
6638	29	28	1177
6639	28	30	370
6640	30	28	469
6641	28	34	471
6642	34	28	412
6643	28	37	1299
6644	37	28	1389
6645	28	40	756
6646	40	28	559
6647	28	41	1428
6648	41	28	1458
6649	28	43	1504
6650	43	28	1500
6651	28	12	1663
6652	12	28	1523
6653	28	5	2496
6654	5	28	2398
6655	28	38	1185
6656	38	28	1249
6657	28	25	1601
6658	25	28	1420
6659	28	21	1543
6660	21	28	1507
6661	28	16	1921
6662	16	28	1957
6663	28	44	1586
6664	44	28	1606
6665	28	33	308
6666	33	28	364
6667	28	31	1257
6668	31	28	1251
6669	28	2	1116
6670	2	28	1329
6671	28	3	972
6672	3	28	1097
6673	28	39	921
6674	39	28	1089
6675	28	32	1412
6676	32	28	1448
6677	28	36	435
6678	36	28	497
6679	28	14	2107
6680	14	28	2215
6681	28	35	1610
6682	35	28	1710
6683	29	30	1571
6684	30	29	1393
6685	29	34	1558
6686	34	29	1403
6687	29	37	2071
6688	37	29	1897
6689	29	40	1159
6690	40	29	1364
6691	29	41	1851
6692	41	29	1880
6693	29	43	2079
6694	43	29	2038
6695	29	12	1987
6696	12	29	2064
6697	29	5	2889
6698	5	29	2872
6699	29	38	1746
6700	38	29	1649
6701	29	25	1901
6702	25	29	1869
6703	29	21	2095
6704	21	29	2005
6705	29	16	2214
6706	16	29	2325
6707	29	44	1900
6708	44	29	1956
6709	29	33	1122
6710	33	29	1225
6711	29	31	1932
6712	31	29	1811
6713	29	2	1711
6714	2	29	1614
6715	29	3	1588
6716	3	29	1532
6717	29	39	1581
6718	39	29	1542
6719	29	32	2054
6720	32	29	1923
6721	29	36	1365
6722	36	29	1496
6723	29	14	1962
6724	14	29	1858
6725	29	35	2198
6726	35	29	2146
6727	30	34	198
6728	34	30	235
6729	30	37	1527
6730	37	30	1520
6731	30	40	746
6732	40	30	968
6733	30	41	1708
6734	41	30	1763
6735	30	43	1721
6736	43	30	1540
6737	30	12	1871
6738	12	30	1951
6739	30	5	2523
6740	5	30	2650
6741	30	38	1325
6742	38	30	1464
6743	30	25	1644
6744	25	30	1724
6745	30	21	1889
6746	21	30	1816
6747	30	16	1964
6748	16	30	2073
6749	30	44	1634
6750	44	30	1627
6751	30	33	585
6752	33	30	453
6753	30	31	1412
6754	31	30	1537
6755	30	2	1388
6756	2	30	1365
6757	30	3	1349
6758	3	30	1161
6759	30	39	1127
6760	39	30	1194
6761	30	32	1769
6762	32	30	1651
6763	30	36	113
6764	36	30	81
6765	30	14	2341
6766	14	30	2399
6767	30	35	1951
6768	35	30	1785
6769	34	37	1596
6770	37	34	1641
6771	34	40	920
6772	40	34	864
6773	34	41	1608
6774	41	34	1721
6775	34	43	1558
6776	43	34	1737
6777	34	12	1802
6778	12	34	1829
6779	34	5	2672
6780	5	34	2544
6781	34	38	1269
6782	38	34	1318
6783	34	25	1640
6784	25	34	1805
6785	34	21	1944
6786	21	34	1802
6787	34	16	2001
6788	16	34	2151
6789	34	44	1645
6790	44	34	1618
6791	34	33	411
6792	33	34	628
6793	34	31	1420
6794	31	34	1607
6795	34	2	1486
6796	2	34	1328
6797	34	3	1141
6798	3	34	1361
6799	34	39	1292
6800	39	34	1179
6801	34	32	1802
6802	32	34	1798
6803	34	36	296
6804	36	34	109
6805	34	14	2372
6806	14	34	2433
6807	34	35	1936
6808	35	34	1859
6809	37	40	987
6810	40	37	1053
6811	37	41	329
6812	41	37	268
6813	37	43	161
6814	43	37	286
6815	37	12	615
6816	12	37	600
6817	37	5	2490
6818	5	37	2532
6819	37	38	991
6820	38	37	1067
6821	37	25	759
6822	25	37	766
6823	37	21	448
6824	21	37	521
6825	37	16	1988
6826	16	37	2019
6827	37	44	305
6828	44	37	195
6829	37	33	1385
6830	33	37	1414
6831	37	31	232
6832	31	37	314
6833	37	2	712
6834	2	37	728
6835	37	3	440
6836	3	37	436
6837	37	39	608
6838	39	37	667
6839	37	32	264
6840	32	37	351
6841	37	36	1669
6842	36	37	1567
6843	37	14	2830
6844	14	37	2810
6845	37	35	1883
6846	35	37	1726
6847	40	41	927
6848	41	40	993
6849	40	43	847
6850	43	40	1001
6851	40	12	1292
6852	12	40	1298
6853	40	5	2428
6854	5	40	2403
6855	40	38	624
6856	38	40	676
6857	40	25	1620
6858	25	40	1481
6859	40	21	1213
6860	21	40	1256
6861	40	16	1951
6862	16	40	1879
6863	40	44	1000
6864	44	40	941
6865	40	33	592
6866	33	40	525
6867	40	31	737
6868	31	40	845
6869	40	2	1207
6870	2	40	1118
6871	40	3	527
6872	3	40	508
6873	40	39	456
6874	39	40	558
6875	40	32	1117
6876	32	40	979
6877	40	36	855
6878	36	40	854
6879	40	14	2161
6880	14	40	2079
6881	40	35	1679
6882	35	40	1653
6883	41	43	335
6884	43	41	166
6885	41	12	508
6886	12	41	576
6887	41	5	2382
6888	5	41	2510
6889	41	38	950
6890	38	41	1070
6891	41	25	748
6892	25	41	733
6893	41	21	553
6894	21	41	524
6895	41	16	1856
6896	16	41	2057
6897	41	44	189
6898	44	41	242
6899	41	33	1451
6900	33	41	1354
6901	41	31	286
6902	31	41	366
6903	41	2	650
6904	2	41	549
6905	41	3	581
6906	3	41	618
6907	41	39	545
6908	39	41	696
6909	41	32	87
6910	32	41	165
6911	41	36	1697
6912	36	41	1789
6913	41	14	2882
6914	14	41	2928
6915	41	35	1833
6916	35	41	1672
6917	43	12	563
6918	12	43	652
6919	43	5	2518
6920	5	43	2564
6921	43	38	969
6922	38	43	1052
6923	43	25	670
6924	25	43	709
6925	43	21	527
6926	21	43	630
6927	43	16	1960
6928	16	43	1960
6929	43	44	145
6930	44	43	209
6931	43	33	1297
6932	33	43	1418
6933	43	31	321
6934	31	43	260
6935	43	2	695
6936	2	43	757
6937	43	3	465
6938	3	43	478
6939	43	39	461
6940	39	43	651
6941	43	32	365
6942	32	43	251
6943	43	36	1700
6944	36	43	1672
6945	43	14	2967
6946	14	43	2950
6947	43	35	1783
6948	35	43	1911
6949	12	5	2606
6950	5	12	2698
6951	12	38	1214
6952	38	12	1414
6953	12	25	762
6954	25	12	823
6955	12	21	231
6956	21	12	154
6957	12	16	2016
6958	16	12	1970
6959	12	44	349
6960	44	12	385
6961	12	33	1501
6962	33	12	1586
6963	12	31	716
6964	31	12	536
6965	12	2	686
6966	2	12	847
6967	12	3	975
6968	3	12	850
6969	12	39	836
6970	39	12	888
6971	12	32	365
6972	32	12	521
6973	12	36	1860
6974	36	12	1936
6975	12	14	2916
6976	14	12	2928
6977	12	35	1853
6978	35	12	1770
6979	5	38	3025
6980	38	5	2838
6981	5	25	2434
6982	25	5	2408
6983	5	21	2614
6984	21	5	2626
6985	5	16	2736
6986	16	5	2654
6987	5	44	2428
6988	44	5	2557
6989	5	33	2421
6990	33	5	2376
6991	5	31	2746
6992	31	5	2741
6993	5	2	2159
6994	2	5	2147
6995	5	3	2735
6996	3	5	2804
6997	5	39	2736
6998	39	5	2763
6999	5	32	2397
7000	32	5	2362
7001	5	36	2654
7002	36	5	2583
7003	5	14	3769
7004	14	5	3619
7005	5	35	2562
7006	35	5	2674
7007	38	25	1519
7008	25	38	1586
7009	38	21	1381
7010	21	38	1399
7011	38	16	2486
7012	16	38	2388
7013	38	44	1088
7014	44	38	960
7015	38	33	984
7016	33	38	1163
7017	38	31	950
7018	31	38	814
7019	38	2	1516
7020	2	38	1608
7021	38	3	683
7022	3	38	668
7023	38	39	551
7024	39	38	593
7025	38	32	1165
7026	32	38	1139
7027	38	36	1484
7028	36	38	1404
7029	38	14	2531
7030	14	38	2740
7031	38	35	2107
7032	35	38	2281
7033	25	21	704
7034	21	25	803
7035	25	16	1873
7036	16	25	1868
7037	25	44	613
7038	44	25	756
7039	25	33	1443
7040	33	25	1484
7041	25	31	920
7042	31	25	777
7043	25	2	712
7044	2	25	532
7045	25	3	1117
7046	3	25	1105
7047	25	39	1149
7048	39	25	1244
7049	25	32	680
7050	32	25	667
7051	25	36	1627
7052	36	25	1765
7053	25	14	2788
7054	14	25	2815
7055	25	35	1844
7056	35	25	1632
7057	21	16	2072
7058	16	21	1953
7059	21	44	535
7060	44	21	468
7061	21	33	1487
7062	33	21	1531
7063	21	31	606
7064	31	21	507
7065	21	2	628
7066	2	21	620
7067	21	3	884
7068	3	21	931
7069	21	39	1018
7070	39	21	1006
7071	21	32	353
7072	32	21	387
7073	21	36	1836
7074	36	21	1798
7075	21	14	2820
7076	14	21	2885
7077	21	35	1804
7078	35	21	1832
7079	16	44	1982
7080	44	16	1865
7081	16	33	1748
7082	33	16	1760
7083	16	31	2191
7084	31	16	2227
7085	16	2	1592
7086	2	16	1556
7087	16	3	2251
7088	3	16	2364
7089	16	39	2378
7090	39	16	2278
7091	16	32	1868
7092	32	16	1918
7093	16	36	1982
7094	36	16	2002
7095	16	14	3072
7096	14	16	3187
7097	16	35	281
7098	35	16	310
7099	44	33	1448
7100	33	44	1353
7101	44	31	456
7102	31	44	258
7103	44	2	590
7104	2	44	646
7105	44	3	601
7106	3	44	539
7107	44	39	722
7108	39	44	582
7109	44	32	291
7110	32	44	268
7111	44	36	1629
7112	36	44	1607
7113	44	14	2714
7114	14	44	2929
7115	44	35	1763
7116	35	44	1823
7117	33	31	1202
7118	31	33	1176
7119	33	2	1160
7120	2	33	1162
7121	33	3	990
7122	3	33	988
7123	33	39	972
7124	39	33	1029
7125	33	32	1434
7126	32	33	1453
7127	33	36	595
7128	36	33	580
7129	33	14	2042
7130	14	33	2064
7131	33	35	1558
7132	35	33	1511
7133	31	2	755
7134	2	31	719
7135	31	3	547
7136	3	31	401
7137	31	39	401
7138	39	31	373
7139	31	32	333
7140	32	31	391
7141	31	36	1429
7142	36	31	1560
7143	31	14	2748
7144	14	31	2786
7145	31	35	1906
7146	35	31	1969
7147	2	3	1135
7148	3	2	973
7149	2	39	1149
7150	39	2	1115
7151	2	32	564
7152	32	2	698
7153	2	36	1381
7154	36	2	1333
7155	2	14	2522
7156	14	2	2503
7157	2	35	1518
7158	35	2	1471
7159	3	39	169
7160	39	3	136
7161	3	32	675
7162	32	3	660
7163	3	36	1253
7164	36	3	1148
7165	3	14	2562
7166	14	3	2529
7167	3	35	2038
7168	35	3	2099
7169	39	32	606
7170	32	39	681
7171	39	36	1147
7172	36	39	1328
7173	39	14	2419
7174	14	39	2550
7175	39	35	2015
7176	35	39	1977
7177	32	36	1703
7178	36	32	1801
7179	32	14	2843
7180	14	32	2746
7181	32	35	1709
7182	35	32	1683
7183	36	14	2263
7184	14	36	2407
7185	36	35	1898
7186	35	36	1876
7187	14	35	2838
7188	35	14	2905
\.


--
-- TOC entry 3526 (class 0 OID 1087391)
-- Dependencies: 226
-- Data for Name: points; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.points (id, address, created_at, coordinate, img, is_delivered_card, last_date_issue_card, quantity_requests, quantity_card) FROM stdin;
1	г. Краснодар, ул. Ставропольская, д. 140	2023-11-08	{"y": 39.003962, "x": 45.019916}	\N	f	\N	0	0
4	г. Краснодар, ул. Красноармейская, д. 12	2023-09-07	{"y": 38.977244, "x": 45.037961}	\N	t	2023-11-09	38	23
6	г. Краснодар, тер. Пашковский жилой массив, ул. Крылатая, д. 2	2023-10-10	{"y": 39.120427, "x": 45.010057}	\N	t	2023-10-28	19	1
7	г. Краснодар, ул. Восточно-Кругликовская, д. 64/2	2023-10-09	{"y": 39.025368, "x": 45.068133}	\N	t	2023-10-13	19	12
8	г. Краснодар, ул. Красных Партизан, д. 439	2023-09-01	{"y": 38.956475, "x": 45.051538}	\N	t	2023-10-07	84	63
9	г. Краснодар, ул. Таманская, д. 153 к. 3, кв. 2	2023-11-07	{"y": 39.013054, "x": 45.023121}	\N	t	2023-11-07	15	1
10	г. Краснодар, ул. им. Дзержинского, д. 165	2023-11-07	{"y": 38.976481, "x": 45.090285}	\N	t	\N	19	0
11	г. Краснодар, ст-ца. Елизаветинская, ул. Широкая, д. 260	2023-10-03	{"y": 38.803374, "x": 45.049464}	\N	t	2023-10-25	29	15
13	г. Краснодар, ул. Уральская, д. 162	2023-10-02	{"y": 39.095554, "x": 45.041209}	\N	t	2023-11-05	21	5
15	г. Краснодар, ул. им. Селезнева, д. 197/5	2023-09-09	{"y": 39.054215, "x": 45.016728}	\N	t	2023-11-02	14	3
19	г. Краснодар, ул. Зиповская, д. 1	2023-08-08	{"y": 38.993391, "x": 45.06411}	\N	t	2023-11-03	32	9
20	г. Краснодар, ул. им. 40-летия Победы, д. 20/1	2023-09-02	{"y": 39.001218, "x": 45.054788}	\N	t	2023-11-05	35	15
22	г. Краснодар, ул. им. Героя Аверкиева А.А., д. 8	2023-10-03	{"y": 39.029266, "x": 45.060211}	\N	t	2023-11-03	18	6
24	г. Краснодар, ул. им. Тургенева, д. 106	2023-10-02	{"y": 38.959746, "x": 45.052153}	\N	t	2023-11-07	96	20
26	г. Краснодар, ул. Северная, д. 389	2023-09-08	{"y": 38.993378, "x": 45.037706}	\N	t	\N	16	0
27	г. Краснодар, ул. Уральская, д. 166/3	2023-10-01	{"y": 39.095624, "x": 45.038942}	\N	t	2023-11-06	43	29
28	г. Краснодар, ул. Северная, д. 524	2023-10-04	{"y": 39.000753, "x": 45.035935}	\N	t	2023-11-06	13	4
29	г. Краснодар, ул. им. Кирилла Россинского, д. 61/1	2023-09-01	{"y": 39.036991, "x": 45.088866}	\N	t	2023-11-03	19	5
30	г. Краснодар, ул. Коммунаров, д. 258	2023-10-11	{"y": 38.981449, "x": 45.043705}	\N	t	2023-10-24	45	30
34	г. Краснодар, ул. Красная, д. 176	2023-07-14	{"y": 38.980909, "x": 45.045855}	\N	t	2023-08-25	82	72
37	г. Краснодар, ул. Красная, д. 149	2023-10-08	{"y": 38.978161, "x": 45.048348}	\N	t	2023-10-31	10	7
40	г. Краснодар, ул. Российская, д. 418	2023-10-08	{"y": 39.014789, "x": 45.085209}	\N	t	2023-11-03	30	14
41	г. Краснодар, ул. им. Володи Головатого, д. 313	2023-09-08	{"y": 38.974688, "x": 45.039351}	\N	t	2023-11-03	65	12
43	г. Краснодар, ул. Красная, д. 145	2023-10-02	{"y": 38.978004, "x": 45.047609}	\N	t	2023-11-06	20	4
12	г. Краснодар, ул. им. Тургенева, д. 174, 1 этаж	2023-11-08	{"y": 38.962929, "x": 45.062447}	\N	t	\N	0	0
5	г. Краснодар, хутор Ленина, п/о. 37	2023-10-03	{"y":39.209458, "x": 45.019074}	\N	t	\N	14	0
38	г. Краснодар, п. Березовый, ул. Целиноградская, д. 6/1	2023-11-08	{"y": 38.998664, "x": 45.14541}	\N	t	\N	13	0
25	г. Краснодар, ул. Красных Партизан, д. 117	2023-11-08	{"y": 38.919027, "x": 45.063349}	\N	t	\N	0	0
21	г. Краснодар, ул. им. Атарбекова, д. 24	2023-11-08	{"y": 38.949082, "x": 45.059149}	\N	t	\N	6	0
16	г. Краснодар, ул. Уральская, д. 117	2023-11-08	{"y": 39.072704, "x": 45.037697}	\N	t	\N	0	0
44	г. Краснодар,ул. Красная, д. 154	2023-11-08	{"y": 38.975481, "x": 45.037196}	\N	t	\N	0	0
33	г. Краснодар, ул. им. 40-летия Победы, д. 34	2023-11-08	{"y": 39.003825, "x": 45.054543}	\N	t	\N	19	0
31	г. Краснодар, ул. им. Дзержинского, д. 101	2023-10-12	{"y": 38.972376, "x": 45.069416}	\N	t	2023-11-08	19	4
2	г. Краснодар, ул. Горького, 128\n	2023-10-28	{"y": 38.979517, "x": 45.030113}	\N	t	2023-11-06	15	3
3	г. Краснодар, ул. им. Дзержинского, д. 100	2023-10-20	{"y": 38.983856, "x": 45.102209}	\N	t	2023-11-06	9	1
39	г. Краснодар, ул. им. Дзержинского, д. 102	2023-11-08	{"y": 38.983928, "x": 45.103787}	\N	t	\N	10	0
32	г. Краснодар, ул. Северная, д. 326	2023-10-13	{"y": 38.970795, "x": 45.040445}	\N	t	2023-11-06	20	9
36	г. Краснодар, ул. Северная, д. 327	2023-10-08	{"y": 38.986255, "x": 45.038986}	\N	t	2023-11-05	19	4
14	г. Краснодар, ул. Уральская, д. 78	2023-11-08	{"y": 39.036893, "x": 45.031228}	\N	t	\N	5	0
35	г. Краснодар, ул. Уральская, д. 79/1	2023-09-08	{"y": 39.051463, "x": 45.035273}	\N	t	2023-10-17	32	21
\.


--
-- TOC entry 3528 (class 0 OID 1087397)
-- Dependencies: 228
-- Data for Name: priorities; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.priorities (id, name, value) FROM stdin;
1	Высокий	3
2	Средний	2
3	Низкий	1
4	Крайне высокий	4
\.


--
-- TOC entry 3530 (class 0 OID 1087401)
-- Dependencies: 230
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (id, name, is_public) FROM stdin;
1	Сотрудник	t
2	Менеджер	t
3	Админ	f
\.


--
-- TOC entry 3532 (class 0 OID 1087405)
-- Dependencies: 232
-- Data for Name: skills; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.skills (id, name) FROM stdin;
1	Творческий
2	Организованный
3	Аккуратный
4	Креативный
5	Дружелюбный
6	Энергичный
7	Аналитический
8	Гибкий
9	Самостоятельный
10	Ответственный
11	Общительный
12	Адаптивный
13	Внимательный
\.


--
-- TOC entry 3534 (class 0 OID 1087409)
-- Dependencies: 234
-- Data for Name: task_statusess; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task_statusess (id, name, in_history) FROM stdin;
1	Выполнена	t
2	Отменена	t
6	В очереди	f
3	Назначена	f
4	Выполняется	f
\.


--
-- TOC entry 3536 (class 0 OID 1087413)
-- Dependencies: 236
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tasks (id, type_id, point_id, status_id, date_begin, date_create, priority_id, employee_id) FROM stdin;
890	2	9	6	\N	2023-11-11 19:50:00.582452	2	\N
894	2	20	6	\N	2023-11-11 19:50:00.588552	2	\N
896	2	24	6	\N	2023-11-11 19:50:00.591263	2	\N
897	2	28	6	\N	2023-11-11 19:50:00.591806	2	\N
899	2	40	6	\N	2023-11-11 19:50:00.592874	2	\N
900	2	41	6	\N	2023-11-11 19:50:00.594507	2	\N
901	2	43	6	\N	2023-11-11 19:50:00.596156	2	\N
903	2	2	6	\N	2023-11-11 19:50:00.599056	2	\N
907	1	7	6	\N	2023-11-11 19:50:00.602719	1	\N
910	1	30	6	\N	2023-11-11 19:50:00.604714	1	\N
911	1	34	6	\N	2023-11-11 19:50:00.60572	1	\N
913	1	35	6	\N	2023-11-11 19:50:00.608121	1	\N
898	2	29	3	2023-11-11 09:00:00	2023-11-11 19:50:00.592339	2	16
891	2	13	3	2023-11-11 12:00:00	2023-11-11 19:50:00.583473	2	16
902	2	31	3	2023-11-11 14:00:00	2023-11-11 19:50:00.597952	2	16
888	3	1	3	2023-11-11 09:00:00	2023-11-11 19:50:00.572419	3	23
909	1	11	3	2023-11-11 09:00:00	2023-11-11 19:50:00.604714	1	15
895	2	22	3	2023-11-11 14:00:00	2023-11-11 19:50:00.590193	2	15
912	1	37	3	2023-11-11 09:00:00	2023-11-11 19:50:00.607113	1	19
908	1	8	3	2023-11-11 13:00:00	2023-11-11 19:50:00.60372	1	19
889	2	6	3	2023-11-11 09:00:00	2023-11-11 19:50:00.581143	2	22
893	2	19	3	2023-11-11 11:00:00	2023-11-11 19:50:00.587495	2	22
905	2	32	3	2023-11-11 14:00:00	2023-11-11 19:50:00.600706	2	22
904	2	3	3	2023-11-11 09:00:00	2023-11-11 19:50:00.599567	2	20
892	2	15	3	2023-11-11 12:00:00	2023-11-11 19:50:00.584501	2	20
906	2	36	3	2023-11-11 14:00:00	2023-11-11 19:50:00.601723	2	20
\.


--
-- TOC entry 3538 (class 0 OID 1087417)
-- Dependencies: 238
-- Data for Name: traffics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.traffics (id, hour, level) FROM stdin;
41	9	0
42	10	0
43	11	1
44	12	1
45	13	2
46	14	2
47	15	2
48	16	2
49	17	2
50	18	2
\.


--
-- TOC entry 3540 (class 0 OID 1087421)
-- Dependencies: 240
-- Data for Name: type_task_grade_links; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.type_task_grade_links (type_task_id, grade_id) FROM stdin;
1	1
2	1
2	2
3	2
3	3
3	1
\.


--
-- TOC entry 3541 (class 0 OID 1087424)
-- Dependencies: 241
-- Data for Name: type_task_skill_links; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.type_task_skill_links (type_task_id, skill_id) FROM stdin;
1	1
1	3
1	7
1	11
1	10
2	11
2	8
2	10
2	13
3	10
3	6
3	3
3	2
\.


--
-- TOC entry 3542 (class 0 OID 1087427)
-- Dependencies: 242
-- Data for Name: type_tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.type_tasks (id, name, priority_id, duration, details, interval_block) FROM stdin;
1	Выезд на точку для стимулирования выдач	1	4	{}	5
2	Обучение агента	2	2	{}	4
3	Доставка карт и материалов	3	1.5	{}	2
\.


--
-- TOC entry 3544 (class 0 OID 1087433)
-- Dependencies: 244
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, hashed_password, firstname, lastname, patronymic, img, created_at, role_id, is_active) FROM stdin;
23	nikolaev@yandex.ru	$2b$12$h30NkY6rIQkqg.1qcZNoj.A.9PoaBZhhi0xXwYw6EqvunmyUNN0kC	Азарий	Николаев	Платонович	\N	2023-11-07 18:42:01.073211	1	t
1	mistybit@mail.ru	$2b$12$h30NkY6rIQkqg.1qcZNoj.A.9PoaBZhhi0xXwYw6EqvunmyUNN0kC	root	\N	\N	\N	2023-11-05 12:04:11.491811	3	t
15	katsumiproo@gmail.com	$2b$12$h30NkY6rIQkqg.1qcZNoj.A.9PoaBZhhi0xXwYw6EqvunmyUNN0kC	Максим	Исаев	Александрович	\N	2023-11-07 06:55:07.57166	1	t
18	mr.vaynbaum@mail.ru	$2b$12$QDuRYJsFJF.BwurBPOnt0u6JtA0w386/x7QK1NULTxNaJ51rLfB7O	Денис	Вайнбаум	Алексеевич	\N	2023-11-07 07:00:47.666981	2	t
16	vromanmelnikov@yandex.ru	$2b$12$h30NkY6rIQkqg.1qcZNoj.A.9PoaBZhhi0xXwYw6EqvunmyUNN0kC	Роман	Мельников	Васильевич	\N	2023-11-07 06:56:55.341622	1	t
17	v.romankozlov@gmail.com	$2b$12$h30NkY6rIQkqg.1qcZNoj.A.9PoaBZhhi0xXwYw6EqvunmyUNN0kC	Роман	Козлов	Васильевич	\N	2023-11-07 06:59:39.304732	1	t
19	vaynbaum50@gmail.com	$2b$12$h30NkY6rIQkqg.1qcZNoj.A.9PoaBZhhi0xXwYw6EqvunmyUNN0kC	Денис	Виноградов	Алексеевич	\N	2023-11-07 18:37:35.838947	1	t
20	ngtumaksimisaev@gmail.com	$2b$12$h30NkY6rIQkqg.1qcZNoj.A.9PoaBZhhi0xXwYw6EqvunmyUNN0kC	Иаксим	Мисаев	Алексеевич	\N	2023-11-07 18:39:28.821603	1	t
21	maksim228775@gmail.com	$2b$12$3RGqYtzMrWztMO8iEK4D3u1XfK/7.R62em0vN9D2hs9vHwtVzKp9u	Степанов	Ярослав	Альбертович	\N	2023-11-07 18:40:49.533261	1	t
22	Ccoo00@yandex.ru	$2b$12$h30NkY6rIQkqg.1qcZNoj.A.9PoaBZhhi0xXwYw6EqvunmyUNN0kC	Екатерина	Панкратова	Антоновна	\N	2023-11-07 18:41:27.536595	1	t
\.


--
-- TOC entry 3546 (class 0 OID 1087439)
-- Dependencies: 246
-- Data for Name: vakt_policies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vakt_policies (id, resources, actions, subjects, description) FROM stdin;
1	[{"name": "/users/profile"}]	[{"name": "get"}]	[{"role_id": 3}, {"role_id": 2}, {"role_id": 1, "is_owner": true}]	Администраторы и менеджры могут просматривать все профили, пользователь только свой
2	[{"name": "/users/registration"}]	[{"name": "post"}]	[{"role_id": 3}]	Только администраторы могут добавлять новых пользователей
3	[{"name": "/offices/"}]	[{"name": "delete"}]	[{"role_id": 3}]	Только админы могут удалять офисы
4	[{"name": "/offices/"}]	[{"name": "put"}]	[{"role_id": 3}]	Только админы могут изменять офисы
5	[{"name": "/users/skills"}]	[{"name": "post"}]	[{"role_id": 2}]	Только менеджеры могут добавлять навыки
6	[{"name": "/users/skills/employee"}]	[{"name": "post"}]	[{"role_id": 1}]	Только сотрудники могут добавлять навыки
7	[{"name": "/users/skills/employee"}]	[{"name": "delete"}]	[{"role_id": 1}]	Только сотрудники могут удалять свои навыки
8	[{"name": "/users/"}]	[{"name": "put"}]	[{"role_id": 3}, {"role_id": 2}, {"role_id": 1, "is_owner": true}]	Администраторы и менеджеры могут изменять любой профиль, сотрудники только свой
9	[{"name": "/users/"}]	[{"name": "delete"}]	[{"role_id": 3}, {"role_id": 2}, {"role_id": 1, "is_owner": true}]	Все могут удалять свой профиль
10	[{"name": "/offices/image"}]	[{"name": "post"}]	[{"role_id": 2}]	Только менеджер может изменять картинку офиса
11	[{"name": "/offices/points/image"}]	[{"name": "post"}]	[{"role_id": 2}]	Только менеджер может изменять картинку точки
12	[{"name": "/users/image"}]	[{"name": "post"}]	[{"role_id": 3}, {"role_id": 1}, {"role_id": 2}]	Все могут изменять картинку своего профиля
13	[{"name": "/users/image"}]	[{"name": "delete"}]	[{"role_id": 3}, {"role_id": 1}, {"role_id": 2}]	Все могут удалять картинку профиля
14	[{"name": "/offices/"}]	[{"name": "post"}]	[{"role_id": 3}]	Только админы могут добавлять офисы
15	[{"name": "/users/is_active"}]	[{"name": "put"}]	[{"role_id": 3}]	Только админы могут переводить сотрудника в актив/неактив
16	[{"name": "/users/employees"}]	[{"name": "put"}]	[{"role_id": 2}]	Только менеджеры могут изменять грейд и офис сотрудника
17	[{"name": "/offices/points"}]	[{"name": "post"}]	[{"role_id": 3}]	Только админы могут добавлять точки
18	[{"name": "/offices/points"}]	[{"name": "put"}]	[{"role_id": 3}]	Только админы могут изменять точки
19	[{"name": "/offices/points"}]	[{"name": "delete"}]	[{"role_id": 3}]	Только админы могут удалять точки
20	[{"name": "/tasks/types"}]	[{"name": "post"}]	[{"role_id": 2}]	Только менеджер может добавлять типы задач
21	[{"name": "/tasks/types"}]	[{"name": "put"}]	[{"role_id": 2}]	Только менеджер может изменять типы задач
22	[{"name": "/tasks/types"}]	[{"name": "delete"}]	[{"role_id": 2}]	Только менеджер может удалять типы задач
23	[{"name": "/tasks/types/grades"}]	[{"name": "post"}]	[{"role_id": 2}]	Только менеджер может добавлять грейды для типов задач
24	[{"name": "/tasks/types/grades"}]	[{"name": "delete"}]	[{"role_id": 2}]	Только менеджер может удалять грейды для типов задач
25	[{"name": "/tasks/types/skills"}]	[{"name": "post"}]	[{"role_id": 2}]	Только менеджер может добавлять навыки для типов задач
26	[{"name": "/tasks/types/skills"}]	[{"name": "delete"}]	[{"role_id": 2}]	Только менеджер может удалять навыки для типов задач
27	[{"name": "/tasks/conditions"}]	[{"name": "post"}]	[{"role_id": 2}]	Только менеджер может добавлять условия к типу задачи
28	[{"name": "/tasks/conditions"}]	[{"name": "delete"}]	[{"role_id": 2}]	Только менеджер может удалять условия у типа задачи
29	[{"name": "/tasks/conditions"}]	[{"name": "put"}]	[{"role_id": 2}]	Только менеджер может изменять условия у типа задачи
30	[{"name": "/users/all"}]	[{"name": "get"}]	[{"role_id": 3}]	Только админы могут просматривать всех пользователей
31	[{"name": "/users/employees/all"}]	[{"name": "get"}]	[{"role_id": 3}, {"role_id": 2}]	Только админы и менеджеры могут просматривать всех сотрудников
32	[{"name": "/secure/methods/all"}]	[{"name": "get"}]	[{"role_id": 3}]	Только админы могут просматривать защищенные методы
33	[{"name": "/secure/policies/all"}]	[{"name": "get"}]	[{"role_id": 3}]	Только админы могут просматривать политики безопасности защищенных методов
34	[{"name": "/secure/policies"}]	[{"name": "put"}]	[{"role_id": 3}]	Только админы могут изменять политики безопасности защищенных методов
35	[{"name": "/tasks/completed"}]	[{"name": "post"}]	[{"role_id": 2}, {"role_id": 1, "is_owner": true}]	Менеджеры могут завершать задачи а сотрудники только свои задачи
36	[{"name": "/tasks/cancelled"}]	[{"name": "post"}]	[{"role_id": 2}, {"role_id": 1, "is_owner": true}]	Менеджеры могут отменять задачи а сотрудники только свои задачи
37	[{"name": "/tasks/distribution"}]	[{"name": "post"}]	[{"role_id": 2}]	Только менеджеры могут распределять задачи по сотрудникам
38	[{"name": "/tasks/accept_task"}]	[{"name": "put"}]	[{"role_id": 1, "is_owner": true}]	Только сотрудники могут принять свои задачи
39	[{"name": "/tasks/by_manager"}]	[{"name": "put"}]	[{"role_id": 2}]	Только менеджер может назначать задачи сотруднику
40	[{"name": "/notifications/"}]	[{"name": "get"}]	[{"role_id": 3}, {"role_id": 2}, {"role_id": 1}]	Все могут получать свои уведомления
\.


--
-- TOC entry 3577 (class 0 OID 0)
-- Dependencies: 212
-- Name: conditions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.conditions_id_seq', 11, true);


--
-- TOC entry 3578 (class 0 OID 0)
-- Dependencies: 216
-- Name: grades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.grades_id_seq', 1, false);


--
-- TOC entry 3579 (class 0 OID 0)
-- Dependencies: 218
-- Name: history_tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.history_tasks_id_seq', 50, true);


--
-- TOC entry 3580 (class 0 OID 0)
-- Dependencies: 248
-- Name: notes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notes_id_seq', 37, true);


--
-- TOC entry 3581 (class 0 OID 0)
-- Dependencies: 221
-- Name: office_durations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.office_durations_id_seq', 792, true);


--
-- TOC entry 3582 (class 0 OID 0)
-- Dependencies: 223
-- Name: offices_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.offices_id_seq', 5, true);


--
-- TOC entry 3583 (class 0 OID 0)
-- Dependencies: 225
-- Name: point_durations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.point_durations_id_seq', 7188, true);


--
-- TOC entry 3584 (class 0 OID 0)
-- Dependencies: 227
-- Name: points_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.points_id_seq', 44, true);


--
-- TOC entry 3585 (class 0 OID 0)
-- Dependencies: 229
-- Name: priorities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.priorities_id_seq', 1, false);


--
-- TOC entry 3586 (class 0 OID 0)
-- Dependencies: 231
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_id_seq', 1, false);


--
-- TOC entry 3587 (class 0 OID 0)
-- Dependencies: 233
-- Name: skills_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.skills_id_seq', 13, true);


--
-- TOC entry 3588 (class 0 OID 0)
-- Dependencies: 235
-- Name: task_statusess_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_statusess_id_seq', 1, false);


--
-- TOC entry 3589 (class 0 OID 0)
-- Dependencies: 237
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tasks_id_seq', 913, true);


--
-- TOC entry 3590 (class 0 OID 0)
-- Dependencies: 239
-- Name: traffics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.traffics_id_seq', 50, true);


--
-- TOC entry 3591 (class 0 OID 0)
-- Dependencies: 243
-- Name: type_tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.type_tasks_id_seq', 3, true);


--
-- TOC entry 3592 (class 0 OID 0)
-- Dependencies: 245
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 23, true);


--
-- TOC entry 3593 (class 0 OID 0)
-- Dependencies: 247
-- Name: vakt_policies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.vakt_policies_id_seq', 1, false);


--
-- TOC entry 3290 (class 2606 OID 1087462)
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (id);


--
-- TOC entry 3292 (class 2606 OID 1087464)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 3294 (class 2606 OID 1087466)
-- Name: conditions conditions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conditions
    ADD CONSTRAINT conditions_pkey PRIMARY KEY (id);


--
-- TOC entry 3296 (class 2606 OID 1087468)
-- Name: employee_skill_links employee_skill_links_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee_skill_links
    ADD CONSTRAINT employee_skill_links_pkey PRIMARY KEY (employe_id, skill_id);


--
-- TOC entry 3298 (class 2606 OID 1087470)
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- TOC entry 3300 (class 2606 OID 1087472)
-- Name: grades grades_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades
    ADD CONSTRAINT grades_name_key UNIQUE (name);


--
-- TOC entry 3302 (class 2606 OID 1087474)
-- Name: grades grades_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades
    ADD CONSTRAINT grades_pkey PRIMARY KEY (id);


--
-- TOC entry 3304 (class 2606 OID 1087476)
-- Name: history_tasks history_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.history_tasks
    ADD CONSTRAINT history_tasks_pkey PRIMARY KEY (id);


--
-- TOC entry 3306 (class 2606 OID 1087478)
-- Name: managers managers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.managers
    ADD CONSTRAINT managers_pkey PRIMARY KEY (id);


--
-- TOC entry 3344 (class 2606 OID 1087644)
-- Name: notes notes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notes
    ADD CONSTRAINT notes_pkey PRIMARY KEY (id);


--
-- TOC entry 3308 (class 2606 OID 1087480)
-- Name: office_durations office_durations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.office_durations
    ADD CONSTRAINT office_durations_pkey PRIMARY KEY (id);


--
-- TOC entry 3310 (class 2606 OID 1087482)
-- Name: offices offices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.offices
    ADD CONSTRAINT offices_pkey PRIMARY KEY (id);


--
-- TOC entry 3312 (class 2606 OID 1087484)
-- Name: point_durations point_durations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.point_durations
    ADD CONSTRAINT point_durations_pkey PRIMARY KEY (id);


--
-- TOC entry 3314 (class 2606 OID 1087486)
-- Name: points points_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.points
    ADD CONSTRAINT points_pkey PRIMARY KEY (id);


--
-- TOC entry 3316 (class 2606 OID 1087488)
-- Name: priorities priorities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.priorities
    ADD CONSTRAINT priorities_pkey PRIMARY KEY (id);


--
-- TOC entry 3318 (class 2606 OID 1087490)
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- TOC entry 3320 (class 2606 OID 1087492)
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- TOC entry 3322 (class 2606 OID 1087494)
-- Name: skills skills_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_name_key UNIQUE (name);


--
-- TOC entry 3324 (class 2606 OID 1087496)
-- Name: skills skills_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_pkey PRIMARY KEY (id);


--
-- TOC entry 3326 (class 2606 OID 1087498)
-- Name: task_statusess task_statusess_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_statusess
    ADD CONSTRAINT task_statusess_pkey PRIMARY KEY (id);


--
-- TOC entry 3328 (class 2606 OID 1087500)
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- TOC entry 3330 (class 2606 OID 1087502)
-- Name: traffics traffics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.traffics
    ADD CONSTRAINT traffics_pkey PRIMARY KEY (id);


--
-- TOC entry 3332 (class 2606 OID 1087504)
-- Name: type_task_grade_links type_task_grade_links_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.type_task_grade_links
    ADD CONSTRAINT type_task_grade_links_pkey PRIMARY KEY (type_task_id, grade_id);


--
-- TOC entry 3334 (class 2606 OID 1087506)
-- Name: type_task_skill_links type_task_skill_links_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.type_task_skill_links
    ADD CONSTRAINT type_task_skill_links_pkey PRIMARY KEY (type_task_id, skill_id);


--
-- TOC entry 3336 (class 2606 OID 1087508)
-- Name: type_tasks type_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.type_tasks
    ADD CONSTRAINT type_tasks_pkey PRIMARY KEY (id);


--
-- TOC entry 3338 (class 2606 OID 1087510)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 3340 (class 2606 OID 1087512)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 3342 (class 2606 OID 1087514)
-- Name: vakt_policies vakt_policies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vakt_policies
    ADD CONSTRAINT vakt_policies_pkey PRIMARY KEY (id);


--
-- TOC entry 3345 (class 2606 OID 1087515)
-- Name: admins admins_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_id_fkey FOREIGN KEY (id) REFERENCES public.users(id);


--
-- TOC entry 3346 (class 2606 OID 1087520)
-- Name: conditions conditions_type_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conditions
    ADD CONSTRAINT conditions_type_task_id_fkey FOREIGN KEY (type_task_id) REFERENCES public.type_tasks(id);


--
-- TOC entry 3347 (class 2606 OID 1087525)
-- Name: employee_skill_links employee_skill_links_employe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee_skill_links
    ADD CONSTRAINT employee_skill_links_employe_id_fkey FOREIGN KEY (employe_id) REFERENCES public.employees(id);


--
-- TOC entry 3348 (class 2606 OID 1087530)
-- Name: employee_skill_links employee_skill_links_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee_skill_links
    ADD CONSTRAINT employee_skill_links_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(id);


--
-- TOC entry 3349 (class 2606 OID 1087535)
-- Name: employees employees_grade_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_grade_id_fkey FOREIGN KEY (grade_id) REFERENCES public.grades(id);


--
-- TOC entry 3350 (class 2606 OID 1087540)
-- Name: employees employees_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_id_fkey FOREIGN KEY (id) REFERENCES public.users(id);


--
-- TOC entry 3351 (class 2606 OID 1087545)
-- Name: employees employees_office_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_office_id_fkey FOREIGN KEY (office_id) REFERENCES public.offices(id);


--
-- TOC entry 3352 (class 2606 OID 1087550)
-- Name: history_tasks history_tasks_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.history_tasks
    ADD CONSTRAINT history_tasks_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.task_statusess(id);


--
-- TOC entry 3353 (class 2606 OID 1087555)
-- Name: managers managers_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.managers
    ADD CONSTRAINT managers_id_fkey FOREIGN KEY (id) REFERENCES public.users(id);


--
-- TOC entry 3369 (class 2606 OID 1087645)
-- Name: notes notes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notes
    ADD CONSTRAINT notes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3354 (class 2606 OID 1087560)
-- Name: office_durations office_durations_office_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.office_durations
    ADD CONSTRAINT office_durations_office_id_fkey FOREIGN KEY (office_id) REFERENCES public.offices(id);


--
-- TOC entry 3355 (class 2606 OID 1087565)
-- Name: office_durations office_durations_point_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.office_durations
    ADD CONSTRAINT office_durations_point_id_fkey FOREIGN KEY (point_id) REFERENCES public.points(id);


--
-- TOC entry 3356 (class 2606 OID 1087570)
-- Name: point_durations point_durations_point_id1_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.point_durations
    ADD CONSTRAINT point_durations_point_id1_fkey FOREIGN KEY (point_id1) REFERENCES public.points(id);


--
-- TOC entry 3357 (class 2606 OID 1087575)
-- Name: point_durations point_durations_point_id2_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.point_durations
    ADD CONSTRAINT point_durations_point_id2_fkey FOREIGN KEY (point_id2) REFERENCES public.points(id);


--
-- TOC entry 3358 (class 2606 OID 1087580)
-- Name: tasks tasks_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id);


--
-- TOC entry 3359 (class 2606 OID 1087585)
-- Name: tasks tasks_point_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_point_id_fkey FOREIGN KEY (point_id) REFERENCES public.points(id);


--
-- TOC entry 3360 (class 2606 OID 1087590)
-- Name: tasks tasks_priority_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_priority_id_fkey FOREIGN KEY (priority_id) REFERENCES public.priorities(id);


--
-- TOC entry 3361 (class 2606 OID 1087595)
-- Name: tasks tasks_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.task_statusess(id);


--
-- TOC entry 3362 (class 2606 OID 1087600)
-- Name: tasks tasks_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.type_tasks(id);


--
-- TOC entry 3363 (class 2606 OID 1087605)
-- Name: type_task_grade_links type_task_grade_links_grade_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.type_task_grade_links
    ADD CONSTRAINT type_task_grade_links_grade_id_fkey FOREIGN KEY (grade_id) REFERENCES public.grades(id);


--
-- TOC entry 3364 (class 2606 OID 1087610)
-- Name: type_task_grade_links type_task_grade_links_type_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.type_task_grade_links
    ADD CONSTRAINT type_task_grade_links_type_task_id_fkey FOREIGN KEY (type_task_id) REFERENCES public.type_tasks(id);


--
-- TOC entry 3365 (class 2606 OID 1087615)
-- Name: type_task_skill_links type_task_skill_links_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.type_task_skill_links
    ADD CONSTRAINT type_task_skill_links_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(id);


--
-- TOC entry 3366 (class 2606 OID 1087620)
-- Name: type_task_skill_links type_task_skill_links_type_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.type_task_skill_links
    ADD CONSTRAINT type_task_skill_links_type_task_id_fkey FOREIGN KEY (type_task_id) REFERENCES public.type_tasks(id);


--
-- TOC entry 3367 (class 2606 OID 1087625)
-- Name: type_tasks type_tasks_priority_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.type_tasks
    ADD CONSTRAINT type_tasks_priority_id_fkey FOREIGN KEY (priority_id) REFERENCES public.priorities(id);


--
-- TOC entry 3368 (class 2606 OID 1087630)
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


-- Completed on 2023-11-11 22:51:51

--
-- PostgreSQL database dump complete
--

