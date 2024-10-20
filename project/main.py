from fastapi import FastAPI
from routers.books_router import book_router
from routers.author_router import author_router
from routers.save_report import report_router

app = FastAPI()
app.include_router(book_router)
app.include_router(author_router)
app.include_router(report_router)