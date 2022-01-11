create table if not exists scene (
	id_scene integer PRIMARY KEY,
	scene_name text NOT NULL
);

create table if not exists sphere (
	id_sphere integer PRIMARY KEY AUTOINCREMENT,
	x real NOT NULL,
	y real NOT NULL,
	z real NOT NULL,
	radius real NOT NULL,
	
	id_scene integer,
	id_colour integer DEFAULT 1,
	FOREIGN KEY(id_scene) REFERENCES scene(id_scene),
	FOREIGN KEY(id_colour) REFERENCES colour(id_colour)
);

create table if not exists plane (
	id_plane integer PRIMARY KEY AUTOINCREMENT,
	x float NOT NULL,
	y float NOT NULL,
	z float NOT NULL,
	plane_size_x float NOT NULL,
	plane_size_y float NOT NULL,
	
	id_scene integer,
	id_colour integer DEFAULT 1,
	FOREIGN KEY(id_scene) REFERENCES scene(id_scene),
	FOREIGN KEY(id_colour) REFERENCES colour(id_colour)
);

create table if not exists cube (
	id_cube integer PRIMARY KEY AUTOINCREMENT,
	x real NOT NULL,
	y real NOT NULL,
	z real NOT NULL,
	cube_size real NOT NULL,
	
	id_scene integer,
	id_colour integer DEFAULT 1,
	FOREIGN KEY(id_scene) REFERENCES scene(id_scene),
	FOREIGN KEY(id_colour) REFERENCES colour(id_colour)
);

create table if not exists light (
	id_light integer PRIMARY KEY AUTOINCREMENT,
	x real NOT NULL,
	y real NOT NULL,
	z real NOT NULL,
	a_x real NOT NULL,
	a_y real NOT NULL,
	a_z real NOT NULL,
	light_type text NOT NULL,

	id_scene integer,
	id_colour integer DEFAULT 1,
	FOREIGN KEY(id_scene) REFERENCES scene(id_scene),
	FOREIGN KEY(id_colour) REFERENCES colour(id_colour),
	CHECK (light_type IN ("POINT", "DIRECTIONAL"))
);

create table if not exists colour (
	id_colour integer PRIMARY KEY AUTOINCREMENT,
	r real NOT NULL,
	g real NOT NULL,
	b real NOT NULL
);

--WHITE--
insert into colour (r, g, b)
	values(1.0, 1.0, 1.0);

--RED--
insert into colour (r, g, b)
	values(1.0, 0.0, 0.0);

--GREEN--
insert into colour (r, g, b)
	values(0.0, 1.0, 0.0);
	
--BLUE--
insert into colour (r, g, b)
	values(0.0, 0.0, 1.0);
