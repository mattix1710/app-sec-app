CREATE TABLE "users"(
    "id" SERIAL PRIMARY KEY,
    "username" VARCHAR(100) NOT NULL,
    "email" VARCHAR(255)    NOT NULL,
    "password" VARCHAR(72)  NOT NULL,
    "is_active" BOOLEAN     NOT NULL,
    "is_admin" BOOLEAN      NOT NULL DEFAULT FALSE,
    "last_logged" date      NOT NULL DEFAULT NOW(),

    UNIQUE("username"),
    UNIQUE("email")
);

CREATE TABLE "user_personal_data"(
    "user_id" SERIAL PRIMARY KEY REFERENCES users(id),
    "PESEL" CHAR(11)        UNIQUE KEY,
    "first_name" VARCHAR(100),
    "last_name" VARCHAR(100),
    "blood_type" VARCHAR(5)
);

CREATE TABLE "user_giving_dates"(
    "id" SERIAL PRIMARY KEY,
    "user_id" SERIAL REFERENCES users(id) NOT NULL,
    "date" date             NOT NULL,
    "amount" DECIMAL        NOT NULL,
    "location" VARCHAR(150) NOT NULL
);

CREATE TABLE "sessions"(
    "id" uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    "uid" SERIAL REFERENCES users(id) ON DELETE CASCADE,
    "timestamp" TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE "pass_reset_session"(
    "id" SERIAL PRIMARY KEY,
    "uid" SERIAL REFERENCES users(id) ON DELETE CASCADE,
    "token" CHAR(50) NOT NULL,
    "timestamp" TIMESTAMP NOT NULL DEFAULT NOW(),

    UNIQUE("token")
);

CREATE TABLE "blood_state"(
    "id" SMALLSERIAL PRIMARY KEY,
    "blood_type" VARCHAR(7) NOT NULL,
    "amount" VARCHAR(3) NOT NULL,
    "last_update" TIMESTAMP NOT NULL DEFAULT NOW(),

    UNIQUE("blood_type")
);

-- NOT INSERTED YET

ALTER TABLE "users" ADD "is_supervisor" BOOLEAN DEFAULT FALSE;

CREATE TABLE "branch"(
    "id" SERIAL PRIMARY KEY,
    "supervisor" SERIAL REFERENCES users(id) NOT NULL,
    "name" VARCHAR(255) UNIQUE KEY NOT NULL,
    "address" VARCHAR(255) UNIQUE KEY NOT NULL
);

CREATE TABLE "post"(
    "id" SERIAL PRIMARY KEY,
    "branch_id" SERIAL REFERENCES branch(id) NOT NULL,
    "content" TEXT NOT NULL
);

CREATE TABLE "comment"(
    "id" SERIAL PRIMARY KEY,
    "post_id" SERIAL REFERENCES post(id) NOT NULL,
    "author_id" SERIAL REFERENCES users(id) NOT NULL,
    "content" TEXT NOT NULL
);