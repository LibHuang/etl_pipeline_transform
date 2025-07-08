select
    ID,
    NAME,
    COLOUR,
    PRODUCTCODE,
    IMAGEURL,
    "price.current.value",
    "price.previous.value",
    {{ dollars_to_cents('"price.current.value"') }} as centvalue, -- need to double quote ' "" ' for columns with "."
    {{ price_difference('"price.current.value"', '"price.previous.value"') }} as price_adjustment
from
    {{ ref('stg_tpch_products') }}