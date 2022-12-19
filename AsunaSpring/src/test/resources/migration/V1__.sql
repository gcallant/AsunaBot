CREATE TABLE character_classes
(
    id         UUID default gen_random_uuid() NOT NULL,
    class_name VARCHAR(255),
    CONSTRAINT pk_character_classes PRIMARY KEY (id)
);

CREATE TABLE character_races
(
    id        UUID default gen_random_uuid() NOT NULL,
    race_name VARCHAR(50)                    NOT NULL,
    CONSTRAINT pk_character_races PRIMARY KEY (id)
);

CREATE TABLE eso_characters
(
    id                 UUID    default gen_random_uuid() NOT NULL,
    created_at         TIMESTAMP with time zone          NOT NULL,
    updated_at         TIMESTAMP with time zone          NOT NULL,
    eso_user_id        UUID                              NOT NULL,
    character_name     VARCHAR(50)                       NOT NULL,
    event_role_id      UUID                              NOT NULL,
    character_class_id UUID                              NOT NULL,
    character_race_id  UUID                              NOT NULL,
    certified          BOOLEAN default false             NOT NULL,
    CONSTRAINT pk_eso_characters PRIMARY KEY (id)
);

CREATE TABLE eso_users
(
    id              UUID default gen_random_uuid() NOT NULL,
    created_at      TIMESTAMP with time zone       NOT NULL,
    updated_at      TIMESTAMP with time zone       NOT NULL,
    family_name     VARCHAR(300)                   NOT NULL,
    guild_member_id UUID                           NOT NULL,
    CONSTRAINT pk_eso_users PRIMARY KEY (id)
);

CREATE TABLE event_data
(
    id                    UUID    default gen_random_uuid() NOT NULL,
    created_at            TIMESTAMP with time zone          NOT NULL,
    updated_at            TIMESTAMP with time zone          NOT NULL,
    event_id              UUID                              NOT NULL,
    event_time            TIMESTAMP with time zone          NOT NULL,
    event_description     VARCHAR(2000)                     NOT NULL,
    event_leader          UUID                              NOT NULL,
    required_minimum_role BOOLEAN default false             NOT NULL,
    minimum_event_role_id UUID,
    CONSTRAINT pk_event_data PRIMARY KEY (id)
);

CREATE TABLE event_roles
(
    id         UUID default gen_random_uuid() NOT NULL,
    created_at TIMESTAMP with time zone       NOT NULL,
    updated_at TIMESTAMP with time zone       NOT NULL,
    role_name  VARCHAR(50)                    NOT NULL,
    CONSTRAINT pk_event_roles PRIMARY KEY (id)
);

CREATE TABLE event_rosters
(
    id                   UUID default gen_random_uuid() NOT NULL,
    created_at           TIMESTAMP with time zone       NOT NULL,
    updated_at           TIMESTAMP with time zone       NOT NULL,
    event_id             UUID                           NOT NULL,
    max_tanks            SMALLINT,
    max_heals            SMALLINT,
    max_ranged_dps       SMALLINT,
    max_melee_dps        SMALLINT,
    signed_up_tanks      SMALLINT                       NOT NULL,
    signed_up_heals      SMALLINT                       NOT NULL,
    signed_up_ranged_dps SMALLINT                       NOT NULL,
    signed_up_melee_dps  SMALLINT                       NOT NULL,
    CONSTRAINT pk_event_rosters PRIMARY KEY (id)
);

CREATE TABLE event_signups
(
    id                 UUID default gen_random_uuid() NOT NULL,
    created_at         TIMESTAMP with time zone       NOT NULL,
    updated_at         TIMESTAMP with time zone       NOT NULL,
    role_id            UUID                           NOT NULL,
    eso_character_id   UUID                           NOT NULL,
    no_call_no_show    BOOLEAN                        NOT NULL,
    guild_member_notes VARCHAR(4000),
    guild_member_id    UUID                           NOT NULL,
    CONSTRAINT pk_event_signups PRIMARY KEY (id)
);

