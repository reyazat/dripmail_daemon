SELECT  IF(es.parent IS NULL,DATEDIFF( NOW( ) , es.senddate ),DATEDIFF( NOW( ) , esp.senddate )) as elapsed_days,
IFNULL(da.actionname,'main') as actionname,es.* FROM `om_email_status` es
LEFT OUTER JOIN `om_dripaction` da ON es.iddripaction = da.id
LEFT OUTER JOIN `om_email_status` esp ON es.parent = esp.id
WHERE es.parent IS NOT NULL AND DATEDIFF(NOW(),esp.senddate) < 28
OR es.parent IS NULL AND DATEDIFF(NOW(),es.senddate) < 28

--------------------------------------

SELECT allow,status FROM `om_robot_status`
WHERE robotname = 'dripaction'
