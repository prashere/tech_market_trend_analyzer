from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=True)
import asyncio
import numpy as np
from typing import Dict, List, Optional

from main import full_data_pipeline, update_data_pipeline
from views import get_cluster_analysis_for_frontend, process_all_clusters, numpy_json_encoder
from agent.clusters import get_article_clusters

app = FastAPI(
    title="Tech Market Trend Analyzer API",
    version="1.0.0",
    description="AI-powered market analysis and trend clustering system"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NumpyJSONResponse(JSONResponse):
    # Custom JSON response class for handling numpy types
    def render(self, content) -> bytes:
        return json.dumps(content, default=numpy_json_encoder, ensure_ascii=False, indent=None, separators=(',', ':')).encode('utf-8')


if Path("frontend").exists():
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

pipeline_status = {
    "is_running": False,
    "last_run": None,
    "last_update": None,
    "status": "idle",
    "message": ""
}


@app.get("/", response_class=HTMLResponse)
async def serve_homepage():
    try:
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Frontend not found</h1>", status_code=404)


@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard():
    try:
        with open("frontend/dashboard.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Dashboard not found</h1>", status_code=404)


# DATA PIPELINE ROUTES

@app.get("/api/pipeline/status")
async def get_pipeline_status():
    """Get current pipeline status"""
    return JSONResponse(content={
        "status": pipeline_status["status"],
        "is_running": pipeline_status["is_running"],
        "last_run": pipeline_status["last_run"],
        "last_update": pipeline_status["last_update"],
        "message": pipeline_status["message"]
    })


@app.post("/api/pipeline/run")
async def run_data_pipeline(background_tasks: BackgroundTasks, update_mode: bool = False):
    if pipeline_status["is_running"]:
        raise HTTPException(
            status_code=400,
            detail="Pipeline is already running. Please wait for completion."
        )

    # Run pipeline in background
    background_tasks.add_task(run_pipeline_background, update_mode)

    return JSONResponse(content={
        "message": f"Data pipeline started in {'update' if update_mode else 'full'} mode",
        "status": "started"
    })


async def run_pipeline_background(update_mode: bool = False):
    """Background task to run the data pipeline"""
    pipeline_status["is_running"] = True
    pipeline_status["status"] = "running"
    pipeline_status["message"] = f"Running {'update' if update_mode else 'full'} pipeline..."

    try:
        # Run the pipeline
        success = full_data_pipeline(update_mode=update_mode)

        current_time = datetime.now().isoformat()
        if success:
            pipeline_status["status"] = "completed"
            pipeline_status["message"] = "Pipeline completed successfully"
            pipeline_status["last_run"] = current_time
            if update_mode:
                pipeline_status["last_update"] = current_time
        else:
            pipeline_status["status"] = "error"
            pipeline_status["message"] = "Pipeline completed with errors"

    except Exception as e:
        pipeline_status["status"] = "error"
        pipeline_status["message"] = f"Pipeline failed: {str(e)}"

    finally:
        pipeline_status["is_running"] = False


# CLUSTER ANALYSIS ROUTES

@app.get("/api/clusters")
async def get_clusters():
    try:
        clusters = get_article_clusters()

        return NumpyJSONResponse(content={
            "success": True,
            "total_clusters": len(clusters),
            "clusters": clusters
        })

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving clusters: {str(e)}")


@app.get("/api/analysis")
async def get_market_analysis():
    try:
        if os.path.exists("cluster_analysis.json"):
            with open("cluster_analysis.json", "r", encoding="utf-8") as f:
                cached_data = json.load(f)

            return JSONResponse(content={
                "success": True,
                "source": "cache",
                "message": "Retrieved cached analysis",
                "total_clusters": len(cached_data),
                "clusters": cached_data,
                "generated_at": datetime.now().isoformat()
            })
        else:
            result = get_cluster_analysis_for_frontend()
            return JSONResponse(content=result)

    except FileNotFoundError as e:
        return JSONResponse(content={
            "success": False,
            "message": str(e),
            "clusters": []
        })
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating analysis: {str(e)}")


@app.post("/api/analysis/refresh")
async def refresh_market_analysis(background_tasks: BackgroundTasks):
    if pipeline_status["is_running"]:
        raise HTTPException(
            status_code=400,
            detail="Cannot refresh analysis while pipeline is running"
        )

    background_tasks.add_task(refresh_analysis_background)

    return JSONResponse(content={
        "message": "Analysis refresh started",
        "status": "started"
    })


async def refresh_analysis_background():
    try:
        if os.path.exists("cluster_analysis.json"):
            os.remove("cluster_analysis.json")

        result = get_cluster_analysis_for_frontend()
        print(f"Analysis refreshed: {result['message']}")

    except Exception as e:
        print(f"Error refreshing analysis: {e}")


# INDIVIDUAL CLUSTER ROUTES

@app.get("/api/clusters/{cluster_id}")
async def get_cluster_details(cluster_id: int):
    """Get detailed information about a specific cluster"""
    try:
        # Load analysis data
        if os.path.exists("cluster_analysis.json"):
            with open("cluster_analysis.json", "r", encoding="utf-8") as f:
                analysis_data = json.load(f)

            # Find the specific cluster
            for cluster in analysis_data:
                if cluster["cluster_id"] == cluster_id:
                    return JSONResponse(content={
                        "success": True,
                        "cluster": cluster
                    })

            raise HTTPException(
                status_code=404, detail=f"Cluster {cluster_id} not found")
        else:
            raise HTTPException(
                status_code=404, detail="No analysis data available")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving cluster: {str(e)}")


# SYSTEM INFO ROUTES

@app.get("/api/system/info")
async def get_system_info():
    """Get system information and health status"""
    try:
        # Check if required files exist
        faiss_exists = os.path.exists("faiss/articles_faiss.index")
        metadata_exists = os.path.exists("faiss/articles_metadata.pkl")
        analysis_exists = os.path.exists("cluster_analysis.json")

        # Get latest CSV file info
        import glob
        csv_files = glob.glob('articles_cleaned_*.csv')
        latest_csv = None
        if csv_files:
            csv_files.sort(key=os.path.getmtime, reverse=True)
            latest_csv = csv_files[0]

        return JSONResponse(content={
            "system_status": "healthy" if all([faiss_exists, metadata_exists]) else "incomplete",
            "components": {
                "faiss_index": faiss_exists,
                "metadata": metadata_exists,
                "analysis_cache": analysis_exists,
                "latest_data": latest_csv
            },
            "pipeline_status": pipeline_status,
            "api_version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting system info: {str(e)}")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "tech-market-trend-analyzer"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True,
        log_level="info"
    )
