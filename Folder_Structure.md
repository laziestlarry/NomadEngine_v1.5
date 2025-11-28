NomadEngine_v1.5/
│
├── api/
│   ├── __init__.py
│   ├── server.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── tasks.py
│   │   ├── events.py
│   │   ├── blueprints.py
│   │   ├── workers.py
│   │   ├── system.py
│   │   └── income.py
│   └── schemas/
│       ├── __init__.py
│       ├── task_schema.py
│       ├── event_schema.py
│       ├── blueprint_schema.py
│       └── income_schema.py
│
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── bootstrap.py
│   ├── logger.py
│   ├── env.py
│   └── paths.py
│
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── opportunity_classifier.py
│   ├── roi_ranker.py
│   ├── strategy_builder.py
│   ├── workflow_planner.py
│   ├── human_step_mapper.py
│   ├── autofill_agent.py
│   ├── optimization_agent.py
│   └── risk_evaluator.py
│
├── scheduler/
│   ├── __init__.py
│   ├── scheduler_engine.py
│   ├── jobs_alpha_scan.py
│   ├── jobs_income_scan.py
│   ├── jobs_health.py
│   ├── jobs_retry.py
│   └── jobs_reconnect.py
│
├── db/
│   ├── __init__.py
│   ├── engine.py
│   ├── session.py
│   ├── models.py
│   └── migrations/
│       ├── __init__.py
│       └── init_db.py
│
├── events/
│   ├── __init__.py
│   ├── event_bus.py
│   ├── event_store.py
│   └── event_definitions.py
│
├── modules/
│   ├── __init__.py
│   ├── loader.py
│   ├── toloka.py
│   ├── hive.py
│   ├── remotasks.py
│   ├── uhrs.py
│   └── appen.py
│
├── pipelines/
│   ├── __init__.py
│   ├── taskpipe.py
│   ├── blueprint_pipeline.py
│   ├── execution_pipeline.py
│   └── income_pipeline.py
│
├── workers/
│   ├── __init__.py
│   ├── python_worker.py
│   ├── node_bridge.py
│   ├── worker_controller.py
│   └── platform_workers/
│       ├── __init__.py
│       ├── toloka_worker.py
│       ├── hive_worker.py
│       ├── remotasks_worker.py
│       └── generic_worker.py
│
├── common/
│   ├── __init__.py
│   ├── utils.py
│   ├── deep_compare.py
│   ├── time_utils.py
│   ├── validation.py
│   ├── hashing.py
│   └── serialization.py
│
├── launcher/
│   ├── __init__.py
│   ├── nomad_v15.py
│   ├── start_api.py
│   ├── start_scheduler.py
│   ├── start_python_worker.py
│   ├── start_node_worker.js
│   └── environment_check.py
│
├── scripts/
│   ├── launch_nomad_v15.sh
│   ├── build.sh
│   ├── migrate.sh
│   ├── reset_db.sh
│   └── test_local.sh
│
├── logs/
│   └── .gitkeep
│
└── README.md
