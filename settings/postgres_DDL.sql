CREATE TABLE "users"(
    "id" BIGINT NOT NULL,
    "username" VARCHAR(50) NOT NULL,
    "email" VARCHAR(50) NOT NULL,
    "password" CHAR(72) NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "is_admin" BOOLEAN NOT NULL
);
ALTER TABLE
    "users" ADD PRIMARY KEY("id");
ALTER TABLE
    "users" ADD CONSTRAINT "users_username_unique" UNIQUE("username");
ALTER TABLE
    "users" ADD CONSTRAINT "users_email_unique" UNIQUE("email");
CREATE TABLE "user_giving_dates"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "date" DATE NOT NULL,
    "amount" DECIMAL(8, 2) NOT NULL,
    "location" VARCHAR(150) NOT NULL
);
ALTER TABLE
    "user_giving_dates" ADD PRIMARY KEY("id");
CREATE TABLE "user_personal_data"(
    "user_id" BIGINT NOT NULL,
    "PESEL" CHAR(11) NULL,
    "first_name" VARCHAR(100) NULL,
    "last_name" VARCHAR(100) NULL,
    "Blood type" BIGINT NULL
);
ALTER TABLE
    "user_personal_data" ADD PRIMARY KEY("user_id");
ALTER TABLE
    "user_personal_data" ADD CONSTRAINT "user_personal_data_pesel_unique" UNIQUE("PESEL");
ALTER TABLE
    "users" ADD CONSTRAINT "users_id_foreign" FOREIGN KEY("id") REFERENCES "user_personal_data"("user_id");
ALTER TABLE
    "user_giving_dates" ADD CONSTRAINT "user_giving_dates_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");