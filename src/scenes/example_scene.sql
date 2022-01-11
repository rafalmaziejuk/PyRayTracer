insert into scene (id_scene, scene_name)
	values(1, "example_scene");

--OBJECTS--
insert into sphere (x, y, z, radius, id_scene)
	values(-7.5, 2.5, 0.0, 1.0, 1);
	
insert into sphere (x, y, z, radius, id_scene)
	values(7.5, 2.5, 0.0, 1.0, 1);
	
insert into sphere (x, y, z, radius, id_scene)
	values(0.0, 2.5, 7.5, 1.0, 1);
	
insert into sphere (x, y, z, radius, id_scene)
	values(0.0, 2.5, -7.5, 1.0, 1);
	
insert into sphere (x, y, z, radius, id_scene)
	values(0.0, 7.5, 0.0, 1.0, 1);
	
insert into plane (x, y, z, plane_size_x, plane_size_y, id_scene)
	values(0.0, 0.0, 0.0, 30.0, 30.0, 1);
	
insert into cube (x, y, z, cube_size, id_scene)
	values(0.0, 3.0, 0.0, 6.0, 1);
	
--LIGHTS--
insert into light (x, y, z, a_x, a_y, a_z, light_type, id_scene)
	values(0.0, 20.0, 0.0, 0.0, 0.0, 0.5, "POINT", 1);
		   
insert into light (x, y, z, a_x, a_y, a_z, light_type, id_scene)
	values(10.0, 10.0, 0.0, 0.0, 0.0, 3.0, "POINT", 1);
		   
insert into light (x, y, z, a_x, a_y, a_z, light_type, id_scene)
	values(-10.0, 10.0, 0.0, 0.0, 0.0, 3.0, "POINT", 1);

insert into light (x, y, z, a_x, a_y, a_z, light_type, id_scene)
	values(0.0, 10.0, -10.0, 0.0, 0.0, 3.0, "POINT", 1);
