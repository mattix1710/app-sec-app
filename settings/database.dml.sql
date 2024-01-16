-- INSERT initial records to the database

INSERT INTO blood_state(id, blood_type, amount, last_update)
        VALUES  (0, '0 Rh +', 'qF', '1970-01-01 01:01:01'),
                (1, '0 Rh -', 'qF', '1970-01-01 01:01:01'),
                (2, 'A Rh +', 'qF', '1970-01-01 01:01:01'),
                (3, 'A Rh -', 'qF', '1970-01-01 01:01:01'),
                (4, 'B Rh +', 'qF', '1970-01-01 01:01:01'),
                (5, 'B Rh -', 'qF', '1970-01-01 01:01:01'),
                (6, 'AB Rh +', 'qF', '1970-01-01 01:01:01'),
                (7, 'AB Rh -', 'qF', '1970-01-01 01:01:01');

INSERT INTO users (username, email, password, is_active, is_supervisor, is_admin)
    VALUES('admin1', 'admin_new@admin.com', '$2b$12$vAYV0dEzp.Lu8Focy/5Zc.b94kR5cIcW052FvOr2pTV5duiSKvWPK', TRUE, FALSE, TRUE),
        ('admin_super', 'supervisor@admin.com', '$2b$12$sQf2G9PlyVvokbPOLKtZGOTEdYqXqB7ZVXUfWEUKc.HfMkZ/.0u1i', TRUE, TRUE, TRUE),
        ('super_second', 'kropelka.app@gmail.com', '$2b$12$0SDsx9XGd4aJAf7vSnJLQOrKjRHwAOVsdatiYt8jkMG7eMaUhix/G', TRUE, TRUE, FALSE),
        ('theVisor', 'visioner@ilookat.you', '$2b$12$dwK9su3YlF.vvLLV2XYj.OE6zXL1GiPspEruMMdcq9OE5guHGZq4a', TRUE, TRUE, FALSE),
        ('iCu', 'ccc@u2.com', '$2b$12$DRvi/haVmNUow1x90z2uLO6H0v1UTJsk8q9OTbsNCi0vZEOJ8WZVG', TRUE, TRUE, FALSE);

INSERT INTO branch(supervisor, name, address)
        VALUES  ((SELECT id FROM users WHERE username='admin_super'), 'RCKIK Poznań', 'Marcelińska 44, Poznań'),
                ((SELECT id FROM users WHERE username='super_second'), 'Oddział Terenowy Piła', 'Al. Wojska Polskiego 43'),
                ((SELECT id FROM users WHERE username='theVisor'), 'Oddział Terenowy Szamotuły', 'Sukiennicza 13'),
                ((SELECT id FROM users WHERE username='iCu'), 'Oddział Terenowy Chodzież', 'Żeromskiego 29');

INSERT INTO post(branch_id, title, title_normalized, content)
    VALUES((SELECT id FROM branch WHERE name='Oddział Terenowy Piła'), 'New Year 2023 stats!', 'new-year-2023-stats!', E'The first week of 2024 marked a notable surge in participation at blood donation centers, reflecting a commendable increase in community engagement and awareness. Statistics revealed a significant uptick in the number of individuals who willingly contributed to this life-saving cause. The heightened participation is indicative of a positive shift in public attitudes towards blood donation, showcasing a collective commitment to supporting healthcare initiatives. This surge in donors during the initial week of the year not only speaks to the community\'s sense of responsibility but also suggests that awareness campaigns and outreach efforts have been successful in conveying the importance of regular blood donations. The improved statistics underscore a promising trend, portraying a community that is increasingly proactive in its dedication to providing a vital resource for those in need.\r\n\r\nTYSM! 🥰😊😊🥰😏'),
    ((SELECT id FROM branch WHERE name='Oddział Terenowy Szamotuły'), 'Next away action on PP!', 'next-away-action-on-pp!', E'Hello dear blood donors!\r\nWe are organizing next blood donation action on the campus of Poznan University of Technology❕❕\r\nWe are very excited and we hope you will come to us with your blood 🧛');

INSERT INTO comment(post_id, author_id, content)
    VALUES((SELECT id FROM post WHERE title_normalized='next-away-action-on-pp!'), (SELECT id FROM users WHERE username='theVisor'), 'first!'),
    ((SELECT id FROM post WHERE title_normalized='next-away-action-on-pp!'), (SELECT id FROM users WHERE username='theVisor'), E'yeahhh 🤣\nbut whenn?'),
    ((SELECT id FROM post WHERE title_normalized='next-away-action-on-pp!'), (SELECT id FROM users WHERE username='iCu'), E'I\'m so red and what\'s &lt;b&gt;important&lt;/b&gt;! Cherry-like XD');