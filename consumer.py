from kafka import KafkaConsumer
import psycopg2
import json

# Kafka 설정
consumer = KafkaConsumer(
    'test-topic',
    bootstrap_servers='localhost:9092',
	group_id='my-consumer-group',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# TimescaleDB 연결
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="mydb",
    user="myuser",
    password="mypassword"
)
cursor = conn.cursor()

for message in consumer:
    raw = message.value  # Kafka에서 받은 dict
    print(f"받은 데이터: {raw}")  # 원본 출력

    try:
        # 키 매핑
        data = {
            "year": int(raw["year"]),
            "company_name": raw["기업명"],
            "stock_gr": float(raw["stock_gr(주가수익율)"]),
            "sale_gr": float(raw["sale_gr(매출증가율)"]),
            "debt_gr": float(raw["debt_gr(부채증가율)"]),
            "profit_gr": float(raw["profit_gr(이익증가율)"]),
            "sales_profit": float(raw["매출*이익"]),
            "is_kospi": int(raw["D.KOSPI"]),
            "market": raw["거래시장"]
        }

        # DB에 삽입
        cursor.execute("""
            INSERT INTO stock_data (
                year, company_name, stock_gr, sale_gr, debt_gr, 
                profit_gr, sales_profit, is_kospi, market
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data["year"],
            data["company_name"],
            data["stock_gr"],
            data["sale_gr"],
            data["debt_gr"],
            data["profit_gr"],
            data["sales_profit"],
            data["is_kospi"],
            data["market"]
        ))
        conn.commit()
        print("DB에 데이터 저장 완료")

    except Exception as e:
        print(f"데이터 저장 중 오류 발생: {e}")
