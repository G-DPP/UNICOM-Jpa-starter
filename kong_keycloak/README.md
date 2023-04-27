<h1>Setup instructions:</h1>

1) From the project directory run docker compose up --build -d

<h2>Kong & Konga</h2>

2) Go to localhost:1337 and register a new admin user

3) In the konga welcome dashboard, put:
    - "kong" in the Name field
    - "http://kong:8001" in the Kong Admin URL field

4) Go to the "Connections" tab of the sidebar and activate the new connection.

5) Go to the "Snapshots" tab of the sidebar and:
    - Click on "Import from file"
    - Choose shapshots/konga/konga_snapshot.json
    - Click on "Details" -> "Restore"
    - Mark all the checkboxes and then click on "Import objects"

<h2> Keycloak </h2>

6) Go to localhost:8180 and login with the keycloak admin credentials listed in the docker-compose.yml
    - Defaults are admin admin

7) Click on create new realm in the upper left corner:
    - Click on Select file
    - Choose shapshots/keycloak/keycloak_snapshot.json

<h2> Graphana, Prometheus & StatsD </h2>

6) Go to localhost:3000 and register a new admin user

7) Go to http://localhost:3000/datasources and add Prometheus as datasource:
    - In the "URL" section put in http://prometheus:9090
    - On the bottom of the page click on "Save & test"
    - From the "Dashboard" tab on the top of the page import "Prometheus 2.0 Stats" dashboards

8) Go to localhost:3000/dashboards and:
    - Click on New -> Import
    - Choose Upload JSON file
    - Select the dashboard snapshot in snapshots/grafana/grafana_snapshot.json

<hr>
<br>

<h1> Usage instructions</h1>

1) Access to Konga from localhost:1337

2) Test the APIs from localhost:8000

3) Access to prometheus admin panel from localhost:9090

4) Check the metrics sent from kong to StatsD from http://localhost:9123/metrics (they begin with "kong")

5) Access to grafana dashboards from localhost:3000/dashboards

6) Access to Keycloak from localhost:8080

<hr>
<br>

<h1> Useful documentation:</h1>

<ul>
    <li>
        <a href= "https://docs.konghq.com/gateway/latest/">Official Kong Documentation</a>
    </li>
    <li>
        <a href= "https://www.keycloak.org/docs/latest/server_admin/">Official Keycloak Documentation</a>
    </li>
    <li>
        <a href= "https://www.lua.org/manual/5.4/">Official LUA Documentation</a>
    </li>
    <li>
        <a href= "https://github.com/nokia/kong-oidc">Useful OIDC AUTH Repository</a>
    </li>
    <li>
        <a href= "https://github.com/d4rkstar/kong-konga-keycloak">Kong, Konga and Keycloak tutorial</a>
    </li>
    <li>
        <a href= "https://tech.aufomm.com/use-kong-enterprise-openid-connect-plugin-to-protect-your-api-services/">Keycloak - OpenID Tutorial</a>
    </li>
    <li>
        <a href= "https://tech.aufomm.com/use-kong-openid-connect-plugin-enterprise-to-map-users-from-idp-keycloak-directly/">Keycloak mapping to Kong consumer tutorial</a>
    </li>
    <li>
        <a href= "https://curity.io/resources/learn/kong-user-routing-plugin/">Kong user routing and custom plugin tutorial</a>
    </li>
    <li>
        <a href= "https://docs.konghq.com/gateway/latest/kong-enterprise/analytics/prometheus-strategy/">Vitals metrics with Kong, StatsD and Prometheus </a>
    </li>
    <li>
        <a href = "https://docs.konghq.com/hub/kong-inc/statsd/">Official StatsD Kong Plugin Documentation</a>
    </li>
     <li>
        <a href = "https://dev.to/kirklewis/metrics-with-prometheus-statsd-exporter-and-grafana-5145">Useful StatsD, Kong and Grafana Tutorial</a>
    </li>

<ul>


