-- dim_customers
SELECT 
    CUSTNAME          AS customer_number
    ,CUSTDES           AS customer_name
    ,CUSTDESLONG       AS full_customer_name
    ,ECUSTDES          AS customer_name_english
    ,STATDES           AS customer_status
    ,OWNERLOGIN        AS customer_owner
    ,INACTIVEFLAG      AS inactive_flag
    ,CREATEDDATE       AS crate_date
    ,BUSINESSTYPE      AS business_area
    ,CTYPENAME         AS customer_type_desc
    ,PCUSTNAME         AS holding_company
    ,CTYPE2NAME        AS customer_sub_type_desc
    ,STATENAME         AS state
    ,STATEA            AS city
    ,COUNTRYNAME       AS country
    ,AGENTCODE         AS agent_number
    ,COMMISSION        AS agent_commission_percent
    ,EMPNUM            AS employee_headcount
    ,PAYCODE           AS terms_of_payment_code
    ,PAYDES            AS terms_of_payment_desc
    ,MAX_CREDIT        AS credit_limit
    ,FORECAST          AS sales_target
FROM CUSTOMERS;







-- fact_je

SELECT
     f.fncnum                      as je_number
    ,f.kline                       as line_number
    ,f.fnclotnum                   as batch_num
    ,f.accname                     as account_number
    ,f.accdes                      as account_name
    ,f.dc                          as credit_debit
    ,f.fncpatname                  as je_type
    ,f.details                     as details
    ,f.fncdate                     as value_date
    ,f.curdate                     as refrence_date
    ,f.credit1                     as credit_in_local_currency
    ,f.debit1                      as debit_in_local_currency
    ,f.credit3                     as credit_in_foreign_currency
    ,f.debit3                      as debit_in_foreign_currency
    ,f.baldate                     as balance_date
    ,f.ivnum                       as refrence
    ,f.booknum                     as refrence_2
    ,f.iaccname                    as offset_account_number
    ,f.iaccdes                     as offset_account_name
    ,f.userlogin                   as username
    ,f.udate                       as je_insert_date
    ,f.debit1 - f.credit1          as amount_in_local_currency
    ,f.debit3 - f.credit3          as amount_in_foreign_currency
    ,f.extractiontimestamputc      as extraction_timestamp_utc
    ,f.extractionid                as extraction_id
    
FROM stg_fnclog f;



-- dim_gl_accounts
SELECT 
    acc.accname                   as account_num
    ,acc.accdes                   as account_name
    ,acc.eaccdes                  as english_account_name
    ,acc.code                     as account_currency
    ,acc.trialbalcode             as level_1_code
    ,acc.trialbaldes              as level_1_desc
    ,acc.secname                  as level_2_desc
    ,acc.acctypename              as level_3_desc
    ,acc.balflag                  as pnl_flag
    ,acc.baltypedes               as financial_statements_title
    ,acct.ord                     as order
    ,acct.acctotal                as pnl_impact
    ,acct.eacctotal               as english_pnl_impact

FROM stg_accounts acc
LEFT JOIN stg_acctypes acct ON (acc.acctypename = acct.acctypename);


-- fact collection
SELECT 
    baldate                       as balance_date
    ,fncnum                       as je_number
    ,ivnum                        as reference_number
    ,fnpatname                    as je_type
    ,details                      as details
    ,sum1                         as amount
    ,code                         as currency
    ,fncref2                      as reference_2
    ,fncdate                      as payment_date
    ,ordname                      as order_name
    ,accname                      as account
    ,sum5                         as amount_in_transaction_currency
    ,code5                        as transaction_currency
    ,fnctrans                     as transaction_id
    ,kline                        as line_id
    ,cust                         as customer_name
    ,requesttimestamputc          as request_timestamp_utc
    ,extractionid                 as extraction_id
FROM stg_obligo_fncitems obf
