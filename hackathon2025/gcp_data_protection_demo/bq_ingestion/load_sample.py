
from google.cloud import bigquery

client = bigquery.Client()

dataset_id = "demo_data"
table_id = "customers"

schema = [
    bigquery.SchemaField("customer_id", "STRING"),
    bigquery.SchemaField("full_name", "STRING"),
    bigquery.SchemaField("email", "STRING"),
    bigquery.SchemaField("phone", "STRING"),
    bigquery.SchemaField("credit_card", "STRING"),
    bigquery.SchemaField("dob", "DATE")
]

client.create_dataset(dataset_id, exists_ok=True)
table_ref = f"{client.project}.{dataset_id}.{table_id}"

table = bigquery.Table(table_ref, schema=schema)
table = client.create_table(table, exists_ok=True)

rows = [
    ("001", "Alice Smith", "alice@example.com", "1234567890", "4111111111111111", "1990-01-01"),
    ("002", "Bob Jones", "bob@example.com", "0987654321", "5500000000000004", "1985-05-12"),
    ("003", "Norma Fisher", "ysullivan@yahoo.com", "5938242194", "4157815659387784087", "1955-06-30"),
    ("004", "Ryan Page", "vclayton@cross.com", "9332871158", "180018583989474", "1960-10-09"),
    ("005", "Janice Johnston", "jaimelopez@hotmail.com", "7112201868", "4947751591791", "1997-06-02"),
    ("006", "Connor Smith", "thorntonnathan@gmail.com", "6012309891", "3561510903217308", "2000-10-07"),
    ("007", "Jeffery Garcia", "walkerdeborah@yahoo.com", "2087091634", "4022584197207698", "1989-02-23"),
    ("008", "Linda White", "raymondmurray@johnson.biz", "2084928183", "6011891490545995", "1993-05-13"),
    ("009", "Stephanie Nguyen", "traceygarcia@griffin.com", "5133954012", "6011169707197763", "1966-11-25"),
    ("010", "Victor Simmons", "vaughncarla@harvey.org", "5049988925", "4929031881974723", "1992-03-08"),
    ("011", "Cameron Allen", "brownbrittany@yahoo.com", "3127720413", "4485815536891", "1984-01-17"),
    ("012", "Isabel Young", "kevin68@porter.com", "7158290237", "6011473162292437", "2001-07-06"),
    ("013", "Martha Bennett", "langdaniel@yahoo.com", "9362224503", "4024007155208710", "1982-09-11"),
    ("014", "Leslie Sanchez", "shelleyortiz@freeman.org", "7157656004", "6011425853526455", "1999-10-01"),
    ("015", "Ronnie Thompson", "bobby42@jefferson.com", "5035550498", "4485378860361", "1987-04-14"),
    ("016", "Darryl Berry", "jimmyoconnell@hotmail.com", "9702181837", "6011921699928491", "1974-08-29"),
    ("017", "Tasha Gomez", "mcmahonjennifer@jimenez.net", "4099952134", "6011583854325982", "1991-06-19"),
    ("018", "Veronica Sanders", "stephenspatricia@wright.com", "7193209456", "6011120032145921", "1969-12-03"),
    ("019", "Kara Fields", "rickygregory@gmail.com", "6154246629", "4024007115579473", "2000-01-27"),
    ("020", "Franklin Castillo", "ysoto@bennett.com", "3034357912", "3556259126721206", "1985-10-14"),
    ("021", "Harvey Warner", "tylerboyd@ford.info", "2148795729", "6011013378934405", "1978-06-04"),
    ("022", "Traci Stone", "kim82@powell.org", "2176302133", "6011033678371332", "1996-08-08"),
    ("023", "Clinton Lambert", "latashahowell@jordan.net", "4192238013", "4716726082416", "1981-09-24"),
    ("024", "Ana Grant", "herrerathomas@yahoo.com", "3187203433", "6011868261034215", "1995-11-19"),
    ("025", "Beverly Ferguson", "jameshart@hotmail.com", "8014190398", "6011381542265214", "1973-04-01"),
    ("026", "Bobby Patrick", "kelleyhoffman@campbell.com", "8324002091", "4024007131148121", "1967-07-10"),
    ("027", "Kaitlyn Newton", "kelly07@porter.net", "9123401394", "6011130805829112", "1998-02-05"),
    ("028", "Eleanor Peters", "smithderek@oliver.com", "4143207864", "4916373832265", "1980-11-22"),
    ("029", "Mario Tran", "pamelahill@hotmail.com", "6789123765", "6011613511622581", "1986-03-17"),
    ("030", "Cheryl Cook", "shermanjennifer@gmail.com", "7709832579", "4024007168004214", "1993-12-28"),
    ("031", "Gerald Stanley", "bateslaura@jackson.biz", "4152974523", "6011685734722164", "1999-09-09"),
    ("032", "Tony Daniels", "beverlymcdonald@yahoo.com", "7026598913", "3540590248132354", "2002-06-18"),
    ("033", "Brent Blair", "veronicacoleman@hotmail.com", "7018659017", "6011392013392852", "1968-05-30"),
    ("034", "Kellie Caldwell", "travis57@garner.com", "2095172213", "4024007151260970", "1994-10-13"),
    ("035", "Holly Perez", "waltoneric@nichols.org", "8139921934", "6011364377868492", "1983-07-03"),
    ("036", "Raymond Richards", "joannacarroll@combs.com", "3194830982", "4024007199416741", "1972-11-12"),
    ("037", "Travis Harmon", "bmurphy@walton.net", "6052948123", "6011373875122264", "1990-01-03"),
    ("038", "Karen Wells", "dblackburn@white.com", "2104081159", "6011922520990551", "1987-03-15"),
    ("039", "Patricia Huffman", "tiffanymartinez@gmail.com", "9127939871", "6011137766010386", "1996-05-07"),
    ("040", "Karl Terry", "julia82@dunn.biz", "7075482431", "4024007121371784", "1984-08-19"),
    ("041", "Marshall Bryant", "kathy57@lambert.org", "9183206719", "4929653899016437", "2003-02-11"),
    ("042", "Max Torres", "robertasimmons@keller.info", "6623891254", "6011843924012373", "1997-06-30"),
    ("043", "Ricky Malone", "reedkaren@mitchell.org", "6262100948", "6011358375638557", "1979-04-25"),
    ("044", "Desiree Mullins", "vmonroe@yahoo.com", "4785642938", "6011949218364758", "1963-12-14"),
    ("045", "Stanley Pratt", "brittanyjordan@french.org", "8304223985", "6011131455793856", "1998-09-20"),
    ("046", "Lauren Love", "kristawilliams@leonard.com", "7029156708", "4024007198874020", "2001-07-22"),
    ("047", "Charlotte West", "angelaalexander@gmail.com", "9367290843", "6011047387128927", "1988-11-05"),
    ("048", "Joel Weber", "lucasbyrd@rodriguez.com", "4783095471", "6011173098240112", "1977-01-18"),
    ("049", "Felix Vargas", "larryluna@harper.com", "5128997161", "6011320554021238", "1992-03-02"),
    ("050", "Angelica Ruiz", "michaelsmith@mitchell.com", "9174029834", "4024007120112583", "2000-04-27")    
]

errors = client.insert_rows_json(table, [dict(zip([f.name for f in schema], row)) for row in rows])
print("Errors:", errors)
