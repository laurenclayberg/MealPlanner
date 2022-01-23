BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

CREATE EXTENSION "uuid-ossp";

CREATE TABLE schema_version (
  id      BIGSERIAL PRIMARY KEY,
  version BIGINT
);
INSERT INTO schema_version (id, version) VALUES (0, 0);

CREATE TABLE tags (
    id      BIGSERIAL PRIMARY KEY,

    name    VARCHAR(128) NOT NULL UNIQUE,

    created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted TIMESTAMPTZ DEFAULT NULL
);

CREATE TABLE recipes (
    id      BIGSERIAL PRIMARY KEY,
    pubid   UUID UNIQUE DEFAULT uuid_generate_v4(),

    name         TEXT NOT NULL,
    time         INTEGER,  -- Minutes to bake
    servings     INTEGER,
    instructions TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
    source       TEXT,  -- Link to where recipe is from
    rating       INTEGER CHECK (rating >= 1 AND rating <= 5),  -- Eventually migrate this to a user-specific rating

    created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted TIMESTAMPTZ DEFAULT NULL
);

CREATE TABLE store_locations (
    id      BIGSERIAL PRIMARY KEY,
    pubid   UUID UNIQUE DEFAULT uuid_generate_v4(),

    name    VARCHAR(128) NOT NULL UNIQUE,

    created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted TIMESTAMPTZ DEFAULT NULL
);

CREATE TABLE ingredients (
    id      BIGSERIAL PRIMARY KEY,
    pubid   UUID UNIQUE DEFAULT uuid_generate_v4(),

    name         VARCHAR(128) NOT NULL UNIQUE,
    location_id  BIGINT,

    created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted TIMESTAMPTZ DEFAULT NULL,

    CONSTRAINT fk_location
      FOREIGN KEY(location_id)
      REFERENCES store_locations(id)
      ON DELETE SET NULL
);

CREATE TABLE units (
    id      BIGSERIAL PRIMARY KEY,
    pubid   UUID UNIQUE DEFAULT uuid_generate_v4(),

    name            VARCHAR(128) NOT NULL UNIQUE,
    weight_in_grams NUMERIC DEFAULT NULL,
    volume_in_ml    NUMERIC DEFAULT NULL,

    created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted TIMESTAMPTZ DEFAULT NULL
);

CREATE TABLE tag_recipe_edges (
    tag_id     BIGINT NOT NULL,
    recipe_id  BIGINT NOT NULL,

    created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted TIMESTAMPTZ DEFAULT NULL,

    PRIMARY KEY (tag_id, recipe_id), 
    CONSTRAINT fk_tag
      FOREIGN KEY(tag_id)
      REFERENCES tags(id)
      ON DELETE CASCADE,
    CONSTRAINT fk_recipe
      FOREIGN KEY(recipe_id)
      REFERENCES recipes(id)
      ON DELETE CASCADE
);

CREATE TABLE recipe_ingredient_edges (
    recipe_id     BIGINT NOT NULL,
    ingredient_id BIGINT NOT NULL,
    quantity      NUMERIC NOT NULL,
    unit_id       BIGINT NOT NULL,

    created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted TIMESTAMPTZ DEFAULT NULL,

    PRIMARY KEY (recipe_id, ingredient_id, unit_id),
    CONSTRAINT fk_recipe
      FOREIGN KEY(recipe_id)
      REFERENCES recipes(id)
      ON DELETE CASCADE,
    CONSTRAINT fk_ingredient
      FOREIGN KEY(ingredient_id)
      REFERENCES ingredients(id)
      ON DELETE CASCADE,
    CONSTRAINT fk_unit
      FOREIGN KEY(unit_id)
      REFERENCES units(id)
      ON DELETE CASCADE
);

INSERT INTO units (name, weight_in_grams, volume_in_ml) VALUES
  ('item', NULL, NULL),
  ('cup', NULL, 236.588),
  ('pounds', 453.592, NULL);


COMMIT;
