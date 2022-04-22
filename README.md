# Umamusume Suppoter Server
[![GitHub action status - Docker build](https://github.com/riemannulus/umamusume-server/actions/workflows/docker.yml/badge.svg)](https://hub.docker.com/repository/docker/riemannulus/umamusume-server)

이 프로젝트는 [우마서포터](https://uma.sonagi.dev)의 백엔드 서버입니다.
[Lightsail](https://aws.amazon.com/ko/lightsail/)에 Nginx + Docker-Compose로 서빙되고 있습니다.

## 개발환경
이 프로젝트는 mysql을 사용한다는 것을 가정하고 작성되어 있습니다.

[TBD]

## 의존사항

### `pip`

`pip install sqlalchemy bs4 pytest\
 flask flask-cors flask-graphql werkzeug`

### `MySQL`

#### macOS

`brew install mysql`
