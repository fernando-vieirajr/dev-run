# Dev Run | Azure DevOps Effort Calculator

Este projeto executa um **job pontual em Docker** para calcular métricas de velocidade e business value a partir de itens concluídos no **Azure DevOps**, persistindo o resultado em arquivo de log no host. O container executa, gera o resultado, registra o log e encerra automaticamente.

No geral, o projeto foi desenvolvido para resolver uma necessidade pessoal. Na empresa em que trabalho, a velocidade de entrega é um fator importante para acompanhamento e tomada de decisão. Diante disso, desenvolvi esta ferramenta para poder acompanhar, medir e analisar a velocidade de entrega de forma contínua, trazendo mais visibilidade sobre o desempenho ao longo do mês.

---

## Visão Geral

1. O container é buildado via Docker
2. O script `main.py` é executado
3. Dados são coletados do Azure DevOps via API
4. As métricas são calculadas:

   * Velocidade atual
   * Velocidade final estimada
   * Effort adicional necessário para atingir a meta
   * Business Value total
5. O resultado é:

   * exibido no console (`docker logs`)
   * gravado em `./logs/run.log`
6. O container se encerra.


---

## Arquitetura

```
.
├── docker/
│   └── Dockerfile
├── src/
│   ├── main.py
│   ├── clients/
│   ├── services/
│   └── config/
├── logs/
│   └── run.log
├── docker-compose.yml
├── requirements.txt
└── .env
```

---

## Logs

* Todos os logs são gravados em:

  ```
  ./logs/run.log
  ```
* O arquivo **é sempre sobrescrito** a cada execução

---

## Configuração de Ambiente

As variáveis são definidas no arquivo `.env`:

```env
ORGANIZATION_NAME=...
PROJECT_NAME=...
USER_EMAIL=...
PERSONAL_ACCESS_TOKEN=...
TARGET_VELOCITY=...
```

> Preencha conforme seus dados.

---

### Build e execução padrão

```bash
docker compose build --no-cache --pull
docker compose up -d
```

Após a execução:

* o container encerra automaticamente
* o resultado estará disponível em `logs/run.log`

---

## Comportamento Esperado

* `docker ps` → não exibe o container
* `docker ps -a` → mostra `Exited (0)`

Isso **não representa erro**. O container foi projetado para finalizar após a execução.

---
