전체 흐름
csv->nifi->kafka->python->timescaledb->superset

data 폴더: 	csv파일
		(nifi 프로세서가 csv파일을 읽고 삭제함)

tool 폴더: 	code.txt= 필요한 대부분의 코드
		CSVToKafka= nifi 프로세서(nifi processor group)
		dashboard_export.zip= superset 데이터(superset dashbboard)
		result.png= dashboard_export.zip의 결과

consumer.py:	직접 실행할 python code(kafka->timescale db)

docker-compose.yml: docker 파일

readme.txt:	지금 이 텍스트