CREATE TABLE event_signups_event
(
    event_id        UUID NOT NULL,
    event_signup_id UUID NOT NULL,
    CONSTRAINT pk_event_signups_event PRIMARY KEY (event_id)
);

CREATE TABLE event_types
(
    id              UUID default gen_random_uuid() NOT NULL,
    created_at      TIMESTAMP with time zone       NOT NULL,
    updated_at      TIMESTAMP with time zone       NOT NULL,
    event_type_name VARCHAR(100)                   NOT NULL,
    CONSTRAINT pk_event_types PRIMARY KEY (id)
);

CREATE TABLE events
(
    id            UUID default gen_random_uuid() NOT NULL,
    created_at    TIMESTAMP with time zone       NOT NULL,
    updated_at    TIMESTAMP with time zone       NOT NULL,
    event_name    VARCHAR(200)                   NOT NULL,
    event_type_id UUID                           NOT NULL,
    guild_id      UUID                           NOT NULL,
    CONSTRAINT pk_events PRIMARY KEY (id)
);

CREATE TABLE gear_piece_gear_requests
(
    id              UUID    default gen_random_uuid() NOT NULL,
    created_at      TIMESTAMP with time zone          NOT NULL,
    updated_at      TIMESTAMP with time zone          NOT NULL,
    gear_request_id UUID                              NOT NULL,
    gear_piece_id   UUID                              NOT NULL,
    active          BOOLEAN default false             NOT NULL,
    CONSTRAINT pk_gear_piece_gear_requests PRIMARY KEY (id)
);

CREATE TABLE gear_pieces
(
    id              UUID default gen_random_uuid() NOT NULL,
    created_at      TIMESTAMP with time zone       NOT NULL,
    updated_at      TIMESTAMP with time zone       NOT NULL,
    gear_piece_name VARCHAR(100)                   NOT NULL,
    CONSTRAINT pk_gear_pieces PRIMARY KEY (id)
);

CREATE TABLE gear_requests
(
    id              UUID default gen_random_uuid() NOT NULL,
    created_at      TIMESTAMP with time zone       NOT NULL,
    updated_at      TIMESTAMP with time zone       NOT NULL,
    guild_member_id UUID                           NOT NULL,
    gear_set_id     UUID                           NOT NULL,
    CONSTRAINT pk_gear_requests PRIMARY KEY (id)
);

CREATE TABLE gear_sets
(
    id            UUID default gen_random_uuid() NOT NULL,
    created_at    TIMESTAMP with time zone       NOT NULL,
    updated_at    TIMESTAMP with time zone       NOT NULL,
    gear_set_name VARCHAR(300)                   NOT NULL,
    location_id   UUID                           NOT NULL,
    CONSTRAINT pk_gear_sets PRIMARY KEY (id)
);

CREATE TABLE guild_guild_members
(
    id              UUID default gen_random_uuid() NOT NULL,
    created_at      TIMESTAMP with time zone       NOT NULL,
    updated_at      TIMESTAMP with time zone       NOT NULL,
    guild_id        UUID                           NOT NULL,
    guild_member_id UUID                           NOT NULL,
    CONSTRAINT pk_guild_guild_members PRIMARY KEY (id)
);

CREATE TABLE guild_members
(
    id              UUID default gen_random_uuid() NOT NULL,
    created_at      TIMESTAMP with time zone       NOT NULL,
    updated_at      TIMESTAMP with time zone       NOT NULL,
    name            VARCHAR(300)                   NOT NULL,
    discord_user_id BIGINT                         NOT NULL,
    CONSTRAINT pk_guild_members PRIMARY KEY (id)
);

CREATE TABLE guild_roles
(
    id              UUID default gen_random_uuid() NOT NULL,
    created_at      TIMESTAMP with time zone       NOT NULL,
    updated_at      TIMESTAMP with time zone       NOT NULL,
    discord_role_id BIGINT                         NOT NULL,
    CONSTRAINT pk_guild_roles PRIMARY KEY (id)
);

