from flask import Flask, render_template, request, jsonify
import decimal
from os import stat, path
import numpy as np
from flask import Flask, render_template, url_for
import json
import pymysql
from datetime import timedelta
from datetime import datetime
import pandas as pd
import xlwt as xlwt
from flask import jsonify
from flask import request
import warnings
import openpyxl
app = Flask(__name__)
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)

@app.route('/')
def index_cg():
    return render_template("采购日报.html")
@app.route('/仓库日报.html')
def index_ck():
    return render_template('仓库日报.html')
@app.route('/test3', methods=['POST'])
def index_jy():
    con = pymysql.connect(host='192.168.86.79', user='wanjunsheng', passwd='df2932141LFDF', db='warehouse', port=3307,
                          charset='utf8')
    cur = con.cursor()
    # sql_jy = 'SELECT	a.warehouse_code,	sum( a.num ) AS num,	a.type FROM	(	SELECT		warehouse_code,		purchase_order_no,		storage_position,		sku,		sum( actual_num ) AS num,	CASE						WHEN post_code_start_time IS NOT NULL 			AND post_code_end_time IS NOT NULL 			AND quality_time IS NOT NULL 			AND upper_start_time IS NOT NULL 			AND upper_end_time IS NULL THEN				"SJZ" 				WHEN post_code_start_time IS NOT NULL 				AND post_code_end_time IS NOT NULL 				AND quality_time IS NOT NULL 				AND paragraph != 11 				AND upper_start_time IS NULL THEN					"DSJ" 					WHEN post_code_start_time IS NOT NULL 					AND post_code_end_time IS NOT NULL 					AND quality_time IS NOT NULL 					AND paragraph = 11 					AND upper_start_time IS NULL THEN						"DGNZJ" 						WHEN post_code_start_time IS NULL THEN						"DTM" ELSE "else" 					END AS type,					cast( ROUND( ( unix_timestamp( now()) - unix_timestamp( quality_start_time ) ) / 3600, 2 ) AS DECIMAL ) AS s 				FROM					ueb_quality_warehousing_record 				WHERE					paragraph != 5 					AND purchase_order_no NOT LIKE "ABD%" 					AND warehouse_code IN ( "HM_AA", "SZ_AA" ) 					AND storage_position NOT IN ( "MV0028", "MV0015", "MV0054" ) 				GROUP BY					purchase_order_no,					sku,					warehouse_code 				) a 			GROUP BY				a.warehouse_code,				a.type UNION			SELECT				a.warehouse_code,				sum( a.quality_num ),				a.type AS num 			FROM				(				SELECT					warehouse_code,					"RK" AS purchase_order_no,					car_no AS storage_position,					"RK" AS sku,					box_number AS quality_num,					"DRK" AS type,					cast( ROUND( ( unix_timestamp( now()) - unix_timestamp( add_time ) ) / 3600, 2 ) AS DECIMAL ) AS s 				FROM					ueb_express_receipt 				WHERE					STATUS = 1 					AND warehouse_type = 1 					AND is_abnormal = "2" 					AND is_quality = "2" 					AND is_end = "1" 				) a 			GROUP BY				a.warehouse_code,				a.type UNION			SELECT				a.warehouse_code,				sum( a.quality_num ) AS num ,								a.type			FROM				(				SELECT					a.warehouse_code,					a.order_id AS purchase_order_no,					a.platform_code AS storage_position,					a.platform_order_id AS sku,					sum( b.quantity ) AS quality_num,				CASE			WHEN a.wh_order_status IN ( 1, 2 ) 		AND a.order_id NOT LIKE "FB%" THEN				"DLD" 											WHEN a.wh_order_status IN ( 3 ) 							AND a.order_id NOT LIKE "FB%" THEN								"DJH" 									WHEN a.wh_order_status IN ( 7 ) 									AND a.order_id NOT LIKE "FB%" THEN										"DDB" 										WHEN a.wh_order_status IN ( 8 ) 										AND a.order_id NOT LIKE "FB%" THEN											"DCK" 												WHEN a.wh_order_status IN ( 1, 2 ) 												AND a.order_id LIKE "FB%" THEN													"FDLD" 													WHEN a.wh_order_status IN ( 3 ) 													AND a.order_id LIKE "FB%" THEN														"FDJH" 														WHEN a.wh_order_status IN ( 4 ) 														AND a.order_id LIKE "FB%" THEN															"FJHZ" 															WHEN a.wh_order_status IN ( 7 ) 															AND a.order_id LIKE "FB%" THEN																"FDDB" 																WHEN a.wh_order_status IN ( 8 ) 																AND a.order_id LIKE "FB%" THEN																	"FDCK" 																	WHEN a.wh_order_status IN ( 9 ) 																	AND a.order_id LIKE "FB%" THEN																		"FDJY" ELSE "else" 																		END AS type,																IF																	(																		a.scaner_time > "2020-01-01",																		ROUND( ( unix_timestamp( now()) - unix_timestamp( a.scaner_time ) ) / 3600, 2 ),																	ROUND( ( unix_timestamp( now()) - a.wait_pull_time ) / 3600, 2 )) AS s 																FROM																	ueb_order a,																	ueb_order_detail_tmp b 																WHERE																	a.order_id = b.order_id 																	AND a.is_normal IN ( 0, 3 ) 																	AND a.wh_order_status IN ( 1, 2, 3, 4, 7, 8, 9 ) 																GROUP BY																	a.order_id 																ORDER BY																	s 	  															) a 															GROUP BY															a.warehouse_code,	a.type union SELECT real_warehouse_code,sum(purchase_qty)as num,case when `status`=1 then "DBDRK" when `status`=2 then "DBRKZ" else "else" end as type FROM	ueb_purchase WHERE	is_del = 1 	AND warehouse_type = 1 	AND purchase_type IN ( 3, 4 ) AND  real_warehouse_code in ("HM_AA","SZ_AA")  GROUP BY	real_warehouse_code,type  union select warehouse_code,sum(order_product_number) as num, case when pay_time >0 and wait_pull_time >0 and pick_time >0 and  pack_time >0 and outstock_time > 0 and delivery_time = 0  then "DBDJY"when pay_time >0 and wait_pull_time >0 and pick_time >0 and ((choice_time =0 and pack_time>0) or (choice_time >0 and pack_time >0)) and outstock_time = 0  then "DBDCK"when pay_time >0 and wait_pull_time >0 and pick_time >0 and pack_time = 0  then "DBDDB"when pay_time >0 and wait_pull_time >0 and pick_time =0  then "DBDJH"when pay_time >0 and wait_pull_time =0  then "DBDLD"ELSE "else" end as `status` from ueb_order_operate_time where order_is_cancel =0 and delivery_time = 0 and order_id like "ALLOT%" GROUP BY warehouse_code,status union select warehouse_code,sum(order_product_number) num ,CASE when order_id like "FB%" then "FDPK" when order_id like "ALLOT%" THEN "DBDPK" ELSE "DPK" END AS type from ueb_order where wh_order_status = -1 and is_normal = 0 and warehouse_code in("HM_AA","SZ_AA")  group by warehouse_code,type;'
    sql_jy = 'SELECT  warehouse_code,	sum(quality_num),	case	when paragraph in(1,3,4) then "DSJ"	when paragraph =11 then "DGNZJ" ELSE "ELSE" END a 	FROM	ueb_quality_warehousing_record WHERE	paragraph IN ( -1, 0, 1, 2, 3, 4, 11 ) 	AND type = 1  group by a,warehouse_code union		SELECT  warehouse_code,	sum(quality_num),	"DTM" as a FROM	ueb_quality_warehousing_record WHERE	paragraph IN ( -1, 0, 1, 2, 3, 4, 11 ) 	AND type = 1  and post_code =1	 group by warehouse_code UNION SELECT warehouse_code,count(order_id) as num , case when wh_order_status=-1 then "DPK" when wh_order_status IN(1,2) then "DLD" when wh_order_status=3 then "DJH" when wh_order_status=4 then "JHZ" when wh_order_status=7 then "DDB" when wh_order_status=8 then "DCK" ELSE "ELSE" END type FROM ueb_order WHERE batch_type != 6 and wh_order_status < 9  group by type,warehouse_code UNION SELECT warehouse_code,sum(order_product_number) num , case when wh_order_status=-1 then "FDPK" when wh_order_status IN(1) then "FDFPLD" when wh_order_status IN(2) then "FDLD" when wh_order_status=3 then "FDJH" when wh_order_status=4 then "FJHZ" when wh_order_status=7 then "FDDB" when wh_order_status=8 then "FDCK" when wh_order_status IN (9,19,20) then "FDJY"  ELSE "ELSE" END type FROM ueb_order WHERE batch_type = 6 and wh_order_status not in (10,11,14,13)  group by warehouse_code,type  union SELECT	real_warehouse_code,	count(DISTINCT  purchase_order_no ) AS num,CASE		WHEN `status` = 1 THEN	"DBDRK" 	WHEN `status` = 2 THEN	"DBRKZ" ELSE "else" 	END AS type FROM	ueb_purchase WHERE	is_del = 1 	AND warehouse_type = 1 	AND purchase_type IN ( 3, 4 ) 	AND real_warehouse_code IN ( "HM_AA", "SZ_AA" ) GROUP BY	real_warehouse_code,	type UNION SELECT warehouse_code,count(DISTINCT order_id), case when wh_order_status=-1 then "DBDPK" when wh_order_status IN(1,2) then "DBDLD" when wh_order_status=3 then "DBDJH"  when wh_order_status IN (4,7) then "DBDDB" when wh_order_status=8 then "DBDCK"  when wh_order_status IN (9,19,20) then "DBDJY" ELSE "ELSE" END type FROM ueb_order WHERE order_id LIKE "ALLOT%"   group by type,warehouse_code union SELECT	a.warehouse_code,	sum( a.quality_num ),	a.type AS num FROM	(SELECT	warehouse_code,	"RK" AS purchase_order_no,	car_no AS storage_position,	"RK" AS sku,	box_number AS quality_num,	"DRK" AS type,	cast( ROUND( ( unix_timestamp( now( ) ) - unix_timestamp( add_time ) ) / 3600, 2 ) AS DECIMAL ) AS s FROM	ueb_express_receipt WHERE	STATUS = 1 	AND warehouse_type = 1 	AND is_abnormal = "2" 	AND is_quality = "2" 	AND is_end = "1" 	) a GROUP BY	a.warehouse_code,	a.type ;'
    sql_zl = 'SELECT	a.warehouse_code,	round(sum( a.available_qty * b.product_cost )/10000,2) AS total_cost,CASE				WHEN ROUND( ( unix_timestamp( now()) - unix_timestamp( a.update_time ) ) / 3600, 2 ) <= 24 THEN		"24" 		WHEN ROUND( ( unix_timestamp( now()) - unix_timestamp( a.update_time ) ) / 3600, 2 ) <= 48 AND ROUND( ( unix_timestamp( now()) - unix_timestamp( a.update_time ) ) / 3600, 2 ) > 24 THEN		"48" 		WHEN ROUND( ( unix_timestamp( now()) - unix_timestamp( a.update_time ) ) / 3600, 2 ) > 48 THEN		"48<" ELSE "" 	END AS s FROM	ueb_warehouse_shelf_sku_map a,	ueb_product b WHERE	a.warehouse_code IN ( "HM_AA", "SZ_AA" ) 	AND a.shelf_type NOT IN ( 11, 1, 20 ) 	AND b.product_cost > 0 	AND a.shelf NOT IN ( "MV0102", "MV0150", "WT0002", "WT0001", "MV0028", "MV0015", "MV0054" ) 	AND a.available_qty > 0 	AND a.sku = b.sku GROUP BY	a.warehouse_code,	s'
    # sql_sx = 'SELECT	a.Date,	a.warehouse_code,	"in" AS type,	round(	a.avg_delevery_time + a.avg_postcode_time + a.avg_quality_time +	IF( a.avg_quality_all_time IS NOT NULL, a.avg_quality_all_time, 0.0000 ) + a.avg_upper_end_time,2 ) `total` FROM	(	SELECT		date_format( upper_end_time, "%Y-%m-%d" ) Date,		warehouse_code,		avg( IF ( add_time > quality_start_time, timestampdiff( HOUR, quality_start_time, add_time ), NULL ) ) avg_delevery_time,		avg( IF ( post_code_end_time > add_time, timestampdiff( HOUR, add_time, post_code_end_time ), NULL ) ) avg_postcode_time,		avg( IF ( quality_time > post_code_end_time, timestampdiff( HOUR, post_code_end_time, quality_time ), timestampdiff( HOUR, quality_time, post_code_end_time ) ) ) avg_quality_time,		avg( IF ( quality_all_time > quality_time, timestampdiff( HOUR, quality_time, quality_all_time ), NULL ) ) avg_quality_all_time,		avg(		IF			(				upper_end_time > quality_all_time 				AND quality_all_time > "2000-01-01",				timestampdiff( HOUR, quality_all_time, upper_end_time ),			IF				(					upper_end_time > quality_time 					AND quality_time > post_code_end_time,					timestampdiff( HOUR, quality_time, upper_end_time ),				IF				( upper_end_time > post_code_end_time AND post_code_end_time > quality_time, timestampdiff( HOUR, quality_time, upper_end_time ), NULL )))) avg_upper_end_time 	FROM		ueb_quality_warehousing_record 	WHERE		type = 1 		AND paragraph = 5 		AND quality_start_time > 0 		AND add_time > 0 		AND post_code_end_time > 0 		AND upper_end_time > "2020-01-01" 		AND TO_DAYS( NOW( ) ) - TO_DAYS( upper_end_time ) IN ( 1,2,3,4,5,6,7 ) 	GROUP BY		warehouse_code,		date_format( upper_end_time, "%Y-%m-%d" ) 	) a UNION	(	SELECT		a.`date`,		a.warehouse_code,		"out" AS type,		round(a.avg_pull_time + a.avg_pick_time + a.avg_pack_time + a.avg_outstock_time,2) AS 平均总用时 	FROM		(		SELECT			date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) AS date,			warehouse_code,		IF			( wait_pull_time != 0 AND pull_time != 0, ROUND(( avg( pull_time )- avg( wait_pull_time ))/ 3600, 2 ), NULL ) AS avg_pull_time,			ROUND(( avg( pick_time )- avg( pull_time ))/ 3600, 2 ) AS avg_pick_time,			ROUND( avg(( pack_time ) - ( pick_time ))/ 3600, 2 ) AS avg_pack_time,		IF			(				pack_time != 0 				AND outstock_time != 0,				ROUND( ( avg( outstock_time ) - avg( pack_time ) ) / 3600, 2 ),			NULL 			) AS avg_outstock_time 		FROM			ueb_order_operate_time 		WHERE			order_is_cancel = 0 			AND order_id NOT LIKE "FB%" 			AND pick_time != 0 			AND ( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) > "2020-01-01" 			AND TO_DAYS( NOW( ) ) - TO_DAYS( ( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) ) IN ( 1,2,3,4,5,6,7 ) 		GROUP BY			warehouse_code,		date_format( from_unixtime( outstock_time ), "%Y-%m-%d" )) a 	) UNION SELECT a.`date`,	a.warehouse_code,	"FBA" AS type,	round(a.avg_pull_time + a.avg_pick_time + a.avg_pack_time + a.avg_outstock_time,2) AS 平均总用时 FROM	(	SELECT		date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) AS date,		warehouse_code,	IF		( wait_pull_time != 0 AND pull_time != 0, ROUND(( avg( pull_time )- avg( wait_pull_time ))/ 3600, 2 ), NULL ) AS avg_pull_time,		ROUND(( avg( pick_time )- avg( pull_time ))/ 3600, 2 ) AS avg_pick_time,		ROUND( avg(( pack_time ) - ( pick_time ))/ 3600, 2 ) AS avg_pack_time,	IF		(			pack_time != 0 			AND outstock_time != 0,			ROUND( ( avg( outstock_time ) - avg( pack_time ) ) / 3600, 2 ),		NULL 		) AS avg_outstock_time 	FROM		ueb_order_operate_time 	WHERE		order_is_cancel = 0 		AND order_id LIKE "FB%" 		AND pick_time != 0 		AND ( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) > "2020-01-01" 		AND TO_DAYS( NOW( ) ) - TO_DAYS( ( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) ) IN ( 1,2,3,4,5,6,7 ) 	GROUP BY	warehouse_code,	date_format( from_unixtime( outstock_time ), "%Y-%m-%d" )) a;'
    sql_sx = 'SELECT	a.Date,	a.warehouse_code,	"in" AS type,	round(	a.avg_delevery_time + a.avg_postcode_time + a.avg_quality_time +IF	( a.avg_quality_all_time IS NOT NULL, a.avg_quality_all_time, 0.0000 ) + a.avg_upper_end_time,	2 	) `total` FROM	(SELECT	date_format( upper_end_time, "%m-%d" ) Date,	warehouse_code,	avg( IF ( add_time > quality_start_time, timestampdiff( HOUR, quality_start_time, add_time ), NULL ) ) avg_delevery_time,	avg( IF ( post_code_end_time > add_time, timestampdiff( HOUR, add_time, post_code_end_time ), NULL ) ) avg_postcode_time,	avg( IF ( quality_time > post_code_end_time, timestampdiff( HOUR, post_code_end_time, quality_time ), timestampdiff( HOUR, quality_time, post_code_end_time ) ) ) avg_quality_time,	avg( IF ( quality_all_time > quality_time, timestampdiff( HOUR, quality_time, quality_all_time ), NULL ) ) avg_quality_all_time,	avg(IF	(	upper_end_time > quality_all_time 	AND quality_all_time > "2000-01-01",	timestampdiff( HOUR, quality_all_time, upper_end_time ),IF	(	upper_end_time > quality_time 	AND quality_time > post_code_end_time,	timestampdiff( HOUR, quality_time, upper_end_time ),IF	( upper_end_time > post_code_end_time AND post_code_end_time > quality_time, timestampdiff( HOUR, quality_time, upper_end_time ), NULL ) 	) 	) 	) avg_upper_end_time FROM	ueb_quality_warehousing_record WHERE	type = 1 	AND paragraph = 5 	AND quality_start_time > 0 	AND add_time > 0 	AND post_code_end_time > 0 	AND upper_end_time > "2020-01-01" 	AND TO_DAYS( NOW( ) ) - TO_DAYS( upper_end_time ) IN ( 1, 2, 3, 4, 5, 6, 7 ) GROUP BY	warehouse_code,	date_format( upper_end_time, "%m-%d" ) 	) a UNION	 SELECT date ,	CASE						WHEN a.warehouse_code = "HM_AA" THEN			"HM_AA" 			WHEN a.warehouse_code = "SZ_AA" THEN			"SZ_AA" ELSE "1" 		END AS warehouse_code,"out" as type, round((pull_time - wait_pull_time)/3600,2)+round((pick_time - pull_time)/3600,2)+round((scaner_time - pick_time)/3600,2)+round((scaner_last_time - scaner_time)/3600,2)as total FROM (		SELECT  date_format( from_unixtime( outstock_time ), "%m-%d" ) date,  warehouse_code,	avg( wait_pull_time) AS wait_pull_time,	avg( pull_time ) AS pull_time,	avg( pick_time ) AS pick_time,	avg( pack_time ) AS scaner_time,	avg( outstock_time ) AS scaner_last_time,	avg( abnormal_time ) AS abnormal_time,	avg( choice_time ) AS collected_time FROM	`ueb_order_operate_time` WHERE	TO_DAYS( NOW( ) ) - TO_DAYS( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) in (1,2,3,4,5,6,7)	AND `wait_pull_time` > 0 	AND `pull_time` > 0 	AND `pick_time` > 0 	AND `pack_time` > 0 	AND `outstock_time` > 0 	AND `delivery_time` > 0 	AND `pick_time` > 0 	AND `pack_time` > 0 	AND `batch_no` NOT LIKE "%-6-%"group by warehouse_code,date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) )a UNION	SELECT		a.`date`,	CASE						WHEN a.warehouse = "HM_AA" THEN			"HM_AA" 			WHEN a.warehouse = "SZ_AA" THEN			"SZ_AA" ELSE "1" 		END AS warehouse_code,    "FBA" as type, 		a.avg_pull_time + a.avg_pick_time + a.avg_post_time+a.avg_pack_time + a.avg_outstock_time AS total 	FROM		(		SELECT			date_format( from_unixtime( outstock_time ), "%m-%d" ) AS date,			warehouse_code AS warehouse,		IF			( wait_pull_time != 0 AND pull_time != 0, ROUND(( avg( pull_time )- avg( wait_pull_time ))/ 3600, 2 ), NULL ) AS avg_pull_time,			ROUND(( avg( pick_time )- avg( pull_time ))/ 3600, 2 ) AS avg_pick_time,			ROUND( avg(( choice_time ) - ( pick_time ))/ 3600, 2 ) AS avg_post_time,			ROUND( avg(( pack_time ) - ( choice_time ))/ 3600, 2 ) AS avg_pack_time,		IF			(				pack_time != 0 				AND outstock_time != 0,				ROUND( ( avg( outstock_time ) - avg( pack_time ) ) / 3600, 2 ),			NULL 			) AS avg_outstock_time 		FROM			ueb_order_operate_time 		WHERE			order_is_cancel = 0 			AND order_id LIKE "FB%" 			AND pick_time != 0 			and choice_time != 0			AND TO_DAYS( NOW( ) ) - TO_DAYS( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) in (1,2,3,4,5,6,7)		GROUP BY			warehouse_code,		date_format( from_unixtime( outstock_time ), "%m-%d" )) a;							'
    sql4 = 'SELECT	a.warehouse_code,	a.date,  a.num/(b.num+c.num) as num 	FROM			(			SELECT				a.warehouse_code,				date_format( from_unixtime( a.pack_time ), "%Y-%m-%d" ) AS date,				"out" AS `type`,				sum( b.quantity ) AS num 			FROM				ueb_order_operate_time a,				ueb_order_detail_tmp b 			WHERE				a.order_id = b.order_id 				AND a.pack_time IS NOT NULL 				AND TO_DAYS( NOW( ) ) - TO_DAYS(				date_format( from_unixtime( a.pack_time ), "%Y-%m-%d" )) = 1 			GROUP BY				a.warehouse_code,				date 				) a,			(			SELECT				warehouse_code,				DATE_FORMAT( post_code_start_time, "%Y-%m-%d" ) AS date,				"in" AS type,				sum( actual_num ) AS num 			FROM				ueb_quality_warehousing_record 			WHERE				post_code_start_time IS NOT NULL 				AND warehouse_code IN ( "HM_AA", "SZ_AA" ) 				AND TO_DAYS( NOW( ) ) - TO_DAYS( post_code_start_time ) IN ( 1 ) 			GROUP BY				warehouse_code,				date 			) b,			(			SELECT				warehouse_code,				DATE_SUB( curdate(), INTERVAL 1 DAY ) AS date,				"stock" AS type,				sum( num ) AS num 			FROM				stock_list_line 			WHERE				shelf NOT LIKE "A%" 				AND warehouse_code IN ( "HM_AA", "SZ_AA" ) 			GROUP BY				warehouse_code 			)  c 		where a.warehouse_code = b.warehouse_code and				  a.warehouse_code = c.warehouse_code and				      a.date = b.date and 					a.date = c.date		'
    # sql_rk = 'SELECT	a.warehouse_code,date_format( from_unixtime( a.pack_time ), "%Y-%m-%d" ) AS date,				"out" AS `type`,				sum( b.quantity ) AS num 			FROM				ueb_order_operate_time a,				ueb_order_detail_tmp b 			WHERE				a.order_id = b.order_id 				AND a.pack_time IS NOT NULL 				AND TO_DAYS( NOW( ) ) - TO_DAYS(				date_format( from_unixtime( a.pack_time ), "%Y-%m-%d" )) = 1 			GROUP BY				a.warehouse_code,				date 				union							SELECT				a.warehouse_code,				date_format( from_unixtime( a.pull_time ), "%Y-%m-%d" ) AS date,				"LD" AS `type`,				count(a.order_id) AS num 			FROM				ueb_order_operate_time a			WHERE				 a.pack_time IS NOT NULL 				AND TO_DAYS( NOW( ) ) - TO_DAYS(				date_format( from_unixtime( a.pull_time ), "%Y-%m-%d" )) = 1 			GROUP BY				a.warehouse_code,				date 			  union 								SELECT				warehouse_code,				DATE_FORMAT( post_code_start_time, "%Y-%m-%d" ) AS date,				"in" AS type,				sum( actual_num ) AS num 			FROM				ueb_quality_warehousing_record 			WHERE				post_code_start_time IS NOT NULL 				AND warehouse_code IN ( "HM_AA", "SZ_AA" ) 				AND TO_DAYS( NOW( ) ) - TO_DAYS( post_code_start_time ) IN ( 1 ) 			GROUP BY				warehouse_code,				date 																																												'
    sql_rk = 'SELECT	CASE 	WHEN warehouse_code = "AFN"  THEN "HM_AA"  WHEN warehouse_code = "HM_AA" THEN "HM_AA"	WHEN warehouse_code = "SZ_AA" THEN "SZ_AA"	ELSE "ELSE" END AS `仓库`,	add_time AS `日期`,	"in" as type ,	IFNULL( sum( JSON_UNQUOTE( JSON_EXTRACT( work_parme_num, "$.delivery.delivery.piece_total" ))), 0 ) AS `num`	FROM	`ueb_work_num_log_history` WHERE	add_time NOT IN ( "num", "user_name", "warehouse_code" ) and TO_DAYS(NOW( )) - TO_DAYS( add_time) = 1 GROUP BY	仓库,	add_time  union  	SELECT	CASE 	WHEN warehouse_code = "AFN"  THEN "HM_AA"  WHEN warehouse_code = "HM_AA" THEN "HM_AA"	WHEN warehouse_code = "SZ_AA" THEN "SZ_AA"	ELSE "ELSE" END AS `仓库`,	add_time AS `日期`,	"out" as type ,	IFNULL(sum(	JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_sku_bao.piece_total" ))),0) +	IFNULL(sum( JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_single.piece_total" ))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_multi.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_zf.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_ex_order.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_singl_more.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_express.piece_total"))),0) +	IFNULL(sum(	JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_sku_bao.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE( JSON_EXTRACT( work_parme_num, "$.FBA.FBA.piece_total" ))),0) AS `num`	FROM	`ueb_work_num_log_history` WHERE	add_time NOT IN ( "num", "user_name", "warehouse_code" )  and TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) = 1 GROUP BY	仓库,	add_time  union	  SELECT	a.warehouse_code,	date_format( from_unixtime( a.pull_time ), "%Y-%m-%d" ) AS date,	"LD" AS `type`,	count( a.order_id ) AS num FROM	ueb_order_operate_time a WHERE	a.pack_time IS NOT NULL 	AND TO_DAYS( NOW( ) ) - TO_DAYS( date_format(from_unixtime( a.pull_time ), "%Y-%m-%d" ) ) = 1 GROUP BY	a.warehouse_code,	date'
    # 2天前版本sql_tph= 'select DATE_FORMAT(a.date,"%m-%d") date,a.warehouse, round(a.`work`/b.`hour`,1) AS TPH ,round(a.`work2`/b.`hour`,1) AS UPH from(SELECT 	DATE_FORMAT(add_time,"%Y-%m-%d") AS `date`,	case	when warehouse_code = "HM_AA" THEN "HM_AA"	when warehouse_code = "AFN" Then "HM_AA"	when warehouse_code = "SZ_AA" then "SZ_AA"	else "else" end  as 	warehouse,	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "	$.instock.question_instock.piece_total"))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.instock.instock.piece_total" ))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.instock.return_instock.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_single.piece_total" ))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_multi.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_zf.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_ex_order.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_singl_more.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_express.piece_total"))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_sku_bao.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.FBA.FBA.piece_total" ))),0) AS `work`,	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_single.piece_total" ))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_multi.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_zf.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_ex_order.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_singl_more.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_express.piece_total"))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_sku_bao.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.FBA.FBA.piece_total" ))),0) as `work2`FROM	`ueb_work_num_log_history` WHERE	add_time NOT IN ( "num", "user_name", "warehouse_code" ) and TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) in (2,3,4,5,6,7) and warehouse_code not in ("shzz","CX")GROUP BY DATE_FORMAT(add_time,"%Y-%m-%d")	,warehouse )a ,(select date,warehouse_code,sum(`hour`) as `hour` from (SELECT	warehouse_code,	date,	`group`,	sum( HOUR ) `hour` FROM	((SELECT	a.warehouse_code,	a.date,	a.`group`,	(	a.temporary_hour +	a.group_leader + 	a.receive_hour + 	a.instock_hour + 	a.return_deal + 	a.allocate_instock + 	a.working_hour + 	a.all_quality + 	a.instock_putaway + 	a.return_putaway + 	a.problem_putaway +	a.pick_hour +	a.move_hour +	a.inventory_hour +	a.check_hour + 	a.second_pick + 	a.pack_hour + 	a.channel_pick + 	a.scan_weigh + 	a.delivery_hour +	a.fba_change + 	a.fba_pack + 	a.fba_delivery +	a.iqc_hour + 	a.confirm_exception +	a.instock_exception +	a.warehouse_exception + 	a.order_exception + 	a.transit_receive +	a.transit_pack + 	a.transit_send + 	a.transit_manage + 	a.other_hour 	) + (case when a.`group`="manage" then a.actual_work *8 else 0 end)AS HOUR FROM	yb_daily_report a GROUP BY	a.`group`,	a.warehouse_code,	a.date) UNION	(SELECT	warehouse_code,	date,	`group`,	sum( `hour` ) AS `hour` FROM	(SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[0].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[0].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[0].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL  UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[1].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[1].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[1].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[2].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[2].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[2].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[3].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[3].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[3].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[4].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[4].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[4].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[5].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[5].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[5].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[6].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[6].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[6].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[7].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[7].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[7].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	 support_out IS NOT NULL 	) a WHERE	a.warehouse_code IS NOT NULL GROUP BY	date,	warehouse_code,	`group` 	) 	 )d 	 where warehouse_code  in ("HM_AA","SZ_AA") and `group` not in ("iqc") GROUP BY	warehouse_code,	date,	`group`)a 	group  by warehouse_code,date)	b where a.date = b.date and a.warehouse = b.warehouse_code  	AND TO_DAYS( NOW( ) ) - TO_DAYS( a.date ) in (2,3,4,5,6,7)	group by date,warehouse_code order by warehouse_code;'
    sql_tph = 'select DATE_FORMAT(a.date,"%m-%d") date,a.warehouse, round(a.`work`/b.`hour`,1) AS TPH ,round(a.`work2`/b.`hour`,1) AS UPH from(SELECT 	DATE_FORMAT(add_time,"%Y-%m-%d") AS `date`,	case	when warehouse_code = "HM_AA" THEN "HM_AA"	when warehouse_code = "AFN" Then "HM_AA"	when warehouse_code = "SZ_AA" then "SZ_AA"	else "else" end  as 	warehouse,	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "	$.instock.question_instock.piece_total"))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.instock.instock.piece_total" ))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.instock.return_instock.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_single.piece_total" ))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_multi.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_zf.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_ex_order.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_singl_more.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_express.piece_total"))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_sku_bao.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.FBA.FBA.piece_total" ))),0) AS `work`,	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_single.piece_total" ))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_multi.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_zf.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_ex_order.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_singl_more.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_express.piece_total"))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_sku_bao.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.FBA.FBA.piece_total" ))),0) as `work2`FROM	`ueb_work_num_log_history` WHERE	add_time NOT IN ( "num", "user_name", "warehouse_code" ) and TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) in (1,2,3,4,5,6,7) and warehouse_code not in ("shzz","CX")GROUP BY DATE_FORMAT(add_time,"%Y-%m-%d")	,warehouse )a ,(select date,warehouse_code,sum(`hour`) as `hour` from (SELECT	warehouse_code,	date,	`group`,	sum( HOUR ) `hour` FROM	((SELECT	a.warehouse_code,	a.date,	a.`group`,	(	a.temporary_hour +	a.group_leader + 	a.receive_hour + 	a.instock_hour + 	a.return_deal + 	a.allocate_instock + 	a.working_hour + 	a.all_quality + 	a.instock_putaway + 	a.return_putaway + 	a.problem_putaway +	a.pick_hour +	a.move_hour +	a.inventory_hour +	a.check_hour + 	a.second_pick + 	a.pack_hour + 	a.channel_pick + 	a.scan_weigh + 	a.delivery_hour +	a.fba_change + 	a.fba_pack + 	a.fba_delivery +	a.iqc_hour + 	a.confirm_exception +	a.instock_exception +	a.warehouse_exception + 	a.order_exception + 	a.transit_receive +	a.transit_pack + 	a.transit_send + 	a.transit_manage + 	a.other_hour 	) + (case when a.`group`="manage" then a.actual_work *8 else 0 end)AS HOUR FROM	yb_daily_report a GROUP BY	a.`group`,	a.warehouse_code,	a.date) UNION	(SELECT	warehouse_code,	date,	`group`,	sum( `hour` ) AS `hour` FROM	(SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[0].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[0].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[0].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL  UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[1].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[1].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[1].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[2].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[2].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[2].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[3].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[3].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[3].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[4].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[4].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[4].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[5].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[5].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[5].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[6].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[6].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[6].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[7].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[7].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[7].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	 support_out IS NOT NULL 	) a WHERE	a.warehouse_code IS NOT NULL GROUP BY	date,	warehouse_code,	`group` 	) 	 )d 	 where warehouse_code  in ("HM_AA","SZ_AA") and `group` not in ("iqc") GROUP BY	warehouse_code,	date,	`group`)a 	group  by warehouse_code,date)	b where a.date = b.date and a.warehouse = b.warehouse_code  	AND TO_DAYS( NOW( ) ) - TO_DAYS( a.date ) in (1,2,3,4,5,6,7)	group by date,warehouse_code order by warehouse_code;'
    # 2天前sql_ry = 'select a.warehouse_code,a.date,a.now_staff,a.enter_staff,a.actual_work,a.actual_work-b.actual_work as actual_last,a.temporary_people,a.temporary_people-b.temporary_people as temporary_last,a.temporary_hour,a.temporary_hour-b.temporary_hour as t_hour_last ,a.now_hour,a.now_hour-b.now_hour as n_hour_last,b.actual_work as work2,b.now_hour as hour2 from (select * from (	SELECT a.warehouse_code,		a.date ,		sum( a.now_staff ) AS now_staff,		sum( a.actual_work ) AS actual_work,		sum( a.enter_staff ) AS enter_staff,		sum( a.leave_staff ) AS leave_staff,		sum( a.normal_rest ) AS normal_rest,		sum( a.temporary_people ) AS temporary_people,		sum( a.temporary_hour ) AS temporary_hour,		sum(			(				a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour 			) 		) AS now_hour,		sum(			(				a.temporary_hour + a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour 			) 		) AS total_hour 	FROM		yb_daily_report a 	WHERE		a.`group` NOT IN ( "iqc", "general_manage" ) 		AND TO_DAYS( NOW( ) ) - TO_DAYS( a.date ) in (2)	GROUP BY	a.warehouse_code,a.date)a)a  , (select warehouse_code,date_add(date,interval 1 day)date,now_staff,actual_work,temporary_people,temporary_hour,now_hour from (	SELECT a.warehouse_code,		a.date ,		sum( a.now_staff ) AS now_staff,		sum( a.actual_work ) AS actual_work,		sum( a.enter_staff ) AS enter_staff,		sum( a.leave_staff ) AS leave_staff,		sum( a.normal_rest ) AS normal_rest,		sum( a.temporary_people ) AS temporary_people,		sum( a.temporary_hour ) AS temporary_hour,		sum(			(				a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour 			) 		) AS now_hour,		sum(			(				a.temporary_hour + a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour 			) 		) AS total_hour 	FROM		yb_daily_report a 	WHERE		a.`group` NOT IN ( "iqc", "general_manage" ) 		AND TO_DAYS( NOW( ) ) - TO_DAYS( a.date ) in (3)	GROUP BY	a.warehouse_code,a.date)a )b where a.warehouse_code = b.warehouse_code and a.date = b.date  group by a.warehouse_code,a.date order by a.warehouse_code'
    sql_ry = 'select a.warehouse_code, IFNULL(b.date,0),IFNULL(b.now_staff,0),IFNULL(b.enter_staff,0),IFNULL(b.actual_work,0),IFNULL(b.actual_last,0),IFNULL(b.temporary_people,0),IFNULL(b.temporary_last,0),IFNULL(b.temporary_hour,0),IFNULL(b.t_hour_last,0),IFNULL(b.now_hour,0),IFNULL(b.n_hour_last,0),IFNULL(b.work2,0),IFNULL(b.hour2,0)from (select "AFN" AS warehouse_code union  select "HM_AA" AS warehouse_code union select "SZ_AA" AS warehouse_code union select "shzz" AS warehouse_code) a left join (select a.warehouse_code,a.date,a.now_staff,a.enter_staff,a.actual_work,a.actual_work-b.actual_work as actual_last,a.temporary_people,a.temporary_people-b.temporary_people as temporary_last,a.temporary_hour,a.temporary_hour-b.temporary_hour as t_hour_last ,a.now_hour,a.now_hour-b.now_hour as n_hour_last,b.actual_work as work2,b.now_hour as hour2 from (select * from (	SELECT a.warehouse_code,		a.date ,		sum( a.now_staff ) AS now_staff,		sum( a.actual_work ) AS actual_work,		sum( a.enter_staff ) AS enter_staff,		sum( a.leave_staff ) AS leave_staff,		sum( a.normal_rest ) AS normal_rest,		sum( a.temporary_people ) AS temporary_people,		sum( a.temporary_hour ) AS temporary_hour,		sum(			(				a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour 			) 		) AS now_hour,		sum(			(				a.temporary_hour + a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour 			) 		) AS total_hour 	FROM		yb_daily_report a 	WHERE		a.`group` NOT IN ( "iqc", "general_manage" ) 		AND TO_DAYS( NOW( ) ) - TO_DAYS( a.date ) in (1)	GROUP BY	a.warehouse_code,a.date)a)a  , (select warehouse_code,date_add(date,interval 1 day)date,now_staff,actual_work,temporary_people,temporary_hour,now_hour from (	SELECT a.warehouse_code,		a.date ,		sum( a.now_staff ) AS now_staff,		sum( a.actual_work ) AS actual_work,		sum( a.enter_staff ) AS enter_staff,		sum( a.leave_staff ) AS leave_staff,		sum( a.normal_rest ) AS normal_rest,		sum( a.temporary_people ) AS temporary_people,		sum( a.temporary_hour ) AS temporary_hour,		sum(			(				a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour 			) 		) AS now_hour,		sum(			(				a.temporary_hour + a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour 			) 		) AS total_hour 	FROM		yb_daily_report a 	WHERE		a.`group` NOT IN ( "iqc", "general_manage" ) 		AND TO_DAYS( NOW( ) ) - TO_DAYS( a.date ) in (2)	GROUP BY	a.warehouse_code,a.date)a )b where a.warehouse_code = b.warehouse_code and a.date = b.date  group by a.warehouse_code,a.date order by a.warehouse_code)b on a.warehouse_code = b.warehouse_code'
    sql_ry2='select a.*,ifnull(b.date,0),ifnull(b.now_staff,0),ifnull(b.actual_work,0),ifnull(b.enter_staff,0),ifnull(b.leave_staff,0),ifnull(b.normal_rest,0),ifnull(b.temporary_people,0),ifnull(b.temporary_hour,0),ifnull(b.now_hour,0),ifnull(b.total_hour,0)from (select "AFN" as warehouse_code union select "HM_AA" as warehouse_code union select "SZ_AA" as warehouse_code union select "shzz" as warehouse_code ) a left join (SELECT	a.warehouse_code,	DATE_FORMAT(a.date,"%v") date ,	sum( a.now_staff ) AS now_staff,	sum( a.actual_work ) AS actual_work,	sum( a.enter_staff ) AS enter_staff,	sum( a.leave_staff ) AS leave_staff,	sum( a.normal_rest ) AS normal_rest,	sum( a.temporary_people ) AS temporary_people,	sum( a.temporary_hour ) AS temporary_hour,	sum(	(	a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour 	) 	) AS now_hour,	sum(	(	a.temporary_hour + a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour 	) 	) AS total_hour FROM	yb_daily_report a WHERE	a.`group` NOT IN ( "iqc", "general_manage" ) 	AND DATE_FORMAT(now(),"%v")-DATE_FORMAT(a.date,"%v")=0 and a.date>"2021-01-01"GROUP BY	a.warehouse_code,	DATE_FORMAT(a.date,"%v") order by a.warehouse_code) b on a.warehouse_code = b.warehouse_code'
    # sql_zt = 'SELECT    case    when warehouse_code = "AFN" then "HM_AA"  else warehouse_code end  AS `warehouse`,    DATE_FORMAT(add_time,"%m-%d") AS `日期`,  IFNULL(  sum( JSON_UNQUOTE( JSON_EXTRACT( work_parme_num, "$.delivery.delivery.piece_total" )) ),0) AS `点数总件数`,  IFNULL(sum( JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_single.piece_total" ))),0) +  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_multi.piece_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_zf.piece_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_ex_order.piece_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_singl_more.piece_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack.piece_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_express.piece_total"))),0) +  IFNULL(sum(  JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_sku_bao.piece_total" ))),0) AS `打包总件数`,	IFNULL(sum( JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_single.order_total" ))),0) +  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_multi.order_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_zf.order_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_ex_order.order_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_singl_more.order_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack.order_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_express.order_total"))),0) +  IFNULL(sum(  JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_sku_bao.order_total" ))),0) AS `打包单数`,  IFNULL(sum(JSON_UNQUOTE( JSON_EXTRACT( work_parme_num, "$.FBA.FBA.piece_total" ))),0) AS `FBA打包件数`,	IFNULL(sum(JSON_UNQUOTE( JSON_EXTRACT( work_parme_num, "$.FBA.FBA.order_total" ))),0) AS `FBA打包单数`  FROM    `ueb_work_num_log_history`   WHERE    warehouse_code in ("HM_AA","SZ_AA","AFN")    and    TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) <= 5   GROUP BY    warehouse,    add_time;'
    sql_zt = 'SELECT    case    when warehouse_code = "AFN" then "HM_AA"  else warehouse_code end  AS `warehouse`,    DATE_FORMAT(add_time,"%m-%d") AS `日期`,  IFNULL(  sum( JSON_UNQUOTE( JSON_EXTRACT( work_parme_num, "$.delivery.delivery.piece_total" )) ),0) AS `点数总件数`,  IFNULL(sum( JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_single.piece_total" ))),0) +  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_multi.piece_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_zf.piece_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_ex_order.piece_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_singl_more.piece_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack.piece_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_express.piece_total"))),0) +  IFNULL(sum(  JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_sku_bao.piece_total" ))),0) AS `打包总件数`,	IFNULL(sum( JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_single.order_total" ))),0) +  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_multi.order_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_zf.order_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_ex_order.order_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_singl_more.order_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack.order_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_express.order_total"))),0) +  IFNULL(sum(  JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_sku_bao.order_total" ))),0) AS `打包单数`,  IFNULL(sum(JSON_UNQUOTE( JSON_EXTRACT( work_parme_num, "$.FBA.FBA.piece_total" ))),0) AS `FBA打包件数`,	IFNULL(sum(JSON_UNQUOTE( JSON_EXTRACT( work_parme_num, "$.FBA.FBA.order_total" ))),0) AS `FBA打包单数`  FROM    `ueb_work_num_log_history`   WHERE    warehouse_code in ("HM_AA","SZ_AA","AFN")    and    TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) <= 7   GROUP BY    warehouse,    add_time;'
    sql_dcl='select a.warehouse_code,ifnull(b.type,a.type),ifnull(b.date,0),ifnull(b.rk,0) ,ifnull(b.tm,0),ifnull(b.zj,0) ,ifnull(b.sj,0)from (select "HM_AA" as warehouse_code , "1" as type union select "HM_AA" as warehouse_code , "2" as type union select "HM_AA" as warehouse_code , "3" as type union select "SZ_AA" as warehouse_code , "1" as type union select "SZ_AA" as warehouse_code , "2" as type union select "SZ_AA" as warehouse_code , "3" as type ) a  left join (SELECT			warehouse_code, "1" as type,			date_format( upper_end_time, "%Y-%m-%d") date,			avg( IF ( add_time > quality_start_time, timestampdiff( HOUR, quality_start_time, add_time ), NULL ) ) as rk,			avg( IF ( post_code_end_time > add_time, timestampdiff( HOUR, add_time, post_code_end_time ), NULL ) ) as tm,			avg( IF ( quality_time > post_code_end_time, timestampdiff( HOUR, post_code_end_time, quality_time ), timestampdiff( HOUR, quality_time, post_code_end_time ) ) ) as zj,			avg(			IF				(					upper_end_time > quality_all_time 					AND quality_all_time > "2000-01-01",					timestampdiff( HOUR, quality_all_time, upper_end_time ),				IF					(						upper_end_time > quality_time 						AND quality_time > post_code_end_time,						timestampdiff( HOUR, quality_time, upper_end_time ),					IF					( upper_end_time > post_code_end_time AND post_code_end_time > quality_time, timestampdiff( HOUR, quality_time, upper_end_time ), NULL )))) as sj		FROM			ueb_quality_warehousing_record		WHERE			type = 1 			AND paragraph = 5 			AND quality_start_time > 0 			AND add_time > 0 		  and TO_DAYS( NOW( ) ) - TO_DAYS( upper_end_time ) = 1 			AND upper_end_time is not null 		GROUP BY			warehouse_code,			date_format( upper_end_time, "%Y-%m-%d" ) union 											SELECT				warehouse_code AS warehouse,"2"as type,				date_format( from_unixtime( outstock_time ), "%Y-%m-%d") AS date,			IF				( wait_pull_time != 0 AND pull_time != 0, ROUND(( avg( pull_time )- avg( wait_pull_time ))/ 3600, 2 ), NULL ) AS ld,					ROUND(( avg( pick_time )- avg( pull_time ))/ 3600, 2 ) AS jh,			ROUND( avg(( pack_time ) - ( pick_time ))/ 3600, 2 ) AS db,				IF				(					pack_time != 0 					AND outstock_time != 0,					ROUND( ( avg( outstock_time ) - avg( pack_time ) ) / 3600, 2 ),				NULL 				) AS ck 			FROM				ueb_order_operate_time			WHERE				order_is_cancel = 0 				AND order_id NOT LIKE "FB%" 				and 	TO_DAYS( NOW( ) ) - TO_DAYS( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) = 1 				AND pick_time != 0 AND  batch_no not like "%-6-%" 			GROUP BY				warehouse_code,			date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) union		 				SELECT			warehouse_code AS warehouse,"3"as type ,			date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) AS date,		IF			( wait_pull_time != 0 AND pull_time != 0, ROUND(( avg( pull_time )- avg( wait_pull_time ))/ 3600, 2 ), NULL ) AS ld,				ROUND(( avg( pick_time )- avg( pull_time ))/ 3600, 2 )  AS jh,				ROUND( avg(( pack_time ) - ( pick_time ))/ 3600, 2 )  AS db,						IF			(				pack_time != 0 				AND outstock_time != 0,				ROUND( ( avg( outstock_time ) - avg( pack_time ) ) / 3600, 2 ),			NULL 			)  AS ck			FROM			ueb_order_operate_time		WHERE			order_is_cancel = 0 			and 	TO_DAYS( NOW( ) ) - TO_DAYS( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) = 1 			AND order_id LIKE "FB%" 			AND pick_time != 0 		GROUP BY			warehouse_code,		date_format( from_unixtime( outstock_time ),"%Y-%m-%d") 	order by warehouse_code,type	) b on a.warehouse_code = b.warehouse_code and a.type = b.type  		'
    sql_db = 'select a.date,a.warehouse,IFNULL(b.`in`,0) `in` ,IFNULL(c.`out`,0)`out`,IFNULL(b.`in`,0)+IFNULL(c.`out`,0) as `total` from (select DATE_FORMAT(Date,"%m-%d") date,"HM_AA"as warehouse from date where `year` ="2021" and TO_DAYS( NOW( ) ) - TO_DAYS( `Date` ) in (0,1,2,3,4,5,6)union select DATE_FORMAT(Date,"%m-%d") date,"SZ_AA"as warehouse from date where `year` ="2021" and TO_DAYS( NOW( ) ) - TO_DAYS( `Date` ) in (0,1,2,3,4,5,6))a left join (SELECT	case	when warehouse_code = "AFN" then "HM_AA" else warehouse_code end 	warehouse,	DATE_FORMAT( upper_end_time, "%m-%d" ) date  ,	count(DISTINCT purchase_order_no) as `in`FROM	ueb_quality_warehousing_record WHERE	purchase_order_no LIKE "ALLOT%" 	AND TO_DAYS( NOW( ) ) - TO_DAYS( upper_end_time )<= 6 GROUP BY warehouse,	DATE_FORMAT( upper_end_time, "%m-%d" )) b on a.warehouse=b.warehouse and a.date = b.date left join(select warehouse_code,FROM_UNIXTIME(delivery_time,"%m-%d") date,count(DISTINCT IFNULL(order_id,0)) `out` from ueb_order_operate_time where order_id like "ALLOT%" and order_is_cancel = 0  and TO_DAYS( NOW( ) ) - TO_DAYS( FROM_UNIXTIME(delivery_time,"%Y-%m-%d")  ) <= 6 group by FROM_UNIXTIME(delivery_time,"%m-%d"),warehouse_code )c on  a.date = c.date  and a.warehouse = c.warehouse_code'
    sql_dcl2 = 'SELECT  a.*,ifnull(round(b.`fba`,3),0) fba,ifnull(round(c.`out`,3),0) `out`, ifnull(round(d.`in`,3),0) `in` from (SELECT  "HM_AA" AS warehouse_code,"1" as use_hours   union SELECT  "HM_AA" AS warehouse_code,"2" as use_hours  union  SELECT  "SZ_AA" AS warehouse_code,"1" as use_hours  union SELECT  "SZ_AA" AS warehouse_code,"2" as use_hours   union  SELECT  "HM_AA" AS warehouse_code,"1" as use_hours   union SELECT  "HM_AA" AS warehouse_code,"2" as use_hours union SELECT  "SZ_AA" AS warehouse_code,"1" as use_hours union SELECT  "SZ_AA" AS warehouse_code,"2" as use_hours  union  SELECT  "HM_AA" AS warehouse_code,"1" as use_hours  union SELECT  "HM_AA" AS warehouse_code,"2" as use_hours union SELECT  "SZ_AA" AS warehouse_code,"1" as use_hours union SELECT  "SZ_AA" AS warehouse_code,"2" as use_hours union SELECT  "HM_AA" AS warehouse_code,"3" as use_hours   union SELECT  "SZ_AA" AS warehouse_code,"3" as use_hours) a  LEFT JOIN (SELECT a.warehouse_code,ceil((if((if(a.pick_time > a.pull_time, a.pick_time - a.pull_time, 0) + if(a.choice_time > a.pick_time, a.choice_time - a.pick_time, 0) + if(a.choice_time and a.pack_time > a.choice_time, a.pack_time - a.choice_time, a.pack_time - a.pick_time)) > 0 , if(a.pick_time > a.pull_time, a.pick_time - a.pull_time, 0) + if(a.choice_time > a.pick_time, a.choice_time - a.pick_time, 0) + if(a.choice_time and a.pack_time > a.choice_time, a.pack_time - a.choice_time, a.pack_time - a.pick_time), 0))/43200) as use_hours,count(*)as num, b.total as total, count(*)/b.total as fba  FROM ueb_order_operate_time as a left join(SELECT  warehouse_code,count(*) as total FROM ueb_order_operate_time WHERE 	TO_DAYS( NOW( ) ) - TO_DAYS( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) in (1) and wait_pull_time > 0 and pull_time > 0 and pick_time > 0 and pack_time > 0 and outstock_time > 0 and delivery_time > 0 and batch_no like "%-6-%" and order_id not like "HW%" and order_id not like "ALLOT%" and order_id not like "PTH%" and choice_time > 0 group by warehouse_code ORDER BY warehouse_code asc  ) as  b on a.warehouse_code = b.warehouse_code WHERE 	TO_DAYS( NOW( ) ) - TO_DAYS( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) in (1) and wait_pull_time > 0 and pull_time > 0 and pick_time > 0 and pack_time > 0 and outstock_time > 0 and delivery_time > 0 and batch_no like "%-6-%" and order_id not like "HW%" and order_id not like "ALLOT%" and order_id not like "PTH%" and choice_time > 0 group by use_hours,warehouse_code )b on a.warehouse_code=b.warehouse_code  and a.use_hours =b.use_hours  left join (SELECT  a.warehouse_code,ceil((if((if(a.pull_time > a.wait_pull_time, a.pull_time - a.wait_pull_time, 0) + if(a.pick_time > a.pull_time, a.pick_time - a.pull_time, 0) + if(a.choice_time > a.pick_time, a.choice_time - a.pick_time, 0) + if(a.choice_time and a.pack_time > a.choice_time, a.pack_time - a.choice_time, a.pack_time - a.pick_time) + if(a.outstock_time > a.pack_time, a.outstock_time - a.pack_time, 0) - if(a.abnormal_time > 0, a.abnormal_time, 0)) > 0 , if(a.pull_time > a.wait_pull_time, a.pull_time - a.wait_pull_time, 0) + if(a.pick_time > a.pull_time, a.pick_time - a.pull_time, 0) +if(a.choice_time > a.pick_time, a.choice_time - a.pick_time, 0) + if(a.choice_time and a.pack_time > a.choice_time, a.pack_time - a.choice_time, a.pack_time - a.pick_time) + if(a.outstock_time > a.pack_time, a.outstock_time - a.pack_time, 0) - if(a.abnormal_time > 0, a.abnormal_time, 0), 0))/43200) as use_hours,count(*),b.total,count(*)/b.total as   `out` FROM ueb_order_operate_time a left join (SELECT  a.warehouse_code,count(*) as total FROM ueb_order_operate_time a WHERE TO_DAYS( NOW( ) ) - TO_DAYS( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) in (1)  and wait_pull_time > 0 and pull_time > 0 and pick_time > 0 and pack_time > 0 and outstock_time > 0 and delivery_time > 0  and batch_no not like "%-6-%" group by warehouse_code)b on a.warehouse_code=b.warehouse_code WHERE TO_DAYS( NOW( ) ) - TO_DAYS( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) in (1)  and wait_pull_time > 0 and pull_time > 0 and pick_time > 0 and pack_time > 0 and outstock_time > 0 and delivery_time > 0  and batch_no not like "%-6-%" group by warehouse_code,use_hours )c on a.warehouse_code=c.warehouse_code and a.use_hours =c.use_hours  left join (		SELECT a.warehouse_code 	,	CASE								WHEN a.time <= 12 THEN "1" WHEN a.time > 12 				AND a.time <= 24 THEN "2" WHEN a.time > 24 					AND a.time <= 36 THEN "3" WHEN a.time > 36 						AND a.time <= 48 THEN "4" WHEN a.time > 48 							AND a.time <= 60 THEN "5" WHEN a.time > 60 								AND a.time <= 108 THEN									"6" ELSE "7" 									END AS `use_hours`,								count( a.time ) AS num,								b.time,								round( count( a.time )/ b.time ,4 ) "in" 							FROM								(								SELECT 									warehouse_code,									date_format( upper_end_time, "%Y-%m-%d" ) AS Date,									ROUND(( unix_timestamp( upper_end_time ) - unix_timestamp( quality_start_time )) / 3600, 2 ) AS time 								FROM									ueb_quality_warehousing_record a 								WHERE									type = 1 									AND paragraph = 5 									AND quality_start_time > 0 									AND add_time > 0 									AND post_code_end_time > 0 												AND TO_DAYS( NOW( ) ) - TO_DAYS( upper_end_time ) IN ( 1) 								) a,								(								SELECT 									a.warehouse_code,									"in" AS `way`,									count( a.time ) AS time 								FROM									(									SELECT 										warehouse_code,										date_format( upper_end_time, "%Y-%m-%d" ) AS Date,										ROUND(( unix_timestamp( upper_end_time ) - unix_timestamp( quality_start_time )) / 3600, 2 ) AS time 									FROM										ueb_quality_warehousing_record 									WHERE										type = 1 										AND paragraph = 5 										AND quality_start_time > 0 										AND add_time > 0 										AND post_code_end_time > 0 			AND TO_DAYS( NOW( ) ) - TO_DAYS( upper_end_time ) IN ( 1) 																		) a 								GROUP BY									a.warehouse_code,									a.Date 								) b 							WHERE								a.warehouse_code = b.warehouse_code 							GROUP BY								a.warehouse_code,									`use_hours`)d on a.warehouse_code = d.warehouse_code and a.use_hours = d.use_hours group by a.warehouse_code,a.use_hours order by a.warehouse_code,a.use_hours'
    # sql3 = 'update ueb_order_operate_time set order_product_number = 1 where order_product_number=0'
    #
    # try:
    #     cur.execute(sql3)
    #     con.commit()
    #     print("update OK")
    # except:
    #     con.rollback()
    cur.execute(sql_dcl2)
    see_dcl2 = cur.fetchall()
    dcl2_in = []
    dcl2_out = []
    dcl2_fba = []
    for data_dcl2 in see_dcl2:
        dcl2_in.append(data_dcl2[4])
        dcl2_out.append(data_dcl2[3])
        dcl2_fba.append(data_dcl2[2])

    dcl2_in.append(sum(dcl2_in[0:2]))
    dcl2_in.append(sum(dcl2_in[3:5]))
    dcl2_out.append(sum(dcl2_out[0:2]))
    dcl2_out.append(sum(dcl2_out[3:5]))
    dcl2_fba.append(sum(dcl2_fba[0:2]))
    dcl2_fba.append(sum(dcl2_fba[0:3]))
    dcl2_fba.append(sum(dcl2_fba[3:5]))
    dcl2_fba.append(sum(dcl2_fba[3:6]))

    cur.execute(sql_db)
    see_db = cur.fetchall()
    db_in = []
    db_out = []
    db_total = []
    db_date = []
    for data_db in see_db:
        db_in.append(data_db[2])
        db_out.append(data_db[3])
        db_total.append(data_db[4])
        db_date.append(data_db[0])
    db_date = db_date[0:7]
    db_in.append(max(db_in[0:7] + db_out[0:7]) + 100)
    db_in.append(max(db_in[7:15] + db_out[7:15]) + 100)
    db_in.append(max(db_total[0:7]) + 100)
    db_in.append(max(db_total[7:15]) + 100)

    cur.execute(sql_dcl)
    see_dcl = cur.fetchall()
    dcl_1 = []
    dcl_2 = []
    dcl_3 = []
    dcl_4 = []
    for data_dcl in see_dcl:
        dcl_1.append(round(data_dcl[3], 2))
        dcl_2.append(round(data_dcl[4], 2))
        dcl_3.append(round(data_dcl[5], 2))
        dcl_4.append(round(data_dcl[6], 2))

    cur.execute(sql_zt)
    see_zt = cur.fetchall()
    zt_warehouse = []
    zt_date = []
    zt_1 = []
    zt_2 = []
    zt_3 = []
    zt_4 = []
    zt_5 = []
    for data_zt in see_zt:
        zt_warehouse.append(data_zt[0])
        zt_date.append(data_zt[1])
        zt_1.append(data_zt[2])
        zt_2.append(data_zt[3])
        zt_3.append(data_zt[4])
        zt_4.append(data_zt[5])
        zt_5.append(data_zt[6])
    zt_1.append(max(zt_1[0:4]) + max(zt_2[0:4]) + max(zt_4[0:4]) + 40000)
    zt_1.append(max(zt_1[5:9]) + max(zt_2[5:9]) + max(zt_4[5:9]) + 40000)
    zt_1.append(max(zt_3[0:4]) + 10000)
    zt_1.append(max(zt_3[5:9]) + 10000)

    cur.execute(sql_ry)
    see_ry = cur.fetchall()

    ry_warehouse = []
    ry_date = []
    ry_1 = []
    ry_2 = []
    ry_3 = []
    ry_4 = []
    ry_5 = []
    ry_6 = []
    ry_7 = []
    ry_8 = []
    ry_9 = []
    ry_10 = []
    ry_11 = []
    ry_12 = []
    ry_13 = []
    ry_14 = []

    for data_ry in see_ry:
        ry_warehouse.append(data_ry[0])
        ry_date.append(data_ry[1])
        ry_1.append(data_ry[2])
        ry_2.append(data_ry[3])
        ry_3.append(data_ry[4])
        ry_4.append(data_ry[5])
        ry_5.append(data_ry[6])
        ry_6.append(data_ry[7])
        ry_7.append(data_ry[8])
        ry_8.append(data_ry[9])
        ry_9.append(data_ry[10])
        ry_10.append(data_ry[11])
        ry_11.append(data_ry[12])
        ry_12.append(data_ry[13])

    cur.execute(sql_ry2)
    see_ry2 = cur.fetchall()

    for data_ry in see_ry2:
        ry_13.append(data_ry[4])
        ry_14.append(data_ry[5])
    if ry_13:
        print('1')
    else:
        ry_13 = [0, 0, 0, 0]

    if ry_14:
        print('1')
    else:
        ry_14 = [0, 0, 0, 0]

    ##需语句修正
    hm_total = []
    tx_total = []
    hm_change = []
    tx_change = []
    hm_total.append(float(ry_1[1]))
    hm_total.append(float(ry_1[0]))
    hm_total.append(float(ry_3[0] + ry_3[1]))
    hm_total.append(float(ry_5[0] + ry_5[1]))
    hm_total.append(float(ry_7[0] + ry_7[1]))
    hm_total.append(float(ry_9[0] + ry_9[1]))
    try:
       hm_total.append(round(hm_total[5] / hm_total[2], 2))
    except ZeroDivisionError:
       hm_total.append(0)


    hm_total.append(float(ry_13[0] + ry_13[1]))
    hm_total.append(float(ry_14[0] + ry_14[1]))
    
    tx_total.append(float(ry_1[2]))
    tx_total.append(float(ry_1[3]))
    tx_total.append(float(ry_3[3] + ry_3[2]))
    tx_total.append(float(ry_5[3] + ry_5[2]))
    tx_total.append(float(ry_7[3] + ry_7[2]))
    tx_total.append(float(ry_9[3] + ry_9[2]))
    try:
       tx_total.append(round(tx_total[5] / tx_total[2], 2))
    except ZeroDivisionError:
       tx_total.append(0)
    tx_total.append(float(ry_13[2] + ry_13[3]))
    tx_total.append(float(ry_14[2] + ry_14[3]))

    hm_change.append(float(ry_2[1]))
    hm_change.append(float(ry_2[0]))
    hm_change.append(float(ry_4[0]) + float(ry_4[1]))
    hm_change.append(float(ry_6[0]) + float(ry_6[1]))
    hm_change.append(round(float(ry_8[0]) + float(ry_8[1]), 0))
    hm_change.append(round(float(ry_10[0]) + float(ry_10[1]), 0))
    try:
     hm_change.append(
        round(float(hm_total[6]) - ((float(ry_12[0]) + float(ry_12[1])) / (float(ry_11[0]) + float(ry_11[1]))), 2))
    except ZeroDivisionError:
     hm_change.append(0)
    tx_change.append(float(ry_2[3]))
    tx_change.append(float(ry_2[2]))
    tx_change.append(float(ry_4[3]) + float(ry_4[2]))
    tx_change.append(float(ry_6[3]) + float(ry_6[2]))
    tx_change.append(round(float(ry_8[3]) + float(ry_8[2]), 0))
    tx_change.append(round(float(ry_10[3]) + float(ry_10[2]), 0))
    try:
     tx_change.append(
        round(tx_total[6] - ((float(ry_12[3]) + float(ry_12[2])) / (float(ry_11[3]) + float(ry_11[2]))), 2))
    except ZeroDivisionError:
        tx_change.append(0)
    cur.execute(sql_tph)
    see_tph = cur.fetchall()
    warehouse_tph = []
    tph_date = []
    tph = []
    uph = []
    for data_tph in see_tph:
        tph_date.append(data_tph[0])
        warehouse_tph.append(data_tph[1])
        tph.append(data_tph[2])
        uph.append(data_tph[3])
    hm_tph_date = []
    hm_tph = []
    hm_uph = []
    tx_tph_date = []
    tx_tph = []
    tx_uph = []
    for i in range(len(warehouse_tph)):
        if warehouse_tph[i] == 'HM_AA':
            hm_tph_date.append(tph_date[i])
            hm_tph.append(tph[i])
            hm_uph.append(uph[i])
    for i in range(len(warehouse_tph)):
        if warehouse_tph[i] == 'SZ_AA':
            tx_tph_date.append(tph_date[i])
            tx_tph.append(tph[i])
            tx_uph.append(uph[i])
    a = round(max(hm_tph), 0) + 10
    b = round(min(hm_uph), 0) - 10
    hm_tph.append(a)
    hm_tph.append(b)
    a = round(max(tx_tph), 0) + 10
    b = round(min(tx_uph), 0) - 10
    hm_uph.append(a)
    hm_uph.append(b)

    cur.execute(sql_jy)
    see_jy = cur.fetchall()
    warehouse_jy = []
    num_jy = []
    type_jy = []
    for data_jy in see_jy:
        warehouse_jy.append(data_jy[0])
        num_jy.append(data_jy[1])
        type_jy.append(data_jy[2])

    cur.execute(sql_zl)
    see_zl = cur.fetchall()
    warehouse_zl = []
    cost_zl = []
    time_zl = []
    jsonData = {}
    for data_zl in see_zl:
        warehouse_zl.append(data_zl[0])
        cost_zl.append(data_zl[1])
        time_zl.append(data_zl[2])

    cur.execute(sql_sx)
    see_sx = cur.fetchall()
    warehouse_sx = []
    type_sx = []
    time_sx = []
    date_sx = []

    for data_sx in see_sx:
        date_sx.append(data_sx[0])
        warehouse_sx.append(data_sx[1])
        type_sx.append(data_sx[2])
        time_sx.append(data_sx[3])

    cur.execute(sql_rk)
    see_rk = cur.fetchall()
    warehouse_rk = []
    type_rk = []
    num_rk = []

    for data_rk in see_rk:
        warehouse_rk.append(data_rk[0])
        type_rk.append(data_rk[2])
        num_rk.append(data_rk[3])

    hm_rk_in = []
    hm_rk_out = []
    hm_rk_ld = []
    tx_rk_in = []
    tx_rk_out = []
    tx_rk_ld = []

    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'HM_AA' and type_rk[i] == 'in':
            hm_rk_in.append(num_rk[i])
    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'HM_AA' and type_rk[i] == 'out':
            hm_rk_out.append(num_rk[i])
    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'HM_AA' and type_rk[i] == 'LD':
            hm_rk_ld.append(num_rk[i])
    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'SZ_AA' and type_rk[i] == 'in':
            tx_rk_in.append(num_rk[i])
    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'SZ_AA' and type_rk[i] == 'out':
            tx_rk_out.append(num_rk[i])
    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'SZ_AA' and type_rk[i] == 'LD':
            tx_rk_ld.append(num_rk[i])

    hm_sx_date = []
    tx_sx_date = []
    hm_sx_in = []
    hm_sx_out = []
    hm_sx_fba = []
    tx_sx_in = []
    tx_sx_out = []
    tx_sx_fba = []
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'HM_AA' and type_sx[i] == 'in':
            hm_sx_date.append(date_sx[i])

    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'HM_AA' and type_sx[i] == 'in':
            hm_sx_in.append(time_sx[i])
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'HM_AA' and type_sx[i] == 'out':
            hm_sx_out.append(time_sx[i])
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'HM_AA' and type_sx[i] == 'FBA':
            hm_sx_fba.append(time_sx[i])

    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'SZ_AA' and type_sx[i] == 'in':
            tx_sx_date.append(date_sx[i])
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'SZ_AA' and type_sx[i] == 'in':
            tx_sx_in.append(time_sx[i])
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'SZ_AA' and type_sx[i] == 'out':
            tx_sx_out.append(time_sx[i])
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'SZ_AA' and type_sx[i] == 'FBA':
            tx_sx_fba.append(time_sx[i])

    num_jy_hm = []
    type_jy_hm = []
    num_jy_tx = []
    type_jy_tx = []
    for i in range(len(warehouse_jy)):
        if warehouse_jy[i] == 'HM_AA':
            num_jy_hm.append(num_jy[i])
            type_jy_hm.append(type_jy[i])
    for i in range(len(warehouse_jy)):
        if warehouse_jy[i] == 'SZ_AA':
            num_jy_tx.append(num_jy[i])
            type_jy_tx.append(type_jy[i])

    hm_zl_cost = []
    hm_zl_time = []
    tx_zl_cost = []
    tx_zl_time = []

    for i in range(len(warehouse_zl)):
        if warehouse_zl[i] == "HM_AA":
            hm_zl_cost.append(cost_zl[i])
            hm_zl_time.append(time_zl[i])
    for i in range(len(warehouse_zl)):
        if warehouse_zl[i] == "SZ_AA":
            tx_zl_cost.append(cost_zl[i])
            tx_zl_time.append(time_zl[i])

    hm_jy_data = np.dstack((num_jy_hm, type_jy_hm))
    tx_jy_data = np.dstack((num_jy_tx, type_jy_tx))

    hm_jy_DLD_num = [0]
    hm_jy_DCK_num = [0]
    hm_jy_DDB_num = [0]
    hm_jy_DGNZJ_num = [0]
    hm_jy_DJH_num = [0]
    hm_jy_DRK_num = [0]
    hm_jy_DSJ_num = [0]
    hm_jy_DTM_num = [0]
    hm_jy_FDCK_num = [0]
    hm_jy_FDDB_num = [0]
    hm_jy_FDJH_num = [0]
    hm_jy_FDJY_num = [0]
    hm_jy_FJHZ_num = [0]
    hm_jy_FDLD_num = [0]
    hm_jy_DBDRK_num = [0]
    hm_jy_DBRKZ_num = [0]
    hm_jy_DBDLD_num = [0]
    hm_jy_DBDJH_num = [0]
    hm_jy_DBDDB_num = [0]
    hm_jy_DBDCK_num = [0]
    hm_jy_DBDJY_num = [0]
    hm_jy_DPK_num = [0]
    hm_jy_FDPK_num = [0]
    hm_jy_FDFPLD_num = [0]
    tx_jy_FDFPLD_num = [0]

    tx_jy_DPK_num = [0]
    tx_jy_FDPK_num = [0]
    tx_jy_DBDRK_num = [0]
    tx_jy_DBRKZ_num = [0]
    tx_jy_DBDLD_num = [0]
    tx_jy_DBDJH_num = [0]
    tx_jy_DBDDB_num = [0]
    tx_jy_DBDCK_num = [0]
    tx_jy_DBDJY_num = [0]
    tx_jy_DLD_num = [0]
    tx_jy_DCK_num = [0]
    tx_jy_DDB_num = [0]
    tx_jy_DGNZJ_num = [0]
    tx_jy_DJH_num = [0]
    tx_jy_DRK_num = [0]
    tx_jy_DSJ_num = [0]
    tx_jy_DTM_num = [0]
    tx_jy_FDCK_num = [0]
    tx_jy_FDDB_num = [0]
    tx_jy_FDJH_num = [0]
    tx_jy_FDJY_num = [0]
    tx_jy_FJHZ_num = [0]
    tx_jy_FDLD_num = [0]

    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DCK':
            hm_jy_DCK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DLD':
            hm_jy_DLD_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DDB':
            hm_jy_DDB_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DGNZJ':
            hm_jy_DGNZJ_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DRK':
            hm_jy_DRK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DSJ':
            hm_jy_DSJ_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DTM':
            hm_jy_DTM_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDCK':
            hm_jy_FDCK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDDB':
            hm_jy_FDDB_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDJH':
            hm_jy_FDJH_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDJY':
            hm_jy_FDJY_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FJHZ':
            hm_jy_FJHZ_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDLD':
            hm_jy_FDLD_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DJH':
            hm_jy_DJH_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDRK':
            hm_jy_DBDRK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBRKZ':
            hm_jy_DBRKZ_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDLD':
            hm_jy_DBDLD_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDJH':
            hm_jy_DBDJH_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDDB':
            hm_jy_DBDDB_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDCK':
            hm_jy_DBDCK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDJY':
            hm_jy_DBDJY_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DPK':
            hm_jy_DPK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDPK':
            hm_jy_FDPK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDFPLD':
            hm_jy_FDFPLD_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDFPLD':
            tx_jy_FDFPLD_num[0] = (tx_jy_data[0][i][0])

    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DPK':
            tx_jy_DPK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDPK':
            tx_jy_FDPK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DLD':
            tx_jy_DLD_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DCK':
            tx_jy_DCK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DDB':
            tx_jy_DDB_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DGNZJ':
            tx_jy_DGNZJ_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DRK':
            tx_jy_DRK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DSJ':
            tx_jy_DSJ_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DTM':
            tx_jy_DTM_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDCK':
            tx_jy_FDCK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDDB':
            tx_jy_FDDB_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDJH':
            tx_jy_FDJH_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDJY':
            tx_jy_FDJY_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FJHZ':
            tx_jy_FJHZ_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDLD':
            tx_jy_FDLD_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DJH':
            tx_jy_DJH_num[0] = tx_jy_data[0][i][0]
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDRK':
            tx_jy_DBDRK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBRKZ':
            tx_jy_DBRKZ_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDLD':
            tx_jy_DBDLD_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDJH':
            tx_jy_DBDJH_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDDB':
            tx_jy_DBDDB_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDCK':
            tx_jy_DBDCK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDJY':
            tx_jy_DBDJY_num[0] = (tx_jy_data[0][i][0])
    hm_jy_XB_totoal = []
    hm_jy_FB_totoal = []
    tx_jy_XB_totoal = []
    tx_jy_FB_totoal = []
    hm_jy_DB_totoal = []
    tx_jy_DB_totoal = []

    hm_jy_XB_totoal.append(float(hm_jy_DCK_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DDB_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DJH_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DLD_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DPK_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DSJ_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DTM_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DGNZJ_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DRK_num[0]))

    hm_jy_DB_totoal.append(float(hm_jy_DBDJY_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBDCK_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBDDB_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBDJH_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBDLD_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBRKZ_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBDRK_num[0]))

    tx_jy_DB_totoal.append(float(tx_jy_DBDJY_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBDCK_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBDDB_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBDJH_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBDLD_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBRKZ_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBDRK_num[0]))

    tx_jy_XB_totoal.append(float(tx_jy_DCK_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DDB_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DJH_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DLD_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DPK_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DSJ_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DTM_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DGNZJ_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DRK_num[0]))

    hm_jy_FB_totoal.append(float(hm_jy_FDJY_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDCK_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDDB_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FJHZ_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDJH_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDLD_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDFPLD_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDPK_num[0]))

    tx_jy_FB_totoal.append(float(tx_jy_FDJY_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDCK_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDDB_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FJHZ_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDJH_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDLD_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDFPLD_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDPK_num[0]))

    hm_jy_XB_totoal_color = []
    hm_jy_FB_totoal_color = []
    hm_jy_DB_totoal_color = []
    tx_jy_XB_totoal_color = []
    tx_jy_FB_totoal_color = []
    tx_jy_DB_totoal_color = []
    for i in range(len(hm_jy_XB_totoal)):
        hm_jy_XB_totoal_color.append('{:.2%}'.format(hm_jy_XB_totoal[i] / max(hm_jy_XB_totoal)))
    if hm_jy_XB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(hm_jy_XB_totoal)):
            hm_jy_XB_totoal_color[i] = '{:.2%}'.format(a)
    for i in range(len(hm_jy_FB_totoal)):
        hm_jy_FB_totoal_color.append('{:.2%}'.format(hm_jy_FB_totoal[i] / max(hm_jy_FB_totoal)))
    if hm_jy_FB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(hm_jy_FB_totoal)):
            hm_jy_FB_totoal_color[i] = '{:.2%}'.format(a)
    for i in range(len(hm_jy_DB_totoal)):
        hm_jy_DB_totoal_color.append('{:.2%}'.format(hm_jy_DB_totoal[i] / max(hm_jy_DB_totoal)))
    if hm_jy_DB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(hm_jy_DB_totoal)):
            hm_jy_DB_totoal_color[i] = '{:.2%}'.format(a)
    for i in range(len(tx_jy_XB_totoal)):
        tx_jy_XB_totoal_color.append('{:.2%}'.format(tx_jy_XB_totoal[i] / max(tx_jy_XB_totoal)))
    if tx_jy_XB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(tx_jy_XB_totoal)):
            tx_jy_XB_totoal_color[i] = '{:.2%}'.format(a)
    for i in range(len(tx_jy_FB_totoal)):
        tx_jy_FB_totoal_color.append('{:.2%}'.format(tx_jy_FB_totoal[i] / max(tx_jy_FB_totoal)))
    if tx_jy_FB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(tx_jy_FB_totoal)):
            tx_jy_FB_totoal_color[i] = '{:.2%}'.format(a)
    for i in range(len(tx_jy_DB_totoal)):
        tx_jy_DB_totoal_color.append('{:.2%}'.format(tx_jy_DB_totoal[i] / max(tx_jy_DB_totoal)))
    if tx_jy_DB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(tx_jy_DB_totoal)):
            tx_jy_DB_totoal_color[i] = '{:.2%}'.format(a)

    jsonData['dcl2_in'] = dcl2_in
    jsonData['dcl2_out'] = dcl2_out
    jsonData['dcl2_fba'] = dcl2_fba

    jsonData['db_in'] = db_in
    jsonData['db_out'] = db_out
    jsonData['db_total'] = db_total
    jsonData['db_date'] = db_date
    jsonData['dcl_1'] = dcl_1
    jsonData['dcl_2'] = dcl_2
    jsonData['dcl_3'] = dcl_3
    jsonData['dcl_4'] = dcl_4
    jsonData['zt_date'] = zt_date
    jsonData['zt_1'] = zt_1
    jsonData['zt_2'] = zt_2
    jsonData['zt_3'] = zt_3
    jsonData['zt_4'] = zt_4
    jsonData['zt_5'] = zt_5

    jsonData['hm_change'] = hm_change
    jsonData['tx_change'] = tx_change
    jsonData['hm_total'] = hm_total
    jsonData['tx_total'] = tx_total
    jsonData['hm_jy_XB_totoal'] = hm_jy_XB_totoal
    jsonData['hm_jy_FB_totoal'] = hm_jy_FB_totoal
    jsonData['tx_jy_XB_totoal'] = tx_jy_XB_totoal
    jsonData['tx_jy_FB_totoal'] = tx_jy_FB_totoal
    jsonData['hm_jy_DB_totoal'] = hm_jy_DB_totoal
    jsonData['tx_jy_DB_totoal'] = tx_jy_DB_totoal
    jsonData['hm_jy_XB_totoal_color'] = hm_jy_XB_totoal_color
    jsonData['hm_jy_FB_totoal_color'] = hm_jy_FB_totoal_color
    jsonData['hm_jy_DB_totoal_color'] = hm_jy_DB_totoal_color
    jsonData['tx_jy_XB_totoal_color'] = tx_jy_XB_totoal_color
    jsonData['tx_jy_FB_totoal_color'] = tx_jy_FB_totoal_color
    jsonData['tx_jy_DB_totoal_color'] = tx_jy_DB_totoal_color
    jsonData['hm_zl_cost'] = hm_zl_cost
    jsonData['hm_zl_time'] = hm_zl_time
    jsonData['tx_zl_cost'] = tx_zl_cost
    jsonData['tx_zl_time'] = tx_zl_time

    jsonData['tx_sx_date'] = tx_sx_date
    jsonData['hm_sx_date'] = hm_sx_date
    jsonData['hm_sx_in'] = hm_sx_in
    jsonData['hm_sx_out'] = hm_sx_out
    jsonData['hm_sx_fba'] = hm_sx_fba
    jsonData['tx_sx_in'] = tx_sx_in
    jsonData['tx_sx_out'] = tx_sx_out
    jsonData['tx_sx_fba'] = tx_sx_fba
    jsonData['hm_rk_in'] = hm_rk_in
    jsonData['hm_rk_out'] = hm_rk_out
    jsonData['hm_rk_ld'] = hm_rk_ld
    jsonData['tx_rk_in'] = tx_rk_in
    jsonData['tx_rk_out'] = tx_rk_out
    jsonData['tx_rk_ld'] = tx_rk_ld
    jsonData['hm_tph_date'] = hm_tph_date
    jsonData['hm_tph'] = hm_tph
    jsonData['hm_uph'] = hm_uph
    jsonData['tx_tph_date'] = tx_tph_date
    jsonData['tx_tph'] = tx_tph
    jsonData['tx_uph'] = tx_uph
    j = json.dumps(jsonData, cls=DecimalEncoder)
    cur.close()
    return (j)





if __name__ == '__main__':
    app.run()

