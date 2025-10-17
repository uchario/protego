# History Sidepanel Chrome Extension

A Chrome extension that adds a side panel to display the last visit timestamp and basic page analytics (number of links, words, and images) for the current webpage. It uses a FastAPI backend with a PostgreSQL database, running locally via Docker.

## Features

- Captures page visit data: timestamp, URL, link count, word count, and image count.
- FastAPI backend with REST endpoints to store/fetch page metrics and visit history.
- React-based side panel UI showing current page metrics and past visit timestamps.
- Dockerized setup for easy local deployment of FastAPI and PostgreSQL.

## Tech Stack

- **Frontend**: React (Chrome Extension UI)
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **DevOps**: Docker, Docker Compose
- **Build Tool**: Vite

## Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Node.js](https://nodejs.org/) (v16 or higher)
- [Google Chrome](https://www.google.com/chrome/)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd protego
```

### 2. Set Up the Backend

1. Create a `.env` file in the `backend/` directory with the following content:
   ```plaintext
   POSTGRES_USER=admin
   POSTGRES_PASSWORD=secret
   POSTGRES_DB=pageanalytics
   DATABASE_URL=postgresql://admin:secret@postgres:5432/page_analytics
   ```
2. Start the backend services (FastAPI and PostgreSQL):
   ```bash
    cd backend
    docker-compose up --build
   ```

### 3. Set Up the Chrome Extension:

1.  install dependencies
    ```bash
    cd ../extension
    npm install
    ```

2. Build the extension:
   ```bash
    npm run build
   ```
   - Output is in the dist/ directory
3. Load the extension in Chrome:
   - Open Chrome and go to chrome://extensions/.
   - Enable Developer mode (top-right toggle).
   - Click Load unpacked and select protego/extension/dist/.
4. Open the side panel:
   - Visit a webpage (e.g., https://www.uhcprovider.com or https://www.aetna.com/cpb/medical/data/900_999/0965.html).
   - Click the extension icon in the Chrome toolbar and select Open side panel.
   - View page metrics (links, words, images) and past visit timestamps.

### 4.Testing

- Test on:

  - UHCprovider.com
  - Ustekinumab - Aetna

- Verify:
  - Metrics (link count, word count, image count) appear in the side panel.
  - Past visit timestamps for the current URL are listed.
  - Data is stored in PostgreSQL via the FastAPI backend.

### 5. Stopping the Services

- Stop Docker services:
  ```bash
  cd backend
  docker-compose down
  ```
- Reset database (optional):
  ```bash
  docker-compose down -v
  ```
