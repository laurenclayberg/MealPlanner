BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

DROP TABLE recipe_ingredient_edges;
DROP TABLE tag_recipe_edges;
DROP TABLE units;
DROP TABLE ingredients;
DROP TABLE store_locations;
DROP TABLE recipes;
DROP TABLE tags;
DROP TABLE schema_version;
DROP EXTENSION "uuid-ossp";

COMMIT;