CREATE TABLE guilds
(
    id                   UUID default gen_random_uuid() NOT NULL,
    created_at           TIMESTAMP with time zone       NOT NULL,
    updated_at           TIMESTAMP with time zone       NOT NULL,
    guild_name           VARCHAR(500)                   NOT NULL,
    time_zone            VARCHAR(100)                   NOT NULL,
    create_event_role_id UUID                           NOT NULL,
    admin_role_id        UUID                           NOT NULL,
    CONSTRAINT pk_guilds PRIMARY KEY (id)
);

CREATE TABLE location_types
(
    id         UUID default gen_random_uuid() NOT NULL,
    created_at TIMESTAMP with time zone       NOT NULL,
    updated_at TIMESTAMP with time zone       NOT NULL,
    type_name  VARCHAR(50)                    NOT NULL,
    CONSTRAINT pk_location_types PRIMARY KEY (id)
);

CREATE TABLE locations
(
    id               UUID default gen_random_uuid() NOT NULL,
    created_at       TIMESTAMP with time zone       NOT NULL,
    updated_at       TIMESTAMP with time zone       NOT NULL,
    location_name    VARCHAR(300)                   NOT NULL,
    location_type_id UUID                           NOT NULL,
    CONSTRAINT pk_locations PRIMARY KEY (id)
);

CREATE TABLE parses
(
    id               UUID default gen_random_uuid() NOT NULL,
    created_at       TIMESTAMP with time zone       NOT NULL,
    updated_at       TIMESTAMP with time zone       NOT NULL,
    eso_character_id UUID                           NOT NULL,
    dps              INTEGER                        NOT NULL,
    parse_file_key   UUID                           NOT NULL,
    CONSTRAINT pk_parses PRIMARY KEY (id)
);

CREATE TABLE themes
(
    id         UUID default gen_random_uuid() NOT NULL,
    created_at TIMESTAMP with time zone       NOT NULL,
    updated_at TIMESTAMP with time zone       NOT NULL,
    theme_name VARCHAR(50)                    NOT NULL,
    CONSTRAINT pk_themes PRIMARY KEY (id)
);

CREATE TABLE users
(
    id              UUID    default gen_random_uuid() NOT NULL,
    created_at      TIMESTAMP with time zone          NOT NULL,
    updated_at      TIMESTAMP with time zone          NOT NULL,
    guild_member_id UUID                              NOT NULL,
    locale          VARCHAR(50)                       NOT NULL,
    time_zone       VARCHAR(100)                      NOT NULL,
    theme_id        UUID                              NOT NULL,
    admin           BOOLEAN default false             NOT NULL,
    CONSTRAINT pk_users PRIMARY KEY (id)
);

ALTER TABLE eso_characters
    ADD CONSTRAINT FK_ESO_CHARACTERS_ON_CHARACTER_CLASS FOREIGN KEY (character_class_id) REFERENCES character_classes (id);

CREATE INDEX IDX_ESO_CHARACTERS_ON_CHARACTER_CLASS ON eso_characters (character_class_id);

ALTER TABLE eso_characters
    ADD CONSTRAINT FK_ESO_CHARACTERS_ON_CHARACTER_RACE FOREIGN KEY (character_race_id) REFERENCES character_races (id);

CREATE INDEX IDX_ESO_CHARACTERS_ON_CHARACTER_RACE ON eso_characters (character_race_id);

ALTER TABLE eso_characters
    ADD CONSTRAINT FK_ESO_CHARACTERS_ON_ESO_USER FOREIGN KEY (eso_user_id) REFERENCES eso_users (id);

CREATE INDEX IDX_ESO_CHARACTERS_ON_ESO_USER ON eso_characters (eso_user_id);

