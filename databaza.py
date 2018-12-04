import psycopg2
import json

def PripojenieNaDB():
    pripojenie = "host='localhost' dbname='gis2' user='gis' password='gis'"
    pripojenie = psycopg2.connect(pripojenie)
    return pripojenie.cursor()

def pumpy_pri_ceste(nazov):
    spojenie = PripojenieNaDB()
    spojenie.execute("SELECT osm_id, name, st_asgeojson(st_transform(way,4326)) FROM (WITH RECURSIVE streets AS ( SELECT osm_id, name, way FROM planet_osm_line  WHERE upper(name) = upper('{nazov}'))  SELECT DISTINCT ON (p.osm_id) p.osm_id, p.name, p.way,  trunc(st_distance(st_setsrid(p.way, 4326), st_setsrid(l.way, 4326))) AS distance FROM planet_osm_point p, streets l where p.amenity = 'fuel' AND ST_DWithin(st_setsrid(p.way, 4326), st_setsrid(l.way, 4326), 1000)) pumpy ORDER BY distance;".format(nazov=nazov))
    pumpy = spojenie.fetchall()
    return pumpy

def pumpy_pri_bode(sirka,dlzka):
    spojenie = PripojenieNaDB()
    spojenie.execute("SELECT osm_id, name, st_asgeojson(st_transform(way,4326)) FROM planet_osm_point WHERE ST_DWithin(way, st_transform( st_setsrid(st_makepoint({dlzka}, {sirka}), 4326), 3857), 5000) AND amenity = 'fuel';".format(sirka=sirka, dlzka=dlzka))
    pumpy = spojenie.fetchall()
    return pumpy

def pumpy_v_oblasti(nazov):
    spojenie = PripojenieNaDB()
    spojenie.execute("SELECT DISTINCT point.name, st_asgeojson(st_transform(point.way,4326)), st_asgeojson(st_transform(pol.way,4326))  FROM planet_osm_polygon pol, planet_osm_point point WHERE upper(pol.name) = upper('{nazov}') and point.amenity = 'fuel' AND st_intersects(pol.way, point.way);".format(nazov=nazov))
    pumpy = spojenie.fetchall()
    return pumpy