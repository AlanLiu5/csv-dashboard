from unicodedata import category
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from data_analyze import run_analysis
import matplotlib
matplotlib.use("Agg")
from fastapi.staticfiles import StaticFiles



app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")



def main():
    print(run_analysis())
if __name__=="__main__":
    main()



@app.get("/")
def root():
    return {"message": "hello"}


@app.get("/analyze")
def analyze(
    group_by: str = "category",
    metric: str = "sum",
    field: str = "amount",
    city: str = "",
    k: int = 10
):
    return run_analysis(group_by, metric, field, city, k)



@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    group_by: str = "category",
    metric: str = "sum",
    field: str = "amount",
    city: str = "",
    k: int = 10
):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "group_by": group_by,
            "metric": metric,
            "field": field,
            "city": city,
            "k": k,
        }
    )

