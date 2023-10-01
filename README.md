# Clinic Appointment Apps

An example applications of [DIHub](https://github.com/alfarih31/dihub/tree/dev)
and [DIHub-CQRS](https://github.com/alfarih31/dihub-cqrs/tree/dev) utilization

- [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/3945016-28fab214-aa76-42f9-b28b-eebbf32fb0ab?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D3945016-28fab214-aa76-42f9-b28b-eebbf32fb0ab%26entityType%3Dcollection%26workspaceId%3Dc0082143-67d6-4afc-802a-08e58ae649de)
- [Database Entities Relation Diagram](https://hackmd.io/e3ojOJBGRQ6V9NeyVK0d1Q?view#)

## Prerequisites

1. Python `v3.11`
2. Make
3. Poetry
3. Docker `v20.10.8` (Optional)

## Set-up

### Install Dependencies

### Configure

#### Generate JWT RSA

```shell
make gen-jwt-rsa
```

#### Configure API

1. Copy [.env.example](.env.example) as [.env](.env)

```shell
cp .env.example .env
```

2. Below is available configurations:

| Key                  | Description              | Values                     | Required |
|----------------------|--------------------------|----------------------------|----------|
| `SERVER_HOST`        | Server hostname          | String, Default: `0.0.0.0` |          |
| `SERVER_PORT`        | Server port              | Int, Default: `8080`       | ✓        |
|                      |                          |                            |          |
| `DB_DRIVER`          | SQLAlchemy DB Driver     | String                     | ✓        |
| `DB_USER`            | DB User                  | String                     | ✓        |
| `DB_PASSWORD`        | DB Password              | String                     | ✓        |
| `DB_HOST`            | DB Host                  | String                     | ✓        |
| `DB_PORT`            | DB Port                  | Int                        | ✓        |
| `DB_DATABASE`        | DB Database              | String                     | ✓        |
|                      |                          |                            |          |
| `BCRYPT_SALT_ROUNDS` | BCrypt Salt Rounds       | Int                        | ✓        |
|                      |                          |                            |          |
| `JWT_RSA_FILE`       | JWT RSA secret locations | String                     | ✓        |
| `JWT_ISSUER`         | JWT ISS                  | String                     | ✓        |
| `JWT_RSA_ALG`        | JWT RSA Algorithm        | String                     | ✓        |
| `JWT_AUDIENCE`       | JWT AUD                  | String                     | ✓        |
| `JWT_EXPIRES`        | JWT Expires in seconds   | Int                        | ✓        |

### Development

#### Local Development

#### Run The application

Using Makefile to setup development

1. Setup Dev

```shell
make setup-dev
```

2. Run development runtime

```shell
make dev
```

### Production

#### Using Docker

1. Build the image

```shell
docker build -t clinic-appointment-app:latest .
```

### Contributors ###

- Alfarih Faza <alfarihfz@gmail.com>