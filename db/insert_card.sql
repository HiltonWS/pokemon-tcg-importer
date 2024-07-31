INSERT INTO card(id, number, name, image, rarity, eu_price, set_id)
VALUES(?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(id) DO UPDATE SET
    number=excluded.number,
    name=excluded.name,
    image=excluded.image,
    rarity=excluded.rarity,
    eu_price=excluded.eu_price,
    set_id=excluded.set_id;