
CREATE OR REPLACE VIEW `demo_data.customers_masked` AS
SELECT
  customer_id,
  full_name,
  IF(SESSION_USER() = "admin@example.com", email, SAFE.SUBSTR(email, 1, 3) || "****@****.com") AS email,
  IF(SESSION_USER() = "admin@example.com", phone, "**********") AS phone,
  IF(SESSION_USER() = "admin@example.com", credit_card, "****-****-****-****") AS credit_card,
  dob
FROM
  `demo_data.customers`;
