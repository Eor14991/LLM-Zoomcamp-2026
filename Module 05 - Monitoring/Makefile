run:
	PYTHONPATH=".." uv run python assistant.py

chat:
	PYTHONPATH=".." uv run streamlit run app.py

network:
	docker network create monitoring

postgres:
	docker start course-assistant-pg || docker run -d \
		--name course-assistant-pg \
		--network monitoring \
		-e POSTGRES_USER=user \
		-e POSTGRES_PASSWORD=password \
		-e POSTGRES_DB=course_assistant \
		-p 5432:5432 \
		-v pgdata:/var/lib/postgresql/data \
		postgres:18

db:
	uv run python db_init.py


dashboard:
	PYTHONPATH=".." uv run streamlit run dashboard.py --server.port 8502