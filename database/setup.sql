

CREATE TABLE IF NOT EXISTS player (
    id Serial PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    level INTEGER NOT NULL, 
    xp INTEGER NOT NULL,
    money INTEGER NOT NULL, 
    inventory_slots INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS monster (
    id Serial PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    health INTEGER NOT NULL,
    attack INTEGER NOT NULL,
    defense INTEGER NOT NULL,
    money INTEGER NOT NULL,
    probability INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS object (
    name VARCHAR(100) NOT NULL UNIQUE,
    type VARCHAR(100) NOT NULL,
    property VARCHAR(100) NOT NULL,
    price INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS character (
    name VARCHAR(100) NOT NULL UNIQUE,
    class VARCHAR(100) NOT NULL, -- ICI C'ETAIT UNIQUE : PROBLEME LORS DES INSERTIONS 
    health INTEGER NOT NULL,        -- PARCE QUE LE NOM DE LA CLASSE D'UN MONSTRE N'EST PAS UNIQUE : LOGIQUE
    mana INTEGER NOT NULL,          -- EXEMPLE : Paladin EST PRESENT CHEZ PLUSIEURS PERSONNAGES
    strength INTEGER NOT NULL,      -- ET NE DEVRAIT DONC PAS ETRE UNIQUE
    intelligence INTEGER NOT NULL,
    agility INTEGER NOT NULL,
    username VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS quest (
    name VARCHAR(200) NOT NULL UNIQUE,
    xp INTEGER NOT NULL,
    difficulty INTEGER NOT NULL,
    money INTEGER NOT NULL,
    description VARCHAR(2000)
);

CREATE TABLE IF NOT EXISTS pnjs (
    name VARCHAR(100) NOT NULL UNIQUE,
    dialogue VARCHAR(500) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS pnjs_quest (
    pnj_name VARCHAR(100) REFERENCES pnjs(name) ON DELETE CASCADE,
    quest_name VARCHAR(200) REFERENCES quest(name) ON DELETE CASCADE,
    PRIMARY KEY (pnj_name, quest_name)
);

CREATE TABLE IF NOT EXISTS pnjs_object (
    pnj_name VARCHAR(100) REFERENCES pnjs(name) ON DELETE CASCADE,
    object_name VARCHAR(100) REFERENCES object(name) ON DELETE CASCADE,
    PRIMARY KEY (pnj_name, object_name)
);

CREATE TABLE IF NOT EXISTS spell (
    id Serial PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    mana_cost INTEGER NOT NULL,
    charge_time INTEGER NOT NULL,
    attack_power INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS player_object (
    player_id INTEGER REFERENCES player(id) ON DELETE CASCADE,
    object_name VARCHAR(100) REFERENCES object(name) ON DELETE CASCADE,
    equipped BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (player_id, object_name)
);


CREATE TABLE IF NOT EXISTS quest_object (
    quest_name VARCHAR(200) REFERENCES quest(name) ON DELETE CASCADE,
    object_name VARCHAR(100) REFERENCES object(name) ON DELETE CASCADE,
    PRIMARY KEY (quest_name, object_name)
);

CREATE TABLE IF NOT EXISTS monster_object (
    monster_id INTEGER REFERENCES monster(id) ON DELETE CASCADE,
    object_name VARCHAR(100) REFERENCES object(name) ON DELETE CASCADE,
    probability INTEGER NOT NULL,
    PRIMARY KEY (monster_id, object_name)
);


CREATE TABLE IF NOT EXISTS player_quest (
    player_id INTEGER REFERENCES player(id) ON DELETE CASCADE,
    quest_name VARCHAR(200) REFERENCES quest(name) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'in_progress', -- 'in_progress' or 'completed'
    PRIMARY KEY (player_id, quest_name)
);