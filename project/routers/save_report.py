from fastapi import APIRouter
from fastapi.responses import Response

report_router = APIRouter(prefix="/report", tags=["Funny to Create report"])


@report_router.get("/load")
def save_report():
    try:
        path = "data_files/xml_files/test.fodt"
        with open(path,"r") as file:
            data = file.read()
            print(type(data))
            headers = {
            "Content-Disposition": "attachment; filename=example.fodt",
            "Content-Type": "text/xml; charset=utf-8"
        }
    except Exception as e:
        print(e)
    
    return Response(content=data, headers=headers)