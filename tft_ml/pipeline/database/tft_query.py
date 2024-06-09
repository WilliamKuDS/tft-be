def tft_game_query():
    # query = """select
    # tft_game_info.queue as queue,
    # tft_game_info.lobby_rank as lobby_rank,
    # tft_game.placement as placement,
    # tft_game.level as level,
    # tft_game.round as round,
    # (SELECT tft_augment.name, tft_augment.tier
    # FROM tft_game
    # LEFT JOIN
    # tft_game_augment_id ON tft_game.player_game_id = tft_game_augment_id.game_id
    # LEFT JOIN
    # tft_augment ON tft_game_augment_id.augment_id = tft_augment.augment_id) as augments,
    # (SELECT tft_trait.name, tft_game_trait.count
    # FROM tft_game
    # INNER JOIN tft_game_trait
    # ON tft_game.game_trait_id = tft_game_trait.game_trait_id
    # INNER JOIN tft_trait
    # ON tft_game_trait.trait_id = tft_trait.trait_id) as traits
    # FROM tft_game
    # INNER JOIN tft_game_info
    # ON tft_game.game_id_id = tft_game_info.game_id;
    # """

    # DISTINCT ON allows us to join the tables and not have duplicates
    query = """
    SELECT
    DISTINCT ON (tft_game.player_game_id)
    tft_game.game_id_id as gameID,
    tft_game.placement as placement,
    tft_game.level as level,
    tft_game.round as round,
    tft_game_info.queue as queue,
    tft_game_info.lobby_rank as lobbyrank,
    array_agg(DISTINCT tft_augment.name) as augments,
    json_agg(jsonb_build_object(
        'trait name', tft_trait.name, 
        'count', tft_game_trait.count
    )) AS traits
    FROM tft_game
    LEFT JOIN tft_game_info ON tft_game.game_id_id = tft_game_info.game_id
    LEFT JOIN tft_game_augment_id ON tft_game.player_game_id = tft_game_augment_id.game_id
    LEFT JOIN tft_augment USING (augment_id)
    LEFT JOIN tft_game_game_trait_id ON tft_game.player_game_id = tft_game_game_trait_id.game_id
    LEFT JOIN tft_game_trait ON tft_game_game_trait_id.game_trait_id = tft_game_trait.trait_id_id
    LEFT JOIN tft_trait ON tft_game_trait.trait_id_id = tft_trait.trait_id
    GROUP BY
    tft_game.player_game_id,
    tft_game_info.queue,
    tft_game_info.lobby_rank
    """
    query_two = """
WITH unit_items_cte AS (
    SELECT
        gu.game_id,
        guu.unit_id_id,
        u.name AS unit_name,
        i.name AS item_name
    FROM
        tft_game_game_unit_id gu
    JOIN
        tft_game_unit guu ON gu.game_unit_id = guu.game_unit_id
    JOIN
        tft_unit u ON guu.unit_id_id = u.unit_id
    JOIN
        tft_game_unit_item gui ON guu.game_unit_id = gui.game_unit_id
    JOIN
        tft_item i ON gui.item_id = i.item_id
)
SELECT DISTINCT ON (g.player_game_id)
    g.level,
    g.placement,
    g.length,
    g.round,
    gi.queue,
    gi.lobby_rank,
    array_agg(DISTINCT a.name) AS augment_names,
    array_agg(DISTINCT CONCAT(t.name, ': ', gt.count)) AS trait_info,
    ui.unit_items AS unit_item_info
FROM
    tft_game g
JOIN
    tft_game_info gi ON g.game_id_id = gi.game_id
JOIN
    tft_game_augment_id ga ON g.player_game_id = ga.game_id
JOIN
    tft_augment a ON ga.augment_id = a.augment_id
JOIN
    tft_game_game_trait_id ggt ON g.player_game_id = ggt.game_id
JOIN
    tft_game_trait gt ON ggt.game_trait_id = gt.game_trait_id
JOIN
    tft_trait t ON gt.trait_id_id = t.trait_id
JOIN LATERAL (
    SELECT STRING_AGG(unit_items, ', ') AS unit_items
    FROM (
        SELECT 
            unit_name || ' (' || STRING_AGG(item_name, ', ') || ')' AS unit_items
        FROM unit_items_cte
        WHERE game_id = g.player_game_id
        GROUP BY unit_name
    ) AS unit_items_subquery
) ui ON true
WHERE
    gi.queue = 'Ranked'
GROUP BY
    g.player_game_id, gi.queue, gi.lobby_rank, g.level, g.placement, g.length, g.round, ui.unit_items
"""
    query_optimized = """
WITH ranked_game_ids AS (
    SELECT
        gi.game_id
    FROM
        tft_game_info gi
    WHERE
        gi.queue = 'Ranked'
), ranked_games AS (
    SELECT
        g.player_game_id,
        g.level,
        g.placement,
        g.length,
        g.round,
        gi.queue,
        gi.lobby_rank
    FROM
        ranked_game_ids rgi
    JOIN
        tft_game g ON g.game_id_id = rgi.game_id
    JOIN
        tft_game_info gi ON g.game_id_id = gi.game_id
), unit_items_cte AS (
    SELECT
        gu.game_id,
        guu.unit_id_id,
        u.name AS unit_name,
        guu.star,
        ARRAY_AGG(i.name) AS item_names
    FROM
        tft_game_game_unit_id gu
    JOIN
        tft_game_unit guu ON gu.game_unit_id = guu.game_unit_id
    JOIN
        tft_unit u ON guu.unit_id_id = u.unit_id
    LEFT JOIN
        tft_game_unit_item gui ON guu.game_unit_id = gui.game_unit_id
    LEFT JOIN
        tft_item i ON gui.item_id = i.item_id
    GROUP BY
        gu.game_id, guu.unit_id_id, u.name, guu.star
), augments_cte AS (
    SELECT
        ga.game_id,
        ARRAY_AGG(a.name) AS augment_names
    FROM
        tft_game_augment_id ga
    JOIN
        tft_augment a ON ga.augment_id = a.augment_id
    GROUP BY
        ga.game_id
), traits_cte AS (
    SELECT
        ggt.game_id,
        ARRAY_AGG(JSON_BUILD_OBJECT('name', t.name, 'count', gt.count)) AS trait_info
    FROM
        tft_game_game_trait_id ggt
    JOIN
        tft_game_trait gt ON ggt.game_trait_id = gt.game_trait_id
    JOIN
        tft_trait t ON gt.trait_id_id = t.trait_id
    GROUP BY
        ggt.game_id
)
SELECT
    rg.level,
    rg.placement,
    rg.length,
    rg.round,
    rg.queue,
    rg.lobby_rank,
    a.augment_names as augments,
    t.trait_info as traits,
    (
        SELECT ARRAY_AGG(
            JSON_BUILD_OBJECT(
                'name', u.unit_name,
                'star', u.star,
                'items', u.item_names
            ) ORDER BY u.unit_name
        )
        FROM unit_items_cte u
        WHERE u.game_id = rg.player_game_id
    ) AS units
FROM
    ranked_games rg
JOIN
    augments_cte a ON rg.player_game_id = a.game_id
JOIN
    traits_cte t ON rg.player_game_id = t.game_id
    """
    return query_optimized

def tft_unit_query():
    query = """
    SELECT display_name, tier, stats, ability_name, ability_description, ability_info 
    FROM tft_unit
    """
    return query

def tft_item_query():
    query = """
    SELECT display_name, description 
    FROM tft_item
    """
    return query