ALTER TABLE eso_characters
    ADD CONSTRAINT FK_ESO_CHARACTERS_ON_EVENT_ROLE FOREIGN KEY (event_role_id) REFERENCES event_roles (id);

CREATE INDEX IDX_ESO_CHARACTERS_ON_EVENT_ROLE ON eso_characters (event_role_id);

ALTER TABLE eso_users
    ADD CONSTRAINT FK_ESO_USERS_ON_GUILD_MEMBER FOREIGN KEY (guild_member_id) REFERENCES guild_members (id);

CREATE INDEX IDX_ESO_USERS_ON_GUILD_MEMBER ON eso_users (guild_member_id);

ALTER TABLE events
    ADD CONSTRAINT FK_EVENTS_ON_EVENT_TYPE FOREIGN KEY (event_type_id) REFERENCES event_types (id);

CREATE INDEX IDX_EVENTS_ON_EVENT_TYPE ON events (event_type_id);

ALTER TABLE events
    ADD CONSTRAINT FK_EVENTS_ON_GUILD FOREIGN KEY (guild_id) REFERENCES guilds (id) ON DELETE CASCADE;

CREATE INDEX IDX_EVENTS_ON_GUILD ON events (guild_id);

ALTER TABLE event_data
    ADD CONSTRAINT FK_EVENT_DATA_ON_EVENT FOREIGN KEY (event_id) REFERENCES events (id);

CREATE INDEX IDX_EVENT_DATA_ON_EVENT ON event_data (event_id);

ALTER TABLE event_data
    ADD CONSTRAINT FK_EVENT_DATA_ON_EVENT_LEADER FOREIGN KEY (event_leader) REFERENCES guild_members (id);

CREATE INDEX IDX_EVENT_DATA_ON_EVENT_LEADER ON event_data (event_leader);

ALTER TABLE event_data
    ADD CONSTRAINT FK_EVENT_DATA_ON_MINIMUM_EVENT_ROLE FOREIGN KEY (minimum_event_role_id) REFERENCES guild_roles (id);

CREATE INDEX IDX_EVENT_DATA_ON_MINIMUM_EVENT_ROLE ON event_data (minimum_event_role_id);

ALTER TABLE event_rosters
    ADD CONSTRAINT FK_EVENT_ROSTERS_ON_EVENT FOREIGN KEY (event_id) REFERENCES events (id);

CREATE INDEX IDX_EVENT_ROSTERS_ON_EVENT ON event_rosters (event_id);

ALTER TABLE event_signups
    ADD CONSTRAINT FK_EVENT_SIGNUPS_ON_GUILD_MEMBER FOREIGN KEY (guild_member_id) REFERENCES guild_members (id);

CREATE INDEX IDX_EVENT_SIGNUPS_ON_GUILD_MEMBER ON event_signups (guild_member_id);

ALTER TABLE event_signups
    ADD CONSTRAINT FK_EVENT_SIGNUPS_ON_ROLE FOREIGN KEY (role_id) REFERENCES event_roles (id);

CREATE INDEX IDX_EVENT_SIGNUPS_ON_ROLE ON event_signups (role_id);

ALTER TABLE gear_piece_gear_requests
    ADD CONSTRAINT FK_GEAR_PIECE_GEAR_REQUESTS_ON_GEAR_PIECE FOREIGN KEY (gear_piece_id) REFERENCES gear_pieces (id);

CREATE INDEX IDX_GEAR_PIECE_GEAR_REQUESTS_ON_GEAR_PIECE ON gear_piece_gear_requests (gear_piece_id);

ALTER TABLE gear_piece_gear_requests
    ADD CONSTRAINT FK_GEAR_PIECE_GEAR_REQUESTS_ON_GEAR_REQUEST FOREIGN KEY (gear_request_id) REFERENCES gear_requests (id);

CREATE INDEX IDX_GEAR_PIECE_GEAR_REQUESTS_ON_GEAR_REQUEST ON gear_piece_gear_requests (gear_request_id);

