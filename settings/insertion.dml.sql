INSERT INTO 'users' ('username', 'email', 'password', 'is_active', 'is_supervisor', 'is_admin')
    VALUES('user1', 'dummyuser@user.com', '$2b$12$IjUE5aQzF83/Et.20hN/xeZuRopLAV4icSdSuyCet3qqHXrp76Mum', TRUE, FALSE, FALSE),
    VALUES('admin1', 'admin@admin.com', '$2b$12$vAYV0dEzp.Lu8Focy/5Zc.b94kR5cIcW052FvOr2pTV5duiSKvWPK', TRUE, FALSE, TRUE),
    VALUES('admin_super', 'supervisor@admin.com', '$2b$12$sQf2G9PlyVvokbPOLKtZGOTEdYqXqB7ZVXUfWEUKc.HfMkZ/.0u1i', TRUE, TRUE, TRUE),
    VALUES('super_second', 'kropelka.app@gmail.com', '$2b$12$0SDsx9XGd4aJAf7vSnJLQOrKjRHwAOVsdatiYt8jkMG7eMaUhix/G', TRUE, TRUE, FALSE),
    VALUES('regular&jack', 'jacksmack@user.com', '$2b$12$Su3ast7YjNYP3ok.leVX1ewtQQTUuHBj0xKbm0NVxrGmFXlmIcZk2', TRUE, FALSE, FALSE),
    VALUES('alice_no_bob', 'alice_alone@user.com', '$2b$12$dJFXqaN6xIo9qn.vi6tcourjBHw1xbqGpu.ILE33eWkt/BPs37rbW', TRUE, FALSE, FALSE);

INSERT INTO blood_state(id, blood_type, amount)
        VALUES  (0, '0 Rh +', 'qF'),
                (1, '0 Rh -', 'qF'),
                (2, 'A Rh +', 'qF'),
                (3, 'A Rh -', 'qF'),
                (4, 'B Rh +', 'qF'),
                (5, 'B Rh -', 'qF'),
                (6, 'AB Rh +', 'qF'),
                (7, 'AB Rh -', 'qF');

INSERT INTO branch(supervisor, name, address)
        VALUES  ((SELECT id FROM users WHERE username='admin_super'), 'RCKIK Poznań', 'Marcelińska 44, Poznań'),
        VALUES  ((SELECT id FROM users WHERE username='super_second'), 'Oddział Terenowy Piła', 'Al. Wojska Polskiego 43');

INSERT INTO branch(name, address)
        VALUES  ('Oddział Terenowy Szamotuły', 'Sukiennicza 13'),
        VALUES  ('Oddział Terenowy Chodzież', 'Żeromskiego 29');