# SWA Managed Function Test App (Python)

A minimal app to confirm Python Managed Functions work end-to-end on Azure
Static Web Apps: a static HTML page that calls a `/api/hello` Function
written using the Azure Functions Python v2 programming model.

## Structure

```
swa-managed-function-test-python/
├── index.html                  # static frontend
├── staticwebapp.config.json    # sets apiRuntime to python:3.11
├── .github/workflows/
│   └── azure-static-web-apps.yml
└── api/                        # Managed Function
    ├── function_app.py         # HTTP trigger, v2 programming model
    ├── requirements.txt
    ├── host.json
    └── local.settings.json     # local dev only, don't commit real secrets
```

## 1. Test locally first (optional but recommended)

```bash
cd swa-managed-function-test-python

# Install SWA CLI + Functions Core Tools once, if you haven't already
npm install -g @azure/static-web-apps-cli
npm install -g azure-functions-core-tools@4 --unsafe-perm true

# Terminal 1 — Functions API
cd api
python -m venv .venv
source .venv/bin/activate   # .venv\Scripts\activate on Windows
pip install -r requirements.txt
func start

# Terminal 2 — SWA CLI, proxies the static site + API together
cd ..
swa start . --api-location http://localhost:7071
```

Open `http://localhost:4280` and click **Call API**.

## 2. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: SWA Python managed function test"
gh repo create swa-managed-function-test-python --public --source=. --push
# or manually create a repo on github.com, then:
# git remote add origin https://github.com/<you>/swa-managed-function-test-python.git
# git push -u origin main
```

## 3. Create the Static Web App and link it to the repo

Via the Azure Portal (auto-wires the workflow + deployment token):

1. Portal → **Create a resource** → **Static Web App**.
2. Deployment details → sign in with GitHub → pick the repo/branch.
3. Build details:
   - **Build presets**: Custom
   - **App location**: `/`
   - **Api location**: `api`
   - **Output location**: *(leave blank)*
4. **Review + create** → **Create**.

Or via CLI:

```bash
az staticwebapp create \
  --name swa-managed-function-test-python \
  --resource-group <your-resource-group> \
  --source https://github.com/<you>/swa-managed-function-test-python \
  --location <region> \
  --branch main \
  --app-location "/" \
  --api-location "api" \
  --output-location "" \
  --login-with-github
```

## 4. Test it

Once the GitHub Actions run completes (check the **Actions** tab), open the
URL from the Static Web App's Overview page, click **Call API**, and confirm
you get back JSON from the Python function.

Direct test:

```
https://<your-app-name>.azurestaticapps.net/api/hello?name=Azure
```

## Cleanup

```bash
az staticwebapp delete --name swa-managed-function-test-python --resource-group <your-resource-group>
```
