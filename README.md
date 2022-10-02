# E-Ticketing-System
Repository for AT70.18 SAD course project Jan 2022

Team Members
- Sunsun Kasajoo 
- Mufaddal Enayath Hussain
- Vineela Mukkamala


Contribution

Sunsun - Server Setup, Database Design, Django application.
Mufaddal - Server Setup with docker swarm, deployment handling.
Vineela - Frontend design, database design, django application, JMeter.

Configurations:


For Pg admin stack yaml file 
```
version: '3.7'
services:
  pgadmin:
    image: dpage/pgadmin4
    volumes:
      - pgadmin_data:/bitnami/pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: root
    ports:
      - "80:80"
    networks:
      - pgcluster_network
    deploy:
      placement:
        constraints:
          - "node.Role == worker"
volumes:
  pgadmin_data:
    driver: local
networks:
  pgcluster_network:
    external: true
 ```
 
 For Pg cluster yaml
 
 ```
 version: '3.7'
services:
  pg-0:
    deploy:
      mode: replicated
      placement:
        constraints:
          - "node.Role == worker"
    image: docker.io/bitnami/postgresql-repmgr:11
    ports:
      - 9000:5432
    volumes:
      - pg_0_data:/bitnami/postgresql
    networks:
      - pgcluster_network
    environment:
      - POSTGRESQL_POSTGRES_PASSWORD=password
      - POSTGRESQL_USERNAME=postgres
      - POSTGRESQL_PASSWORD=password
      - POSTGRESQL_DATABASE=eticket
      - POSTGRESQL_NUM_SYNCHRONOUS_REPLICAS=1
      - REPMGR_PASSWORD=repmgrpassword
      - REPMGR_PRIMARY_HOST=pg-0
      - REPMGR_PARTNER_NODES=pg-1,pg-0
      - REPMGR_NODE_NAME=pg-0
      - REPMGR_NODE_NETWORK_NAME=pg-0
  pg-1:
    deploy:
      mode: replicated
      placement:
        constraints:
          - "node.Role == worker"
    image: docker.io/bitnami/postgresql-repmgr:11
    ports:
      - 9001:5432
    volumes:
      - pg_1_data:/bitnami/postgresql
    networks:
      - pgcluster_network
    environment:
      - POSTGRESQL_POSTGRES_PASSWORD=password
      - POSTGRESQL_USERNAME=postgres
      - POSTGRESQL_PASSWORD=password
      - POSTGRESQL_DATABASE=eticket
      - POSTGRESQL_NUM_SYNCHRONOUS_REPLICAS=1
      - REPMGR_PASSWORD=repmgrpassword
      - REPMGR_PRIMARY_HOST=pg-0
      - REPMGR_PARTNER_NODES=pg-0,pg-1
      - REPMGR_NODE_NAME=pg-1
      - REPMGR_NODE_NETWORK_NAME=pg-1
  pgpool:
    image: docker.io/bitnami/pgpool:4
    ports:
      - 5432:5432
    deploy:
      mode: replicated
      placement:
        constraints:
          - "node.Role == worker"
    networks:
      - pgcluster_network
    environment:
      - PGPOOL_BACKEND_NODES=0:192.41.170.117:9000,1:192.41.170.117:9001
      - PGPOOL_SR_CHECK_USER=postgres
      - PGPOOL_SR_CHECK_PASSWORD=password
      - PGPOOL_ENABLE_LDAP=no
      - PGPOOL_POSTGRES_USERNAME=postgres
      - PGPOOL_POSTGRES_PASSWORD=password
      - PGPOOL_ADMIN_USERNAME=admin
      - PGPOOL_ADMIN_PASSWORD=password
      - PGPOOL_ENABLE_LOAD_BALANCING=yes
    healthcheck:
      test: ["CMD", "/opt/bitnami/scripts/pgpool/healthcheck.sh"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  pg_0_data:
    driver: local
  pg_1_data:
    driver: local
networks:
  pgcluster_network:
    external: true
   ```
   For traefix yaml
   
   ```
   version: '3'

services:
  reverse-proxy:
    image: traefik:v2.3.4
    command:
      # Docker swarm configuration
      - "--providers.docker.endpoint=unix:///var/run/docker.sock"
      - "--providers.docker.swarmMode=true"
      - "--providers.docker.exposedbydefault=false"
      - "--providers.docker.network=traefik-public"
      # Configure entrypoint
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      # SSL configuration
      - "--certificatesresolvers.letsencryptresolver.acme.httpchallenge=true"
      - "--certificatesresolvers.letsencryptresolver.acme.httpchallenge.entrypoint=web"
      - "--certificatesresolvers.letsencryptresolver.acme.email=st122331@ait.asia"
      - "--certificatesresolvers.letsencryptresolver.acme.storage=/letsencrypt/acme.json"
      # Global HTTP -> HTTPS
      - "--entrypoints.web.http.redirections.entryPoint.to=websecure"
      - "--entrypoints.web.http.redirections.entryPoint.scheme=https"
    ports:
      - 80:80
      - 443:443
    volumes:
      - traefik-certificates:/letsencrypt
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - traefik-public
    deploy:
      placement:
        constraints:
          - node.role == manager
      labels:
        - "traefik.enable=true"
        - "traefik.http.services.traefik.loadbalancer.server.port=888" # required by swarm but not used.
        - "traefik.http.routers.http-catchall.rule=hostregexp(`{host:.+}`)"
        - "traefik.http.routers.http-catchall.entrypoints=web"
        - "traefik.http.routers.http-catchall.middlewares=redirect-to-https@docker"
        - "traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https"
volumes:
  traefik-certificates:
networks:
  traefik-public:
    external: true
```
Steps to run the project


1. Setup docker swarm with manager and worker nodes.

2. create two overlay networks in docker
  1. pgcluster_network
  2 .traefik-public

3. to deploy the application first we must build a registry, 

```
docker run -d -p 5000:5000 --restart always --name registry registry:2
```
4. Run the above configuration provided

5. next run docker-compose  -f docker-compose-prod.yaml up file to build the image

6. run docker-compose down --volumes  to bring it down 

7. docker-compose -f docker-compose-prod.yaml push to push the image to the registry  

8. run docker stack deploy -c docker -compose-prod django-prod
