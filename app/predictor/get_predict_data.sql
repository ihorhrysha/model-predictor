SELECT
  b.Date AS OrderDate,
  b.Date AS TransactionDate,
  b.UUID AS OrderId,
  b.ClientId as ClientCode,
  cl.ManagerId As ManagerId,
  cl.RFMD,
  cl.Segment,
  bbp.PriceTypeId,
  pt.UnifiedType AS UnifiedPriceType,
  b.PlatformId,
  "Reserved" AS Status,
  pl.Name AS Pratform,
  pl.Region AS Region,
  pl.IsExternal AS IsExternal,
  cl.CountryId,
  cnt.NameEn AS OrderCountry,
  cl.StateId,
  st.NameEn AS State,
  "ActivationsStore" AS StoreGroup,
  b.ProductId,
  pr.NameEn AS Product,
  pr.BrandId AS BrandId,
  br.Name AS Brand,
  pr.IsVirtual AS IsVirtual,
  pr.CategoryId AS CategoryId,
  b.Quantity AS OrderQty,
  b.Amount AS OrderAmount,
  b.Quantity AS SoldQty,
  b.Amount*0.8 AS SoldCost,
  bbp.Price AS BasePrice,
  bbp.Price AS UserPrice
FROM
  prosteer.ShoppingCarts AS b
  LEFT JOIN
  prosteer.Clients AS cl
  ON
  b.ClientId = cl.UserId
  LEFT JOIN
  prosteer.Countries AS cnt
  ON
  cnt.Id = cl.CountryId
  LEFT JOIN
  prosteer.States AS st
  ON
  st.Id = cl.StateId
  LEFT JOIN
  prosteer.Platforms AS pl
  ON
  b.PlatformId = pl.Id
  LEFT JOIN
  prosteer.Products AS pr
  ON
  b.ProductId = pr.Id
  LEFT JOIN
  prosteer.Categories AS cat
  ON
  pr.CategoryId = cat.Id
  LEFT JOIN
  prosteer.Brands AS br
  ON
  br.Id = pr.BrandId
  -- LEFT JOIN
  --   prosteer.OrderCosts AS ocs
  -- ON
  --   ocs.OrderId = b.UUID
  --   AND ocs.ProductId = b.ProductId
  LEFT JOIN
  prosteer.ShoppingCartBasePrices AS bbp
  ON
  bbp.OrderId = b.UUID
    AND bbp.ProductId = b.ProductId
  LEFT JOIN
  prosteer.PriceTypes AS pt
  ON
  pt.Id = bbp.PriceTypeId
WHERE
  b.UUID = "{}"