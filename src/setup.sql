

create Table player (
    id Serial PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    level INTEGER NOT NULL, 
    xp INTEGER NOT NULL,
    money INTEGER NOT NULL, 
    inventory_slots NOT NULL
);

create Table monster (
    id Serial PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    health INTEGER NOT NULL,
    attack INTEGER NOT NULL,
    defense INTEGER NOT NULL,
    money INTEGER NOT NULL,
    probability INTEGER NOT NULL
);

create Table object (
    name VARCHAR(100) NOT NULL UNIQUE,
    type VARCHAR(100) NOT NULL,
    property VARCHAR(100) NOT NULL,
    price INTEGER NOT NULL
);

create Table character (
    name VARCHAR(100) NOT NULL UNIQUE,
    class VARCHAR(100) NOT NULL UNIQUE,
    health INTEGER NOT NULL,
    mana INTEGER NOT NULL,
    strength INTEGER NOT NULL,
    intelligence INTEGER NOT NULL,
    agility INTEGER NOT NULL,
    username VARCHAR(100) NOT NULL
);

create Table quest (
    name VARCHAR(200) NOT NULL UNIQUE,
    xp INTEGER NOT NULL,
    difficulty INTEGER NOT NULL,
    money INTEGER NOT NULL,
    description VARCHAR(2000)
);

create Table pnjs (
    name VARCHAR(100) NOT NULL UNIQUE,
    dialogue VARCHAR(500) NOT NULL UNIQUE,
);

create Table pnjs_quest (
    pnj_name VARCHAR(100) REFERENCES pnjs(name) ON DELETE CASCADE,
    quest_name VARCHAR(200) REFERENCES quest(name) ON DELETE CASCADE,
    PRIMARY KEY (pnj_name, quest_name)
);

create Table pnjs_object (
    pnj_name VARCHAR(100) REFERENCES pnjs(name) ON DELETE CASCADE,
    object_name VARCHAR(100) REFERENCES object(name) ON DELETE CASCADE,
    PRIMARY KEY (pnj_name, object_name)
);

create Table spell (
    id Serial PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    mana_cost INTEGER NOT NULL,
    charge_time INTEGER NOT NULL,
    attack_power INTEGER NOT NULL
);