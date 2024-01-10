INSERT INTO users (username, email, password, is_active, is_supervisor, is_admin)
    VALUES('user1', 'dummyuser@user.com', '$2b$12$IjUE5aQzF83/Et.20hN/xeZuRopLAV4icSdSuyCet3qqHXrp76Mum', TRUE, FALSE, FALSE),
        ('admin1', 'admin_new@admin.com', '$2b$12$vAYV0dEzp.Lu8Focy/5Zc.b94kR5cIcW052FvOr2pTV5duiSKvWPK', TRUE, FALSE, TRUE),
        ('admin_super', 'supervisor@admin.com', '$2b$12$sQf2G9PlyVvokbPOLKtZGOTEdYqXqB7ZVXUfWEUKc.HfMkZ/.0u1i', TRUE, TRUE, TRUE),
        ('super_second', 'kropelka.app@gmail.com', '$2b$12$0SDsx9XGd4aJAf7vSnJLQOrKjRHwAOVsdatiYt8jkMG7eMaUhix/G', TRUE, TRUE, FALSE),
        ('regular&jack', 'jacksmack@user.com', '$2b$12$Su3ast7YjNYP3ok.leVX1ewtQQTUuHBj0xKbm0NVxrGmFXlmIcZk2', TRUE, FALSE, FALSE),
        ('alice_no_bob', 'alice_alone@user.com', '$2b$12$dJFXqaN6xIo9qn.vi6tcourjBHw1xbqGpu.ILE33eWkt/BPs37rbW', TRUE, FALSE, FALSE),
        ('theVisor', 'visioner@ilookat.you', '$2b$12$dwK9su3YlF.vvLLV2XYj.OE6zXL1GiPspEruMMdcq9OE5guHGZq4a', TRUE, TRUE, FALSE);

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
                ((SELECT id FROM users WHERE username='super_second'), 'Oddział Terenowy Piła', 'Al. Wojska Polskiego 43'),
                ((SELECT id FROM users WHERE username='theVisor'), 'Oddział Terenowy Szamotuły', 'Sukiennicza 13'),
                ((SELECT id FROM users WHERE username='theVisor'), 'Oddział Terenowy Chodzież', 'Żeromskiego 29');