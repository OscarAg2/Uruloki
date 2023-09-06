    SELECT *
        FROM (
            SELECT *, ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS row_num
            FROM OscarPrueba
        ) AS t
        WHERE row_num BETWEEN ? AND ?