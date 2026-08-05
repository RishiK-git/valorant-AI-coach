# Valorant AI Coach

An AI-powered coaching system that analyzes Valorant gameplay footage and provides structured coaching feedback using computer vision and multimodal large language models.

## Overview

The goal of this project is to automatically analyze recorded Valorant gameplay and generate coaching similar to what a human coach would provide.

The current pipeline:

1. Upload a gameplay video (currently a single round)
2. Extract representative frames using FFmpeg
3. Detect allies and enemies using a custom YOLO11 model
4. Select the most informative frames
5. Send the selected frames and detector context to Google's Gemini multimodal model
6. Generate structured coaching feedback as validated JSON

The long-term goal is to support full match analysis while keeping inference efficient through intelligent frame selection and parallel processing.

---

# Features

Current functionality:

- Video frame extraction using FFmpeg
- Configurable frame sampling
- Multi-image gameplay analysis
- Gemini-powered coaching
- Structured JSON responses using Pydantic
- Modular Python pipeline
- Custom YOLO11 ally/enemy detector
- Grounded prompting to reduce hallucinations

Planned:

- Event-driven frame selection
- FastAPI backend
- Frontend upload UI
- Full match support
- Round segmentation
- Parallel scatter-gather inference
- Persistent analysis storage

---

# Tech Stack

## AI

- Google Gemini
- YOLO11 (Ultralytics)

## Backend

- Python 3.12
- Pydantic

## Video Processing

- FFmpeg
- OpenCV (planned)

## Future

- FastAPI
- React
- Docker
- Redis (if asynchronous job queue becomes necessary)

---

# High-Level Architecture
