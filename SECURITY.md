# Security and Privacy

## User data
This application does not collect, store, or process any personal information. There are no user accounts, logins, or forms that capture personal data. The only user input is a search term on the search page, which is used solely to filter existing public data and is never stored.

## Input validation
- `/api/signs` and `/api/season-stats` accept optional query parameters (`season`, `q`). Both are validated implicitly: an unrecognised season name or a search term with no matches returns an empty result set rather than causing an error, verified by automated tests (`test_signs_filtered_by_invalid_season`, `test_signs_search_no_matches`).
- `/season/<season_name>` accepts any string in the URL and does not crash on an invalid value, verified by `test_season_page_handles_invalid_season`.

## Secrets and credentials
- No passwords, API keys, tokens, or other secrets are used anywhere in this application.
- Nothing of this kind is committed to the GitHub repository.

## Data source
All data used (weather records, seasonal and cultural information) is drawn from publicly available government and community sources, licensed for reuse (see README.md § Data sources). No private, restricted, or sensitive data is used.

## Deployment
## Deployment
The application is deployed on PythonAnywhere via a WSGI configuration that imports the Flask `app` object directly (`from app import app as application`). This means `app.run(debug=True, ...)` in `app.py` — used only for local development — is never executed in the deployed environment, so Flask's debug mode and its interactive debugger are not exposed in production.