ALTER TABLE gear_requests
    ADD CONSTRAINT FK_GEAR_REQUESTS_ON_GEAR_SET FOREIGN KEY (gear_set_id) REFERENCES gear_sets (id);

CREATE INDEX IDX_GEAR_REQUESTS_ON_GEAR_SET ON gear_requests (gear_set_id);

ALTER TABLE gear_requests
    ADD CONSTRAINT FK_GEAR_REQUESTS_ON_GUILD_MEMBER FOREIGN KEY (guild_member_id) REFERENCES guild_members (id);

CREATE INDEX IDX_GEAR_REQUESTS_ON_GUILD_MEMBER ON gear_requests (guild_member_id);

ALTER TABLE gear_sets
    ADD CONSTRAINT FK_GEAR_SETS_ON_LOCATION FOREIGN KEY (location_id) REFERENCES locations (id);

CREATE INDEX IDX_GEAR_SETS_ON_LOCATION ON gear_sets (location_id);

ALTER TABLE guilds
    ADD CONSTRAINT FK_GUILDS_ON_ADMIN_ROLE FOREIGN KEY (admin_role_id) REFERENCES guild_roles (id);

CREATE INDEX IDX_GUILDS_ON_ADMIN_ROLE ON guilds (admin_role_id);

ALTER TABLE guilds
    ADD CONSTRAINT FK_GUILDS_ON_CREATE_EVENT_ROLE FOREIGN KEY (create_event_role_id) REFERENCES guild_roles (id);

CREATE INDEX IDX_GUILDS_ON_CREATE_EVENT_ROLE ON guilds (create_event_role_id);

ALTER TABLE guild_guild_members
    ADD CONSTRAINT FK_GUILD_GUILD_MEMBERS_ON_GUILD FOREIGN KEY (guild_id) REFERENCES guilds (id) ON DELETE CASCADE;

CREATE INDEX IDX_GUILD_GUILD_MEMBERS_ON_GUILD ON guild_guild_members (guild_id);

ALTER TABLE guild_guild_members
    ADD CONSTRAINT FK_GUILD_GUILD_MEMBERS_ON_GUILD_MEMBER FOREIGN KEY (guild_member_id) REFERENCES guild_members (id) ON DELETE CASCADE;

CREATE INDEX IDX_GUILD_GUILD_MEMBERS_ON_GUILD_MEMBER ON guild_guild_members (guild_member_id);

ALTER TABLE locations
    ADD CONSTRAINT FK_LOCATIONS_ON_LOCATION_TYPE FOREIGN KEY (location_type_id) REFERENCES location_types (id);

CREATE INDEX IDX_LOCATIONS_ON_LOCATION_TYPE ON locations (location_type_id);

ALTER TABLE parses
    ADD CONSTRAINT FK_PARSES_ON_ESO_CHARACTER FOREIGN KEY (eso_character_id) REFERENCES eso_characters (id);

CREATE INDEX IDX_PARSES_ON_ESO_CHARACTER ON parses (eso_character_id);

ALTER TABLE users
    ADD CONSTRAINT FK_USERS_ON_GUILD_MEMBER FOREIGN KEY (guild_member_id) REFERENCES guild_members (id);

CREATE INDEX IDX_USERS_ON_GUILD_MEMBER ON users (guild_member_id);

ALTER TABLE users
    ADD CONSTRAINT FK_USERS_ON_THEME FOREIGN KEY (theme_id) REFERENCES themes (id);

CREATE INDEX IDX_USERS_ON_THEME ON users (theme_id);

ALTER TABLE event_signups_event
    ADD CONSTRAINT fk_evesigeve_on_event FOREIGN KEY (event_signup_id) REFERENCES events (id);

ALTER TABLE event_signups_event
    ADD CONSTRAINT fk_evesigeve_on_event_signup FOREIGN KEY (event_id) REFERENCES event_signups (id);
